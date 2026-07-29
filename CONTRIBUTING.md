# Contributing

Thank you for helping improve the LG monitor companion-software mitigation
guides. This is a controlled-author project: issues and well-supported
proposals are welcome, but changes are accepted at the author's discretion.

## Before contributing

Search existing issues before opening a new one. Use:

- **Guide, build, or accessibility problem** for a factual error, broken
  reference, unclear instruction, unsafe ambiguity, build defect, or
  accessibility problem;
- **Improvement proposal** for a substantive procedure, structure, or usability
  change; and
- **GitHub private vulnerability reporting** for a vulnerability in the
  repository, automation, or generated artifacts.

Do not use this repository for device-specific technical support.

## Evidence and privacy

Use current primary sources whenever possible. A claim about Windows, LG
software, firmware, licensing, product behavior, or security guidance should
include:

- the authoritative source URL;
- the date it was checked;
- the affected edition, version, package identity, or hardware prerequisite;
  and
- a clear distinction between documented behavior, observation, and
  inference.

Never submit recovery material, credentials, tokens, certificates, full logs,
dumps, registry exports, screenshots with account or device data, serial
numbers, hostnames, network identifiers, public IP addresses, or other
sensitive evidence. Replace necessary examples with neutral placeholders.

## Limited permission to prepare a contribution

The
[contribution-only permission in LICENSE.md](LICENSE.md#contribution-only-permission)
allows you to fork, modify, and share repository material only as reasonably
necessary to prepare, discuss, review, and submit a contribution to the
official
[`Amyashi/lg-monitor-companion-software-mitigation`](https://github.com/Amyashi/lg-monitor-companion-software-mitigation)
repository through GitHub.

That permission does not authorize a separate release, a general-purpose
modified fork, commercial use, or redistribution outside the contribution
process. Preserve existing copyright and license notices, identify your
changes, and do not include third-party material unless you have the right to
submit it under the grant below.

## Useful contributions

- Corrections supported by current primary documentation
- Clear distinctions between documented behavior, observed behavior, and a result requiring recheck
- Safer rollback, verification, or failure-mode guidance
- Accessibility and plain-language improvements
- Reproducible two-edition PDF build or validation fixes
- Reports that a Windows, AppLocker, Defender, Store, LG, or dependency change invalidated an instruction

Vendor documentation and Microsoft documentation are preferred over secondary summaries. Identify the precise claim each source supports, include a stable URL, and record the date checked when behavior can change.

## Pull requests

A substantial pull request should be discussed in an issue first. A pull
request should:

- Address one coherent change
- Explain the reader or security impact
- Identify affected guide sections and source files
- Include the commands or checks used to validate the change
- Preserve least privilege, rollback, and evidence-boundary language
- Rebuild and visually inspect every affected PDF and its matching Markdown
  companion when layout or generated content changes
- Avoid unrelated formatting or dependency changes
- Contain no sensitive information

Opening a pull request makes a proposal; it does not incorporate the change
into the project. The author may edit, combine, defer, decline, remove, or
decline to maintain a contribution.

## Contribution grant

By opening a pull request, posting proposed material in an issue, or otherwise
submitting material through the official repository, you represent that you
have the right to submit it and grant Amyashi a perpetual, worldwide,
non-exclusive, royalty-free, irrevocable license to use, reproduce, modify,
prepare derivative works from, distribute, publicly display, publicly perform,
sublicense, and relicense the contribution as part of this project or related
editions.

The grant covers the material you contribute and revisions you submit during
review; it does not transfer ownership of pre-existing repository material. If
accepted, the author may incorporate and distribute the contribution under the
project terms applicable to the resulting material.

You retain any copyright you hold in your original contribution. The grant
remains effective whether the submission is accepted, edited, declined, or
later removed. Submission does not grant contributors a license to other
repository content beyond the contribution-only permission and does not
otherwise change the terms in [LICENSE.md](LICENSE.md).

## Editorial rules

- Do not describe the guide as certified, complete, guaranteed, or universally effective.
- Do not convert an observation into a general product claim.
- Do not generalize the tested `LGElectronics.LGMonitorApp` identity to other
  LG monitor software without separate evidence.
- Keep shared Home and Pro instructions synchronized; edition-specific wording
  belongs only where Windows capabilities materially differ.
- Use neutral, reproducible language and define specialized terms for nontechnical readers.
- Keep public evidence sanitized and non-identifying.
- Preserve warnings before consequential commands.
- Do not add telemetry, network calls, analytics, or external services without prior discussion.

## Local validation

Use Python 3.12 and the documented dependency versions:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --disable-pip-version-check --only-binary=:all: --require-hashes -r requirements.txt
python .\build_lg_monitor_companion_software_guides.py
python .\scripts\validate_pdf.py .\LG_Monitor_Companion_Software_Mitigation_Windows_11_Home_v1.0.0.pdf .\LG_Monitor_Companion_Software_Mitigation_Windows_11_Pro_v1.0.0.pdf --check-tracked-pdf-set --check-tracked-text-disclosures --source .\build_lg_monitor_companion_software_guides.py
```

Automated validation is necessary but not sufficient. Render and inspect every
page of both PDFs before marking a change ready for release.
