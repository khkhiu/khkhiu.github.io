# khkhiu.github.io

Source for my personal site at <https://khkhiu.github.io>, built with [Sphinx](https://www.sphinx-doc.org/), the [Furo](https://pradyunsg.me/furo/) theme and [MyST Markdown](https://myst-parser.readthedocs.io/). Posts are mostly write-ups of HPC and scientific computing work.

## Writing a post

1. Create a Markdown file in `docs/source/posts/`.
2. Start it with this front matter. The `date:` line is what puts the post in order, so don't leave it out.

   ```markdown
   ---
   title: "Post title"
   date: 2026-11-27
   tags: [hpc, openfoam]
   ---

   # Post title

   *Published: 2026-11-27*
   ```

3. Commit and push. Nothing else needs editing: the post appears on the home page automatically, newest first.

Filenames are free-form. A date prefix such as `2026-11-27-short-name.md` keeps the folder tidy, but ordering comes from the `date:` line, not the filename. Renaming a published post changes its URL, so pick the name before the first push.

MyST lets posts use Sphinx directives, for example:

````markdown
```{note}
Working notes, not a controlled benchmark.
```
````

## How the post list is generated

The home page has no hand-written list of posts. Instead:

- A hook at the end of `docs/source/conf.py` runs at the start of every build.
- It reads the `date:` line from each file in `docs/source/posts/`, sorts newest first, and writes `docs/source/_posts_toc.rst`.
- `docs/source/index.rst` pulls that file in with `.. include:: _posts_toc.rst`.

`_posts_toc.rst` is generated, so it is listed in `.gitignore` (never commit it) and in `exclude_patterns` in `conf.py` (so Sphinx doesn't build it as a page of its own). Posts with no `date:` line sort to the bottom. Posts with the same date fall back to filename order.

## Building locally

One-time setup on a new machine:

```bash
cd ~/Documents/github/khkhiu.github.io
python3 -m venv .venv
source .venv/bin/activate
pip install -r docs/requirements.txt
```

Each build:

```bash
cd ~/Documents/github/khkhiu.github.io/docs
source ../.venv/bin/activate
make clean && make html
```

Open `docs/build/html/index.html` in a browser to check the result. `cat docs/source/_posts_toc.rst` shows the order the hook produced.

## Publishing

```bash
cd ~/Documents/github/khkhiu.github.io
git pull origin main
git add docs/source/posts/
git commit -m "Add post: <short title>"
git push origin main
```

GitHub Actions builds and deploys the site on every push to `main`; progress is under the repository's **Actions** tab. After it goes green, hard-refresh the live site (`Ctrl+Shift+R`).

Run `git pull` first when switching between machines, so a stale clone doesn't miss posts written elsewhere.

## Repository layout

```text
.
├── .github/workflows/     # build and deploy on push
├── docs/
│   ├── Makefile
│   ├── requirements.txt   # sphinx, furo, myst-parser
│   ├── build/             # local build output (not committed)
│   └── source/
│       ├── conf.py        # Sphinx config + post-ordering hook
│       ├── index.rst      # home page; includes _posts_toc.rst
│       ├── _posts_toc.rst # generated each build (not committed)
│       ├── _static/       # static assets (.gitkeep keeps it in git)
│       └── posts/         # one Markdown file per post
└── README.md
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `sphinx-build: command not found` | venv missing or not activated | Run the one-time setup, then `source .venv/bin/activate` |
| `no theme named 'furo' found` | Furo not installed in this venv | `pip install -r docs/requirements.txt` |
| `html_static_path entry '_static' does not exist` | Empty `_static/` folder not in git | `mkdir -p docs/source/_static && touch docs/source/_static/.gitkeep` |
| `document is referenced in multiple toctrees` | `_posts_toc.rst` built as its own page | Add `"_posts_toc.rst"` to `exclude_patterns` in `conf.py` |
| New post missing from the home page | No front matter, or no `date:` line | Check the file starts with `---` and has `date: YYYY-MM-DD` |
| Post at the bottom of the list | Missing or malformed `date:` | Use the `YYYY-MM-DD` format exactly |
| Live site unchanged after push | Deploy still running, or browser cache | Check the Actions tab, then hard-refresh |
