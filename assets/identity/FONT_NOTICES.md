# Display typography

The original archive assets use outlined glyphs from the following SIL Open Font License 1.1 families. No font software/binary is distributed in this repository. Full upstream notices are retained as credits in `licenses/`.

- **Cormorant Garamond 600:** Copyright 2015 The Cormorant Project Authors. [Upstream](https://github.com/CatharsisFonts/Cormorant). [Notice](licenses/cormorant-garamond-OFL.txt).
- **Manrope 400:** Copyright 2019 The Manrope Project Authors. [Upstream](https://github.com/sharanda/manrope). [Notice](licenses/manrope-OFL.txt).
- **IBM Plex Mono 400:** Copyright 2017 IBM Corp. All rights reserved. [Upstream](https://github.com/IBM/plex). [Notice](licenses/ibm-plex-mono-OFL.txt).

The source build reads the named Latin WOFF2 files from a separately supplied licensed font directory, converts each glyph to vector paths and emits no `text`, `style`, `@font-face` or remote-resource dependency. Lettering is artwork, not a modified font distribution.
