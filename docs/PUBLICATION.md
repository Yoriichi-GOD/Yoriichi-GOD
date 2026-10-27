# Publication record

Published **27 October 2026**, after the user explicitly approved: “publish it now”.

- [Live GitHub profile](https://github.com/Yoriichi-GOD)
- [Public profile repository](https://github.com/Yoriichi-GOD/Yoriichi-GOD)
- Branch: `main`
- Initial reviewed content commit: `ab64eae1b38659e6b7ffa7bdaa0edc250fd443bc`
- Initial README SHA-256: `869156951e0799dd0db0058275ad2edde14379ccbd42e6eacd51cd0d4371dc96`

## Verified on GitHub

The repository is public. Its initial 48-file remote tree exactly matched the reviewed local tree. The approved README and all four standalone UI images matched their local hashes through anonymous public requests. Ignored review files, raw user PNGs, font binaries and credentials were excluded. REGULENS remains private; only its expressly authorized synthetic-demo screenshot is included here.

The actual anonymous GitHub profile was opened in Chromium at all three requested widths, in both color schemes:

| Viewport | Theme | Live README width | HTTP | Broken images | Overflow | Full UI links |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| 1440 px | dark | 846 px | 200 | 0 | None | 4 |
| 1440 px | light | 846 px | 200 | 0 | None | 4 |
| 1024 px | dark | 590 px | 200 | 0 | None | 4 |
| 1024 px | light | 590 px | 200 | 0 | None | 4 |
| 390 px | dark | 308 px | 200 | 0 | None | 4 |
| 390 px | light | 308 px | 200 | 0 | None | 4 |

All eight responsive picture blocks are present. The mobile hero selects correctly at 390 pixels, the desktop hero at the wider sizes, and the evidence anchor exists. Actual live screenshots were inspected for image delivery and layout; the local preview is no longer the only visual evidence. Receipts and screenshots remain in ignored `.review/`; the compact public result is [VERIFICATION.json](VERIFICATION.json).

This publication changes the profile repository only. Existing project repositories, deployments, datasets, account bio and pinned repositories were not changed. The recommended bio and pins remain in [MAINTENANCE.md](MAINTENANCE.md).

## Mobile UI correction — 27 October 2026

Content commit: `98c8a25`. Current README SHA-256: `ca6df302487b9ffa66f39efdd5e94c9cfce847be8f3c52cf8f31f1ea5ba2a8f9`.

The user reported that SatQuery and GhostTrace still showed an output crop and a schematic on phone. Both now preserve their complete actual public UI viewport. The source builder was corrected, the six desktop panels and all other visual assets are unchanged, and two full-size original-image links were added. No new screenshots, private content or source-project changes were introduced.

The actual live profile was checked again after pushing:

| Viewport | Themes | Live README width | HTTP | Broken images | Overflow | Full UI links | Delivered card hashes |
| --- | --- | ---: | ---: | ---: | --- | ---: | --- |
| 1440 px | dark + light | 846 px | 200 | 0 | None | 6 | Match reviewed desktop SVGs |
| 1024 px | dark + light | 590 px | 200 | 0 | None | 6 | Match reviewed desktop SVGs |
| 390 px | dark + light | 308 px | 200 | 0 | None | 6 | Match corrected mobile SVGs |
| 350 px | dark + light | 268 px | 200 | 0 | None | 6 | Match corrected mobile SVGs |

Live mobile-card screenshots were inspected at 390 dark and 350 light. The two new full-size links returned anonymous HTTP 200 with the pinned source hashes. This is browser verification at phone widths, not a hardware or native GitHub iOS app test. Local receipts: `.review/mobile-fix-checks.json` and `.review/mobile-fix-live-checks.json`.
