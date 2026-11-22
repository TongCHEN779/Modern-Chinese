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
    "ltlq_v1": _scan_spec("ltlq_v1", "从开端到柏拉图", "［英］C.C.W.泰勒 主编，韩东晖等 译"),
    "mrys_01": _scan_spec("mrys_01", "一代大帝：秦始皇", "吴淑君 著"),
    "mrys_02": _scan_spec("mrys_02", "包青天断案", "毕珍 著"),
    "mrys_03": _scan_spec("mrys_03", "风流学士：苏东坡", "丁永淮、熊文祥 著"),
    "mrys_04": _scan_spec("mrys_04", "菩提达摩传奇", "吴洪激 著"),
    "mrys_06": _scan_spec("mrys_06", "八大山人传奇", "李晃生 著"),
    "mrys_07": _scan_spec("mrys_07", "张居正传奇", "刘之昆 著"),
    "mrys_08": _scan_spec("mrys_08", "诗坛鬼才：李贺", "李盾 著"),
    "mrys_09": _scan_spec("mrys_09", "风流才子唐伯虎", "杨行恭 著"),
    "mrys_10": _scan_spec("mrys_10", "末代名臣——张之洞", "彭友元 著"),
    "mrys_11": _scan_spec("mrys_11", "一代名媛：王昭君", "宁发新 著"),
    "mrys_12": _scan_spec("mrys_12", "风流神判：郑板桥", "吴洪激 著"),
    "mrys_13": _scan_spec("mrys_13", "魏晋狂士：竹林七贤", "毕珍 著"),
    "mrys_14": _scan_spec("mrys_14", "北宋重臣：范仲淹", "鄢家声 著"),
    "mrys_15": _scan_spec("mrys_15", "词坛女杰：李清照", "金仕善 著"),
    "mrys_16": _scan_spec("mrys_16", "文苑异才：金圣叹", "郑卫国 著"),
    "mrys_17": _scan_spec("mrys_17", "山水诗人——孟浩然", "陈文道 著"),
    "mrys_18": _scan_spec("mrys_18", "亘古英才：陆放翁", "万文武 著"),
    "mrys_19": _scan_spec("mrys_19", "千古一相：姜子牙", "汪鹤年 著"),
    "mrys_20": _scan_spec("mrys_20", "绝色美人：西施", "熊文祥 著"),
    "bnbz_00": _scan_spec("bnbz_00", "百年百种优秀中国文学图书目录", "多人 著"),
    "bnbz_01": _scan_spec("bnbz_01", "官场现形记", "李宝嘉 著"),
    "bnbz_02": _scan_spec("bnbz_02", "孽海花", "曾朴 著"),
    "bnbz_03": _scan_spec("bnbz_03", "二十年目睹之怪现状", "吴趼人 著"),
    "bnbz_04": _scan_spec("bnbz_04", "老残游记", "刘鹗 著"),
    "bnbz_05": _scan_spec("bnbz_05", "人境庐诗草", "黄遵宪 著"),
    "bnbz_06": _scan_spec("bnbz_06", "尝试集", "胡适 著"),
    "bnbz_07": _scan_spec("bnbz_07", "女神", "郭沫若 著"),
    "bnbz_08": _scan_spec("bnbz_08", "沉沦", "郁达夫 著"),
    "bnbz_09": _scan_spec("bnbz_09", "呐喊", "鲁迅 著"),
    "bnbz_10": _scan_spec("bnbz_10", "繁星", "冰心 著"),
    "bnbz_11": _scan_spec("bnbz_11", "南社丛选", "胡朴安 选录"),
    "bnbz_12": _scan_spec("bnbz_12", "雨天的书", "周作人 著"),
    "bnbz_13": _scan_spec("bnbz_13", "志摩的诗", "徐志摩 著"),
    "bnbz_14": _scan_spec("bnbz_14", "寄小读者", "冰心 著"),
    "bnbz_15": _scan_spec("bnbz_15", "彷徨", "鲁迅 著"),
    "bnbz_16": _scan_spec("bnbz_16", "野草", "鲁迅 著"),
    "bnbz_17": _scan_spec("bnbz_17", "死水", "闻一多 著"),
    "bnbz_18": _scan_spec("bnbz_18", "背影", "朱自清 著"),
    "bnbz_19": _scan_spec("bnbz_19", "在黑暗中", "丁玲 著"),
    "bnbz_20": _scan_spec("bnbz_20", "倪焕之", "叶圣陶 著"),
    "bnbz_21": _scan_spec("bnbz_21", "啼笑因缘", "张恨水 著"),
    "bnbz_22": _scan_spec("bnbz_22", "缘缘堂随笔", "丰子恺 著"),
    "bnbz_23": _scan_spec("bnbz_23", "新月诗选", "陈梦家 编"),
    "bnbz_24": _scan_spec("bnbz_24", "鲁迅杂感选集", "鲁迅 著"),
    "bnbz_25": _scan_spec("bnbz_25", "望舒草", "戴望舒 著"),
    "bnbz_26": _scan_spec("bnbz_26", "烙印", "臧克家 著"),
    "bnbz_27": _scan_spec("bnbz_27", "子夜", "茅盾 著"),
    "bnbz_28": _scan_spec("bnbz_28", "家", "巴金 著"),
    "bnbz_29": _scan_spec("bnbz_29", "边城", "沈从文 著"),
    "bnbz_30": _scan_spec("bnbz_30", "南行记", "艾芜 著"),
    "bnbz_31": _scan_spec("bnbz_31", "死水微澜", "李劼人 著"),
    "bnbz_32": _scan_spec("bnbz_32", "大堰河", "艾青 著"),
    "bnbz_33": _scan_spec("bnbz_33", "湘行散记", "沈从文 著"),
    "bnbz_34": _scan_spec("bnbz_34", "画梦录", "何其芳 著"),
    "bnbz_35": _scan_spec("bnbz_35", "上海屋檐下", "夏衍 著"),
    "bnbz_36": _scan_spec("bnbz_36", "萍踪忆语", "韬奋 著"),
    "bnbz_37": _scan_spec("bnbz_37", "包身工", "夏衍 著"),
    "bnbz_38": _scan_spec("bnbz_38", "骆驼祥子", "老舍 著"),
    "bnbz_39": _scan_spec("bnbz_39", "黄河大合唱", "光未然 著"),
    "bnbz_40": _scan_spec("bnbz_40", "呼兰河传", "萧红 著"),
    "bnbz_41": _scan_spec("bnbz_41", "屈原", "郭沫若 著"),
    "bnbz_42": _scan_spec("bnbz_42", "十四行集", "冯至 著"),
    "bnbz_43": _scan_spec("bnbz_43", "给战斗者", "田间 著"),
    "bnbz_44": _scan_spec("bnbz_44", "速写三篇", "张天翼 著"),
    "bnbz_45": _scan_spec("bnbz_45", "小二黑结婚", "赵树理 著"),
    "bnbz_46": _scan_spec("bnbz_46", "传奇", "张爱玲 著"),
    "bnbz_47": _scan_spec("bnbz_47", "小城风波", "沙汀 著"),
    "bnbz_48": _scan_spec("bnbz_48", "风雪夜归人", "吴祖光 著"),
    "bnbz_49": _scan_spec("bnbz_49", "白毛女", "贺敬之、丁毅 著"),
    "bnbz_50": _scan_spec("bnbz_50", "穆旦诗集（1939—1945）", "穆旦 著"),
    "bnbz_51": _scan_spec("bnbz_51", "财主底儿女们", "路翎 著"),
    "bnbz_52": _scan_spec("bnbz_52", "果园城记", "师陀 著"),
    "bnbz_53": _scan_spec("bnbz_53", "王贵与李香香", "李季 著"),
    "bnbz_54": _scan_spec("bnbz_54", "解放区短篇创作选", "丁玲、孔厥 等著，周扬 编"),
    "bnbz_55": _scan_spec("bnbz_55", "围城", "钱钟书 著"),
    "bnbz_56": _scan_spec("bnbz_56", "人生采访", "萧乾 著"),
    "bnbz_57": _scan_spec("bnbz_57", "雅舍小品", "梁实秋 著"),
    "bnbz_58": _scan_spec("bnbz_58", "曹禺剧本选", "曹禺 著"),
    "bnbz_59": _scan_spec("bnbz_59", "保卫延安", "杜鹏程 著"),
    "bnbz_60": _scan_spec("bnbz_60", "阿诗玛：撒尼民间叙事长诗", "云南人民文工团圭山工作组 搜集整理"),
    "bnbz_61": _scan_spec("bnbz_61", "红旗谱", "梁斌 著"),
    "bnbz_62": _scan_spec("bnbz_62", "茶馆", "老舍 著"),
    "bnbz_63": _scan_spec("bnbz_63", "关汉卿", "田汉 著"),
    "bnbz_64": _scan_spec("bnbz_64", "青春之歌", "杨沫 著"),
    "bnbz_65": _scan_spec("bnbz_65", "白洋淀纪事", "孙犁 著"),
    "bnbz_66": _scan_spec("bnbz_66", "城南旧事", "林海音 著"),
    "bnbz_67": _scan_spec("bnbz_67", "创业史", "柳青 著"),
    "bnbz_68": _scan_spec("bnbz_68", "红岩", "罗广斌、杨益言 著"),
    "bnbz_69": _scan_spec("bnbz_69", "燕山夜话", "马南邨 著"),
    "bnbz_70": _scan_spec("bnbz_70", "毛泽东诗词选", "毛泽东 著"),
    "bnbz_71_1": _scan_spec("bnbz_71_1", "李自成（第1卷）", "姚雪垠 著"),
    "bnbz_71_2": _scan_spec("bnbz_71_2", "李自成（第2卷）", "姚雪垠 著"),
    "bnbz_71_3": _scan_spec("bnbz_71_3", "李自成（第3卷）", "姚雪垠 著"),
    "bnbz_71_4": _scan_spec("bnbz_71_4", "李自成（第4卷）", "姚雪垠 著"),
    "bnbz_71_5": _scan_spec("bnbz_71_5", "李自成（第5卷）", "姚雪垠 著"),
    "bnbz_71_6": _scan_spec("bnbz_71_6", "李自成（第6卷）", "姚雪垠 著"),
    "bnbz_71_7": _scan_spec("bnbz_71_7", "李自成（第7卷）", "姚雪垠 著"),
    "bnbz_73": _scan_spec("bnbz_73", "台北人", "白先勇 著"),
    "bnbz_74": _scan_spec("bnbz_74", "家变", "王文兴 著"),
    "bnbz_75": _scan_spec("bnbz_75", "将军族", "陈映真 著"),
    "bnbz_76": _scan_spec("bnbz_76", "郭小川诗选", "郭小川 著"),
    "bnbz_77": _scan_spec("bnbz_77", "哥德巴赫猜想", "徐迟 著"),
    "bnbz_78": _scan_spec("bnbz_78", "百合花", "茹志鹃 著"),
    "bnbz_79": _scan_spec("bnbz_79", "四世同堂", "老舍 著"),
    "bnbz_80": _scan_spec("bnbz_80", "重放的鲜花", "王蒙 等 著"),
    "bnbz_81": _scan_spec("bnbz_81", "随想录", "巴金 著"),
    "bnbz_82": _scan_spec("bnbz_82", "傅雷家书", "傅雷、朱梅馥 著"),
    "bnbz_83": _scan_spec("bnbz_83", "干校六记", "杨绛 著"),
    "bnbz_84": _scan_spec("bnbz_84", "芙蓉镇", "古华 著"),
    "bnbz_85": _scan_spec("bnbz_85", "白色花：二十人集", "绿原、牛汉 编"),
    "bnbz_86": _scan_spec("bnbz_86", "九叶集", "辛笛、陈敬容、杜运燮、杭约赫、郑敏、唐祈、唐湜、袁可嘉、穆旦 著"),
    "bnbz_87": _scan_spec("bnbz_87", "汪曾祺短篇小说选", "汪曾祺 著"),
    "bnbz_88": _scan_spec("bnbz_88", "棋王", "阿城 著"),
    "bnbz_89": _scan_spec("bnbz_89", "北方的河", "张承志 著"),
    "bnbz_90": _scan_spec("bnbz_90", "男人的一半是女人", "张贤亮 著"),
    "bnbz_91": _scan_spec("bnbz_91", "活动变人形", "王蒙 著"),
    "bnbz_92": _scan_spec("bnbz_92", "平凡的世界", "路遥 著"),
    "bnbz_93": _scan_spec("bnbz_93", "红高粱家族", "莫言 著"),
    "bnbz_94": _scan_spec("bnbz_94", "古船", "张炜 著"),
    "bnbz_95": _scan_spec("bnbz_95", "余光中诗选", "余光中 著，刘登翰、陈圣生 选编"),
    "bnbz_96": _scan_spec("bnbz_96", "南渡记", "宗璞 著"),
    "bnbz_97": _scan_spec("bnbz_97", "蒲桥集", "汪曾祺 著"),
    "bnbz_98": _scan_spec("bnbz_98", "白鹿原", "陈忠实 著"),
    "bnbz_99": _scan_spec("bnbz_99", "舒婷的诗", "舒婷 著"),
    "bnbz_100": _scan_spec("bnbz_100", "尘埃落定", "阿来 著"),
    "qsyy_qianhan": _scan_spec("qsyy_qianhan", "前汉历史演义全书", "蔡东藩 著"),
    "qsyy_houhan": _scan_spec("qsyy_houhan", "后汉历史演义全书", "蔡东藩 著"),
    "qsyy_liangjin": _scan_spec("qsyy_liangjin", "两晋历史演义全书", "蔡东藩 著"),
    "qsyy_nanbeichao": _scan_spec("qsyy_nanbeichao", "南北朝历史演义全书", "蔡东藩 著"),
    "qsyy_tang": _scan_spec("qsyy_tang", "唐代历史演义全书", "蔡东藩 著"),
    "qsyy_wudai": _scan_spec("qsyy_wudai", "五代历史演义全书", "蔡东藩 著"),
    "qsyy_song": _scan_spec("qsyy_song", "宋代历史演义全书", "蔡东藩 著"),
    "qsyy_yuan": _scan_spec("qsyy_yuan", "元代历史演义全书", "蔡东藩 著"),
    "qsyy_ming": _scan_spec("qsyy_ming", "明代历史演义全书", "蔡东藩 著"),
    "qsyy_qing": _scan_spec("qsyy_qing", "清代历史演义全书", "蔡东藩 著"),
    "qsyy_minguo": _scan_spec("qsyy_minguo", "民国历史演义全书", "蔡东藩 著"),
    "qsyy_han_gy": _scan_spec("qsyy_han_gy", "汉代宫廷艳史", "徐哲身 著"),
    "qsyy_sui_gw": _scan_spec("qsyy_sui_gw", "隋代宫闱史", "张恂子 著"),
    "qsyy_tang_gy": _scan_spec("qsyy_tang_gy", "唐代宫廷艳史", "许啸天 著"),
    "qsyy_ming_gw": _scan_spec("qsyy_ming_gw", "明代宫闱史", "许啸天 著"),
    "qsyy_qing_gy": _scan_spec("qsyy_qing_gy", "清代宫廷艳史", "许啸天 著"),
    "qsyy_qing_ms": _scan_spec("qsyy_qing_ms", "清朝秘史", "陆士谔 著"),
    "ltlq_v2": _scan_spec("ltlq_v2", "从亚里士多德到奥古斯丁", "［美］大卫·福莱 主编，冯俊等 译"),
    "ltlq_v3": _scan_spec("ltlq_v3", "中世纪哲学", "［英］约翰·马仁邦 主编，孙毅等 译"),
    "ltlq_v4": _scan_spec("ltlq_v4", "文艺复兴和17世纪理性主义", "［英］G.H.R.帕金森 主编，田平等 译"),
    "ltlq_v5": _scan_spec("ltlq_v5", "英国哲学和启蒙时代", "［英］斯图亚特·布朗 主编，高新民等 译"),
    "ltlq_v6": _scan_spec("ltlq_v6", "德国唯心主义时代", "［美］罗伯特·C·所罗门、凯特林·M·希金斯 主编，储昭华等 译"),
    "ltlq_v7": _scan_spec("ltlq_v7", "19世纪哲学", "［新加坡］C.L.腾 主编，刘永红等 译"),
    "ltlq_v8": _scan_spec("ltlq_v8", "20世纪大陆哲学", "［爱尔兰］理查德·柯尔内 主编，鲍建竹等 译"),
    "ltlq_v9": _scan_spec("ltlq_v9", "20世纪科学、逻辑和数学哲学", "［加］斯图亚特·G·杉克尔 主编，江怡等 译"),
    "ltlq_v10": _scan_spec("ltlq_v10", "20世纪意义、知识和价值哲学", "［加］约翰·V·康菲尔德 主编，江怡等 译"),
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
    "ltlq_v1": "《劳特利奇哲学史》十卷本第一卷，十二章分论古希腊城邦文化、前苏格拉底诸派、智者、希腊数学、苏格拉底与柏拉图，附年表与名词解释。",
    "mrys_01": "“中国名人轶事丛书”之一，以正史为骨架、野史为血肉，用十八章故事演述秦始皇从出生、统一六国到病逝沙丘、秦亡的经历。",
    "mrys_02": "“中国名人轶事丛书”之二，以十八篇故事演述包拯（包青天）巡按各地，凭智谋与神异线索平反冤狱、惩办奸恶的断案传说。",
    "mrys_03": "“中国名人轶事丛书”之三。以正史杂说与黄州一带民间传说，讲述苏东坡的才情趣事与宦海浮沉，共六章。",
    "mrys_04": "以传奇笔法写禅宗初祖菩提达摩自天竺香至国三王子出家，到东渡中土、嵩山面壁、传法慧可、只履西归的生平轶事。",
    "mrys_06": "传记体小说，以明清易代为背景，写明宗室后裔朱耷（八大山人）从甲申之变、流亡避祸、出家为僧、改而为道，到弃道还俗、以画寄怀的一生。",
    "mrys_07": "“中国名人轶事丛书”之七，以隆庆驾崩、张居正辅佐幼主万历推行新政为主线，用十八章故事演述这位明代首辅的宦海风云，至其逝后遭清算。",
    "mrys_08": "“中国名人轶事丛书”之八。以传奇笔法写唐代诗人李贺从昌谷降生、少年成名，到应举受阻、长安落魄、入昭义军幕、病归早逝的一生，穿插其诗作。",
    "mrys_09": "以明代才子唐寅（伯虎）的经历为线索写成的传记小说，从赴钱塘、考状元下狱，到为友纾难、装疯脱身，终至自号六如、悟真，共十章。",
    "mrys_10": "以传奇笔法讲述清末名臣张之洞的轶事：会试夺魁、提督学政、两广封疆、筹款办厂、兴学督鄂，直至垂老病殁。",
    "mrys_11": "据香溪一带关于王昭君的民间传说连缀而成的传奇，共二十九章，写昭君从宝坪村入选、出塞和亲，到受封宁胡阏氏的经历。",
    "mrys_12": "吴洪激据民间传说撰写的郑板桥任范县、潍县知县时的十桩判案故事，自《初审石头案》至《宽判杀人案》，书末附郑板桥年谱。",
    "mrys_13": "台湾毕珍所著竹林七贤传记故事，分十章，依次叙写刘伶、嵇康、王戎、阮籍、阮咸、向秀、山涛及山简、嵇绍等后人的轶事。",
    "mrys_14": "鄢家声所著长篇历史故事，分二十四章，写范仲淹戍边、推行庆历新政，与夏竦等守旧势力的斗争，及其子范纯祐与夏碧英的情事，终于《岳阳楼记》。",
    "mrys_15": "“中国名人轶事丛书”之十五，传记文学体裁，以蔡京党祸与靖康之变为背景，十五章演述李清照从嫁入赵家、青州金石生涯到南渡漂泊、晚年编集《漱玉集》的一生。",
    "mrys_16": "以民间传说与史籍杂说为据，叙述明末清初文学批评家金圣叹从少年才名、批点《水浒》到哭庙案遇难的传奇一生。",
    "mrys_17": "陈文道采集整理的孟浩然传说故事五十八篇，写其自幼聪慧、行侠仗义、惩恶济贫、漫游京华及与诗友交游，书末附孟浩然年表。",
    "mrys_18": "“中国名人轶事丛书”之十八，以十五章故事演述南宋诗人陆游自少年爱诗、沈园惊鸿、从军南郑，到屡遭罢黜、晚年归居山阴的一生。",
    "mrys_19": "“中国名人轶事丛书”之十九。以《封神演义》为主要蓝本，糅进民间传说，从飞熊降世、中年悟道写到八十遇文王、金台拜将、辅周灭商，分二十八节讲述姜子牙的传奇一生。",
    "mrys_20": "以吴越之争为背景，围绕西施入吴、助越灭吴及其结局，编撰的长篇轶事故事，共十五章，各以一句古诗词为题。",
    "bnbz_00": "人民文学出版社1999年编，为“百年百种优秀中国文学图书”评选入选的一百种图书各写作者简介、写作背景、内容与版本概要，附评选委员会名单及推荐书目。",
    "bnbz_01": "晚清谴责小说，现存六十回。以串联式结构描写清末从中央到地方各级官吏的钻营、贪赃、倾轧与丑态，是晚清官场的群像。作者李宝嘉，号南亭亭长。",
    "bnbz_02": "清末章回小说，借状元金雯青与名妓傅彩云的故事，写同治至甲午、维新前后三十年的官场士林与时局。现存三十五回，宇文校注。",
    "bnbz_03": "清末谴责小说。以“九死一生”二十年间的见闻为线索，写官场、商场、洋场中种种怪现状，共一百零八回。",
    "bnbz_04": "清末章回体小说，二十回，附《二集》九回。写江湖郎中老残游历山东，见闻酷吏民瘼与黄河水患，兼谈世道人心。",
    "bnbz_05": "晚清诗人黄遵宪的诗集，十一卷，收同治至光绪末年所作古今体诗；附《日本杂事诗》及传、墓志铭、年谱、诗话，钱仲联笺注（笺注本此处只收正文）。",
    "bnbz_06": "胡适的白话诗集（增订四版），收《尝试集》三编、附录《去国集》，另附初版、再版所删诗作及钱玄同序、作者自序。",
    "bnbz_07": "郭沫若的新诗集，1921年初版，分三辑，收序诗、三部诗剧《女神之再生》《湘累》《棠棣之花》及《凤凰涅槃》《天狗》等六十首诗。",
    "bnbz_08": "郁达夫早期短篇小说集，收《沉沦》《南迁》《银灰色的死》三篇，写留日青年的孤独、性苦闷与漂泊，卷首有作者自序。",
    "bnbz_09": "鲁迅的第一部短篇小说集，收《狂人日记》《孔乙己》《药》《阿Q正传》《故乡》《社戏》等十四篇，另有自序。",
    "bnbz_10": "冰心的小诗集，收《繁星》一百六十四首，附录《春水》一百八十二首及《迎神曲》《晚祷》《纸船》等三十一篇诗作，多为短章。",
    "bnbz_11": "近代革命文学团体南社的诗文词选集，胡朴安从社刊前二十一集中选录文、诗、词三类，按作者编排，反映辛亥革命前后的爱国民主思想与时代情绪。",
    "bnbz_12": "周作人1925年出版的散文集，收《苦雨》《鸟声》《喝茶》《济南道中》等小品，谈生活之艺术、神话、性道德与民族文化，附汪仲贤《十五年前的回忆》。",
    "bnbz_13": "徐志摩第一部诗集，收《这是一个懦怯的世界》《沙扬娜拉十八首》《雪花的快乐》《康桥再会罢》等五十六首，兼有爱情、自然与人生写照之作。",
    "bnbz_14": "冰心写给少年儿童的书信体散文集，收1923至1926年留美途中与养病期间的二十九篇通讯及《山中杂记》，另补录1958—1959年《再寄小读者》、1978—1980年《三寄小读者》。",
    "bnbz_15": "鲁迅的第二部小说集，收1924至1925年所作《祝福》《在酒楼上》《肥皂》《孤独者》《伤逝》《离婚》等短篇十一篇，写辛亥前后知识者与乡镇民众的生活。",
    "bnbz_16": "鲁迅的散文诗集，收1924至1926年所作《秋夜》《影的告别》《复仇》《过客》《这样的战士》等二十三篇及题辞，抒写作者内心的苦闷与抗争。",
    "bnbz_17": "闻一多的诗集，收入《死水》全集诗作及补录，并附早期《红烛》集中的《红烛》《二月庐》《黄鸟》《红豆》诸辑，含《口供》《死水》《红烛》《红豆》等名篇。",
    "bnbz_18": "朱自清散文、诗歌选集，分抒情、游记、议论、诗歌四篇，收《背影》《荷塘月色》《匆匆》《桨声灯影里的秦淮河》及诗作《毁灭》等。",
    "bnbz_19": "丁玲早期短篇小说集，收《梦珂》《莎菲女士的日记》《暑假中》《阿毛姑娘》《最后一页》，写五四之后觉醒女性的苦闷与出路。",
    "bnbz_20": "长篇小说。写小学教员倪焕之从辛亥革命前后到大革命失败的理想追求、教育实践、爱情婚姻与幻灭，反映知识分子的时代历程。",
    "bnbz_21": "张恨水章回体长篇小说，写青年学生樊家树与鼓书艺人沈凤喜、侠女关秀姑、富家女何丽娜的情感纠葛，并附作者序跋、创作谈及续集十回。",
    "bnbz_22": "丰子恺的散文集，收《渐》《儿女》《从孩子得到的启示》《忆儿时》等二十一篇及附录《告缘缘堂在天之灵》，谈人生、艺术与儿童的天真，兼记旧事。",
    "bnbz_23": "陈梦家 1931 年编选的新月派诗歌合集，收徐志摩、闻一多、饶孟侃、孙大雨、朱湘等十八位诗人的诗作，前有编者序言。",
    "bnbz_24": "鲁迅杂文选集，瞿秋白（何凝）编选并作长篇序言，收1918至1932年间《热风》《坟》《华盖集》等七部杂感集中的篇章。",
    "bnbz_25": "诗人戴望舒1933年自编的第二部诗集，收《我的记忆》至《乐园鸟》四十一首现代诗，前有杜衡序，末附诗论零札十七则。",
    "bnbz_26": "臧克家早期诗集，收《难民》《老马》《炭鬼》《生活》等二十二首，取材农民、劳工与底层人生，卷首有闻一多序；附录《罪恶的黑手》诗集。",
    "bnbz_27": "长篇小说。以一九三〇年春夏的上海为背景，写民族资本家吴荪甫在买办资本、外国势力与工潮、农村破产的夹击下由图强走向失败的经过。",
    "bnbz_28": "长篇小说，“激流三部曲”第一部。以成都高公馆为背景，写觉新、觉民、觉慧三兄弟及梅、鸣凤等人在封建大家庭中的爱情、挣扎与反抗。",
    "bnbz_29": "中篇小说。以二十年代湘西边境小镇茶峒为背景，写摆渡老人与孙女翠翠的生活，及翠翠与船总两个儿子之间未能圆满的爱情。",
    "bnbz_30": "艾芜短篇小说集，收《人生哲学的一课》《山峡中》《松岭上》等八篇，写作者早年漂泊滇缅边境时所见的流浪者、马帮、山民与异乡人的生活。",
    "bnbz_31": "长篇小说，以清末甲午至庚子年间成都近郊天回镇为背景，写蔡大嫂（邓幺姑）与罗歪嘴、顾天成等人的爱恨纠葛，及教案风潮下的乡镇世态。",
    "bnbz_32": "艾青早期诗集，收《大堰河——我的褓姆》《芦笛》《马赛》《巴黎》等，附录收诗集《北方》的序及《雪落在中国的土地上》《我爱这土地》等诗。",
    "bnbz_33": "沈从文1934年返乡途中沿沅水所写的散文集，记桃源、鸭窠围、箱子岩、辰溪等沿河风物，及水手、军官、旧友的故事。",
    "bnbz_34": "何其芳早期散文集，收《墓》《秋海棠》《独语》《梦后》《炉边夜话》等篇，文笔瑰丽，多写梦境与寂寞心绪，另附《梦中道路》等篇。",
    "bnbz_35": "三幕话剧，写1937年上海黄梅时节一栋弄堂房子里五户小市民的悲欢；附录收四幕话剧《芳草天涯》，写抗战后期桂林、柳州的知识分子生活。",
    "bnbz_36": "邹韬奋记述1935年赴美考察见闻的政论随笔集，涉及华尔街、劳工运动、黑人问题、新闻事业、青年与农民运动等，共三十六篇。",
    "bnbz_37": "夏衍的报告文学，写上海杨树浦日商纱厂“包身工”制度下女工的非人处境；另收《包身工》余话及作者回忆文字数篇。",
    "bnbz_38": "长篇小说。旧北平洋车夫祥子三起三落，买车、丢车、娶虎妞、失去小福子，终在城市底层的压榨下沦为行尸走肉。",
    "bnbz_39": "光未然的诗集，收《黄河大合唱》八首歌词、《三门峡大合唱》《五月的鲜花》《红树林之歌》《屈原》等诗作，附作者及冼星海关于《黄河》创作的文章。",
    "bnbz_40": "萧红的长篇小说，以回忆笔触写东北小城呼兰河的风土人情、市井民俗，以及祖父、后园、团圆媳妇、有二伯、冯歪嘴子等人事。",
    "bnbz_41": "五幕历史剧。以战国楚怀王时屈原遭谗被逐、南后郑袖与张仪合谋卖国为背景，写屈原与侍女婵娟的遭遇和雷电颂的悲愤，作于1942年。",
    "bnbz_42": "冯至诗集，收组诗《十四行二十七首》，另补录1921—1933年的早期抒情诗与叙事诗《吹箫人的故事》《帷幔》《蚕马》等。",
    "bnbz_43": "田间的抗战诗集，收长诗《给战斗者》及街头诗、小叙事诗《祝山》《她底歌》等，并附作者小引与创作谈。",
    "bnbz_44": "张天翼抗战时期的短篇小说集，收《谭九先生的工作》《华威先生》《“新生”》三篇讽刺小说，附录早期短篇《包氏父子》。",
    "bnbz_45": "赵树理小说集，收《小二黑结婚》《李有才板话》《孟祥英翻身》《地板》《福贵》五篇，写抗日根据地农村的婚姻、斗争与翻身。",
    "bnbz_46": "张爱玲小说集，1944年初版、1946年增订，收《金锁记》《倾城之恋》《红玫瑰与白玫瑰》等中短篇小说十五篇，并附散文《中国的日夜》及作者序跋。",
    "bnbz_47": "沙汀抗战时期的短篇小说集，收《防空》《联保主任的消遣》《在其香居茶馆里》《公道》《三斗小麦》《没有演出的戏》《小城风波》七篇，描写川西北小城的世态。",
    "bnbz_48": "吴祖光创作于1942年的四幕话剧（含序幕、尾声）。以名伶魏莲生与姨太太玉春的相恋与出逃，写旧时代戏子的命运与世态炎凉。",
    "bnbz_49": "歌剧文学剧本，延安鲁迅艺术文学院集体创作，贺敬之、丁毅执笔，五幕，写佃农杨白劳被逼死、女儿喜儿逃入深山变成“白毛女”，后获解放；附作者文论。",
    "bnbz_50": "穆旦（查良铮）1945年自印的第一部诗集，收1939至1945年间所作六十余首，附王佐良《一个中国诗人》。",
    "bnbz_51": "长篇小说。以苏州蒋家兄妹姐弟的命运为线，写1930至40年代知识青年在战争与社会动荡中的追求、幻灭与精神搏斗。卷首有胡风序与作者题记。",
    "bnbz_52": "短篇小说集，收《果园城》《“鬼爷”》《葛天民》《桃红》等十七篇，以假想的中原小城“果园城”为背景，写其中小人物的命运。",
    "bnbz_53": "李季以陕北信天游体写成的长篇叙事诗，讲述三边农民王贵与李香香在地主崔二爷压迫下，借红军游击队之力翻身并结为夫妻；附录收叙事诗《菊花石》。",
    "bnbz_54": "周扬1946年编选的解放区小说与报告文学集，分两辑收丁玲、孔厥、康濯、孙犁、吴伯箫、周而复等二十余位作者的短篇作品，反映抗战与农村改革中的生活与斗争。",
    "bnbz_55": "长篇小说。留学归国的方鸿渐在上海、三闾大学与婚姻之间辗转，写抗战初期一批知识分子的处境，以讽刺见长。",
    "bnbz_56": "萧乾1930年代至1940年代的旅行采访特写集，分国外、国内两部，记欧洲战场、英伦、南洋及国内各地的所见所闻。",
    "bnbz_57": "梁实秋的散文集，收《雅舍小品》正续及三集、四集共一百三十余篇，写人情世态与日常琐事，文笔冲淡幽默，兼有文史掌故。",
    "bnbz_58": "曹禺早期三部多幕话剧《雷雨》《日出》《北京人》合集，附作者1977年所写后记。",
    "bnbz_59": "长篇小说。以1947年西北野战军在陕北的青化砭、蟠龙镇、沙家店等战役为主线，描写保卫延安的战争，并附冯雪峰评论及作者后记。",
    "bnbz_60": "彝族撒尼人的民间叙事长诗，讲述美丽能干的阿诗玛被恶霸热布巴拉家抢婚，哥哥阿黑前往营救，终在归途中失去妹妹，阿诗玛化为回声。重新整理本，附李广田序。",
    "bnbz_61": "长篇小说，写冀中平原锁井镇朱、严两家农民在地主冯家压迫下的反抗，及大革命前后二师学潮、高蠡暴动中的觉醒与斗争。书末附作者《漫谈〈红旗谱〉的创作》。",
    "bnbz_62": "老舍三幕话剧，借北京裕泰茶馆半个世纪里的人来人往，写清末、民初、抗战胜利后三个时代的社会变迁；附录收《龙须沟》及幕前快板。",
    "bnbz_63": "田汉创作的十二场历史话剧，写元代剧作家关汉卿因写《窦娥冤》触怒权贵、与朱帘秀等艺人共赴患难，终被逐出大都。书末附郭沫若与作者往来书信。",
    "bnbz_64": "长篇小说。写20世纪30年代北平女学生林道静从个人反抗走向投身革命的成长历程，背景为九一八后至一二·九学生运动，作者杨沫自1951年起写作。",
    "bnbz_65": "孙犁的小说、散文集，收《荷花淀》《芦花荡》《钟》等抗战至建国初期的短篇小说，及《游击区生活一星期》等通讯、散文、日记，描写冀中抗日根据地与白洋淀一带的人民生活。",
    "bnbz_66": "林海音的自传体短篇小说集，由《惠安馆传奇》《我们看海去》《兰姨娘》《驴打滚儿》《爸爸的花儿落了》五篇组成，以小女孩英子的眼光回忆二十年代北京城南的童年。",
    "bnbz_67": "长篇小说，写1950年代初陕西渭河南岸蛤蟆滩村农民梁生宝带领互助组、办起农业社的故事，展现农村合作化运动中各阶层的矛盾与变迁。",
    "bnbz_68": "长篇小说。以1948年至1949年重庆解放前夕的地下斗争和渣滓洞、白公馆集中营中的狱中斗争为题材，塑造了江姐、许云峰、成岗等革命者形象。",
    "bnbz_69": "邓拓以马南邨为笔名在《北京晚报》“燕山夜话”专栏所写杂文结集，分五集，共一百五十余篇，谈古论今，涉及读书治学、历史掌故、科学常识与生活见闻。",
    "bnbz_70": "收毛泽东1918至1965年所作诗词五十首，分正编、副编，每首附发表出处与编者注释，卷末附作者论诗书信三封。",
    "bnbz_71_1": "长篇历史小说《李自成》第一卷，写崇祯十一年前后明末农民战争：李自成潼关南原兵败后商洛潜伏，张献忠谷城受抚，明廷内外交困。",
    "bnbz_71_2": "长篇历史小说《李自成》第二卷，写崇祯十二至十三年李自成困守商洛山、粉碎官军进剿，及杨嗣昌督师围剿张献忠的故事。",
    "bnbz_71_3": "长篇历史小说《李自成》第三卷。写崇祯十三年冬至次年春，李自成入豫、李岩红娘子起义、攻破洛阳杀福王，及崇祯朝廷的内外交困。",
    "bnbz_71_4": "长篇历史小说《李自成》第四卷，写崇祯十四年李自成再攻开封，同时写洪承畴松锦战役兵败降清及明清、农民军三方角力。",
    "bnbz_71_5": "长篇历史小说《李自成》第五卷，写崇祯十四、十五年李自成围攻开封、朱仙镇之战、袁时中叛变与慧梅之死等。",
    "bnbz_71_6": "长篇历史小说《李自成》第六卷，写大顺军攻入北京、崇祯自缢、李自成登极前后至东征吴三桂的史事。",
    "bnbz_71_7": "长篇历史小说《李自成》第七卷，写1644年清军入关、山海关之战、大顺军撤出北京与西安、南退湖广，直至李自成殉难及余部抗清。",
    "bnbz_73": "白先勇的短篇小说集，收《永远的尹雪艳》《游园惊梦》《国葬》等十四篇，写随国民党迁台的各色人物的今昔沉浮；附欧阳子、夏志清、于梨华三篇评论。",
    "bnbz_74": "台湾现代派小说。范晔不堪忍受衰老的父亲，父亲离家出走后，他登报寻父，在寻找中回溯自己的成长与父子冲突，文字刻意求新。",
    "bnbz_75": "台湾作家陈映真的短篇小说集，收《我的弟弟康雄》《将军族》《唐倩的喜剧》《第一件差事》《夜行货车》《山路》《赵南栋》等十一篇，另附作者序言与写作年表。",
    "bnbz_76": "当代诗人郭小川的诗歌选集，收《女性的豪歌》《望星空》《团泊洼的秋天》等短诗，及《白雪的赞歌》《一个和八个》等长诗。",
    "bnbz_77": "报告文学集，收《向着二十一世纪》《石油头》《地质之光》《哥德巴赫猜想》等篇，写陈景润、李四光、蔡希陶、周培源等科学家与石油工人、画家的事迹，并附作者后记。",
    "bnbz_78": "茹志鹃短篇小说选集，收《关大妈》《百合花》《静静的产院》《回头卒》等十八篇，写战争年代与合作化时期的普通人，附作者后记。",
    "bnbz_79": "长篇小说，共一百段，分《惶惑》《偷生》《饥荒》三部。写抗战时期北平小羊圈胡同祁家四世同堂及邻里在日军占领下的遭遇与抉择。",
    "bnbz_80": "1979年编选的1956至1957年上半年“百花时期”小说、特写与诗歌合集，收刘宾雁、王蒙、陆文夫、宗璞、流沙河等十七位作者的二十篇作品。",
    "bnbz_81": "巴金晚年散文集，含《随想录》《探索集》《真话集》《病中集》《无题集》五集共一百五十篇，回顾“文革”，反思自我，倡导说真话。",
    "bnbz_82": "翻译家傅雷夫妇在1954至1966年间写给旅居海外的钢琴家儿子傅聪的家书选集，谈艺术、音乐、做人与家国，另附音乐笔记及访谈。",
    "bnbz_83": "杨绛回忆1969—1972年随学部下放河南干校的散文集，含“下放记别”等六记，另附《丙午丁未年纪事》和《从“掺沙子”到“流亡”》两篇补录。",
    "bnbz_84": "长篇小说。以湘南山镇芙蓉镇为背景，写米豆腐摊主胡玉音一家在1963至1979年间随政治运动沉浮的遭遇，兼及镇上众人的悲欢。",
    "bnbz_85": "“七月派”二十位诗人的诗选，收一百一十九首作品，多作于四十年代，各家前有作者小传，卷首有绿原所作序言。",
    "bnbz_86": "九位四十年代诗人的合集，每人选录十余至二十余首诗作，附作者小传与袁可嘉所作序言，展现“九叶”诗派的创作面貌。",
    "bnbz_87": "汪曾祺短篇小说自选集，收《复仇》《受戒》《大淖记事》《岁寒三友》等十六篇，写昆明联大旧事、高邮市井与塞外见闻，并附作者自序。",
    "bnbz_88": "阿城中篇小说集，收《棋王》《树王》《孩子王》及短篇系列“遍地风流”七篇，写知青在乡野的生活、棋艺与民间世相，附作者自序。",
    "bnbz_89": "张承志中短篇小说集，收《北方的河》《黑骏马》《西省暗杀考》《黄泥小屋》四篇，写知青一代的追寻、草原的离合与西北回民的历史。",
    "bnbz_90": "中篇小说，写右派知识分子章永璘在西北劳改农场与农妇黄香久相识、结婚，经历爱情与婚姻的波折。",
    "bnbz_91": "长篇小说。以留学归来的知识分子倪吾诚及其家庭为中心，写二十世纪前半叶新旧思想冲撞下的人生遭遇，另有续集交代人物后事。",
    "bnbz_92": "长篇小说，共六卷。写1975至1985年间陕北黄土高原农村与城乡之间，孙少安、孙少平兄弟及周围众多人物的奋斗与生活变迁。",
    "bnbz_93": "长篇小说。以“我”追述祖辈在山东高密东北乡的抗日与生活传奇，写爷爷余占鳌、奶奶戴凤莲等人的爱恨与厮杀，分五章。",
    "bnbz_94": "长篇小说。以胶东洼狸镇隋、赵、李三大家族和粉丝工业的兴衰为线索，写土改以来数十年的历史变迁与人物命运。",
    "bnbz_95": "台湾诗人余光中的诗歌选集，选收1949年至1998年间的作品，依大陆时期、台湾前期、香港时期、台湾后期编排，附选编者所撰评述与后记。",
    "bnbz_96": "长篇小说，《野葫芦引》第一卷。写七七事变前后北平明仑大学教授孟、凌等几家人的离乱与抉择，随校南渡的经过。",
    "bnbz_97": "汪曾祺的散文集，收游记、人物回忆、昆明旧事、故乡风物、草木饮食、文史杂谈和序跋等六十余篇，附自序与再版后记。",
    "bnbz_98": "长篇小说。以关中白鹿原上白、鹿两家三代人的恩怨纠葛为主线，写清末至一九四九年间原上的宗族生活与社会变迁。",
    "bnbz_99": "当代诗人舒婷的诗选，分三辑收入《会唱歌的鸢尾花》《双桅船》《秋思》中的抒情诗，含《致橡树》《神女峰》《惠安女子》等。",
    "bnbz_100": "长篇小说。以康巴藏区麦其土司家的“傻子”二少爷的视角，讲述土司制度在罂粟种植、家族争斗与时代变革中走向崩溃的故事。",
    "qsyy_qianhan": "章回体历史演义，叙西汉二百余年史事，自秦始皇出世、楚汉相争、汉高祖建国，经文景武昭宣诸朝，至外戚擅政、王莽篡汉，共一百回。",
    "qsyy_houhan": "章回体历史演义，叙东汉史事，自王莽篡汉、光武中兴，历宦官外戚专权、党锢、黄巾、董卓之乱，至三国鼎立、司马氏代魏，共一百回。",
    "qsyy_liangjin": "章回体历史演义，叙西晋武帝代魏至东晋覆亡、刘裕代晋，兼述五胡十六国兴替，共一百回。",
    "qsyy_nanbeichao": "章回体历史演义，叙宋齐梁陈与北魏、东西魏、北齐北周两百余年兴亡，自刘裕崛起写至隋文帝统一、炀帝被弑，共一百回。",
    "qsyy_tang": "章回体历史演义，叙唐朝兴亡，自李渊晋阳起兵，历贞观、武周、开元、安史之乱，至朱全忠篡唐，共一百回。",
    "qsyy_wudai": "章回体历史演义，演述朱温篡唐、五代更迭及十国兴亡，迄于周世宗殂、赵匡胤陈桥受禅，共六十回。",
    "qsyy_song": "章回体历史演义，叙北宋至南宋兴亡，自宋太祖出身写起，历靖康之变、南渡，至宋亡，共一百回。",
    "qsyy_yuan": "章回体历史演义，从蒙古先世与成吉思汗崛起写起，经灭宋，至元顺帝出走、元亡，共六十回。",
    "qsyy_ming": "章回体历史演义（即《明史演义》），自朱元璋起兵濠州叙起，历诸帝，至崇祯殉国、南明覆亡，共一百回。",
    "qsyy_qing": "章回体历史演义，自清太祖兴起叙起，历入关、康雍乾盛世，至鸦片战争、太平天国、甲午、戊戌、庚子，终于宣统退位，共一百回。",
    "qsyy_minguo": "章回体历史演义（《民国演义》），自武昌起义、民国肇建写起，叙袁世凯称帝、军阀混战、护法战争，至第二次直奉战争前夕，共一百六十回。",
    "qsyy_han_gy": "章回体历史演义，以宫廷女性为主线，叙西汉史事，自刘邦起事、吕后专权至王莽篡汉，再写东汉宫闱外戚，终于蜀汉亡国，共一百二十回。",
    "qsyy_sui_gw": "章回小说，自南朝宋宫闱秽事写起，叙北周、隋文帝、独孤后、炀帝及后宫诸妃，至隋亡、萧后流落突厥，共一百回。",
    "qsyy_tang_gy": "章回体历史演义，叙隋炀帝、唐太宗、武则天、唐玄宗与杨贵妃等隋唐宫廷故事，下及肃代德宪诸朝，至五代更替，共一百回。",
    "qsyy_ming_gw": "章回体历史演义，以宫闱后妃、帝王私事为线索，叙元代蒙古兴起、朱元璋建明及历朝宫廷内外故事，至明亡、清初，共一百二十回。",
    "qsyy_qing_gy": "章回体历史演义，写清朝从努尔哈赤起兵到光绪、宣统两朝的宫廷后妃、宗室与朝臣旧事，终于溥仪逊位，共一百回。",
    "qsyy_qing_ms": "章回体历史演义（即《清史演义》），从清太祖努尔哈赤兴起写起，经顺康雍乾，历鸦片战争、太平天国、甲午、戊戌、庚子，至宣统逊位，共一百四十回。",
    "ltlq_v2": "《劳特利奇哲学史》十卷本第二卷，十二章依次论亚里士多德各领域、漫步学派、伊壁鸠鲁派、斯多亚派、怀疑派、希腊化科学、新柏拉图主义与奥古斯丁，附年表与名词解释。",
    "ltlq_v3": "《劳特利奇哲学史》十卷本第三卷，十九章依次论波爱修、阿拉伯与犹太哲学、中世纪早期、12世纪、13至14世纪经院哲学直到苏阿雷斯，附年表与名词解释。",
    "ltlq_v4": "《劳特利奇哲学史》十卷本第四卷，十一章分论意大利及其他地区的文艺复兴哲学、科学与数学、培根、笛卡尔、伽森狄与霍布斯、斯宾诺莎、偶因论和莱布尼兹，附年表与名词解释。",
    "ltlq_v5": "《劳特利奇哲学史》十卷本第五卷，十四章依次论剑桥柏拉图主义、波义耳与牛顿、洛克、贝克莱、休谟、英法德苏的启蒙运动、维科、卢梭与柏克，附年表与名词解释。",
    "ltlq_v6": "《劳特利奇哲学史》十卷本第六卷，十一章依次论康德之前、康德、费希特与谢林、黑格尔、青年黑格尔派与马克思、叔本华、克尔凯郭尔，附年表与名词解释。",
    "ltlq_v7": "《劳特利奇哲学史》十卷本第七卷，十五章分论边沁、密尔、惠威尔、西季威克、孔德、尼采、狄尔泰、数理逻辑、生物学、心理学、实用主义与英国唯心论，附年表与名词解释。",
    "ltlq_v8": "《劳特利奇哲学史》十卷本第八卷，十四章分论现象学、存在哲学、宗教哲学、科学哲学、马克思主义、批判理论、诠释学、结构主义、女权主义、解构与后现代理论，附年表与名词解释。",
    "ltlq_v9": "《劳特利奇哲学史》十卷本第九卷，十章分论逻辑、数学、弗雷格、《逻辑哲学论》、逻辑实证主义、物理学、科学、概率论、控制论与机械论之争，附年表与名词解释。",
    "ltlq_v10": "《劳特利奇哲学史》十卷本第十卷，十四章分论20世纪英语世界的语言哲学、形而上学、伦理学、知识论、维特根斯坦后期哲学、政治哲学、女性主义、法哲学、应用伦理学、美学与宗教哲学。",
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
    "ltlq": {
        "title": "劳特利奇哲学史", "author": "［英］帕金森、［加］杉克尔 总主编", "children": ["ltlq_v1", "ltlq_v2", "ltlq_v3", "ltlq_v4", "ltlq_v5", "ltlq_v6", "ltlq_v7", "ltlq_v8", "ltlq_v9", "ltlq_v10"],
        "labels": {"ltlq_v1": "第一卷", "ltlq_v2": "第二卷", "ltlq_v3": "第三卷", "ltlq_v4": "第四卷", "ltlq_v5": "第五卷", "ltlq_v6": "第六卷", "ltlq_v7": "第七卷", "ltlq_v8": "第八卷", "ltlq_v9": "第九卷", "ltlq_v10": "第十卷"},
        "home_intro": "《劳特利奇哲学史》十卷本，从公元前6世纪的古希腊到20世纪的西方哲学史，中国人民大学出版社中文版；共十卷。",
        "intro": "《劳特利奇哲学史》（Routledge History of Philosophy，十卷本）由英国的帕金森（G.H.R. Parkinson）和加拿大的杉克尔（S.G. Shanker）总主编，对从公元前6世纪开始直到当代的西方哲学史做编年式考察：深入讨论所有重要的哲学发展，为公认的伟大哲学家提供很大篇幅，同时不忽略较小的人物；各分卷由不同学者主编，全书130多位专家撰稿，每章后附参考书目，书中有哲学大事年表、名词解释与索引。中文版由冯俊担任翻译总主编，中国人民大学出版社出版。下面分十卷。",
    },
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
    "zhongguoquanshi": {
        "title": "中国全史演义系列", "author": "大众文艺出版社 编", "children": ["qsyy_qianhan", "qsyy_houhan", "qsyy_liangjin", "qsyy_nanbeichao", "qsyy_tang", "qsyy_wudai", "qsyy_song", "qsyy_yuan", "qsyy_ming", "qsyy_qing", "qsyy_minguo", "qsyy_han_gy", "qsyy_sui_gw", "qsyy_tang_gy", "qsyy_ming_gw", "qsyy_qing_gy", "qsyy_qing_ms"],
        "home_intro": "大众文艺出版社“中国全史”丛书：蔡东藩的历代历史演义（前汉至民国），以及许啸天、徐哲身等的宫闱艳史、陆士谔《清朝秘史》，共十七部，上下册合为一书。",
        "intro": "“中国全史”是大众文艺出版社出版的历史演义丛书，收蔡东藩的《前汉》《后汉》《两晋》《南北朝》《唐代》《五代》《宋代》《元代》《明代》《清代》《民国》历史演义全书，以及《汉代宫廷艳史》《隋代宫闱史》《唐代宫廷艳史》《明代宫闱史》《清代宫廷艳史》《清朝秘史》。原书分上下（或上中下、一至四）册，这里把同一部书的各册合并为一书，按回目分页。",
    },
    "baibaizhong": {
        "title": "百年百种优秀中国文学图书", "author": "人民文学出版社 编", "children": ["bnbz_00", "bnbz_01", "bnbz_02", "bnbz_03", "bnbz_04", "bnbz_05", "bnbz_06", "bnbz_07", "bnbz_08", "bnbz_09", "bnbz_10", "bnbz_11", "bnbz_12", "bnbz_13", "bnbz_14", "bnbz_15", "bnbz_16", "bnbz_17", "bnbz_18", "bnbz_19", "bnbz_20", "bnbz_21", "bnbz_22", "bnbz_23", "bnbz_24", "bnbz_25", "bnbz_26", "bnbz_27", "bnbz_28", "bnbz_29", "bnbz_30", "bnbz_31", "bnbz_32", "bnbz_33", "bnbz_34", "bnbz_35", "bnbz_36", "bnbz_37", "bnbz_38", "bnbz_39", "bnbz_40", "bnbz_41", "bnbz_42", "bnbz_43", "bnbz_44", "bnbz_45", "bnbz_46", "bnbz_47", "bnbz_48", "bnbz_49", "bnbz_50", "bnbz_51", "bnbz_52", "bnbz_53", "bnbz_54", "bnbz_55", "bnbz_56", "bnbz_57", "bnbz_58", "bnbz_59", "bnbz_60", "bnbz_61", "bnbz_62", "bnbz_63", "bnbz_64", "bnbz_65", "bnbz_66", "bnbz_67", "bnbz_68", "bnbz_69", "bnbz_70", "bnbz_71_1", "bnbz_71_2", "bnbz_71_3", "bnbz_71_4", "bnbz_71_5", "bnbz_71_6", "bnbz_71_7", "bnbz_73", "bnbz_74", "bnbz_75", "bnbz_76", "bnbz_77", "bnbz_78", "bnbz_79", "bnbz_80", "bnbz_81", "bnbz_82", "bnbz_83", "bnbz_84", "bnbz_85", "bnbz_86", "bnbz_87", "bnbz_88", "bnbz_89", "bnbz_90", "bnbz_91", "bnbz_92", "bnbz_93", "bnbz_94", "bnbz_95", "bnbz_96", "bnbz_97", "bnbz_98", "bnbz_99", "bnbz_100"],
        "labels": {"bnbz_00": "目录", "bnbz_01": "第1种", "bnbz_02": "第2种", "bnbz_03": "第3种", "bnbz_04": "第4种", "bnbz_05": "第5种", "bnbz_06": "第6种", "bnbz_07": "第7种", "bnbz_08": "第8种", "bnbz_09": "第9种", "bnbz_10": "第10种", "bnbz_11": "第11种", "bnbz_12": "第12种", "bnbz_13": "第13种", "bnbz_14": "第14种", "bnbz_15": "第15种", "bnbz_16": "第16种", "bnbz_17": "第17种", "bnbz_18": "第18种", "bnbz_19": "第19种", "bnbz_20": "第20种", "bnbz_21": "第21种", "bnbz_22": "第22种", "bnbz_23": "第23种", "bnbz_24": "第24种", "bnbz_25": "第25种", "bnbz_26": "第26种", "bnbz_27": "第27种", "bnbz_28": "第28种", "bnbz_29": "第29种", "bnbz_30": "第30种", "bnbz_31": "第31种", "bnbz_32": "第32种", "bnbz_33": "第33种", "bnbz_34": "第34种", "bnbz_35": "第35种", "bnbz_36": "第36种", "bnbz_37": "第37种", "bnbz_38": "第38种", "bnbz_39": "第39种", "bnbz_40": "第40种", "bnbz_41": "第41种", "bnbz_42": "第42种", "bnbz_43": "第43种", "bnbz_44": "第44种", "bnbz_45": "第45种", "bnbz_46": "第46种", "bnbz_47": "第47种", "bnbz_48": "第48种", "bnbz_49": "第49种", "bnbz_50": "第50种", "bnbz_51": "第51种", "bnbz_52": "第52种", "bnbz_53": "第53种", "bnbz_54": "第54种", "bnbz_55": "第55种", "bnbz_56": "第56种", "bnbz_57": "第57种", "bnbz_58": "第58种", "bnbz_59": "第59种", "bnbz_60": "第60种", "bnbz_61": "第61种", "bnbz_62": "第62种", "bnbz_63": "第63种", "bnbz_64": "第64种", "bnbz_65": "第65种", "bnbz_66": "第66种", "bnbz_67": "第67种", "bnbz_68": "第68种", "bnbz_69": "第69种", "bnbz_70": "第70种", "bnbz_71_1": "第71种·第1卷", "bnbz_71_2": "第71种·第2卷", "bnbz_71_3": "第71种·第3卷", "bnbz_71_4": "第71种·第4卷", "bnbz_71_5": "第71种·第5卷", "bnbz_71_6": "第71种·第6卷", "bnbz_71_7": "第71种·第7卷", "bnbz_73": "第73种", "bnbz_74": "第74种", "bnbz_75": "第75种", "bnbz_76": "第76种", "bnbz_77": "第77种", "bnbz_78": "第78种", "bnbz_79": "第79种", "bnbz_80": "第80种", "bnbz_81": "第81种", "bnbz_82": "第82种", "bnbz_83": "第83种", "bnbz_84": "第84种", "bnbz_85": "第85种", "bnbz_86": "第86种", "bnbz_87": "第87种", "bnbz_88": "第88种", "bnbz_89": "第89种", "bnbz_90": "第90种", "bnbz_91": "第91种", "bnbz_92": "第92种", "bnbz_93": "第93种", "bnbz_94": "第94种", "bnbz_95": "第95种", "bnbz_96": "第96种", "bnbz_97": "第97种", "bnbz_98": "第98种", "bnbz_99": "第99种", "bnbz_100": "第100种"},
        "home_intro": "二十世纪（1900—1999）中国文学百种优秀图书：从《官场现形记》《人境庐诗草》到《白鹿原》《尘埃落定》，另收该书目《百年百种优秀中国文学图书》一册；《李自成》七卷各列一项。",
        "intro": "“百年百种优秀中国文学图书”是人民文学出版社1999年前后组织评选的二十世纪（1900—1999）中国文学图书书目，选出小说、诗歌、散文、戏剧等一百种，由人民文学出版社、作家出版社、解放军文艺出版社、中国青年出版社等分别出版丛书本。这里收入各书据2000年前后丛书本（个别书为其他版本）的扫描件识别整理的全文，另收书目《百年百种优秀中国文学图书》一册（各书作者简介与版本概要，目录一项）；《李自成》分七卷、《创业史》为全本，各占一项。下面按书目顺序排列。",
    },
    "mingrenyishi": {
        "title": "中国名人轶事丛书", "author": "吴洪激 主编", "children": ["mrys_01", "mrys_02", "mrys_03", "mrys_04", "pusonglingchuanqi", "mrys_06", "mrys_07", "mrys_08", "mrys_09", "mrys_10", "mrys_11", "mrys_12", "mrys_13", "mrys_14", "mrys_15", "mrys_16", "mrys_17", "mrys_18", "mrys_19", "mrys_20"],
        "labels": {"mrys_01": "之一", "mrys_02": "之二", "mrys_03": "之三", "mrys_04": "之四", "pusonglingchuanqi": "之五", "mrys_06": "之六", "mrys_07": "之七", "mrys_08": "之八", "mrys_09": "之九", "mrys_10": "之十", "mrys_11": "之十一", "mrys_12": "之十二", "mrys_13": "之十三", "mrys_14": "之十四", "mrys_15": "之十五", "mrys_16": "之十六", "mrys_17": "之十七", "mrys_18": "之十八", "mrys_19": "之十九", "mrys_20": "之二十"},      # 各册在丛书中的序号，显示在目录卡片书名前；后续册数在这里补
        "home_intro": "吴洪激主编的传记丛书，搜集中国名人未经正史记载的稗类野史与佚事珍闻，为历史人物立传；共二十册，已全部收入。",
        "intro": "《中国名人轶事丛书》由吴洪激主编。据丛书出版缘由，所谓“轶事”，指未经史书记载而散失之事；丛书倡导广泛搜集中国名人的稗类野史、佚事珍闻，正史、野史兼容，用浅显的口语写成通俗易读的名人传奇，塑造有别于正史的人物形象。共二十册，现已全部收入。",
    },
}
COLLECTION_OF = {}
for _k, _c in COLLECTIONS.items():
    for _child in _c["children"]:
        if isinstance(_child, str):          # 条目也可以是 dict：尚未收入、只在目录里占位的卷册（见 build_collection）
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
INITIAL = {"历": "L", "中": "Z", "宋": "S", "李": "L", "张": "Z", "红": "H", "蒲": "P", "二": "E", "佛": "F", "哥": "G", "献": "X", "九": "J", "聆": "L", "论": "L", "马": "M", "名": "M", "暮": "M", "人": "R", "三": "S", "肖": "X", "遇": "Y", "左": "Z", "大": "D", "劳": "L", "百": "B"}


def build_collection(slug):
    """多级目录页（三言二拍 → 三言/二拍 → 各书）：简介 + 下一级条目的卡片。"""
    c = COLLECTIONS[slug]
    cards = []
    for k in c["children"]:
        if isinstance(k, dict):              # 占位条目：目录里列出，但还没有内容，不带链接
            tag = f'<span class="vol">{esc(k["label"])}</span>' if k.get("label") else ""
            cards.append(f'<li class="pending"><div>{tag}<strong>{esc(k["title"])}</strong><span>{esc(k["author"])}</span><p>{esc(k["intro"])}</p></div></li>')
            continue
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
