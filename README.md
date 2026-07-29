# LG monitor companion-software mitigation guides

This repository contains action-first Windows 11
runbooks for identifying and removing an exact LG monitor companion package
when the user has chosen not to retain it
and, only when justified, adding narrowly scoped controls against its return.
The tested Microsoft Store package is `LGElectronics.LGMonitorApp`. Other LG
applications, package identities, installers, drivers, and delivery paths must
be identified separately before any removal or policy change.

Two reader-facing editions keep the common procedure concise while giving each
reader only the device-metadata instructions that apply to that Windows edition:

- **Windows 11 Home:**
  [`LG_Monitor_Companion_Software_Mitigation_Windows_11_Home_v1.0.0.pdf`](LG_Monitor_Companion_Software_Mitigation_Windows_11_Home_v1.0.0.pdf)
  Accessible companion:
  [`docs/LG_Monitor_Companion_Software_Windows_11_Home.md`](docs/LG_Monitor_Companion_Software_Windows_11_Home.md)
- **Windows 11 Pro:**
  [`LG_Monitor_Companion_Software_Mitigation_Windows_11_Pro_v1.0.0.pdf`](LG_Monitor_Companion_Software_Mitigation_Windows_11_Pro_v1.0.0.pdf)
  Accessible companion:
  [`docs/LG_Monitor_Companion_Software_Windows_11_Pro.md`](docs/LG_Monitor_Companion_Software_Windows_11_Pro.md)

The guides are independently authored and unofficial. They are not LG
Electronics or Microsoft publications, endorsements, support channels,
incident-response substitutes, security certifications, or guarantees that
every present or future software-delivery path will be blocked.

The Windows 11 Home workflow is documentation-derived and structurally
validated, but it has not been field-tested on a Windows 11 Home machine.
Home readers must confirm each effective result locally and stop on any
mismatch. The original observed case and field-test basis used Windows 11 Pro.

## Follow the ordered path

Use the guide that matches **Settings > System > About > Windows
specifications > Edition**, then complete its numbered steps in order:

1. confirm authority, edition, recovery access, and that no monitor firmware
   update is running;
2. preserve the before-state and confirm the exact package and publisher;
3. apply the edition-appropriate device-metadata control;
4. remove only the exact confirmed package identity;
5. decide separately whether to retain LG OnScreen Control;
6. restart at the documented point;
7. verify package state and the monitor functions actually used; and
8. stop when the core result passes.

If the exact tested package later returns, first trace and record the delivery
path. The Pro guide then provides an optional Audit-first AppLocker path, but
only while the returned package remains installed and only when its local tools,
policy authority, backup, and compatibility gates all pass. Defender PUA
evaluation is a detached general-purpose option, not a required LG step.

Do not skip the core path to create an AppLocker rule. Stop on organization
management, unfamiliar policy, an unexpected publisher, a running firmware
update, or a missing recovery or monitor-control path. Treat each expected
result as a decision gate. If a result does not match, use the documented
failure branch instead of repeating a broader removal.

## Home and Pro boundary

Package discovery and removal, restart and functional testing, Defender
evaluation, and current AppLocker platform support are common to both editions.
The material edition difference is the device-metadata layer:

- **Home** uses the Device Installation Settings preference. It is weaker than
  an enforced policy. The Home guide does not install Group Policy Editor hacks
  or force a Pro-only policy registry value. This Home-specific path is
  documentation-derived and structurally validated, not field-tested on a
  Windows 11 Home machine.
- **Pro** can enforce
  `PreventDeviceMetadataFromNetwork` through Local Group Policy and verify the
  corresponding policy state.

Both controls address metadata-associated application retrieval only. They are
not universal blocks for Microsoft Store acquisition, OEM provisioning,
driver-associated software delivery, or Win32 installers. If software returns,
identify the current delivery source before escalating.

AppLocker enforcement is supported on current Windows 11 editions, but local
management tools are not guaranteed to be present on every installation. The
optional procedure therefore checks `secpol.msc`, the AppLocker PowerShell
cmdlets, the Application Identity service, and device management before any
policy change. It stops when those prerequisites are absent and never directs a
Home user to install unofficial management-console hacks.

## Tested-example provenance

The original observed case used an **LG 45GR95QE-B** with the Microsoft Store
product **LG Monitor App Installer**, whose tested package name was
`LGElectronics.LGMonitorApp`, alongside the separate LG OnScreen Control desktop
application. That case is provenance for the tested package and workflow; it is
not a claim that every LG monitor uses the same package or delivery path.

## Safety and evidence boundaries

