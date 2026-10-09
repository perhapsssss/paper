# Contact-aided InEKF translation verification

## Deliverables

- `original.pdf`: supplied 44-page arXiv v2 paper.
- `source.md` and `source-pages/`: extracted English text, one file per PDF page.
- `translation/1-full-zh.md`: structured Chinese reading translation covering the abstract, sections 1–13, equations central to the derivation, figure captions, and appendices A–C.
- `translation-reading.html`: responsive reader with a section navigation, terminology panel, MathJax, print mode, Chinese reading, selected aligned excerpts, and a direct original-PDF link.
- `alignment.json`: title, selected abstract, equation, theorem, and caption alignment records.
- `figure-map.json` and `assets/figures/`: 17 raster assets extracted from the 12 numbered figures in the PDF.
- `glossary.md`, `style-guide.md`, and `chapter-index.md`.

## Checks performed

- Confirmed the input PDF opens and contains 44 pages.
- Extracted text for all 44 pages and retained the original PDF.
- Extracted embedded figure assets; visually inspected a contact sheet to associate assets with figures.
- Verified that all 17 figure asset paths referenced by the figure map exist.
- Confirmed the article catalogue contains the new paper entry and points to its reader, cover, and original PDF.
- Generated the HTML reader from the translation Markdown with MathJax enabled.

## Limitations to retain

The PDF text layer loses alignment in several large block matrices and in some appendix integrals. The translation preserves the principal readable equations and describes the remaining matrix structures, with the supplied PDF linked for exact symbol-by-symbol verification. The English references are kept in the extracted original text and PDF rather than re-typeset individually in Chinese. The parallel mode is a selected excerpt alignment rather than a line-by-line display of every prose paragraph.
