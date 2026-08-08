# 📄 Static Site Generator

A static site generator built from scratch in Python — converts **Markdown files** into a fully rendered **HTML website**, with support for images, links, code blocks, lists, quotes, and more.

Built as part of the [Boot.dev – Build a Static Site Generator in Python](https://www.boot.dev/courses/build-static-site-generator-python) course.

🌐 **Live demo:** [harmen91.github.io/static-site-generator](https://harmen91.github.io/static-site-generator/)

---

## 📖 Overview

This project reimplements the core of what tools like [Hugo](https://gohugo.io/) or [Jekyll](https://jekyllrb.com/) do under the hood: walk a directory of Markdown content, parse it into an in-memory node tree, render it as HTML, copy static assets, and write the result to `docs/` — ready to be served by GitHub Pages.

---

## ✨ Features

- 📝 **Markdown to HTML** — full conversion pipeline including headings, paragraphs, lists, blockquotes, and code blocks
- 🔗 **Inline element parsing** — bold, italic, inline code, links, and images
- 🌳 **Node tree architecture** — HTML built via a composable `HTMLNode` / `LeafNode` / `ParentNode` hierarchy
- 📁 **Static asset copying** — images and CSS are copied to `docs/` automatically
- 🔁 **Recursive directory processing** — mirrors the `content/` folder structure into `docs/`
- 🔧 **Basepath support** — configurable base path for deploying to a GitHub Pages subdirectory
- 🚀 **One-command build** — shell scripts for building, previewing, and testing

---

## 🏗️ Project Structure

```
static-site-generator/
├── template.html            # HTML page template; {{ Title }} and {{ Content }} are replaced at build time
├── main.sh                  # Builds the site locally and serves it on localhost:8888
├── build.sh                 # Builds the site with the GitHub Pages basepath and touches docs/.nojekyll
├── test.sh                  # Runs the full test suite via unittest discover
│
├── src/
│   ├── main.py              # Entry point — deletes docs/, copies static/, generates all pages
│   ├── copystatic.py        # Recursively copies static/ into docs/
│   ├── gencontent.py        # Walks content/, renders each .md to .html using template.html
│   ├── htmlnode.py          # HTMLNode, LeafNode, ParentNode — the HTML rendering layer
│   ├── textnode.py          # TextNode + TextType enum — intermediate inline content representation
│   ├── inline_markdown.py   # Inline Markdown parser (bold, italic, code, links, images)
│   ├── markdown_blocks.py   # Block-level parser + markdown_to_html_node() pipeline
│   ├── test_htmlnode.py
│   ├── test_textnode.py
│   ├── test_inline_markdown.py
│   └── test_markdown_blocks.py
│
├── content/                 # Markdown source files (mirrors into docs/ at build time)
│   ├── index.md
│   ├── contact/
│   │   └── index.md
│   └── blog/
│       ├── glorfindel/
│       │   └── index.md
│       ├── majesty/
│       │   └── index.md
│       └── tom/
│           └── index.md
│
├── static/                  # Static assets — copied as-is into docs/
│   ├── index.css
│   └── images/
│       ├── tolkien.png
│       ├── glorfindel.png
│       ├── rivendell.png
│       └── tom.png
│
└── docs/                    # Generated output — served by GitHub Pages
    ├── .nojekyll            # Tells GitHub Pages to skip Jekyll processing
    ├── index.html
    ├── index.css
    ├── images/
    ├── contact/
    │   └── index.html
    └── blog/
        ├── glorfindel/
        │   └── index.html
        ├── majesty/
        │   └── index.html
        └── tom/
            └── index.html
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
git clone https://github.com/harmen91/static-site-generator.git
cd static-site-generator
```

No external dependencies — pure Python standard library.

### Preview locally

```bash
./main.sh
```

This runs `src/main.py` with a basepath of `/` (so all asset paths resolve correctly on localhost), then serves `public/` on [http://localhost:8888](http://localhost:8888).

### Build for GitHub Pages

```bash
./build.sh
```

This runs `src/main.py` with a basepath of `/static-site-generator/` — matching the GitHub Pages subdirectory — then creates `docs/.nojekyll` so GitHub Pages skips Jekyll processing and serves the pre-built HTML directly.

---

## 🧩 How It Works

```
./build.sh
    │
    ├─► src/main.py "/static-site-generator/"
    │       │
    │       ├─► Delete docs/
    │       ├─► copystatic.py   — copy static/ → docs/ (CSS, images)
    │       └─► gencontent.py   — walk content/ recursively
    │               │
    │               └─► For each index.md:
    │                       │
    │                       ├─► markdown_blocks.py
    │                       │   └─► Split into blocks (heading, paragraph,
    │                       │       list, quote, code)
    │                       │         │
    │                       │         └─► inline_markdown.py
    │                       │             └─► Split inline elements
    │                       │                 (bold, italic, code, link, image)
    │                       │                   │
    │                       │                   └─► TextNode → LeafNode
    │                       │
    │                       ├─► Build ParentNode tree → .to_html()
    │                       ├─► Inject into template.html
    │                       │   (replace {{ Title }} and {{ Content }})
    │                       ├─► Rewrite href="/ and src="/ to basepath
    │                       └─► Write to docs/.../index.html
    │
    └─► touch docs/.nojekyll
```

### The `.nojekyll` file

GitHub Pages runs Jekyll by default, which ignores files and folders starting with `_`. Since the generated site is plain HTML and needs no Jekyll processing, `build.sh` creates an empty `docs/.nojekyll` file after every build. This tells GitHub Pages to serve the contents of `docs/` as-is.

---

## 🧪 Testing

```bash
./test.sh
```

Runs `python3 -m unittest discover -s src`, which picks up all `test_*.py` files in `src/`. Tests cover:

| File | What it tests |
|---|---|
| `test_htmlnode.py` | `props_to_html()`, `LeafNode.to_html()`, `ParentNode.to_html()` with nesting |
| `test_textnode.py` | `TextNode` equality, `text_node_to_html_node()` for all `TextType` values |
| `test_inline_markdown.py` | Delimiter splitting, image/link extraction, `text_to_textnodes()` |
| `test_markdown_blocks.py` | Block splitting, block type detection, full `markdown_to_html_node()` output |

---

## 📚 Course

This project was built following the **[Build a Static Site Generator in Python](https://www.boot.dev/courses/build-static-site-generator-python)** course on Boot.dev, which covers:

| Chapter | Topics |
|---|---|
| 1 – Static Sites | What static sites are; moving and copying HTML and Markdown files |
| 2 – Nodes | Core HTML generation via OOP; `HTMLNode`, `LeafNode`, `ParentNode` |
| 3 – Inline | Inline Markdown parsing; generating inline HTML elements |
| 4 – Blocks | Block-level Markdown parsing; converting blocks to HTML nodes |
| 5 – Website | Wiring everything together; publishing to GitHub Pages |

---

## 🌐 Live Demo

The demo site is a Tolkien fan page generated entirely from Markdown:

> *"I am in fact a Hobbit in all but size."* — J.R.R. Tolkien

👉 [harmen91.github.io/static-site-generator](https://harmen91.github.io/static-site-generator/)

---

## 📄 License

This project is for educational purposes. 
