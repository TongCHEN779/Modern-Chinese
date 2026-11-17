# 现代文库

现代著作的在线阅读站，模板与[古典文库](../Classical-Chinese)完全相同：静态网页，由 `build.py` 从 `src/` 生成到 `books/`，首页有搜索与字母索引。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| `index.html`、`assets/` | 首页（搜索、字母索引）与样式、脚本 |
| `books/<书>/` | 生成的各书目录页与阅读页 |
| `src/<书>/<页>/*.txt` | 标注文本：`# 标题` 开始一节，每个原文段一行 `原：…` |
| `sources/<书>/` | 来源与整理说明（`chapters.json`、`pages.json`、`README.md`）；`sources/wiki_intros.json` 目前为空 |

构建：

```bash
python3 build.py
```

新增一本书：在 `src/<书>/<页>/01.txt` 放文本，在 `sources/<书>/` 放 `chapters.json` 与 `pages.json`（页表，格式见现有的 `wangguodiwang`），然后在 `build.py` 的 `POETRY`、`BOOK_INTRO` 里登记，并在 `INITIAL` 里补书名首字的拼音首字母。

## 书目

- 历代亡国帝王传（李祖德主编，黄山书社，1993）
