# Visual QA and closure record

**27 October 2026 — published and verified on the live GitHub profile.**

## What actually ran

1. GitHub's anonymous, stateless Markdown API rendered the final public-safe README successfully (HTTP 200). All **8 picture elements and 8 mobile source elements** survived its sanitizer. No repository was created or written. The renderer returned no scripts.
2. That exact HTML was opened locally in headless **Chrome 156.0.8078.48**, controlled with Playwright on **Node 24.18.0**. The harness used `github-markdown-css` and local heading IDs to emulate GitHub navigation. The README content hash was checked to reject stale HTML.
3. Full-page and top-of-page screenshots were captured at **1440, 1024 and 390 pixels**, each in **light and dark** mode. The viewport height was 1000 pixels, device scale 1.
4. Browser checks recorded image loading, selected picture sources, element bounds, document overflow, anchor targets and page errors. Every SVG's outlined-lettering bounds were checked against its viewBox.
5. Actual screenshots were visually inspected: cover typography, desktop/mobile project treatments, working principle, top sections, evidence and footer. The current revision restores alternating image/text desktop cards for all six projects while preserving the approved UI inputs and phone compositions. The six changed desktop plates, including the enlarged SatQuery image half, were inspected directly.

The local matrix below records **GitHub-rendered Markdown HTML inspected in a local browser**. After the user approved publication, the actual anonymous GitHub profile was additionally rendered and inspected at 1440, 1024 and 390 pixels in both color schemes. The [publication record](PUBLICATION.md) reports live container widths, image delivery, full-size routes and responsive selection.

## Final render matrix

| Viewport | Theme | Article width | Page height | Broken images | Document overflow | Missing navigation targets / page errors |
| --- | --- | ---: | ---: | ---: | --- | --- |
| 1440 × 1000 | Dark | 896 px | 4745 px | 0 / 14 | None | 0 / 0 |
| 1440 × 1000 | Light | 896 px | 4745 px | 0 / 14 | None | 0 / 0 |
| 1024 × 1000 | Dark | 896 px | 4745 px | 0 / 14 | None | 0 / 0 |
| 1024 × 1000 | Light | 896 px | 4745 px | 0 / 14 | None | 0 / 0 |
| 390 × 1000 | Dark | 366 px | 6980 px | 0 / 14 | None | 0 / 0 |
| 390 × 1000 | Light | 366 px | 6980 px | 0 / 14 | None | 0 / 0 |

The article includes its padding and border. Actual artwork is approximately 846 pixels wide on desktop and 332 pixels on mobile. Desktop/tablet share a conservative 896-pixel maximum article width. GitHub's exact profile sidebar was not reproduced.

## Visual findings and corrections

- **Typography bug caught and fixed:** the first SVG export used character strings against an integer-codepoint font map. Images loaded, but lettering became missing-glyph boxes. The exporter now uses codepoints and stops on missing glyphs. Corrected lettering was rendered and inspected. Image-load success alone was insufficient.
- **Restored alternating direction:** all six desktop cards now alternate right/left screenshots. Each inner card is exactly half text / half image: 784 pixels each inside a 1600-pixel source SVG. Image height follows its own aspect ratio, so no large fitting bands remain beside the screenshot. Geometry checks find less than 0.41 source-layout pixels of rounding slack, with no cropping. The colored rule stays on the text side.
- **Approved images preserved:** Warscythe, REGULENS, REFLEX and Flood Lab still use the same complete captured viewports. SVG scaling remains `meet`, not `slice`, and their desktop/mobile embedded bytes match their standalone **Open full UI** destinations. These are viewport captures, not a claim that every scrollable app panel is fully visible.
- **Mobile direction:** the name and project titles reflow above each screen. Small app labels are naturally reduced at phone width; selectable native copy and the four full-size links remain the reading and inspection routes. SatQuery's existing mobile output crop and GhostTrace's schematic are unchanged.
- **Scope and regression:** README copy, taglines and approved image files are unchanged. All 16 SVGs outside the six changed desktop project plates match their previous SHA-256 hashes, including every mobile plate, the hero, icons, method and rule. The desktop page falls from 6033 to 4745 pixels; mobile remains 6980 pixels.
- **Hierarchy:** the name, handle and founder/engineer line appear before the introduction. The first-screen routes expose repositories, hosted v1, the recorded demonstration and evidence. A 15-second visitor comprehension study was not performed; quick orientation is an editorial judgment from the rendered page.
- **Clipping/consistency:** all 22 SVGs parse, and all outlined text stays inside its viewBox. Titles, rules, frames, captions and full UI bounds were inspected. No clipped critical text or overlapping mobile identity was found.
- **Themes:** artwork backgrounds remain explicitly charcoal in both modes; native text follows GitHub light/dark typography. No attempt is made to impose unsupported page CSS.
- **Length:** the restored alternating desktop structure reduces page length while preserving complete screenshots and all requested content. The secondary archive remains compact. No project or content scope was added.

