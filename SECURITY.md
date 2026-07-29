# Security Policy

## Supported material

Security corrections are provided for the latest published Home and Pro guides
and the current `main` branch. Earlier releases may receive
documentation corrections when a serious risk would otherwise remain unclear,
but they are not independently maintained.

This policy covers:

- Unsafe, materially incorrect, or misleading security instructions
- A repository build or validation flaw with security impact
- Accidental disclosure of credentials, personal information, or sensitive evidence
- A dependency vulnerability that affects the published build or validation process

It does not provide product support for LG Electronics, LG monitors or
software, Microsoft Windows, AppLocker, Microsoft Defender, Python, ReportLab,
or other third-party products.

## Report privately

Use **Security > Advisories > Report a vulnerability**. The direct repository
route is:

<https://github.com/Amyashi/lg-monitor-companion-software-mitigation/security/advisories/new>

If GitHub private vulnerability reporting is unavailable, wait until it is
available. Do not disclose a security-sensitive report through a public issue,
pull request, discussion, commit, branch, release, or attachment.

Please include privately, when safe and relevant:

- A concise description and potential impact
- The affected edition, file, section, release, or commit
- Reproduction steps using sanitized or synthetic data
- A proposed correction, if known
- Whether the issue is already public

## Never place sensitive evidence in public GitHub content

Do not put any of the following in an issue, discussion, pull request, commit, branch, release, or Actions log:

- Passwords, API keys, tokens, cookies, certificates, private keys, or recovery material
- Personal usernames, personal email addresses, account identifiers, hostnames,
  IP addresses, serial numbers, device identifiers, or precise location data
- Raw event logs, registry exports, diagnostic archives, crash dumps, support bundles, or system inventories
- Unredacted screenshots or photographs
- Private vendor correspondence, investigation material, or information belonging to another person

If a credential or secret is exposed, rotate or revoke it immediately. Deleting the visible file or comment is not sufficient because copies may remain in Git history, forks, caches, notifications, or logs.

Use the minimum evidence necessary. Prefer a synthetic reproduction, a redacted excerpt, and a plain-language description over raw evidence.

## Handling and disclosure

Amyashi will make a good-faith effort to acknowledge a complete report, assess impact, prepare a correction, and coordinate publication. No response or remediation time is guaranteed. Please allow a reasonable opportunity to investigate before public disclosure.

Submitting a report does not authorize testing against systems, accounts, devices, or data you do not own or have explicit permission to test.
