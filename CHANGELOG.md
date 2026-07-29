# Changelog

All notable changes are documented here. Dates use ISO 8601
(`YYYY-MM-DD`). The project is maintained as a controlled-author publication.

## [Unreleased]

Planned first public release: `v1.0.0`. No public GitHub release is represented
by this entry while the repository and release remain private.

### Added

- Separate action-first Windows 11 Home and Windows 11 Pro guides, each with
  exact commands or interface paths, expected results, restart points, stop
  conditions, recovery gates, and next-action branches.
- Edition-specific accessible Markdown companions generated from the same
  substantive procedure.
- Preflight gates for Windows edition, organization management, active monitor
  firmware updates, alternate monitor control, official recovery access, and
  exact package and publisher identity.
- Package-absent handling, package-type-aware removal, explicit `REMOVE`
  confirmation, and post-restart monitor-function checks.
- AppLocker capture of local and effective policy and the original Application
  Identity service state for policy rollback and retained service-state
  documentation.
- A deterministic two-edition PDF builder and release validator.
- SHA-256 checksums for both release PDFs.
- Public authorship credit.

### Changed

- Generalized the project scope to LG monitor companion-software delivery while
  limiting the tested package claim to `LGElectronics.LGMonitorApp`.
- Replaced the prior reference-matrix structure with one linear core procedure
  and a clearly separated optional AppLocker escalation path.
- Split the reader artifacts by Windows edition so Home readers receive the
  Device Installation Settings preference and Pro readers receive the Local
  Group Policy procedure, without duplicating unrelated controls.
- Moved governance detail behind the action path while retaining warnings at
  risk-changing gates: authority, firmware and control availability, software
  removal, AppLocker enforcement, and full-policy replacement.
- Updated the Windows edition boundary from current Microsoft documentation:
  package cleanup, Defender potentially unwanted application protection, and
  current AppLocker platform support are common; the documented
  `PreventDeviceMetadataFromNetwork` policy is Pro and higher, while Home uses
  the weaker Device Installation Settings preference.
- Made successful core verification a stopping point. AppLocker is no longer
  presented as an automatic continuation.
- Required Audit-only deployment, a defined compatibility workload, simulated
  policy checks, a timestamp-bounded enforced-denial check, and immediate smoke
  testing before AppLocker-backed removal.
- Made the Home preflight preserve the exact Device Installation Settings
  choice before mutation, and made a missing real AppLocker deny event stop the
  enforcement procedure before package cleanup.
- Preserved the first Defender PUA audit-start timestamp across reruns and
  aligned the PDF with the accessible companion's enable, signature-update,
  quick-scan, and result-verification steps.
- Made rollback restore the captured policy and preference state where
  supported, and documented the protected Application Identity service
  limitation instead of promising an unsupported `sc.exe` reversal.
- Added a fresh pre-replacement policy export, `-WhatIf` preview, exact typed
  confirmation, and post-restore local and effective exports to the emergency
  full-policy rollback path.
- Clarified that metadata controls are not universal software-delivery blocks,
  policy backups do not reinstall removed software, and other LG monitor
  applications require separate identity and delivery-path analysis.
- Updated authoritative-source review through `2026-07-29`.
- Updated SHA-pinned workflow dependencies to `actions/checkout` v6.0.2 and
  `actions/setup-python` v6.2.0.
- Marked the Windows 11 Home procedure as documentation-derived and
  structurally validated, but not field-tested on a Windows 11 Home machine.
- Applied the controlled-author license structure: CC BY-NC-ND 4.0 for guide
  materials, all rights reserved for code and automation, and a narrow
  contribution-only permission.
- Removed public email, Discord, direct-message, and community contact routes.
- Prepared a clean-history repository under the model-neutral project slug.

### Publication gates

- Keep the repository private until Amyashi explicitly approves publication.
- Complete the manual accessibility review in `ACCESSIBILITY.md` for both
  edition artifacts and companions.
- Run the release validator from a clean staged fixture against both editions.
- Confirm that every retained observation is backed by a sanitized source
  record or reclassify it before release.
- Complete maintainer approval of the final Home and Pro rendered artifacts.

[Unreleased]: https://github.com/Amyashi/lg-monitor-companion-software-mitigation/commits/main
