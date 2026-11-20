#!/usr/bin/env python3
"""把 src/ 下的标注文本生成静态网页。用法：python3 build.py"""
import collections
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent
SRC = ROOT / "src"
BOOKS_OUT = ROOT / "books"  # 生成的各书页面统一放在 books/<slug>/ 下

NUM = "零一二三四五六七八九十"


def cn(n):
    if n >= 100:
        h, r = divmod(n, 100)
        if r == 0:
            return NUM[h] + "百"
        if r < 10:
            return NUM[h] + "百零" + NUM[r]
        t, u = divmod(r, 10)
        return NUM[h] + "百" + NUM[t] + "十" + (NUM[u] if u else "")
    if n <= 10:
        return NUM[n]
    if n < 20:
        return "十" + NUM[n - 10]
    t, u = divmod(n, 10)
    return NUM[t] + "十" + (NUM[u] if u else "")


BOOKS = []

CSS_LINK = '<link rel="stylesheet" href="{r}assets/style.css">'


def esc(s):
    return html.escape(s, quote=True)


GLOSS = re.compile(r"(（[^（）]*）|\([^()]*\))")

SENT = re.compile(r"[^。！？；\u2063]*[。！？；\u2063]+(?:[”’」』）]*[。！？；]+)*[”’」』）]*|[^。！？；\u2063]+$")      # \u2063（不可见分隔符，不显示）可加在逗号后，让该处也断成一个悬浮句


def split_sents(s):
    parts = [x for x in SENT.findall(s) if x.strip()]
    # A trailing editorial bracket closes the preceding sentence.
    if len(parts) > 1 and parts[-1].strip() == "〉":
        closing = parts.pop()
        parts[-1] += closing
    return parts


NOTE_HEAD = re.compile(r'[^。！？；：:\n]{1,64}：')
NOTE_QUOTED_HEAD = re.compile(r'“[^”\n]{1,32}”(?:即|指|为|是|同|通|见|出自)')
NOTE_CONTINUATION = re.compile(
    r'(?:的意思是|的看法是|的观点|的立意|'
    r'来对比|借此议论|用几个例子说明|指出.*|最意外的是.*|典出.*|见《.*)$'
)


def split_notes(text):
    """拆开合写的独立词条；引文、括注和同一词条的后续解释保持完整。"""
    stack = []
    opening = {'“': '”', '‘': '’', '「': '」', '『': '』',
               '（': '）', '(': ')', '《': '》', '〈': '〉'}
    starts = [0]
    for i, char in enumerate(text):
        if not stack and i:
            # 允许句末引号后的新词条，但不在尚未结束的引用中拆分。
            before = text[:i].rstrip('”’」』）)》〉 ')
            if before and before[-1] in '。！？；':
                head = NOTE_HEAD.match(text, i)
                quoted = NOTE_QUOTED_HEAD.match(text, i)
                citation = (head and head[0][:-1].endswith(('曰', '云', '载', '爻辞', '象辞'))
                            and text[head.end():].startswith(('“', '‘', '「', '『')))
                if ((head and all(head[0].count(a) == head[0].count(b)
                                  for a, b in opening.items())
                     and not citation
                     and not NOTE_CONTINUATION.search(head[0][:-1])) or quoted):
                    starts.append(i)
        if char in opening:
            stack.append(opening[char])
        elif stack and char == stack[-1]:
            stack.pop()
    starts.append(len(text))
    return [text[a:b].strip() for a, b in zip(starts, starts[1:]) if text[a:b].strip()]


# ---- 注释位置：正文中以上标标出，注释按上标序号排列 ----
ANCHOR_STATS = collections.Counter()
NOTE_MARK = "\x02"                      # 渲染前临时插在正文里的注释位置记号，输出时换成 <sup class="n">
_PAREN = re.compile(r"（[^（）]*）|\([^()]*\)")
_QUOTES = str.maketrans("", "", "“”‘’「」『』")


def _note_terms(note):
    """从注释“词语：解释”里取出可在正文定位的词语候选（由长到短）。取不到词语返回空。"""
    m = re.match(r"([^：:\n]{1,40})[：:]", note)
    if not m:
        m = re.match(r"([^，。；：\n]{1,8})[，,]", note)      # “绠，汲水的井绳；㳅，流传。”一类
    head = m.group(1).strip() if m else ""
    cands = []
    # “某某”即……、校：“某某”他本作……：词语在引号里
    quoted = [q for q in re.findall(r"[“「‘『]([^”」’』]{1,10})[”」’』]", note[:80]) if q][:3]
    if not head or head in ("校", "按", "校勘", "案", "注") or note[:1] in "“「‘『":
        cands.extend(quoted)
    if not head:
        return cands
    for c in (head, _PAREN.sub("", head)):
        for d in (c, c.translate(_QUOTES)):
            d = d.strip()
            if d and d not in cands:
                cands.append(d)
    for piece in re.split(r"[、，,/／或]", _PAREN.sub("", head)):
        for d in (piece.strip(), piece.translate(_QUOTES).strip()):
            if d and d not in cands:
                cands.append(d)
    for q in quoted:
        if q not in cands:
            cands.append(q)
    return cands


_ZGC_NOTE = re.compile(r"底本原注\d+（主文第(\d+)字后）：〈(.*)〉")


def _locate_zgc(texts, note):
    """《战国策》“底本原注NNN（主文第N字后）”自带位置：N 与本站正文有几字的偏差，故在 N 附近找注中引用的字词来校准。"""
    m = _ZGC_NOTE.match(note)
    if not m:
        return None
    n = int(m.group(1))
    text = texts[0]
    best = None
    for tok in re.findall(r"[‘“]([^’”]{1,8})[’”]", m.group(2)):
        for k in range(max(0, n - 24), min(len(text), n + 8)):
            if text.startswith(tok, k):
                end = k + len(tok)
                if best is None or abs(end - n) < abs(best - n):
                    best = end
        if best is not None:
            break
    return 0, (best if best is not None else min(n, len(text)))


def _locate_note(texts, note, p0, pos0):
    """在 texts（正文各段）里找注释词语：先从上一条注释之后找，找不到再从头找。返回 (段号, 词语末尾位置) 或 None。"""
    zgc = _locate_zgc(texts, note)
    if zgc:
        return zgc
    for cand in _note_terms(note):
        for start_p, start_pos in ((p0, pos0), (0, 0)):
            for p in range(start_p, len(texts)):
                k = texts[p].find(cand, start_pos if p == start_p else 0)
                if k >= 0:
                    return p, k + len(cand)
    return None


def anchor_notes(texts, notes):
    """返回 (锚点列表, 按正文位置排序后的注释)。锚点 = (段号, 词语末尾位置)；找不到词语的注释锚点为 None，排在最后。"""
    if not notes or not texts:
        return [], list(notes)
    found, cur = [], (0, 0)
    ANCHOR_STATS["notes"] += len(notes)
    for i, note in enumerate(notes):
        hit = _locate_note(texts, note, *cur)
        if hit:
            cur = hit
        found.append((hit, i))
        ANCHOR_STATS["unplaced"] += hit is None
    order = sorted(found, key=lambda a: (a[0] is None, a[0] or (0, 0), a[1]))
    return [a[0] for a in order], [notes[a[1]] for a in order]


def mark_text(text, positions):
    """在 text 的各位置（可重复）插入注释记号。"""
    for q in sorted(positions, reverse=True):
        text = text[:q] + NOTE_MARK + text[q:]
    return text


def marked_pairs(o, t, positions):
    """split_pairs 的结果里，把注释记号插进各句相应位置；对不齐时返回 None。"""
    pairs = split_pairs(o, t)
    if not positions:
        return pairs
    if "".join(x for x, _ in pairs) != o:
        return None
    ends, pos = [], 0
    for x, _ in pairs:
        pos += len(x)
        ends.append(pos)
    ins = [[] for _ in pairs]
    for q in positions:
        k = next(k for k, e in enumerate(ends) if q <= e)
        ins[k].append(max(q - (ends[k] - len(pairs[k][0])), 0))
    return [(mark_text(x, ins[k]), y) for k, (x, y) in enumerate(pairs)]


_MARKS = re.compile(NOTE_MARK + "+")


def number_marks(html_str, start=1):
    """把输出里的记号换成上标序号（同一处多条注释合并成“1,2”）；返回 (html, 下一个序号)。"""
    n = [start]

    def sub(m):
        k = len(m.group(0))
        nums = list(range(n[0], n[0] + k))
        n[0] += k
        label = f"{nums[0]}" if k == 1 else f"{nums[0]}–{nums[-1]}" if k > 2 else f"{nums[0]},{nums[1]}"
        return f'<sup class="n" data-n="{label}"></sup>'
    return _MARKS.sub(sub, html_str), n[0]


def _frag_groups(raw):
    """把只剩标点、或以逗号等起首的碎句并回上一句（如夹注括号后单独的“。”）。"""
    groups = []
    for k, x in enumerate(raw):
        if groups and (not re.search(r"[\u4e00-\u9fff]", x) or x.lstrip()[:1] in "，；：、）〉"):
            groups[-1].append(k)
        else:
            groups.append([k])
    return groups


def split_pairs(o, t):
    """按句号/叹号/问号/分号把一段原文拆成句，并与译文逐句对应。
    译文里可用「¦」显式分句；句数对不上时整段不拆；碎句并回上一句。"""
    raw = split_sents(o)
    if len(raw) > 1:
        st = t.split("¦") if "¦" in t else split_sents(t)
        if "¦" in t:         # 白话按 sent_units 的句数给（碎句已并入上一句）：原文按同一规则并句
            units = sent_units(o)
            if len(st) == len(units) != len(raw):
                return list(zip(units, st))
        groups = _frag_groups(raw)
        if len(st) == len(raw):
            if "¦" in t:
                # 显式配译保留有正文的句子，即使底本在句首多了逗号。
                # 只有纯标点碎片仍需并回上一句。
                groups = []
                for k, x in enumerate(raw):
                    # 扩展区汉字也有正文意义，不能把单字句当作纯标点。
                    if groups and not any(char.isalnum() for char in x) and _ORPHAN.fullmatch(x):
                        groups[-1].append(k)
                    else:
                        groups.append([k])
            return [("".join(raw[k] for k in g), "".join(st[k] for k in g)) for g in groups]
        if len(st) == len(groups):
            return [("".join(raw[k] for k in g), x) for g, x in zip(groups, st)]
    return [(o, t.replace("¦", ""))]


def has_sentence_pairs(chunk):
    """Recognize explicit, nonempty glosses aligned with each original sentence."""
    original = split_sents(chunk["o"])
    modern = chunk["t"].split("¦")
    return (len(original) == len(modern) and all(t.strip() for t in modern)
            and [o for o, _ in split_pairs(chunk["o"], chunk["t"])] == original)


def orig_html(text):
    """原文中编者加的括注（年份、人名、注音）用淡色显示。"""
    parts = GLOSS.split(esc(text))
    return "".join(
        f'<span class="gl">{p}</span>' if i % 2 else p for i, p in enumerate(parts)
    )