Package or application removal requires reinstallation to undo; a policy backup
does not reinstall software. AppLocker mistakes can block legitimate packaged
apps. The AppLocker workflow is limited to a personally managed computer using
local or Group Policy policy. Its PowerShell tools do not manage AppLocker CSP
and can report CSP effective policy incorrectly. Microsoft also documents that
the protected Application Identity service cannot be returned to Manual with
`sc.exe`; the optional path therefore requires a system backup and explicit
acceptance of that service-state trade-off.

The guides distinguish documentation from local evidence:

- Microsoft and LG documentation establishes documented behavior and scope.
- Command output and real-workload tests on the target PC establish the current
  local result.
- A predicted AppLocker result is not proof of a real block.
- A prior observation is not a current guarantee.

Revalidate after Windows feature or security updates, LG firmware or software
changes, Defender platform changes, or a change in delivery path. Public reports
must contain sanitized summaries only. Never publish raw recovery exports,
event logs, usernames, hostnames, serial numbers, account identifiers,
credentials, tokens, or unredacted diagnostic bundles.

## Repository contents

- `LG_Monitor_Companion_Software_Mitigation_Windows_11_Home_v1.0.0.pdf` -
  action-first reader guide for Windows 11 Home.
- `LG_Monitor_Companion_Software_Mitigation_Windows_11_Pro_v1.0.0.pdf` -
  action-first reader guide for Windows 11 Pro.
- `SHA256SUMS.txt` - release-artifact checksums.
- `docs/LG_Monitor_Companion_Software_Windows_11_Home.md` and
  `docs/LG_Monitor_Companion_Software_Windows_11_Pro.md` - accessible,
  edition-specific companions.
- `build_lg_monitor_companion_software_guides.py` - shared deterministic
  ReportLab source for both editions.
- `scripts/validate_pdf.py` - read-only release, disclosure, navigation, font,
  link, and required-content checks.
- `requirements.txt` - pinned Python build dependencies.
- `SECURITY.md` - private security-reporting and evidence-handling rules.
- `ACCESSIBILITY.md` - accessible-use information and manual review gates.
- `CONTRIBUTING.md` - controlled-author contribution process.
- `LICENSE.md` - controlled-author mixed-license terms.
- `THIRD_PARTY_NOTICES.md` - dependency notices.

## Rebuild and validate

The PDFs use standard PDF Base 14 fonts and a deterministic ReportLab build. The
release workflow is pinned to Python 3.12.13. From a clean virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --disable-pip-version-check --only-binary=:all: --require-hashes -r requirements.txt
python .\build_lg_monitor_companion_software_guides.py
python .\scripts\validate_pdf.py .\LG_Monitor_Companion_Software_Mitigation_Windows_11_Home_v1.0.0.pdf --source .\build_lg_monitor_companion_software_guides.py --source .\docs\LG_Monitor_Companion_Software_Windows_11_Home.md
python .\scripts\validate_pdf.py .\LG_Monitor_Companion_Software_Mitigation_Windows_11_Pro_v1.0.0.pdf --source .\build_lg_monitor_companion_software_guides.py --source .\docs\LG_Monitor_Companion_Software_Windows_11_Pro.md
```

A successful build is not sufficient. Before release, render and inspect every
page of both PDFs, test the PowerShell blocks for syntax, review both Markdown
companions, run the validator against each edition, and confirm that repeated
clean builds are byte-identical.

## Reporting problems

- Use a GitHub issue for non-sensitive factual errors, source corrections,
  accessibility problems, improvement proposals, and reproducible build
  defects.
- Use
  [GitHub private vulnerability reporting](https://github.com/Amyashi/lg-monitor-companion-software-mitigation/security/advisories/new)
  for a vulnerability in this repository, its automation, or its generated
  artifacts.
- Never attach unredacted diagnostics or other sensitive evidence to either
  channel.

## Release policy

A public release must:

1. pass the release validator against both editions from a clean tracked tree;
2. rebuild both PDFs in the documented environment and match the committed
   artifacts byte for byte;
3. receive a complete visual review plus the keyboard and screen-reader spot
   check in `ACCESSIBILITY.md`;
4. contain no account, device, network, recovery, or diagnostic evidence;
5. keep the builder, PDFs, accessible companions, citation metadata,
   repository guidance, and changelog synchronized; and
6. be published from the reviewed `v1.0.0` tag.

## Authorship

**Author:** Amyashi

This is a controlled-author publication. Acceptance, wording, release timing,
and editorial decisions remain with Amyashi.

## Copyright, permissions, and trademarks

The guide materials, generated PDFs, and accessible companions are licensed
under the
[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](LICENSE.md#guide-materials).

The build, validation, workflow, configuration, and automation code is not open
source. It is all rights reserved, with limited permission to download and
execute unmodified copies for personal, noncommercial reproduction and
validation of the unmodified guide materials. The mixed-content builder and
contribution-only exception are governed by [LICENSE.md](LICENSE.md).

Third-party components and product names remain subject to their own licenses
and rights. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
