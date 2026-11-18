#!/usr/bin/env python3
"""检查某本书 src/<slug>/ 的格式与注释：每页能解析；每段 `原：` 后面的 `注：词语：解释` 的词语能否在该段原文里找到（找不到的注释在页面上不挂到词语上）。
用法：python3 tools/check_src_notes.py <slug> [--show]"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build

slug = sys.argv[1]
secs = chunks = notes = unplaced = 0
bad = []
for d in sorted((ROOT / "src" / slug).iterdir()):
    s = build.parse_poems(sorted(d.glob("*.txt")))
    secs += len(s)
    for sec in s:
        for ch in sec["chunks"]:
            if "tbl" in ch or ch.get("diagram"):
                continue
            chunks += 1
            if ch["notes"]:
                before = build.ANCHOR_STATS["unplaced"]
                build.anchor_notes([ch["o"]], ch["notes"])
                notes += len(ch["notes"])
                miss = build.ANCHOR_STATS["unplaced"] - before
                unplaced += miss
                if miss:
                    bad.append((d.name, sec["title"], ch["o"][:20], miss))
print(f"{slug}: {len(list((ROOT/'src'/slug).iterdir()))} 页，{secs} 节，{chunks} 段，注释 {notes} 条，其中 {unplaced} 条的词语不在所属段原文里")
if "--show" in sys.argv:
    for b in bad[:30]:
        print("  ", b)