def parse_juan(path):
    lines = path.read_text(encoding="utf8").splitlines()
    heading = lines[0].strip()
    entries = []
    cur = None
    for ln in lines[1:]:
        ln = ln.rstrip()
        if ln.startswith("# "):
            cur = {"title": ln[2:].strip(), "paras": [[]], "notes": []}
            entries.append(cur)
        elif not ln.strip():
            if cur and cur["paras"][-1]:
                cur["paras"].append([])
        elif ln.startswith("注："):
            cur["notes"].extend(split_notes(ln[2:].strip()))
        elif "||" in ln:
            o, t = (x.strip() for x in ln.split("||", 1))
            cur["paras"][-1].append((o, t))
        else:
            raise ValueError(f"{path}: 无法解析：{ln}")
    for e in entries:
        e["paras"] = [p for p in e["paras"] if p]
    return heading, entries


def is_wiki_source(url):
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    return any(host == domain or host.endswith("." + domain)
               for domain in ("wikisource.org", "wikipedia.org"))


def page(title, body, r, extra_js=False):
    js = f'<script src="{r}assets/reader.js" defer></script>' if extra_js else ""
    return f"""<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
{CSS_LINK.format(r=r)}
<script src="{r}assets/theme.js"></script>
{js}
</head>
<body>
{body}
</body>
</html>
"""


def crumbs(items):
    return '<nav class="crumbs">' + " › ".join(
        f'<a href="{h}">{esc(t)}</a>' if h else f"<span>{esc(t)}</span>" for t, h in items
    ) + "</nav>"


def render_entry(i, e):
    out = [f'<section class="entry" id="e{i}">', f'<h3><span class="no">{cn(i)}</span>{esc(e["title"])}</h3>']
    flat = [o for para in e["paras"] for o, _t in para]
    anchors, notes = anchor_notes(flat, e["notes"])
    where = [[] for _ in flat]
    tail = 0
    for a in anchors:
        if a is None:
            tail += 1
        else:
            where[a[0]].append(a[1])
    num, fi = 1, 0
    for pi, para in enumerate(e["paras"]):
        spans = ""
        for o, t in para:
            pairs = marked_pairs(o, t, where[fi])
            if pairs is None:        # 极少数对不齐：该处注释记到全篇末尾
                tail += len(where[fi])
                pairs = split_pairs(o, t)
            fi += 1
            spans += "".join(f'<span class="s" tabindex="0" data-t="{esc(t2)}">{orig_html(o2)}</span>' for o2, t2 in pairs)
        if pi == len(e["paras"]) - 1:
            spans += NOTE_MARK * tail
        spans, num = number_marks(spans, num)
        out.append(f"<p>{spans}</p>")
    if notes:
        items = "".join(f"<li>{esc(n)}</li>" for n in notes)
        out.append(
            f'<button class="note-btn" type="button" aria-expanded="false" aria-controls="n{i}">'
            f'<span class="caret">▸</span> 注释（{len(notes)}）</button>'
            f'<ol class="notes" id="n{i}" hidden>{items}</ol>'
        )
    out.append("</section>")
    return "\n".join(out)


def build_juan(book, part, vol, src_path, avail):
    pslug, ptitle, pord, nvol = part[:4]
    is_xu = len(part) > 4
    heading, entries = parse_juan(src_path)
    r = "../../../"
    toc = "".join(f'<li><a href="#e{i}">{esc(e["title"])}</a></li>' for i, e in enumerate(entries, 1))
    prev_html = (f'<a href="juan{vol-1:02d}.html">← 卷{cn(vol-1)}</a>' if (vol - 1) in avail
                 else '<span class="off">&nbsp;</span>')
    next_html = (f'<a href="juan{vol+1:02d}.html">卷{cn(vol+1)} →</a>' if (vol + 1) in avail
                 else '<span class="off">下一卷：待整理</span>')
    if is_xu:
        prev_html = next_html = '<span class="off">&nbsp;</span>'
    body = f"""<header class="top">
{crumbs([("现代文库", r + "index.html"), (book["title"], "../index.html"), (ptitle, None)])}
<h1>{esc(ptitle)}<small>{esc(pord)}</small></h1>
<h2>{esc(heading)}</h2>
</header>
<main class="reading-layout">
<details class="toc" open><summary>本卷目录</summary><ol>{toc}</ol></details>
<div class="reading-content">
{chr(10).join(render_entry(i, e) for i, e in enumerate(entries, 1))}
<nav class="pager">{prev_html}<a href="../index.html">目录</a>{next_html}</nav>
</div>
</main>
<div id="tip" role="tooltip" hidden></div>
<footer>白话译文为辅助阅读的意译，如有出入，以原文为准。</footer>"""
    out = BOOKS_OUT / book["slug"] / pslug / f"juan{vol:02d}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(f"{ptitle}·{heading.split('（')[0]}", body, r, True), encoding="utf8")
    return len(entries)


