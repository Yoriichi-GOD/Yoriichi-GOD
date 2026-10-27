# Maintenance and publishing

Prepared locally on 27 October 2026. No remote repository, push, visibility change, deployment or profile-setting update has been performed.

## Recommended GitHub bio

141 characters, including spaces and punctuation:

> Founder & engineer. AI, computer vision, Earth observation, and full-stack products. Build the system. Test the claim. Preserve the evidence.

## Six public pins, in order

1. **SATquery-AI** — lead Earth-observation system and transparent evaluations.
2. **warscythe** — full-stack consumer-product depth and persistent progression.
3. **REFLEX** — visual inspection, an accessible demo and a candid release decision.
4. **GhostTrace** — a distinct privacy-engineering domain and read-only evidence workflow.
5. **SatQuery---Flood-Lab** — geospatial exposure/provenance, with open accuracy limits.
6. **lighthouse** — source retrieval and research-workspace breadth.

REGULENS remains featured as a private project in the README. It is not a public pin recommendation while private. Do not make it public for portfolio symmetry. Peekolitix remains in the secondary archive because Lighthouse adds a more distinct evidence workflow to the six-pin selection.

## Publish only after approval

GitHub requires a **public** repository with the exact account name and a nonempty root `README.md`. See [GitHub's profile README instructions](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

The connected-account and anonymous checks both returned 404 for `Yoriichi-GOD/Yoriichi-GOD` during this review. Recheck before creation; another session could create it later.

1. Review the root README, full preview, provenance record, and final file list. Approve this exact package and the public visibility.
2. After approval, create `Yoriichi-GOD/Yoriichi-GOD` on GitHub, set visibility to **Public**, and leave automatic README/licence/gitignore initialization off when using this prepared local repository.
3. From this local folder, inspect `git status` and `git diff --cached`. Include only `README.md`, `.gitignore`, `assets/`, `docs/`, and `tools/`. The ignored `.review/` cache contains local previews, source originals, dependencies and diagnostic data; never force-add it.
4. Commit the reviewed files locally, add `https://github.com/Yoriichi-GOD/Yoriichi-GOD.git` as the remote, and push `main` **only after approval**.
5. Open the actual GitHub profile and repository README on desktop/mobile in both themes. Confirm picture selection, embedded SVG specimens, the four full-size UI links, local-document routes and the evidence anchor. This is the remaining live-host validation step.
6. Set the bio and six pins manually, or authorize those separate account changes. Uploading this package does not update the bio or pin settings automatically.

After the public repository and this exact upload are approved, the local Git sequence is:

```powershell
git add README.md .gitignore assets docs tools
git diff --cached --stat
git commit -m "Create The Engineering Archive profile"
git remote add origin https://github.com/Yoriichi-GOD/Yoriichi-GOD.git
git push -u origin main
```

Run the inspection step before the commit. If a remote already exists, inspect it before changing anything; do not blindly repeat `remote add`. These commands are instructions only and have not been executed in this task.

If GitHub's live SVG path fails in a client, use the PNG hero fallback; for a broader fallback rasterize the affected plates from their SVG source. Inspect that actual failure before introducing duplicate raster assets.

## Updating content

Treat each claim as a dated record. Edit `docs/CONTENT_PROVENANCE.md` first, then the relevant README sentence. Do not silently replace a historical score with a new run or combine populations. New work enters the profile only when its implementation, status, public route and visual rights are clear.

Before changing the six featured projects, check whether the current body still communicates the engineering identity within a quick scan. A new framework or a new experiment is not automatically a new featured project.

## Rebuild assets

Use an isolated Python environment with Pillow, fonttools[woff] and Brotli. Obtain the three named OFL font files from their credited upstream projects or an authorized local font directory. Font binaries are inputs only and must stay outside tracked files.

1. `python tools/collect_sources.py` downloads only the two retained public specimens listed in `tools/sources.json`, checks Git blob hashes and places them in `.review/sources/`. The four revised UI screens use the tracked optimized copies listed in `tools/ui_sources.json`.
2. When original captures are available, `python tools/prepare_ui_assets.py` verifies their hashes and creates proportional quality-90 WebP copies. If originals are absent in a fresh clone, it validates the existing tracked WebP files instead. Never substitute a new capture without updating its provenance and checking reuse authorization. `python tools/build_assets.py --font-dir <licensed-font-directory> --sources .review/sources` regenerates the static plates.
3. For the local browser harness, provide `ARCHIVE_NODE_MODULES` pointing to a dependency directory containing `playwright`, `marked` and `sharp`, and `ARCHIVE_CHROME` pointing to an installed Chromium browser. Place the MIT-licensed [github-markdown-css](https://github.com/sindresorhus/github-markdown-css) stylesheet in `.review/github-markdown.css`, then run `node tools/preview.cjs`. The harness uses local files and does not upload the README.
4. `python tools/verify_links.py` performs anonymous public GET checks and local asset/unsafe-SVG checks. It does not run project inference.
5. Inspect rendered screenshots. A loaded image can still contain a broken design. The first export in this work demonstrated exactly that with a glyph-mapping bug, which was corrected before delivery.

Keep a local copy of the old evidence and screenshots before updating. Do not overwrite project datasets or historic evaluation records from this repository.

The three user-supplied PNGs remain unchanged in the local `assets/` folder and are explicitly ignored by Git; their optimized copies are tracked in `assets/projects/`. Previous checkpoints are preserved under `.review/revisions/before-full-ui/` and `.review/revisions/before-side-by-side/`. Desktop cards now alternate equal text/image halves with image-proportional heights; keep that geometry when replacing an image so fitting bands do not return. REGULENS screenshot authorization does not authorize copying its private datasets, document evidence or benchmark values.
