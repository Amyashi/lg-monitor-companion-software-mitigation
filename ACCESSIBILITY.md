# Accessibility

Amyashi intends both edition guides to be usable by readers with different
levels of technical experience and by people using assistive technology.
Accessibility defects are treated as publication defects.

## Available formats

The release provides:

- A Windows 11 Home PDF with selectable text
- A Windows 11 Pro PDF with selectable text
- A substantive, linear
  [`Windows 11 Home Markdown companion`](docs/LG_Monitor_Companion_Software_Windows_11_Home.md)
- A substantive, linear
  [`Windows 11 Pro Markdown companion`](docs/LG_Monitor_Companion_Software_Windows_11_Pro.md)
- The shared text and layout source in
  `build_lg_monitor_companion_software_guides.py`
- Plain-text Markdown files for repository guidance, license and third-party
  notices, security reporting, and contribution instructions

Each Markdown companion contains the essential safety warnings, commands or
interface paths, evidence states, rollback procedure, and references for its
edition. It is the preferred accessible alternative if a PDF reader does not
expose the corresponding PDF correctly.

The Python source is included for review and is subject to the limited
execution and contribution permissions in `LICENSE.md`. Its inclusion does not
grant any additional right to copy, modify, or redistribute the code.

## PDF accessibility features and target

Each release PDF is intended to have a meaningful document title,
language metadata, section bookmarks, readable and selectable text, status
words in addition to color, and a deliberate visual reading order. Small-text
foreground and background color pairs are designed to meet at least a 4.5:1
contrast ratio. The project does not claim a complete PDF/UA tag structure.
These features improve navigation but do not, by themselves, establish
standards conformance.

Both editions must be reviewed for:

- A meaningful edition-specific title and document language
- Logical reading order and useful structural information where the generator
  and post-processing toolchain expose it
- Bookmarks for major sections
- Selectable and searchable text rather than text rendered only as an image
- Sufficient color contrast, with status never communicated by color alone
- Legible type at normal viewing magnification
- Descriptive link text and useful table headers
- Keyboard and screen-reader navigation
- Clear expansion of specialized abbreviations and plain-language warnings
- Agreement between each PDF and its edition-specific Markdown companion

Before a public release, a person must review every rendered page of both PDFs
and perform a keyboard and screen-reader spot check of both PDFs and both
Markdown companions. Automated checks are gates, not substitutes for that
review.

## Known limitations

Generated PDFs may not expose every structural relationship, table, code
sample, or status badge correctly to every screen reader. ReportLab generation
and the PDF post-processing toolchain can also create differences between
visual order and assistive-technology reading order. Readers should not rely on
color alone to interpret a status.

Consult the matching Markdown companion if a PDF feature does not work with
your assistive technology. Do not infer that a successful build, bookmarks,
language metadata, selectable text, or visual inspection establishes PDF/UA
conformance. The project does not currently claim formal PDF/UA, WCAG, Section
508, or other accessibility certification.

## Report an accessibility problem

Open a GitHub issue using the accessibility option and include:

- The edition, release, and page or section
- The assistive technology and application used
- What you expected and what occurred
- A sanitized reproduction, if one can be shared safely

Do not attach screenshots, logs, documents, or other evidence containing
personal or system-identifying information. For a security-sensitive
accessibility issue, follow `SECURITY.md` instead.