## Asset and content checks

- **22 SVGs**, four standalone complete-UI WebPs, one **1600 × 500 PNG** hero fallback, font notices and three text-only OFL notices. No font binaries, JavaScript, animation, remote SVG resources, CSS-dependent SVG text or foreignObject elements.
- Publication assets total **3,628,560 bytes**, including the four full-size click targets, notices and fallback. The four optimized UI inputs remain **672,102 bytes**. Original supplied PNGs are ignored and excluded from those publication totals. Outlined coordinates remain rounded to 0.01 source pixels.
- The two retained public specimens matched their pinned Git blob hashes. The four replacement originals and their optimized outputs have SHA-256 records; all four original hashes remain unchanged. Desktop/mobile embeds match their complete standalone WebP sources byte-for-byte.
- **25 distinct README external links** returned anonymous HTTP 200. Candidate destinations excluded from the README include the old Peekolitix Vercel URL (404), a Warscythe DNS failure and an untitled candidate page. The profile-repository API returned 404.
- Local Markdown/document/image links are checked separately at package close. The Evidence navigation anchor works in the local heading-ID emulation.
- REGULENS includes one explicitly authorized actual dashboard screenshot on fictional demo records, replacing the schematic. Its private documents, datasets, benchmark figures, submission files and inaccessible repository link remain excluded.
- Public measurements retain dates, denominators, method scope and limitations. No new product inference, training, software-suite run or deployment occurred in this task.

## Definition of Done

- [x] Isolated root README and exact-name local profile folder.
- [x] Original hero, responsive project plates, five authored discipline icons, method plate and rule.
- [x] Identity, introduction, six projects, disciplines, philosophy, secondary archive, evidence and contact/current work.
- [x] Actual repository inventory, supportable copy, public routes and attribution.
- [x] Design system, content provenance, visual QA, maintenance/publishing notes and file manifest.
- [x] Bio of 141 characters and six public pin recommendations.
- [x] Rendered checks at all requested widths/themes; actual visual inspection and correction.
- [x] No project-source edits or publication actions.
- [x] User approval received; public profile repository created and reviewed package pushed.
- [x] Actual GitHub profile inspected at all requested widths/themes, including live SVG delivery, responsive hero, full-size UI routes and sidebar/container behavior.

Publication gates are closed. The actual GitHub checks are recorded separately from the earlier local-render measurements.

## Local review artifacts

The ignored `.review/` folder contains six `profile-WIDTH-THEME.png` full-page screenshots, six `top-WIDTH-THEME.png` covers, evidence crops, individual plate screenshots, `render-checks.json`, `glyph-bounds.json`, `link-checks.json`, the GitHub-rendered HTML and its content-hash receipt. These are local review files and are not linked as public repository assets.

The final response links the desktop/mobile previews directly for review. [Publishing and maintenance](MAINTENANCE.md) explains the remaining live-host check.

Earlier checkpoints and QA reports are preserved locally in `.review/revisions/before-full-ui/` and `.review/revisions/before-side-by-side/`. The image receipt remains `tools/ui_sources.json`; local checks are `.review/ui-revision-checks.json` and `.review/side-by-side-checks.json`.

## Publication closure

The user approved publication on 27 October 2026. [Live profile and verification receipt](PUBLICATION.md). No source project or account bio/pin change accompanied publication.
