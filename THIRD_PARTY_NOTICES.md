# Third-Party Notices

This project uses third-party software to build or validate the guide. Amyashi claims no ownership of those third-party components, names, marks, or license text. The repository's copyright and permission notice does not replace an upstream license.

## ReportLab

The PDF builder uses ReportLab 5.0.0. ReportLab is distributed under a BSD-style license. A plain-text reproduction of the substantive license terms from the pinned wheel is included at [`licenses/REPORTLAB.txt`](licenses/REPORTLAB.txt). Review the controlling license shipped with the exact installed distribution before redistributing the dependency:

- Project: <https://www.reportlab.com/opensource/>
- Version-pinned upstream source: <https://hg.reportlab.com/hg-public/reportlab/rev/47508099cf5d>
- Upstream license file: <https://hg.reportlab.com/hg-public/reportlab/file/47508099cf5d/src/reportlab/license.txt>

## Fonts in the PDF

The current builder uses the standard PDF Base 14 Helvetica and Courier families through local aliases. It does not embed or redistribute a project-supplied font file.

## pypdf

The validation process uses pypdf, which is distributed under the BSD 3-Clause License. Review the license shipped with the exact installed distribution and the upstream project:

- Project: <https://pypi.org/project/pypdf/>
- Version-pinned upstream license: <https://github.com/py-pdf/pypdf/blob/6.14.2/LICENSE>

## Pillow and charset-normalizer

ReportLab's pinned dependency set includes Pillow and charset-normalizer. Review the licenses shipped with the exact installed distributions before redistributing either dependency:

- Pillow: <https://github.com/python-pillow/Pillow/blob/12.3.0/LICENSE>
- charset-normalizer: <https://github.com/jawah/charset_normalizer/blob/3.4.9/LICENSE>

## Version-specific review

Dependency versions are recorded in the repository's build manifests. Before distributing a rebuilt artifact or dependency bundle, inspect the license metadata and license files included with the exact versions used. This notice is an attribution aid, not a substitute for those controlling terms.

## Documentation, names, and marks

Project licensing does not relicense third-party material. Links to external
documentation and short factual citations do not imply ownership,
affiliation, sponsorship, or endorsement.

LG, UltraGear, Microsoft, Windows, AppLocker, Defender, and other third-party
names and marks belong to their respective owners and are used only for
identification. This independent project is not affiliated with, sponsored by,
or endorsed by LG Electronics or Microsoft.