def build_book(book):
    done = {}
    for part in book["parts"]:
        d = SRC / book["slug"] / part[0]
        files = sorted(d.glob("juan*.txt")) if d.exists() else []
        avail = {int(f.stem[4:]) for f in files}
        for f in files:
            vol = int(f.stem[4:])
            done[(part[0], vol)] = build_juan(book, part, vol, f, avail)
    sections = []
    for part in book["parts"]:
        pslug, ptitle, pord, nvol = part[:4]
        cells = []
        for v in range(1, nvol + 1):
            label = part[4] if len(part) > 4 else f"卷{cn(v)}"
            if (pslug, v) in done:
                count = "" if len(part) > 4 else f"<small>{done[(pslug, v)]}则</small>"
                cells.append(f'<li class="ok"><a href="{pslug}/juan{v:02d}.html">{label}{count}</a></li>')
            else:
                cells.append(f'<li class="todo"><span>{label}<small>待整理</small></span></li>')
        sections.append(f'<section class="part"><h2>{esc(ptitle)}<small>{esc(pord)}{'' if len(part) > 4 else f' · 共{nvol}卷'}</small></h2><ul class="vols">{"".join(cells)}</ul></section>')
    body = f"""<header class="top">
{crumbs([("现代文库", "../../index.html"), (book["title"], None)])}
<h1>{esc(book["title"])}<small>{esc(book["author"])}</small></h1>
{intro_html(book["slug"])}
</header>
<main>{"".join(sections)}</main>
<footer>已整理 {sum(n for (p, _), n in done.items() if p != "xu")} 则。</footer>"""
    out = BOOKS_OUT / book["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(book["title"], body, "../../"), encoding="utf8")


# ---------- 楚辞：按篇目成页，原文分节、逐节译文与注释 ----------
def _orig_spec(slug, title, author):
    """tools/prepare_orig.py 生成的只录原文的大书：页表与分组读自 sources/<slug>/pages.json，节名作页内小目录。"""
    pages_ = json.loads((ROOT / f"sources/{slug}/pages.json").read_text(encoding="utf8"))
    catalog = json.loads((ROOT / f"sources/{slug}/chapters.json").read_text(encoding="utf8"))
    pages, last = [], None
    for sl, tt, grp in pages_:
        if grp and grp != last:
            pages.append((None, grp))
        last = grp
        pages.append((sl, tt))
    return {
        "title": title, "author": author, "prose": True, "home_intro_own": True,
        "no_tip": True, "original_only": True, "ed_notes": True, "side_toc": True,
        "side_toc_always": True, "no_count": True, "wide_index": True,
        "omit_source_credit": True, "reading_hint": "", "original_footer": "未据影印本逐字校勘。",
        "sub_labels": {ch["slug"]: [sec["title"] for sec in ch["sections"]] for ch in catalog},
        "pages": pages, "index_footer": "", "single_page": sum(1 for p in pages if p[0]) == 1,
    }




def _scan_spec(slug, title, author):
    """据书籍扫描件识别整理的书：同 _orig_spec，页首与篇名同名的一节不在子目录里重复，页脚注明识别整理。"""
    return {**_orig_spec(slug, title, author), "skip_lead_toc": True,
            "original_footer": "文字据书籍扫描件识别整理，尚未逐字校对。"}


def _annotated_scan_spec(slug, title, author):
    """原书带注释、题解的选注本（据扫描件识别整理）：注释与题解是原书的，不是编者自撰。"""
    return {**_scan_spec(slug, title, author),
            "original_footer": "注释与题解均为原书所有；文字据书籍扫描件识别整理，尚未逐字校对。"}


POETRY = {
    "wangguodiwang": _scan_spec("wangguodiwang", "中国历代亡国帝王传", "李祖德 主编"),
    "kaiguodiwang": _scan_spec("kaiguodiwang", "中国历代开国帝王传", "李祖德 主编"),
    "songtaizu": _scan_spec("songtaizu", "宋太祖赵匡胤传", "范鑫 编著"),
    "lihongzhang": _scan_spec("lihongzhang", "李鸿章传（全译本）", "梁启超 著"),
    "zhangjuzheng": _scan_spec("zhangjuzheng", "张居正大传", "朱东润 著"),
    "hongloumengyan": _scan_spec("hongloumengyan", "红楼梦魇", "张爱玲 著"),
    "lidaidiwangzhuanji": _scan_spec("lidaidiwangzhuanji", "历代帝王传记", "中华书局 编"),
    "datangli_shaonianyou": _scan_spec("datangli_shaonianyou", "少年游", "张大春 著"),
    "datangli_fenghuangtai": _scan_spec("datangli_fenghuangtai", "凤凰台", "张大春 著"),
    "datangli_jiangjinjiu": _scan_spec("datangli_jiangjinjiu", "将进酒", "张大春 著"),
    "pusonglingchuanqi": _scan_spec("pusonglingchuanqi", "蒲松龄传奇", "熊文祥 著"),
    "libaishixuan": _annotated_scan_spec("libaishixuan", "李白诗选", "薛天纬 选注"),
    "songcisanbaishoujianzhu": _annotated_scan_spec("songcisanbaishoujianzhu", "宋词三百首笺注", "唐圭璋 笺注"),
    "sushishicixuan": _annotated_scan_spec("sushishicixuan", "苏轼诗词选", "陈迩冬 选注"),
    "tangsongcijianshi": _annotated_scan_spec("tangsongcijianshi", "唐宋词简释", "唐圭璋 选释"),
    "jinyuanmingqingcixuan": _annotated_scan_spec("jinyuanmingqingcixuan", "金元明清词选", "夏承焘、张璋 编选"),
    "songshixuanzhu": _annotated_scan_spec("songshixuanzhu", "宋诗选注", "钱锺书 选注"),
    "yuanzhenshiwenxuan": _annotated_scan_spec("yuanzhenshiwenxuan", "元稹诗文选", "杨军、文笙、吕燕芳 选注"),
    "xinqijicixuan": _annotated_scan_spec("xinqijicixuan", "辛弃疾词选", "朱德才 选注"),
    "wangweishixuan": _annotated_scan_spec("wangweishixuan", "王维诗选", "陈铁民 选注"),
    "yuefushixuan": _annotated_scan_spec("yuefushixuan", "乐府诗选", "曹道衡 选注"),
    "yuanrenzajuxuan": _annotated_scan_spec("yuanrenzajuxuan", "元人杂剧选", "顾学颉 选注"),
    "hanyushixuan": _annotated_scan_spec("hanyushixuan", "韩愈诗选", "陈迩冬 选注"),
    "dufushixuanzhu": _annotated_scan_spec("dufushixuanzhu", "杜甫诗选注（增补本）", "萧涤非 选注，萧光干、萧海川 辑补"),
    "shijixuan": _annotated_scan_spec("shijixuan", "史记选", "王伯祥 选注"),
    "liuyongcixuanzhu": _annotated_scan_spec("liuyongcixuanzhu", "柳永词选注", "张惠民、张进 选注"),
    "zgguxijuxuan": _annotated_scan_spec("zgguxijuxuan", "中国古代戏剧选", "宁希元、宁恢 选注"),
    "gongzizhenxuanji": _annotated_scan_spec("gongzizhenxuanji", "龚自珍选集", "孙钦善 选注"),
    "qiujinxuanji": _annotated_scan_spec("qiujinxuanji", "秋瑾选集（增订本）", "［清］秋瑾 著；郭延礼、郭蓁 选注"),
    "chutangsijieshixuan": _annotated_scan_spec("chutangsijieshixuan", "初唐四杰诗选", "倪木兴 选注"),
    "guanhanqingxuanji": _annotated_scan_spec("guanhanqingxuanji", "关汉卿选集（修订版）", "康保成、李树玲 选注"),
    "dufushixuan": _annotated_scan_spec("dufushixuan", "杜甫诗选", "山东大学中文系古典文学教研室 选注，袁世硕等 修订"),
    "tangwenxuan": _annotated_scan_spec("tangwenxuan", "唐文选", "李浩 选，阎琦、李浩、李芳民 注释"),
    "erqiannianjian": _scan_spec("erqiannianjian", "二千年间", "胡绳 著"),
    "fojiaoshijieguan": _scan_spec("fojiaoshijieguan", "佛教世界观", "明贤法师 著"),
    "gebenhagen_qingchen": _scan_spec("gebenhagen_qingchen", "清晨", "［丹麦］托芙·迪特莱弗森 著 刘奕奕 译"),
    "gebenhagen_mingliang": _scan_spec("gebenhagen_mingliang", "所有明亮的梦", "［丹麦］托芙·迪特莱弗森 著 刘奕奕 译"),
    "gebenhagen_baizhou": _scan_spec("gebenhagen_baizhou", "白昼坠落", "［丹麦］托芙·迪特莱弗森 著 刘奕奕 译"),
    "huashu_lingmu": _scan_spec("huashu_lingmu", "献给爱与子宫的花束", "［日］铃木凉美 著　蕾克 译"),
    "jiushixin": _scan_spec("jiushixin", "九诗心：暗夜里的文学启明", "黄晓丹 著"),
    "lingtingsahala": _scan_spec("lingtingsahala", "聆听撒哈拉的歌声：三毛传", "田梦 著"),
    "lwgrkfzzl": _scan_spec("lwgrkfzzl", "论我国人口发展战略", "梁中堂 著"),
    "makewaerduo": _scan_spec("makewaerduo", "马可瓦尔多", "［意］伊塔洛·卡尔维诺 著　马小漠 译"),
    "mayinchukao": _scan_spec("mayinchukao", "马寅初考", "梁中堂 著"),
    "mingrenzhuan": _scan_spec("mingrenzhuan", "名人传", "［法］罗曼·罗兰 著　陈筱卿 译"),
    "muriyaoguang": _scan_spec("muriyaoguang", "暮日耀光：张居正与明代中后期政局", "韦庆远 著"),
    "renkousuzhi": _scan_spec("renkousuzhi", "人口素质论", "梁中堂 等著"),
    "renkouxue": _scan_spec("renkouxue", "人口学", "梁中堂 著"),
    "sanmaozhuan_lxg": _scan_spec("sanmaozhuan_lxg", "三毛传：带着丰满的自己去流浪", "林小光 著"),
    "xiaobang": _scan_spec("xiaobang", "肖邦：生平与时代", "［英］艾伦·沃克 著　胡韵迪 译"),
    "yujianmozhate": _scan_spec("yujianmozhate", "遇见莫扎特：从神童到大师的音乐人生", "［英］保罗·约翰逊 著 成铨 译"),
    "zgrkwt": _scan_spec("zgrkwt", "中国人口问题的“热点”——人口理论、发展战略和生育政策", "梁中堂 著"),
    "zgshenhua_shang": _scan_spec("zgshenhua_shang", "东北、西南族群创世神话及其文化", "王孝廉 著"),
    "zgshenhua_xia": _scan_spec("zgshenhua_xia", "中原民族的神话与信仰", "王孝廉 著"),
    "zuochongyoutu": _scan_spec("zuochongyoutu", "左冲右突：现代政治激流中的中国知识分子", "许纪霖 著"),
}
# 首页卡片上的书籍简介：只写书本身。
BOOK_INTRO = {
    "wangguodiwang": "李祖德主编，黄山书社1993年出版。选编夏桀至清宣统帝溥仪共二十一位亡国之君，各立一传，写其即位、失政与覆亡的经过，是《中国历代开国帝王传》的姊妹篇。",
    "kaiguodiwang": "李祖德主编，黄山书社1987年出版。选编从大禹、夏启到皇太极共二十八位开国帝王，分章述其出身、创业、建制与得失，并附前言。",
    "songtaizu": "范鑫编著，河北人民出版社2016年出版，“中国历代帝王传记”丛书之一。以通俗传记笔法讲述赵匡胤由行伍出身到陈桥兵变、杯酒释兵权、以仁治国、先南后北统一中原的一生。",
    "lihongzhang": "梁启超著，中国城市出版社2010年出版的现代汉语全译本（“20世纪四大传记”之一）。评述李鸿章平定太平天国与捻军、办洋务、甲午战败、外交与晚年，兼论其人其时。",
    "zhangjuzheng": "朱东润著，1943年写成，百花文艺出版社2000年版（“二十世纪四大传记丛书”）。以张居正出身、入仕、内阁斗争、推行新政到身后被清算为线索，写明代中后期政局。",
    "hongloumengyan": "张爱玲著，哈尔滨出版社2003年版（“张爱玲典藏全集”）。考据《红楼梦》版本与八十回后情节的论集，含自序、《红楼梦》未完、插曲及“初详”至“五详”。",
    "lidaidiwangzhuanji": "中华书局“中国历史小丛书”合订本，1990年出版。收秦始皇至康熙帝共十三位古代帝王的传记，每篇另有作者，通俗叙述其生平、业绩与历史作用。",
    "datangli_shaonianyou": "张大春长篇小说《大唐李白》第一卷：写李白少年时在蜀中昌明、大匡山从赵蕤受业，结交僧道、游历成都的经历。",
    "datangli_fenghuangtai": "长篇小说《大唐李白》第二卷：李白出蜀后漫游荆楚、江南，与孟浩然、崔宗之、司马承祯等人在金陵凤凰台一带交游唱和，附黄念欣评论。",
    "datangli_jiangjinjiu": "张大春长篇小说《大唐李白》第三卷：李白沿江漫游广陵、安州，与高适、段七娘、月娘等人纠葛于诗酒、江湖与家国之间，附廖伟棠《李白的天下意、无情游》。",
    "pusonglingchuanqi": "熊文祥著，“中国名人轶事丛书”之五（吴洪激主编），武汉大学出版社、台湾汉欣文化事业有限公司1994年联合出版。以民间传说与志怪式笔法，写蒲松龄从乡居少年、屡试不第、南行做幕、坐馆教书到写成《聊斋志异》的一生。",
    "libaishixuan": "李白诗歌的选注本，选289题343首，按生平分蜀中、安陆至初入长安、东鲁与翰林、去朝十年、从璘与流夜郎、晚年、未编年七期编年排列，附前言与逐篇题解、注释。",
    "songcisanbaishoujianzhu": "朱祖谋所编《宋词三百首》的笺注本：每首词后附评笺（本事与历代评语），作者小传、词语注释与校记并录，书前有三篇序。",
    "sushishicixuan": "陈迩冬选注的苏轼诗词选本：诗选二百四十九题，词选八十五首，各篇有题解、编年和详注，诗、词两部之前各有前言。",
    "tangsongcijianshi": "唐圭璋选释唐五代两宋词二百三十二首，每首附简释，析其章法、层次与情致，不作词语注释。",
    "jinyuanmingqingcixuan": "选录金、元、明、清四代词人二百二十余家的词作，每位词人有小传，每首词附题解、注释和前人评语，书前有前言。",
    "songshixuanzhu": "钱锺书选注的宋诗选本，收柳开至萧立之八十家近三百首，每家附小传，诗后有详注，卷首有长序。",
    "yuanzhenshiwenxuan": "人民文学出版社“中国古典文学读本丛书典藏”之一，选元稹诗、文及传奇《莺莺传》，有前言、校记注释与元稹谱略。",
    "xinqijicixuan": "朱德才选注辛弃疾词一百六十八首，按编年与未编年编次，各篇附注释与简评，书前有前言，书后附词评辑要与行年事略。",
    "wangweishixuan": "陈铁民选注，收王维诗二〇五首，分编年诗、未编年诗两部分，每首有题解式评析、详注，难句另有串讲，前有前言。",
    "yuefushixuan": "曹道衡选注汉魏至隋乐府诗：郊庙乐曲、汉魏民歌、南北朝民歌与文人拟作，逐首题解并加词语注释，书前有前言。",
    "yuanrenzajuxuan": "选录关汉卿、白朴、马致远等元代杂剧十六种，以《元曲选》为底本并据他本校补，逐剧注释，书前有长篇前言。",
    "hanyushixuan": "陈迩冬选注韩愈诗九十首，每首有题解与词语注释，卷首有舒芜序，附《新唐书·韩愈列传》。",
    "dufushixuanzhu": "萧涤非选注杜甫诗二百余题，按生平分四期编年，诗后有题解与详注，书末附萧涤非晚年批注辑补。",
    "shijixuan": "选录《史记》本纪、世家、列传二十篇，逐篇校勘、注释，书前有序例概述司马迁与《史记》，书末附出版社后记。",
    "liuyongcixuanzhu": "选注柳永《乐章集》词一百五十三首，每首有题解与词语注释，前有前言论柳永生平与词作，书末辑录历代柳词评语。",
    "zgguxijuxuan": "选录元、明、清杂剧三十三种，上册元杂剧十五种，下册元后期至清杂剧十八种；每剧有作者简介、剧本说明与注释。",
    "gongzizhenxuanji": "孙钦善选注龚自珍诗一百三十四首（含《己亥杂诗》六十三首）、文二十六篇、词十六首，每篇有题解与词语注释，卷首有长篇前言。",
    "qiujinxuanji": "秋瑾文章、书信、诗、词、歌词及弹词《精卫石》前六回选注本，附年谱简编，各篇有题解和注释。",
    "chutangsijieshixuan": "选录王勃、杨炯、卢照邻、骆宾王四家诗二百六十五首，按《全唐诗》次序编排，每首有题解与逐句注释，前有总论四杰生平与诗风的前言。",
    "guanhanqingxuanji": "选录关汉卿《窦娥冤》《救风尘》《单刀会》等杂剧十二部及小令、套数二十余首，每剧每曲附题解与详注，前有前言，后有修订后记。",
    "dufushixuan": "选杜诗一百九十余题（含《雕赋》），按创作时序编排，卷首有前言，每首有题解与逐句词语注释。",
    "tangwenxuan": "按作者时序选录唐代六十三位作家的文章一百四十余篇，骈散兼收；每位作家有小传，每篇有题解与注释。",
    "erqiannianjian": "中国封建专制主义时代两千余年历史的专题通论，分皇帝、官僚、军队、农民、民族关系等问题，写于1944至1945年。",
    "fojiaoshijieguan": "以“一人一世界”为主线，从空性、缘起、二谛与三重境界出发，讨论佛教世界观及其与科学、传统文化的关系，并阐述人文佛教。",
    "gebenhagen_qingchen": "托芙·迪特莱弗森自传体《哥本哈根三部曲》的第一部。",
    "gebenhagen_mingliang": "托芙·迪特莱弗森自传体《哥本哈根三部曲》的第二部。",
    "gebenhagen_baizhou": "托芙·迪特莱弗森自传体《哥本哈根三部曲》的第三部，分两个部分。",
    "huashu_lingmu": "日本作家铃木凉美的随笔集，以夜场、写作与自身经历为线索，写女儿与母亲之间的爱、控制与和解，并记述母亲病重离世的最后时光。",
    "jiushixin": "细读屈原、李陵、曹丕、陶渊明、杜甫、欧阳修、李清照、文天祥、吴梅村九位诗人的生命与诗作，讲述文学如何转化时代与生命中的痛苦。",
    "lingtingsahala": "以三毛的出生、少女时代、留学西班牙、撒哈拉岁月、荷西之死、万水千山的漫游直至离世为线索，叙写其一生的传记。",
    "lwgrkfzzl": "梁中堂1979至1984年间所撰人口学论文集，围绕本世纪末人口增长为零的方案提出批评，主张二胎间隔八至十年的人口发展战略，并论及老龄化与农村人口。",
    "makewaerduo": "二十则短篇，按春夏秋冬四季循环排列，写城市小工马可瓦尔多一家在工业都市里捕捉自然与梦想的遭遇。",
    "mayinchukao": "考证“马寅初事件”：上篇梳理马寅初与新人口论受批判的经过，下篇考辨“康生、陈伯达批判马寅初”之说，附《光明日报》大事记及批判文章目录。",
    "mingrenzhuan": "罗曼·罗兰合集传记，收《贝多芬传》《米开朗琪罗传》《托尔斯泰传》，并附托尔斯泰遗作简析、亚洲反响及致甘地信等。",
    "muriyaoguang": "明清史学者韦庆远的张居正传记与政局研究，自早年生平写到隆万改革及身后清算，另附大事记与引用文献。",
    "renkousuzhi": "从人口学角度系统论述人口素质的专著，依次讲人口素质思想史、人口素质的构成与发展、制约与作用人口素质的社会因素，以及提高人口素质的社会途径。",
    "renkouxue": "分五篇论述人口学说史、现代人口论争、理论人口学与经济人口学、人口社会学与人口经济学及世界人口现状，以马克思主义观点立论。",
    "sanmaozhuan_lxg": "三毛的传记，依其诗文与书信，从重庆出生、少年休学写起，历撒哈拉岁月、荷西之死，直至晚年与离世。",
    "xiaobang": "英国音乐学者艾伦·沃克所撰肖邦传记，依据波兰学界新近研究，自家世、华沙少年时代写到巴黎岁月、与乔治·桑的交往及晚年病逝，并附作品目录与参考书目。",
    "yujianmozhate": "英国历史学家保罗·约翰逊为莫扎特所作的简明传记，依神童、乐器、婚姻、歌剧与晚年五章写其生平与创作，另附丹尼尔·约翰逊《莫扎特在伦敦》。",
    "zgrkwt": "梁中堂人口学文集。收作者1980年代论人口理论、人口发展战略、生育政策及晚婚晚育加间隔试点的文章、报告与书信，附翼城县试行规定和报道。",
    "zgshenhua_shang": "考察东北、西南各族群的创世神话与始祖传说，涉及满、蒙、朱蒙、氐羌、藏、百越、台湾高山族、苗蛮诸系，附蚩尤、昆仑与摩梭普米三篇专论。",
    "zgshenhua_xia": "论中原民族的神话与信仰：族神与姓氏、古代神话、仙乡与归墟、死与再生、牵牛织女、石头、夸父、西王母、王权与神话、黄河水神，附神话与诗、神话研究开拓者等篇。",
    "zuochongyoutu": "论文集：从自由主义、社会民主主义、公共领域，到知识分子的社会角色与人格困境，再到政治正当性的演变，考察1840至1949年现代中国的思想与政治。",
}

WIKI_INTRO = json.loads((ROOT / "sources/wiki_intros.json").read_text(encoding="utf8"))
assert set(BOOK_INTRO) == set(POETRY) | {b["slug"] for b in BOOKS}, set(BOOK_INTRO) ^ (set(POETRY) | {b["slug"] for b in BOOKS})
for _b in BOOKS:
    _b["intro"] = BOOK_INTRO[_b["slug"]]
for _k, _v in POETRY.items():
    _v["intro"] = WIKI_INTRO[_k]["text"] if WIKI_INTRO.get(_k, {}).get("verbatim") and not _v.get("home_intro_own") else BOOK_INTRO[_k]


TIJIE_LINKS = {}

COLLECTIONS = {
    "datangli": {
        "title": "大唐李白", "author": "张大春 著", "children": ["datangli_shaonianyou", "datangli_fenghuangtai", "datangli_jiangjinjiu"],
        "labels": {"datangli_shaonianyou": "第一卷", "datangli_fenghuangtai": "第二卷", "datangli_jiangjinjiu": "第三卷"},
        "home_intro": "张大春的长篇小说，写李白的一生，共三卷：《少年游》《凤凰台》《将进酒》，广西师范大学出版社（理想国）出版。",
        "intro": "《大唐李白》是台湾作家张大春的长篇小说，以小说笔法写李白从少年到中年的游历、交游与诗酒生涯，共三卷：第一卷《少年游》（2014年1月）、第二卷《凤凰台》（2014年7月）、第三卷《将进酒》（2015年6月），广西师范大学出版社（理想国）简体字版。各卷书末附有他人所写的评论或对谈。下面分三卷。",
    },
    "gebenhagen": {
        "title": "哥本哈根三部曲", "author": "［丹麦］托芙·迪特莱弗森 著", "children": ["gebenhagen_qingchen", "gebenhagen_mingliang", "gebenhagen_baizhou"],
        "labels": {"gebenhagen_qingchen": "第一部", "gebenhagen_mingliang": "第二部", "gebenhagen_baizhou": "第三部"},
        "home_intro": "丹麦女作家托芙·迪特莱弗森的自传体三部曲《清晨》《所有明亮的梦》《白昼坠落》，写她在哥本哈根工人家庭的成长、写作与成瘾之路。",
        "intro": "《哥本哈根三部曲》是丹麦女作家托芙·迪特莱弗森（Tove Ditlevsen）的自传体作品，由《清晨》《所有明亮的梦》《白昼坠落》三部组成，写她在哥本哈根工人家庭的成长、写作与成瘾之路。中译本为刘奕奕译，南海出版公司2024年版。下面分三部。",
    },
    "zgshenhua": {
        "title": "中国神话世界", "author": "王孝廉 著", "children": ["zgshenhua_shang", "zgshenhua_xia"],
        "labels": {"zgshenhua_shang": "上编", "zgshenhua_xia": "下编"},
        "home_intro": "王孝廉的中国神话研究，分上、下编：上编考察东北、西南族群的创世神话，下编论中原民族的神话与信仰。",
        "intro": "《中国神话世界》是台湾学者王孝廉的中国神话研究，分上、下两编：上编《东北、西南族群创世神话及其文化》以各民族的创世神话为研究主轴，下编《中原民族的神话与信仰》以主题学的方式对中国神话作宏观论述。洪叶文化事业有限公司2006年增订版。下面分上、下编两项。",
    },
    "gudianwenxuedudu": {
        "title": "中国古典文学读本丛书典藏", "author": "人民文学出版社 编", "children": ["libaishixuan", "songcisanbaishoujianzhu", "sushishicixuan", "tangsongcijianshi", "jinyuanmingqingcixuan", "songshixuanzhu", "yuanzhenshiwenxuan", "xinqijicixuan", "wangweishixuan", "yuefushixuan", "yuanrenzajuxuan", "hanyushixuan", "dufushixuanzhu", "shijixuan", "liuyongcixuanzhu", "zgguxijuxuan", "gongzizhenxuanji", "qiujinxuanji", "chutangsijieshixuan", "guanhanqingxuanji", "dufushixuan", "tangwenxuan"],
        "home_intro": "人民文学出版社“中国古典文学读本丛书典藏”：李白、杜甫、苏轼、辛弃疾等诗词选注，宋词、元杂剧、史记、唐文选等二十二种，原书的题解与注释一并收入。",
        "intro": "“中国古典文学读本丛书”是人民文学出版社的古典文学选注本丛书，这里收其典藏本中的二十二种：李白、王维、杜甫、韩愈、元稹、龚自珍、秋瑾等诗文选，宋词三百首笺注、唐宋词简释、柳永、苏轼、辛弃疾和金元明清词选，乐府诗选、宋诗选注、史记选、唐文选，以及元人杂剧选、关汉卿选集和中国古代戏剧选。各册的题解与注释都是原书的，已按本站的格式放在所注段落之后；文字据书籍扫描件识别整理，尚未逐字校对。",
    },
    "mingrenyishi": {
        "title": "中国名人轶事丛书", "author": "吴洪激 主编", "children": ["pusonglingchuanqi"],
        "labels": {"pusonglingchuanqi": "之五"},      # 各册在丛书中的序号，显示在目录卡片书名前；后续册数在这里补
        "home_intro": "吴洪激主编的传记丛书，搜集中国名人未经正史记载的稗类野史与佚事珍闻，为历史人物立传；目前收第五册《蒲松龄传奇》。",
        "intro": "《中国名人轶事丛书》由吴洪激主编。据丛书出版缘由，所谓“轶事”，指未经史书记载而散失之事；丛书倡导广泛搜集中国名人的稗类野史、佚事珍闻，正史、野史兼容，用浅显的口语写成通俗易读的名人传奇，塑造有别于正史的人物形象。目前收入第五册《蒲松龄传奇》（熊文祥著），其余各册陆续补入。",
    },
}
COLLECTION_OF = {}
for _k, _c in COLLECTIONS.items():
    for _child in _c["children"]:
        COLLECTION_OF[_child] = _k
PARENT_CRUMBS = {}      # 书 slug → 它上面各层目录的面包屑（从外到内）；href 相对于 books/<书>/
for _child, _k in COLLECTION_OF.items():
    _chain, _cur = [], _k
    while _cur:
        _chain.append((COLLECTIONS[_cur]["title"], f"../{_cur}/index.html"))
        _cur = COLLECTIONS[_cur].get("parent")
    PARENT_CRUMBS[_child] = _chain[::-1]


def top_crumbs(slug, r):
    return [("现代文库", r + "index.html")] + PARENT_CRUMBS.get(slug, [])


INTRO_ED_CASE = {"mutianzi"}


def intro_html(slug):
    """目录页简介：维基文库标题下有介绍则用之，否则同首页简介；按换行分段。"""
    text = WIKI_INTRO.get(slug, {}).get("text") or BOOK_INTRO[slug]
    fmt = ed_plain if POETRY.get(slug, {}).get("original_only") else (lambda h: ed_html(h, [False]))  # 仅“只整理原文”的书去尖括号
    if slug in INTRO_ED_CASE:      # 简介里编者的“案：……”按语显示为小字灰体
        base = fmt
        fmt = lambda h: re.sub(r"( 案：.*)$", r'<span class="ed">\1</span>', base(h))
    out = "".join(f'<p class="intro">{fmt(esc(x))}</p>' for x in text.split("\n") if x.strip())
    # 全书题解（src/<slug>/tijie）不另立页面，接在简介之后，每段以“主题。”领起
    path = ROOT / "src" / slug / "tijie" / "01.txt"
    if path.exists():
        for para in parse_poems([path])[0]["intro"][:2]:       # 只留前两段，去掉“主题。”标题，并入简介
            head, sep, rest = para.partition("。")
            out += f'<p class="intro tijie">{esc(rest if sep else para)}</p>'
    for label, url, *shown in TIJIE_LINKS.get(slug, []):
        out += f'<p class="intro tijie"><strong>{esc(label)}：</strong><a href="{esc(url)}">{esc(shown[0] if shown else url)}</a></p>'
    return out


CIRC = re.compile(r"([\u2460-\u2473\u3251-\u325f]+)")
CIRC1 = re.compile(r"[\u2460-\u2473\u3251-\u325f]")
CIRC_LEAD = re.compile(r"^([\u2460-\u2473\u3251-\u325f])\s*")


def circ_num(c):
    """①→1 … ⑳→20，㉑→21 …"""
    return ord(c) - 0x2460 + 1 if c <= "\u2473" else ord(c) - 0x3251 + 21


def ed_html(h, state):
    """〈…〉是编者夹注：包进 .ed（小字灰色）；夹注跨句时在每句内各自闭合、续开。state 是长度 1 的列表，记录是否仍在夹注内。"""
    if "〈" not in h and "〉" not in h and not state[0]:
        return h
    out = ['<span class="ed">'] if state[0] else []
    prev = ""
    for c in h:       # state[0] 是夹注嵌套深度（〈…〈…〉…〉 里层不另开 span）
        pc, prev = prev, c
        if c == "〈" and pc == "■":     # “■〈…〉”是原站对缺字的造字描述，不是夹注，照字面显示
            out.append(c)
        elif c == "〈":
            if not state[0]:
                out.append('<span class="ed">')
            out.append('<i class="br">〈</i>'); state[0] = int(state[0]) + 1       # 尖括号留在文本里（保持原文），但不显示
        elif c == "〉" and state[0]:
            out.append('<i class="br">〉</i>'); state[0] = int(state[0]) - 1
            if not state[0]:
                out.append("</span>")
        else:
            out.append(c)
    if state[0]:
        out.append("</span>")
    return "".join(out)


def ed_plain(h):
    """标题、目录、简介里的〈…〉小注：去掉尖括号，只留小字灰体。"""
    return ed_html(h, [False]).replace("〈", "").replace("〉", "")


def title_h(t):
    """标题（目录条目、页标题）：转义后，〈…〉小注去掉尖括号、显示为小字灰体。"""
    return ed_plain(esc(t))


def poem_orig(text):
    out = []
    for i, part in enumerate(CIRC.split(esc(text))):
        out.append(f"<sup>{part}</sup>" if i % 2 else part.replace("/", "<br>"))
    return "".join(out)


def parse_poems(paths):
    sections = []
    cur = None
    for path in paths:
        for ln in path.read_text(encoding="utf8").splitlines():
            ln = ln.rstrip()
            if not ln.strip():
                continue
            if ln.startswith("# "):
                cur = {"title": ln[2:].strip(), "intro": [], "chunks": []}
                sections.append(cur)
            elif ln.startswith("题解："):
                cur["intro"].append(ln[3:].strip())
            elif ln.startswith("原："):
                if "||" in ln:
                    o, t = (x.strip() for x in ln[2:].split("||", 1))
                else:
                    o, t = ln[2:].strip(), None
                cur["chunks"].append({"o": o, "t": t, "notes": []})
            elif ln.startswith("诗："):
                if "||" in ln:      # 带白话的诗行：居中显示，逐句悬浮白话
                    o, t = (x.strip() for x in ln[2:].split("||", 1))
                    cur["chunks"].append({"o": o, "t": t, "verse": True, "notes": []})
                else:
                    cur["chunks"].append({"o": ln[2:].strip(), "t": None, "verse": True, "notes": []})
            elif ln.startswith("图题："):
                cur["chunks"].append({"o": ln[3:], "t": None, "diagram": True, "notes": []})
            elif ln.startswith("图行："):
                last = cur["chunks"][-1]
                assert last.get("diagram"), (path, "图行没有图题")
                last["o"] += "\n" + ln[3:]
            elif ln.startswith("表题："):
                cur["chunks"].append({"tbl": {"cap": ln[3:].strip(), "head": None, "rows": []}, "notes": []})
            elif ln.startswith("表头："):
                last = cur["chunks"][-1] if cur["chunks"] else None
                if last and "tbl" in last and last["tbl"]["head"] is None and not last["tbl"]["rows"]:
                    last["tbl"]["head"] = ln[3:].split("｜")
                else:
                    cur["chunks"].append({"tbl": {"cap": "", "head": ln[3:].split("｜"), "rows": []}, "notes": []})
            elif ln.startswith("表行："):
                if not cur["chunks"] or "tbl" not in cur["chunks"][-1]:      # 无题无头的表：由首行表行开表
                    cur["chunks"].append({"tbl": {"cap": "", "head": None, "rows": []}, "notes": []})
                cur["chunks"][-1]["tbl"]["rows"].append(ln[3:].split("｜"))
            elif ln.startswith("注原："):      # 照录原站注释：一行一条，不再拆分
                cur["chunks"][-1]["notes"].append(ln[3:].strip())
            elif ln.startswith("注："):
                cur["chunks"][-1]["notes"].extend(split_notes(ln[2:].strip()))
            else:
                raise ValueError(f"{path}: 无法解析：{ln}")
    return sections


YEAR_LEAD = re.compile(r"^((?:宋|金)?(?:徽宗|钦宗|高宗|孝宗|光宗|宁宗)?(?:宣和|靖康|建炎|绍兴|隆兴|乾道|淳熙|绍熙|庆元|嘉泰|开禧|嘉定)?(?:[一二三四五六七八九十]+|元)年(?:[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]?)?)")      # 瓯北诗话·陆放翁年谱的纪年
DRAMA = re.compile(r"(〔[^〕]*〕|【[^】]*】)")
# 只有题解与注释、不设白话的书（原文本身是白话或半白话）
NOTES_ONLY = set()
STAGE_BOOKS = set()
# 科白、脚色用圆括号标注的剧本（桃花扇，以及维基文库上一批元杂剧、六十种曲）：括号内同样显示为小字灰体
PAREN_STAGE_BOOKS = set()
# 姑妄言：行内批语【…】
GUJIN_COMMENT = re.compile(r"(〔[^〕]*〕)")      # 古今笑（原名古今谭概）：各部小序“〔子犹曰：……〕”
GUWANG_BATCH = re.compile(r"(【[^】]*】)")
# 花月痕：〔曲牌〕、（科白）以及“《金缕曲》一阕云”式的词牌
HUAYUE_DRAMA = re.compile(r"(〔[^〕]*〕|\([^()]*\)|（[^（）]*）|《[^》]{2,6}》(?=词?一?[阕首]|词云|词曰))")
PEACH_DRAMA = re.compile(r"(〔[^〕]*〕|【[^】]*】|\([^()]*\)|（[^（）]*）)")
ERKE_STAGE = re.compile(r"(〈（[^〉]*）〉|〔[^〕]*〕|【[^】]*】)")
PEACH_TUNES = {"鹧鸪天", "皂罗袍"}
WESTERN_STAGE = re.compile(r"扮|科|(?:云|唱|下|上|上开|上去|念|念曰|白|了|坐|叫|起发)$")
WESTERN_STAGE_EXTRA = {"洁叫了，住", "红见仆人", "见夫人", "歌曰"}


def _verse_like(o):
    return len(o) >= 8 and "“" not in o and "”" not in o and all(len(x) <= 9 for x in re.split(r"[，。！？；、]", o))


def _lyric_like(o):
    """曲词：分句平均不超过 9 字。"""
    parts = [x for x in re.split(r"[，。！？；、]", o) if x]
    return len(o) >= 8 and len(parts) >= 3 and sum(map(len, parts)) / len(parts) <= 9


def hyh_verse(o, prev_poem=False):
    """花月痕：书中的诗多以“…”引出，首行带引号，通用的 is_poem 认不全。整段是五言或七言诗句（至少两句，或紧接在诗行之后）才居中。"""
    t = o.strip().lstrip("“‘").rstrip("”’")
    if not 5 <= len(t) <= 64 or re.search(r"[“”：（）〔〕]", t):
        return False
    clauses = [x for x in re.split(r"[，。！？；、]", t) if x]
    return (len(clauses) >= 2 or prev_poem) and all(len(x) in (5, 7) for x in clauses)


def is_poem(o, prev, prev_poem=False, nxt=""):
    """红楼梦等：诗词曲联在原文里没有单独标记。以“/”分行的短行段落，紧接在“念道：”“联云：”“正是：”等引语之后的无引号短段，
    紧接在诗行之后的无引号短段，以及曲牌名（短标题，后面紧跟曲词），视为诗歌（含对联、曲），页面居中。“下回分解”之类的回末套语不算。"""
    segs = o.split("/")
    if len(segs) > 1:
        if "下回" in o or re.search(r"[道曰笑说][：:]“", o):
            return False
        return max(len(re.sub(r"\s*[—―]+.*$", "", x)) for x in segs) <= 40
    if len(o) <= 10 and not re.search(r"[，。！？；：“”、]", o) and nxt and "/" not in nxt and _lyric_like(nxt):
        return True    # 曲牌名
    if prev_poem and len(o) <= 200 and not re.search(r"却说|且说|话说|看官|只见|当下", o) and _lyric_like(o) and len(prev) <= 10 and not re.search(r"[，。！？；：“”、]", prev):
        return True    # 曲牌名之后的曲词
    if len(o) >= 60 or "“" in o or "”" in o or "下回" in o or "且听" in o:
        return False
    if prev and re.search(r"(诗|词|曰|云|歌|赞|联|道|是|如|念|唱)[：:—]+$", prev):
        return True
    return prev_poem and bool(re.search(r"[，。！？；]$", o)) and all(len(x) in (5, 7) or "兮" in x for x in re.split(r"[，。！？；]", o) if x)


def _verse_seg(x):
    return (len(x) <= 40 and re.search(r"[，。！？；]$", x) and not re.search(r"[“”‘’「」『』：]", x)
            and "下回" not in x and all(4 <= len(y) <= 9 for y in re.split(r"[，。！？；]", x) if y))


def split_poem_runs(o):
    """正文里夹着的整行诗（连续两行以上，如回首诗、回末对联）：返回 [(是否诗, 文本), ...]；没有则 None。"""
    segs = o.split("/")
    flags = [bool(_verse_seg(x)) for x in segs]
    out, i = [], 0
    while i < len(segs):
        j = i
        while j < len(segs) and flags[j] == flags[i]:
            j += 1
        out.append([flags[i] and j - i >= 2, "/".join(segs[i:j])])
        i = j
    merged = []
    for isp, t in out:
        if merged and merged[-1][0] == isp:
            merged[-1][1] += "/" + t
        else:
            merged.append([isp, t])
    return merged if any(m[0] for m in merged) and len(merged) > 1 else None


_ORPHAN = re.compile(r"[\s…⋯□.。)）」』’”〉：；，、！？\]〕]*")


def sent_units(text):
    """切句；只剩标点、省略号或缺字符的残片，并入上一句（与 split_pairs 的配对一致）。"""
    sents = []
    for s in split_sents(text):
        if sents and _ORPHAN.fullmatch(s):
            sents[-1] += s
        else:
            sents.append(s)
    return sents


def drama_html(text, stage_book=None):
    out = []
    pattern = GUJIN_COMMENT if stage_book == "gujintangai" else GUWANG_BATCH if stage_book == "guwangyan" else HUAYUE_DRAMA if stage_book == "huayuehen" else PEACH_DRAMA if stage_book in PAREN_STAGE_BOOKS else {"erke": ERKE_STAGE}.get(stage_book, DRAMA)
    for i, part in enumerate(pattern.split(text)):
        if i % 2:
            label = part[1:-1].strip()
            tune = part.startswith("【") or (stage_book == "erke" and part.startswith("〔"))
            if stage_book == "xixiangji" and tune:
                tune = not (WESTERN_STAGE.search(label) or label in WESTERN_STAGE_EXTRA)
            elif stage_book in ("guwangyan", "gujintangai"):      # 行内批语、小序整体为小字灰体
                tune = False
            elif stage_book == "huayuehen":      # 书中穿插的曲：〔曲牌〕为曲牌，（…）为科白
                tune = part.startswith(("〔", "《"))
            elif stage_book == "taohuashan":
                tune = tune or label in PEACH_TUNES or bool(re.fullmatch(r"鼓词[一二三四五六七八九十]+", label))
            cls = "cp" if tune else "sd"
            label_html = esc(part).replace("/", "<br>") if stage_book else esc(part)
            if stage_book == "gujintangai":      # 〔〕留在文本里（保持原文），但不显示
                label_html = f'<i class="br">〔</i>{esc(part[1:-1])}<i class="br">〕</i>'
            out.append(f'<span class="{cls}">{label_html}</span>')
        else:
            out.append(esc(part).replace("/", "<br>"))
    return "".join(out)


def circ_sup(h, on):
    """原站正文里的圆圈数字注号（①②…）显示为上标。"""
    return CIRC1.sub(lambda m: f'<sup class="n" data-n="{circ_num(m.group())}"></sup>', h) if on else h


def table_html(t):
    def cell(tag, c):
        return f"<{tag}>" + "<br>".join(esc(x) for x in c.split("／")) + f"</{tag}>"
    head = ""
    if t["head"]:
        head = "<thead><tr>" + "".join(cell("th", c) for c in t["head"]) + "</tr></thead>"
    body = "".join("<tr>" + "".join(cell("td", c) for c in r) + "</tr>" for r in t["rows"])
    cap = f"<h4 class=\"tcap\">{esc(t['cap'])}</h4>" if t["cap"] else ""
    return f'{cap}<div class="biao-wrap"><table class="biao{" biao-n" if len(t["rows"][0] if t["rows"] else []) >= 10 else ""}">{head}<tbody>{body}</tbody></table></div>'


toc_written = set()
TOC_JS = """(function(){var D=__DATA__;var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
"""


def overlay_notes(bslug, slug, secs):
    """白话小说（只有原文的几十部）的自撰题解与注释：sources/<书>/notes/<页>.json = {"题解": "…", "注": ["词语：解释", ...]}。
    每条注挂到原文里含该词语的段（从上一条所在段起往后找，找不到再从头找），所以注的顺序最好随原文顺序。"""
    f = ROOT / "sources" / bslug / "notes" / f"{slug}.json"
    if not f.exists():
        return
    d = json.loads(f.read_text(encoding="utf8"))
    guide = [g.strip() for g in d.get("题解", "").split("\n") if g.strip()]
    assert guide, (bslug, slug, "缺题解")
    secs[0]["intro"].extend(guide)
    chunks = [c for s_ in secs for c in s_["chunks"] if "tbl" not in c]
    i = 0
    for note in d.get("注", []):
        word = note.split("：", 1)[0].strip() if "：" in note else ""
        assert word, (bslug, slug, "注格式应为“词语：解释”", note[:20])
        for k in list(range(i, len(chunks))) + list(range(0, i)):
            if word in chunks[k]["o"].replace("/", ""):
                chunks[k]["notes"].extend(split_notes(note.strip()))
                i = k
                break
        else:
            raise AssertionError((bslug, slug, "注的词语不在本回原文里", word))


def overlay_gloss(bslug, slug, secs):
    """给只有原文页的书叠加逐句白话：sources/<书>/gloss/<页>__<起始段号>.json = {"start": 起始段号, "白话": ["句白话¦句白话", ...]}，
    每个元素对应该页第 start+k 个原文段（段序同 tools/gloss_book.py show 所列），段内每个以。！？；结束的原文句对应一句，¦ 分隔。"""
    d = ROOT / "sources" / bslug / "gloss"
    files = sorted(d.glob(f"{slug}__*.json")) + ([d / f"{slug}.json"] if (d / f"{slug}.json").exists() else [])
    if not files:
        return
    chunks = [c for s_ in secs for c in s_["chunks"] if "tbl" not in c]
    for f in files:
        data = json.loads(f.read_text(encoding="utf8"))
        start = data.get("start", 0)
        for k, tr in enumerate(data["白话"]):
            c = chunks[start + k]
            sents, parts = split_sents(c["o"]), tr.split("¦")
            assert len(parts) == len(sents) and all(x.strip() for x in parts), (bslug, slug, start + k, "句数", len(sents), len(parts))
            assert [o for o, _t in split_pairs(c["o"], tr)] == sents, (bslug, slug, start + k, "会退回整段悬浮")
            c["t"] = tr


def build_poetry(bslug, spec):
    r = "../../"
    base = SRC / bslug
    btitle = spec["title"]
    pages = []
    for slug, title in spec["pages"]:
        if slug is None:
            pages.append((None, title, []))
            continue
        files = sorted((base / slug).glob("*.txt")) if (base / slug).exists() else []
        pages.append((slug, title, files))
    avail = [i for i, (_, _, f) in enumerate(pages) if f]
    cells, total = [], 0
    for i, (slug, title, files) in enumerate(pages):
        if slug is None:
            wide = ' style="grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr))"' if spec.get("wide_index") else ""
            cells.append(f'</ul><h3 class="grp">{esc(title)}</h3><ul class="vols"{wide}>')
            continue
        if not files:
            status = "阙" if slug in spec.get("missing_slugs", ()) else "亡" if slug in spec.get("lost_slugs", ()) else "待整理"
            cells.append(f'<li class="todo"><span>{esc(title)}<small>{status}</small></span></li>')
            continue
        secs = parse_poems(files)
        overlay_notes(bslug, slug, secs)
        overlay_gloss(bslug, slug, secs)
        stage_book = bslug if bslug in STAGE_BOOKS and (bslug != "taohuashan" or slug.startswith("p")) else None
        if (bslug, slug) == ("erke", "040"):
            stage_book = bslug
        paragraph_style = "dr" if stage_book or not spec.get("prose") else ({"huayuehen": "nv sdi", "guwangyan": "nv gwy", "gujintangai": "nv sdi"}.get(bslug, "nv"))
        dstyle = stage_book or (bslug if bslug in ("huayuehen", "guwangyan", "gujintangai") else None)      # 花月痕：正文里穿插的曲牌、科白也显示为小字灰体
        nchunk = sum(1 for s in secs for c in s["chunks"] if "tbl" not in c)
        total += len(secs) if spec.get("count_entries") else nchunk
        cnt = (spec["count"](secs) if "count" in spec else
               (None if spec.get("no_count") else (len(secs), spec.get("unit2", spec.get("unit", "节")))))
        small = f"<small>{cnt[0]}{cnt[1]}</small>" if cnt and cnt[0] > 1 else ""
        index_label = spec.get("page_options", {}).get(slug, {}).get("index_label")
        if index_label:
            small = f"<small>{esc(index_label)}</small>"
        cells.append(f'<li class="ok"><a href="{slug}.html">{title_h(title)}{small}</a></li>')
        uid = 0
        body_secs = []
        for si, sec in enumerate(secs, 1):
            parts = [f'<section class="entry" id="e{si}">']
            multi = len(secs) > 1 or bool(spec.get("sub_single"))      # 选本：卷内只有一篇也列子目录条目、正文加子标题
            parts.append(f'<h3>{ed_plain(esc(sec["title"]))}</h3>' if multi and sec["title"] != title and not (bslug == "gujintangai" and sec["title"] == "正文") else "")
            entry_source = spec.get("section_sources", {}).get(slug, {}).get(sec["title"])
            if entry_source:
                label = esc(entry_source.get("label", "维基文库"))
                revision = entry_source.get("revision")
                version = f"（修订版本 {esc(revision)}）" if revision else ""
                credit = f'；原文据<a href="{esc(entry_source["url"])}">{label}</a>{version}'
                if is_wiki_source(entry_source["url"]):
                    credit = f'<span hidden>{credit}</span>'
                parts.append(f'<p class="hint source-note">原署／材料归属：{esc(entry_source["author"])}{credit}。</p>')
            if sec["intro"]:
                uid += 1
                items = "".join(f"<p>{esc(x)}</p>" for x in sec["intro"])
                parts.append(
                    f'<button class="note-btn" type="button" aria-expanded="false" aria-controls="n{uid}">'
                    f'<span class="caret">▸</span> 题解</button><div class="notes intro-box" id="n{uid}" hidden>{items}</div>')
            prev_o, prev_poem = "", False
            ed_state = [False]
            held_cn = []          # 花月痕：曲牌段的注释，并入随后的曲词段
            held_cn_open = False   # 正处在“科白/曲牌 → 曲词”的连排中
            chunks_ = sec["chunks"]
            for ci, ch in enumerate(chunks_):
                if "tbl" in ch:
                    parts.append(table_html(ch["tbl"]))
                    continue
                if ch.get("diagram"):
                    parts.append(f'<pre class="source-diagram" style="max-width:100%;overflow-x:auto">{esc(ch["o"])}</pre>')
                    continue
                chunk_start = len(parts)
                _tune = lambda c: "o" in c and bool(re.fullmatch(r"〔[^〕]*〕", c["o"].strip()))
                _stage = lambda c: "o" in c and bool(re.fullmatch(r"（[^）]*）", c["o"].strip()))
                # 花月痕：（科白）+〔曲牌〕+曲词 视作同一行：前两者靠左、曲词接其后，注号连续、注释合成一组
                lead_tune = bslug == "huayuehen" and (_tune(ch) or (_stage(ch) and ci + 1 < len(chunks_) and _tune(chunks_[ci + 1])))
                follow_tune = bslug == "huayuehen" and not lead_tune and bool(held_cn_open)
                pg = spec.get("ping_paras", {}).get(slug, 0)
                pg = pg if isinstance(pg, list) else [0, pg]
                pstyle = paragraph_style + (" ping" if pg[0] <= ci < pg[0] + pg[1] else "") + (" tl" if lead_tune else " tn" if follow_tune else "")      # 花月痕：曲牌靠左，曲词接在其后      # 姑妄言：回前卷评，小字灰体
                src_marks = bool(spec.get("source_markers"))
                if src_marks:
                    anchors, chunk_notes = [], ch["notes"]
                else:
                    anchors, chunk_notes = anchor_notes([ch["o"]], ch["notes"])
                at = [a[1] for a in anchors if a is not None]
                tail = sum(1 for a in anchors if a is None)
                is_p = ch.get("verse") or bool(bslug in ("huayuehen", "chanzhenyishi") and hyh_verse(ch["o"], prev_poem)) or bool(bslug != "huayuehen" and spec.get("center_poems") and ch["t"] is None and is_poem(ch["o"], prev_o, prev_poem, chunks_[ci + 1]["o"] if ci + 1 < len(chunks_) and "o" in chunks_[ci + 1] else ""))
                poem = (" poem cen" if bslug in ("taohuashan", "classic_list", "yinshuici", "taoyuanmingji") else " poem") if is_p else ""
                prev_o, prev_poem = ch["o"], is_p
                if ch["t"] is None:
                    runs = split_poem_runs(ch["o"]) if spec.get("center_poems") and not poem else None
                    if runs:
                        pos = 0
                        for ri, (isp, txt) in enumerate(runs):
                            end = pos + len(txt)
                            ins = [max(q - pos, 0) for q in at if q <= end]
                            at = [q for q in at if q > end]
                            body = drama_html(mark_text(txt, ins), dstyle)
                            if ri == len(runs) - 1:
                                body += NOTE_MARK * tail
                            parts.append(f'<p class="v {pstyle}{" poem" if isp else ""}">{circ_sup(body, src_marks)}</p>')
                            pos = end + 1
                    else:
                        body = drama_html(mark_text(ch["o"], at), dstyle)
                        if spec.get("ed_notes"):
                            body = ed_html(body, ed_state)
                        body += NOTE_MARK * tail
                        parts.append(f'<p class="v {pstyle}{poem}">{circ_sup(body, src_marks)}</p>')
                else:
                  spans = ""
                  pairs = marked_pairs(ch["o"], ch["t"], at)
                  if pairs is None:        # 极少数对不齐：该段注释记到段末
                      tail += len(at)
                      pairs = split_pairs(ch["o"], ch["t"])
                  if spec.get("unaligned_translation_details") and not has_sentence_pairs(ch):
                      parts.append(f'<p class="v nv">{drama_html(ch["o"])}</p>'
                                   f'<details class="translation-draft"><summary>段落白话</summary>'
                                   f'<p>{esc(ch["t"])}</p></details>')
                      pairs = []
                  if spec.get("strict_pairs"):
                      original_sents = sent_units(ch["o"])
                      if (len(original_sents) != len(ch["t"].split("¦"))
                              or [o.replace(NOTE_MARK, "") for o, _t in pairs] != original_sents):
                          raise ValueError(f"{bslug}/{slug}: 原文与白话必须逐句对应，不能整段回退")
                  year_bold = bslug == "oubeishihua" and sec["title"] == "陆放翁年谱"      # 年谱：每条开头的年份加粗
                  for pi_, (o2, t2) in enumerate(pairs):
                      if o2.startswith("/"):
                          spans += "<br>"
                          o2 = o2[1:]
                      shown = drama_html(o2, dstyle) if dstyle else poem_orig(o2)      # 戏曲：科白、曲牌在悬浮句内也显示为小字灰体
                      if year_bold and pi_ == 0:
                          shown = YEAR_LEAD.sub(lambda m_: f'<b class="yr">{m_.group(1)}</b>', shown, count=1)
                      spans += f'<span class="s" tabindex="0" data-t="{esc(t2)}">{ed_html(shown, ed_state)}</span>'
                  if pairs:
                      spans += NOTE_MARK * tail
                      label = ch["o"].strip() if bslug == "hanfeizi" else ""
                      if bslug == "guanzi" and re.fullmatch(r"右[^，。；：！？]{1,12}", ch["o"].strip()):
                          parts.append(f'<p class="v end-marker">{spans}</p>')
                      elif label == "右经":
                          parts.append(f'<p class="hf-end-marker">{spans}</p>')
                      elif re.fullmatch(r"说[一二三四五六七八九十]+", label):
                          parts.append(f'<h3 class="hf-example-heading">{spans}</h3>')
                      elif bslug in ("wulinjiushi", "changwuzhi", "yuanye"):      # 地名/条目名单列一行加粗，其后的解释缩进，分清层次
                          is_name = len(ch["o"]) <= (12 if bslug == "wulinjiushi" else 14) and not re.search(r"[。，；：！？“”]" if bslug != "wulinjiushi" else r"[。，；：！？、（“]", ch["o"])
                          parts.append(f'<p class="v {"wl-n" if is_name else "wl-d"}">{spans}</p>')
                      elif ch.get("verse"):
                          parts.append(f'<p class="v {pstyle}{poem}">{spans}</p>')
                      else:
                          parts.append(f'<p class="v">{spans}</p>')
                if lead_tune and not held_cn_open:          # 连排的科白/曲牌/曲词放进同一个块，与上下段分开
                    parts.insert(chunk_start, '<div class="tchain">')
                num = 1 + (len(held_cn) if (lead_tune or follow_tune) and held_cn_open else 0)      # 连排各段视作一段，注号接着排
                for k in range(chunk_start, len(parts)):
                    parts[k], num = number_marks(parts[k], num)
                if lead_tune:
                    held_cn = held_cn + list(chunk_notes)
                    held_cn_open = True
                    chunk_notes = []
                elif follow_tune:
                    chunk_notes = held_cn + list(chunk_notes)
                    held_cn, held_cn_open = [], False
                    parts.append("</div>")
                if chunk_notes:
                    uid += 1
                    if src_marks:     # 原站注释前的圆圈数字改为纯数字序号（无序号的补充说明不编号）
                        li = ""
                        for n in chunk_notes:
                            m = CIRC_LEAD.match(n)
                            li += f'<li data-n="{circ_num(m.group(1))}">{esc(n[m.end():])}</li>' if m else f"<li>{esc(n)}</li>"
                    else:
                        li = "".join(f"<li>{esc(n)}</li>" for n in chunk_notes)
                    note_html = (
                        f'<button class="note-btn" type="button" aria-expanded="false" aria-controls="n{uid}">'
                        f'<span class="caret">▸</span> 注释（{len(chunk_notes)}）</button><ul class="notes plain{" src" if src_marks else ""}" id="n{uid}" hidden>{li}</ul>')
                    parts.append(note_html)
            if held_cn_open:
                parts.append("</div>")
            if si == len(secs) and spec.get("page_tails", {}).get(slug):      # 页末另起一行的附注/链接
                parts.append(spec["page_tails"][slug])
            parts.append("</section>")
            body_secs.append("\n".join(x for x in parts if x))
        single = bool(spec.get("single_page")) and len(pages) == 1     # 只有一个目录条目：书的首页直接就是阅读页
        toc = ""
        if spec.get("side_toc", True):
            # 全书总目录每本书只存一份 toc.js，页面里只留空位、本页的小目录和当前页文件名，由 toc.js 在页面里填入（省下每页重复的整份目录）
            data, sub = [], ""
            for sl, tt, page_files in pages:
                if sl is None:
                    data.append(["g", tt])
                elif sl == slug:
                    if spec.get("sub_toc", True):
                        labels = spec.get("sub_labels", {}).get(slug)
                        subs = [(k, s_) for k, s_ in enumerate(secs, 1) if not (s_["title"] == title and (not s_["chunks"] or spec.get("skip_lead_toc"))) and not (bslug == "gujintangai" and s_["title"] == "正文") and not (spec.get("sub_single") and s_["title"] == title)]
                        numeric = sum(1 for _k, s_ in subs if s_["title"].isdigit()) * 2 > len(subs)
                        if len(subs) >= (1 if spec.get("sub_single") else 2):
                            sub = (f'<ul class="sub{" num" if numeric else ""}">' + "".join(
                                f'<li><a href="#e{k}">{ed_plain(esc(labels[k - 1] if labels and k - 1 < len(labels) else s_["title"]))}</a></li>'
                                for k, s_ in subs) + "</ul>")
                    data.append(["l", ("index" if single else sl) + ".html", title_h(tt)])
                elif page_files:
                    data.append(["l", f"{sl}.html", title_h(tt)])
                else:
                    status = "阙" if sl in spec.get("missing_slugs", ()) else "亡" if sl in spec.get("lost_slugs", ()) else "待整理"
                    data.append(["x", f"{tt}（{status}）"])
            toc_ver = hashlib.md5(json.dumps(data, ensure_ascii=False).encode("utf8")).hexdigest()[:8]      # 目录内容变了就换一个版本号，避免浏览器沿用旧 toc.js
            if bslug not in toc_written:
                toc_written.add(bslug)
                (BOOKS_OUT / bslug).mkdir(parents=True, exist_ok=True)
                (BOOKS_OUT / bslug / "toc.js").write_text(TOC_JS.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":"))), encoding="utf8")
            toc = (f'<details class="toc side" open data-cur="{"index" if single else slug}.html"><summary>总目录</summary><ul></ul>'
                   f'<template>{sub}</template><noscript><p><a href="index.html">全书目录</a></p></noscript></details>'
                   f'<script src="toc.js?v={toc_ver}"></script>')
            if single and not sub:      # 全书只有一页、页内又无小目录：左侧不放只有一条的总目录
                toc = ""
        elif secs:
            tocs = [(k, s) for k, s in enumerate(secs, 1) if not (s["title"] == title and not s["chunks"])]
            numeric = sum(1 for _k, s in tocs if s["title"].isdigit()) * 2 > len(tocs)
            if numeric:
                toc = ('<details class="toc" open><summary>本页目录</summary><ul class="num">'
                       + "".join(f'<li><a href="#e{k}">{esc(s["title"])}</a></li>' for k, s in tocs)
                       + "</ul></details>")
            else:
                toc = ('<details class="toc" open><summary>本页目录</summary><ol>'
                       + "".join(f'<li><a href="#e{k}">{esc(s["title"])}</a></li>' for k, s in tocs)
                       + "</ol></details>")
        prev_i = max([j for j in avail if j < i], default=None)
        next_i = min([j for j in avail if j > i], default=None)
        prev_h = (f'<a href="{pages[prev_i][0]}.html">← {esc(pages[prev_i][1])}</a>' if prev_i is not None
                  else '<span class="off">&nbsp;</span>')
        next_h = (f'<a href="{pages[next_i][0]}.html">{esc(pages[next_i][1])} →</a>' if next_i is not None
                  else '<span class="off">&nbsp;</span>')
        source = spec.get("page_sources", {}).get(slug)
        page_options = spec.get("page_options", {}).get(slug, {})
        revision_note = f'（修订版本 {esc(source["revision"])}）' if source and source.get("revision") else ""
        source_note = (f'{esc(source.get("prefix", "原文据"))}<a href="{esc(source["url"])}">{esc(source.get("label", "维基文库"))}</a>整理{revision_note}；{esc(source.get("after", ""))}'
                       if source else ("本页题解为编者自撰；" if slug == "tijie" and bslug in ("xixiangji", "xiyouji", "shuihuzhuan", "sanguoyanyi", "roupotuan", "zuozhuan") else "原文依所标明底本整理；"))
        if spec.get("omit_source_credit"):
            source_note = ""
        elif source and is_wiki_source(source["url"]):
            source_note = f'<span hidden>{source_note}</span>'
        if page_options.get("no_tip", spec.get("no_tip")):
            hint = ""
            foot_text = "注释为编者自撰，仅供辅助阅读，以原文为准。"
            if spec.get("original_only"):
                hint = "原文阅读版；白话与注释待整理。条目编号为整理者所加。"
                foot_text = spec.get("original_footer", "保留原站校勘记及缺文标记；尚未据影印本逐字校勘。")
        else:
            hint = ""
            foot_text = "白话译文、注释、题解为编者自撰，仅供辅助阅读，以原文为准。"
        if bslug in NOTES_ONLY:
            hint, foot_text = "", "注释、题解为编者自撰，仅供辅助阅读，以原文为准。"
        hint = page_options.get("reading_hint", spec.get("reading_hint", hint))
        foot_text = page_options.get("footer", foot_text)
        if single:
            head = f"""{crumbs(top_crumbs(bslug, r) + [(btitle, None)])}
<h1>{esc(btitle)}<small>{esc(spec["author"])}</small></h1>
{intro_html(bslug)}"""
            pager = ""
        else:
            head = f"""{crumbs(top_crumbs(bslug, r) + [(btitle, "index.html"), (title.replace("〈", "").replace("〉", ""), None)])}
<h1>{title_h(title)}<small>{esc(btitle)}</small></h1>"""
            pager = f'<nav class="pager">{prev_h}<a href="index.html">目录</a>{next_h}</nav>'
        body = f"""<header class="top">
{head}
{f'<p class="hint">{hint}</p>' if hint else ""}
</header>
<main class="reading-layout{"" if toc else " solo"}">
{toc}
<div class="reading-content">
{chr(10).join(body_secs)}
{pager}
</div>
</main>
<div id="tip" role="tooltip" hidden></div>
<footer>{source_note}{foot_text}</footer>"""
        out = BOOKS_OUT / bslug / ("index.html" if single else f"{slug}.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(btitle if single else f'{title.replace("〈", "").replace("〉", "")}·{btitle}', body, r, True), encoding="utf8")
        if single and (BOOKS_OUT / bslug / f"{slug}.html").exists():
            (BOOKS_OUT / bslug / f"{slug}.html").unlink()
    if spec.get("single_page") and len(pages) == 1:
        return total
    intro_credit = ""
    if WIKI_INTRO.get(bslug, {}).get("verbatim") and not spec.get("omit_source_credit"):
        url = esc(WIKI_INTRO[bslug]["url"])
        visibility = "" if spec.get("visible_intro_credit") else " hidden"
        label = "简介据维基文库" if spec.get("visible_intro_credit") else "维基文库"
        intro_credit = (f'<span{visibility}> · <a href="{url}">{label}</a> · '
                        '<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a></span>')
    entry_search = entry_empty = entry_script = ""
    if spec.get("entry_search"):       # 目录页内的篇目搜索框（只过滤本页的篇目，不跳转）
        entry_search = (f'<div class="book-search" role="search" aria-label="搜索篇目">\n<label for="entry-search">搜索篇名或作者</label>\n'
                        '<div class="search-row"><input type="search" id="entry-search" placeholder="例如：赤壁、苏轼、赋" autocomplete="off" '
                        'aria-controls="entry-list"><button type="button" id="entry-clear">清空</button></div>\n'
                        '<p class="search-status" id="entry-status" role="status" aria-live="polite"></p>\n</div>\n')
        entry_empty = '<p class="search-empty" id="entry-empty" hidden>没有找到匹配的篇目，请换个关键词。</p>'
        entry_script = '<script src="../../assets/entry-search.js" defer></script>'
    body = f"""<header class="top">
{crumbs(top_crumbs(bslug, "../../") + [(btitle, None)])}
<h1>{esc(btitle)}<small>{esc(spec["author"])}</small></h1>
{intro_html(bslug)}
</header>
<main>{entry_search}<section class="part"><ul class="vols"{' id="entry-list"' if spec.get('entry_search') else ''}{' style="grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr))"' if spec.get('wide_index') else ''}>{"".join(cells)}</ul>{entry_empty}</section>{entry_script}</main>
<footer>{esc(spec.get("index_footer", f'已整理 {total} {spec.get("summary_unit", "节")}。'))}{intro_credit}</footer>"""
    (BOOKS_OUT / bslug).mkdir(parents=True, exist_ok=True)
    (BOOKS_OUT / bslug / "index.html").write_text(page(btitle, body, "../../"), encoding="utf8")
    for old_slug, target in spec.get("page_redirects", {}).items():
        redirect = f'<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0; url={esc(target)}"><link rel="canonical" href="{esc(target)}"><title>{esc(btitle)}·合并阅读</title></head><body><h1>合并阅读</h1><p>本篇已合入统一阅读页：<a href="{esc(target)}">打开本篇</a></p></body></html>'
        (BOOKS_OUT / bslug / (old_slug + ".html")).write_text(redirect, encoding="utf8")
    return total


# 书名首字的拼音首字母，供首页字母索引使用；新增书目若首字不在表内，build 会报错提醒补充。
INITIAL = {"历": "L", "中": "Z", "宋": "S", "李": "L", "张": "Z", "红": "H", "蒲": "P", "二": "E", "佛": "F", "哥": "G", "献": "X", "九": "J", "聆": "L", "论": "L", "马": "M", "名": "M", "暮": "M", "人": "R", "三": "S", "肖": "X", "遇": "Y", "左": "Z", "大": "D"}


def build_collection(slug):
    """多级目录页（三言二拍 → 三言/二拍 → 各书）：简介 + 下一级条目的卡片。"""
    c = COLLECTIONS[slug]
    cards = []
    for k in c["children"]:
        if k in COLLECTIONS:
            title, author, intro = COLLECTIONS[k]["title"], COLLECTIONS[k]["author"], COLLECTIONS[k]["card_intro"]
        else:
            title, author, intro = POETRY[k]["title"], POETRY[k]["author"], BOOK_INTRO[k]
        vol = c.get("labels", {}).get(k)
        tag = f'<span class="vol">{esc(vol)}</span>' if vol else ""
        cards.append(f'<li><a href="../{k}/index.html">{tag}<strong>{esc(title)}</strong><span>{esc(author)}</span><p>{esc(intro)}</p></a></li>')
    body = f"""<header class="top">
{crumbs([("现代文库", "../../index.html")] + PARENT_CRUMBS.get(slug, []) + [(c["title"], None)])}
<h1>{esc(c["title"])}<small>{esc(c["author"])}</small></h1>
<p class="intro">{esc(c["intro"])}</p>
</header>
<main><ul class="books">{"".join(cards)}</ul></main>
<footer>本页简介为编者自撰。</footer>"""
    (BOOKS_OUT / slug).mkdir(parents=True, exist_ok=True)
    (BOOKS_OUT / slug / "index.html").write_text(page(c["title"], body, "../../"), encoding="utf8")


def build_home():
    def card(href, b):
        first = b["title"][0]
        assert first in INITIAL, f"首页字母索引缺少“{first}”的拼音首字母（build.py INITIAL）"
        return (f'<li data-letter="{INITIAL[first]}"><a href="books/{href}/index.html"><strong>{esc(b["title"])}</strong>'
                f'<span>{esc(b["author"])}</span><p>{esc(b["intro"])}</p></a></li>')
    cards = ("".join(card(b["slug"], b) for b in BOOKS) + "".join(card(k, v) for k, v in POETRY.items() if k not in COLLECTION_OF)
             + "".join(card(k, dict(c, intro=c["home_intro"])) for k, c in COLLECTIONS.items() if "parent" not in c))
    letters = "".join(f'<button type="button" class="letter" data-letter="{c}" aria-pressed="false">{c}</button>'
                      for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    body = f"""<header class="top"><h1>现代文库<small>现代著作的整理本</small></h1></header>
<main>
<div class="book-search" role="search" aria-label="搜索书籍">
<label for="book-search">搜索书名、作者或简介</label>
<div class="search-row"><input type="search" id="book-search" placeholder="例如：亡国、帝王、李祖德" autocomplete="off" aria-controls="book-list"><button type="button" id="search-clear">清空</button></div>
<div class="letters" id="letter-bar" role="group" aria-label="按书名首字拼音首字母浏览">{letters}</div>
<p class="search-status" id="search-status" role="status" aria-live="polite"></p>
</div>
<ul class="books" id="book-list">{cards}</ul>
<nav class="pager" id="pager" aria-label="分页"></nav>
<p class="search-empty" id="search-empty" hidden>没有找到匹配的书籍，请换个关键词。</p>
<script src="assets/search.js" defer></script>
</main>"""
    (ROOT / "index.html").write_text(page("现代文库", body, ""), encoding="utf8")


if __name__ == "__main__":
    for b in BOOKS:
        build_book(b)
    for _k, _v in POETRY.items():
        build_poetry(_k, _v)
    for _k in COLLECTIONS:
        build_collection(_k)
    build_home()
    print("done", dict(ANCHOR_STATS))
