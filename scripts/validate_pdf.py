"""Read-only public-release checks for the generated LG mitigation runbooks.

The validator never rewrites a PDF or its accessible companion. It checks the
two-edition release identity, navigation, unsafe active content, attachments,
links, font resources, required and forbidden edition content, metadata,
accessible-companion parity, and accidental private-session or workstation
disclosures.
"""

from __future__ import annotations

import argparse
import ipaddress
import re
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from pypdf import PdfReader
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject, StreamObject


ROOT = Path(__file__).resolve().parents[1]
BUILDER_SOURCE = "build_lg_monitor_companion_software_guides.py"
EXPECTED_AUTHOR = "Amyashi"
EXPECTED_LANGUAGE = "en-US"

COMMON_REQUIRED_TEXT = (
    "LG Monitor Companion-Software",
    "DOCUMENTED EXAMPLE AND ELIGIBILITY",
    "LG 45GR95QE-B",
    "LG Monitor App Installer",
    "9PM9N6F47JB8",
    "LGElectronics.LGMonitorApp",
    "LG Electronics Inc.",
    "Never substitute another package name",
    "Windows PowerShell 5.1",
    "RegisteredPackageCount",
    "ProvisionedPackageCount",
    "restart once",
    "Stop here",
    "STEP 2A - DECIDE ABOUT LG ONSCREEN CONTROL",
    "firmware update is running",
    "Independent, unofficial and unaffiliated",
    "not endorsed by LG or Microsoft",
    "CC BY-NC-ND 4.0",
    "Author: Amyashi",
    "CN=4A5401D9-32C2-486E-A8CB-EFECB124AF89",
    "cfnzzhwkr8z5w",
    "LGElectronics.LGMonitorApp_cfnzzhwkr8z5w",
    "PUA-Audit-Started.clixml",
    "FreshScanCompleted = True",
)

COMPANION_COMMON_REQUIRED_TEXT = (
    "LG Monitor Companion Software: Cleanup and Recurrence Mitigation",
    "Documented example and exact target",
    "LG 45GR95QE-B",
    "LG Monitor App Installer",
    "9PM9N6F47JB8",
    "LGElectronics.LGMonitorApp",
    "LG Electronics Inc.",
    "Never substitute another package name",
    "Windows PowerShell 5.1",
    "RegisteredPackageCount",
    "ProvisionedPackageCount",
    "Restart once and verify",
    "Stop when every core result passes",
    "OnScreen Control is not the Store package",
    "no LG monitor firmware update is running",
    "independently authored, unofficial, and unaffiliated",
    "Neither LG nor Microsoft has endorsed it",
    "CC BY-NC-ND 4.0",
    "Author: Amyashi",
    "CN=4A5401D9-32C2-486E-A8CB-EFECB124AF89",
    "cfnzzhwkr8z5w",
    "LGElectronics.LGMonitorApp_cfnzzhwkr8z5w",
    "PUA-Audit-Started.clixml",
    "FreshScanCompleted = True",
)

COMMON_REQUIRED_LINK_FRAGMENTS = (
    "apps.microsoft.com/detail/9pm9n6f47jb8",
    "lg.com/us/support",
    "lg.com/us/support/help-library/lg-monitor-onscreen-control",
    "learn.microsoft.com/en-us/powershell/module/appx/get-appxpackage",
    "learn.microsoft.com/en-us/powershell/module/appx/remove-appxpackage",
    "learn.microsoft.com/en-us/powershell/module/dism/get-appxprovisionedpackage",
    "learn.microsoft.com/en-us/powershell/module/dism/remove-appxprovisionedpackage",
)

EDITION_SPECS = {
    "home": {
        "filename": (
            "LG_Monitor_Companion_Software_Mitigation_"
            "Windows_11_Home_v1.0.0.pdf"
        ),
        "title": (
            "LG Monitor Companion-Software Cleanup and Recurrence Mitigation - "
            "Windows 11 Home Edition"
        ),
        "edition_name": "Windows 11 Home",
        # The Home runbook should remain compact while allowing normal
        # pagination changes caused by accessible layout improvements.
        "min_pages": 7,
        "max_pages": 12,
        "min_https_links": 8,
        "accessible_doc": (
            "docs/LG_Monitor_Companion_Software_Windows_11_Home.md"
        ),
        "required_text": (
            "Windows 11 Home Edition",
            "SystemPropertiesHardware.exe",
            "Device Installation Settings",
            "Device-Installation-Settings-Before.clixml",
            "Home control is a broader, weaker user preference",
            "Do not install third-party Group Policy or Local Security Policy hacks",
            "not been field-tested on a Windows 11 Home machine",
        ),
        "companion_required_text": (
            "Windows 11 Home runbook",
            "SystemPropertiesHardware.exe",
            "Device Installation Settings",
            "broader, weaker Home preference",
            "Do not force the Pro-only policy onto Home",
            "third-party policy-editor hacks",
            "not been field-tested on a Windows 11 Home machine",
        ),
        # The Home artifact may explain the boundary at a high level, but it
        # must not carry the Pro GPO path or actionable AppLocker procedure.
        "forbidden_text": (
            "gpedit.msc",
            "secpol.msc",
            "gpupdate /target:computer /force",
            "PreventDeviceMetadataFromNetwork",
            "Computer Configuration > Administrative Templates",
            "Get-AppLockerPolicy",
            "Set-AppLockerPolicy",
            "Test-AppLockerPolicy",
            "New-AppLockerPolicy",
            "AppIDSvc",
            "Application Identity service",
            "REPLACE LOCAL APPLOCKER POLICY",
            "EnforcedTargetDenyEventCount",
            "STOP: no real target deny event was found.",
            "8022,8025",
        ),
        "required_link_fragments": (
            "support.microsoft.com/en-us/windows/experience/"
            "system-configuration-tools-in-windows",
        ),
    },
    "pro": {
        "filename": (
            "LG_Monitor_Companion_Software_Mitigation_"
            "Windows_11_Pro_v1.0.0.pdf"
        ),
        "title": (
            "LG Monitor Companion-Software Cleanup and Recurrence Mitigation - "
            "Windows 11 Pro Edition"
        ),
        "edition_name": "Windows 11 Pro",
        # The optional, gated AppLocker procedure legitimately makes the Pro
        # edition longer than Home; avoid pinning the check to one page count.
        "min_pages": 9,
        "max_pages": 15,
        "min_https_links": 16,
        "accessible_doc": (
            "docs/LG_Monitor_Companion_Software_Windows_11_Pro.md"
        ),
        "required_text": (
            "Windows 11 Pro Edition",
            "gpedit.msc",
            "Prevent automatic download of applications associated with device metadata",
            "PreventDeviceMetadataFromNetwork",
            "MetadataPolicyValue = 1",
            "Optional AppLocker A - back up, inspect, start in Audit only",
            "Optional AppLocker B - create the exact deny and test it",
            "Optional AppLocker C - enforce, smoke-test, then remove",
            "AppLocker CSP",
            "secpol.msc",
            "Packaged app Rules",
            "Audit only",
            "Do not configure EXE, MSI, Script or DLL collections",
            "Block LG Monitor App Installer",
            "Get-AppLockerPolicy",
            "Test-AppLockerPolicy",
            "Set-AppLockerPolicy",
            "Local-Before.xml",
            "Effective-Before.xml",
            "AppIDSvc",
            "DeniedByDefault",
            "EnforcedTargetDenyEventCount",
            "STOP: no real target deny event was found.",
            "8022,8025",
            "-WhatIf",
            "REPLACE LOCAL APPLOCKER POLICY",
            "delete only Block LG Monitor App Installer",
        ),
        "companion_required_text": (
            "Windows 11 Pro runbook",
            "gpedit.msc",
            "Prevent automatic download of applications associated with device metadata",
            "PreventDeviceMetadataFromNetwork",
            "MetadataPolicyValue = 1",
            "Optional AppLocker - decision, backup, and Audit only",
            "Optional AppLocker - create the exact deny and test",
            "Optional AppLocker - enforce and prove the result",
            "AppLocker is not managed through MDM/CSP",
            "secpol.msc",
            "Packaged app Rules",
            "Audit only",
            "Leave EXE, MSI, Script, and DLL collections unchanged",
            "Block LG Monitor App Installer",
            "Get-AppLockerPolicy",
            "Test-AppLockerPolicy",
            "Set-AppLockerPolicy",
            "Local-Before.xml",
            "Effective-Before.xml",
            "AppIDSvc",
            "DeniedByDefault",
            "EnforcedTargetDenyEventCount",
            "8022,8025",
            "-WhatIf",
            "REPLACE LOCAL APPLOCKER POLICY",
            "Delete only",
        ),
        "forbidden_text": (
            "DO THIS - WINDOWS 11 HOME",
            "SystemPropertiesHardware.exe",
        ),
        "required_link_fragments": (
            "learn.microsoft.com/en-us/windows/client-management/mdm/"
            "policy-csp-deviceinstallation",
            "learn.microsoft.com/en-us/windows/security/application-security/"
            "application-control/app-control-for-business/applocker/"
            "requirements-to-use-applocker",
            "learn.microsoft.com/en-us/powershell/module/applocker/"
            "get-applockerpolicy",
            "learn.microsoft.com/en-us/powershell/module/applocker/"
            "set-applockerpolicy",
            "learn.microsoft.com/en-us/powershell/module/applocker/"
            "test-applockerpolicy",
            "learn.microsoft.com/en-us/windows/security/application-security/"
            "application-control/app-control-for-business/applocker/"
            "using-event-viewer-with-applocker",
        ),
    },
}

EXPECTED_REPOSITORY_PDFS = frozenset(
    spec["filename"] for spec in EDITION_SPECS.values()
)
EXPECTED_ACCESSIBLE_DOCS = frozenset(
    spec["accessible_doc"] for spec in EDITION_SPECS.values()
)
LEGACY_RELEASE_ARTIFACTS = frozenset(
    {
        "LG_45GR95QE-B_Windows_Hardening_Guide_v1.0.0.pdf",
        "docs/ACCESSIBLE_GUIDE.md",
        "build_lg_45gr95qe_b_hardening_guide.py",
    }
)
APPROVED_LINK_HOSTS = frozenset(
    {
        "apps.microsoft.com",
        "learn.microsoft.com",
        "support.microsoft.com",
        "www.lg.com",
        "www.microsoft.com",
        "www.w3.org",
    }
)
APPROVED_BASE14_FONTS = frozenset(
    {
        "/Courier",
        "/Courier-Bold",
        "/Courier-BoldOblique",
        "/Courier-Oblique",
        "/Helvetica",
        "/Helvetica-Bold",
        "/Helvetica-BoldOblique",
        "/Helvetica-Oblique",
    }
)
MAX_XMP_BYTES = 1_000_000

FORBIDDEN_PHRASES = (
    "work " + "sol",
    "chat" + "gpt",
    "co" + "dex",
    "referenced " + "chat",
    "prior " + "session",
    "prior " + "conversation",
    "blocking lg " + "monitor apps",
    "lyo" + "ko",
    "[]" + " close",
    "discord" + ".gg/",
    "discord.com/" + "invite",
    "support" + "@",
    "lg-45gr95qe-b-" + "windows-hardening",
)

TRACKED_TEXT_SUFFIXES = frozenset(
    {".cff", ".in", ".md", ".py", ".txt", ".yaml", ".yml"}
)
TRACKED_TEXT_NAMES = frozenset({".gitattributes", ".gitignore"})
TRACKED_TEXT_EXCLUSIONS = frozenset({"licenses/REPORTLAB.txt"})

DISCLOSURE_PATTERNS = (
    (
        "a private Windows user-profile path",
        re.compile(
            r"(?i)[a-z]:[\\/]+(?:users|documents and settings)[\\/]+[^\\/\s]+"
        ),
    ),
    ("a private Unix user-profile path", re.compile(r"(?i)/(?:home|users)/[^/\s]+")),
    (
        "a private UNC path",
        re.compile(r"\\\\[a-z0-9._-]+[\\/]+[^\s<>]+", re.IGNORECASE),
    ),
    (
        "a labeled workstation or host identifier",
        re.compile(
            r"(?i)\b(?:pc|computer|host(?:name)?)\s*:\s*"
            r"(?!windows\b|system\b)[a-z0-9][a-z0-9._-]{1,62}\b"
        ),
    ),
    (
        "an email address",
        re.compile(
            r"(?i)\b[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
            r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
            r"[a-z]{2,63}\b"
        ),
    ),
    (
        "a Discord invite",
        re.compile(
            r"(?i)\b(?:https?://)?(?:www\.)?"
            r"(?:discord\.gg|discord(?:app)?\.com/invite)/"
            r"[a-z0-9-]+\b"
        ),
    ),
    (
        "a MAC address",
        re.compile(
            r"(?i)(?<![0-9a-f])"
            r"(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}"
            r"(?![0-9a-f])"
        ),
    ),
    (
        "a user- or machine-specific Windows SID",
        re.compile(r"\bS-1-5-21-(?:\d+-){2}\d+-\d+\b", re.IGNORECASE),
    ),
    (
        "a Discord user-profile identifier",
        re.compile(
            r"(?i)\bdiscord(?:app)?\.com/" + r"users/\d{15,20}\b"
        ),
    ),
)

IPV4_CANDIDATE_PATTERN = re.compile(
    r"(?<![\w.])"
    r"(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)"
    r"(?![\w.])"
)
APPROVED_NON_ADDRESS_IPV4_LITERALS = frozenset({"0.0.0.0", "9.43.0.0"})
IPV6_CANDIDATE_PATTERN = re.compile(
    r"(?i)(?<![0-9a-z_:])"
    r"(?:[0-9a-f]{0,4}:){2,7}[0-9a-f]{0,4}"
    r"(?![0-9a-z_:])"
)


def dereference(value: Any) -> Any:
    """Resolve a pypdf indirect object without assuming one is present."""

    return value.get_object() if isinstance(value, IndirectObject) else value


def dictionary(value: Any) -> DictionaryObject:
    """Return a resolved PDF dictionary or an empty one."""

    resolved = dereference(value)
    return resolved if isinstance(resolved, DictionaryObject) else DictionaryObject()


def array(value: Any) -> Iterable[Any]:
    """Return a resolved PDF array as an iterable."""

    resolved = dereference(value)
    return resolved if isinstance(resolved, ArrayObject) else ()


def count_outline_items(items: Any) -> int:
    """Count outline destinations, including nested outline lists."""

    if not isinstance(items, list):
        return 0
    total = 0
    for item in items:
        if isinstance(item, list):
            total += count_outline_items(item)
        else:
            total += 1
    return total


def action_contains_javascript(action_value: Any, seen: set[int] | None = None) -> bool:
    """Detect JavaScript in an action dictionary or chained /Next actions."""

    action = dictionary(action_value)
    if not action:
        return False
    if seen is None:
        seen = set()
    marker = id(action)
    if marker in seen:
        return False
    seen.add(marker)

    if str(action.get("/S", "")) == "/JavaScript" or action.get("/JS") is not None:
        return True
    next_action = dereference(action.get("/Next"))
    if isinstance(next_action, ArrayObject):
        return any(action_contains_javascript(item, seen) for item in next_action)
    return action_contains_javascript(next_action, seen) if next_action is not None else False


def inspect_outline_actions(catalog: DictionaryObject) -> list[str]:
    """Require direct, internal outline destinations and reject action dictionaries."""

    failures: list[str] = []
    outlines = dictionary(catalog.get("/Outlines"))
    seen: set[tuple[Any, ...]] = set()

    def walk(item_value: Any, depth: int = 0) -> None:
        if depth > 64:
            failures.append("outline nesting exceeds the safety limit")
            return

        current_value = item_value
        while current_value is not None:
            marker = (
                ("indirect", current_value.idnum, current_value.generation)
                if isinstance(current_value, IndirectObject)
                else ("direct", id(dereference(current_value)))
            )
            current = dictionary(current_value)
            if not current:
                return
            if marker in seen:
                failures.append("outline tree contains a cycle")
                return
            seen.add(marker)

            if current.get("/AA") is not None:
                failures.append("outline item contains additional actions (/AA)")

            if current.get("/A") is not None:
                failures.append("outline item contains an action dictionary (/A)")

            destination = dereference(current.get("/Dest"))
            if not isinstance(destination, ArrayObject) or len(destination) < 2:
                failures.append("outline item lacks a valid direct destination array")

            child = current.get("/First")
            if child is not None:
                walk(child, depth + 1)
            current_value = current.get("/Next")

    first = outlines.get("/First")
    if first is not None:
        walk(first)
    return failures


def normalized_text(reader: PdfReader) -> str:
    """Extract and normalize searchable document text."""

    page_text = []
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            page_text.append(page.extract_text() or "")
        except Exception as exc:  # pypdf raises several parser-specific types
            raise ValueError(f"page {page_number} text extraction failed: {exc}") from exc
    return re.sub(r"\s+", " ", "\n".join(page_text)).strip()


def disclosure_failures(surface: str, label: str) -> list[str]:
    """Report disclosure classes without echoing sensitive matched content."""

    failures: list[str] = []
    scrubbed = surface
    folded = scrubbed.casefold()
    if any(phrase.casefold() in folded for phrase in FORBIDDEN_PHRASES):
        failures.append(f"{label} contains forbidden private-session wording")
    for description, pattern in DISCLOSURE_PATTERNS:
        if pattern.search(scrubbed):
            failures.append(f"{label} contains {description}")
    for match in IPV4_CANDIDATE_PATTERN.finditer(scrubbed):
        if match.group(0) not in APPROVED_NON_ADDRESS_IPV4_LITERALS:
            failures.append(f"{label} contains an IPv4 address")
            break
    for match in IPV6_CANDIDATE_PATTERN.finditer(scrubbed):
        candidate = match.group(0)
        if candidate == "::":
            continue
        try:
            if isinstance(ipaddress.ip_address(candidate), ipaddress.IPv6Address):
                failures.append(f"{label} contains an IPv6 address")
                break
        except ValueError:
            continue
    return failures


def inspect_xmp_metadata(
    catalog: DictionaryObject,
) -> tuple[list[str], list[str]]:
    """Decode and disclosure-scan the catalog XMP metadata stream, if present."""

    metadata_value = catalog.get("/Metadata")
    if metadata_value is None:
        return [], ["XMP metadata: absent"]

    try:
        metadata = dereference(metadata_value)
    except Exception as exc:
        return [
            f"XMP metadata could not be resolved: {type(exc).__name__}"
        ], []
    if not isinstance(metadata, StreamObject):
        return ["catalog /Metadata is not a PDF stream"], []

    raw_data = getattr(metadata, "_data", b"")
    if not isinstance(raw_data, bytes):
        return ["XMP metadata raw stream is not bytes"], []
    if len(raw_data) > MAX_XMP_BYTES:
        return [
            f"compressed XMP metadata exceeds {MAX_XMP_BYTES:,} bytes"
        ], []

    try:
        decoded_data = metadata.get_data()
    except Exception as exc:
        return [f"XMP metadata decoding failed: {type(exc).__name__}"], []
    if not isinstance(decoded_data, bytes):
        return ["decoded XMP metadata is not bytes"], []
    if len(decoded_data) > MAX_XMP_BYTES:
        return [
            f"decoded XMP metadata exceeds {MAX_XMP_BYTES:,} bytes"
        ], []

    encoding = (
        "utf-16"
        if decoded_data.startswith((b"\xff\xfe", b"\xfe\xff"))
        else "utf-8-sig"
    )
    try:
        xmp_text = decoded_data.decode(encoding, errors="strict")
    except UnicodeError as exc:
        return [
            f"XMP metadata is not valid UTF-8/UTF-16 text: {type(exc).__name__}"
        ], []

    return disclosure_failures(xmp_text, "PDF XMP metadata"), [
        f"XMP metadata disclosure scan: {len(xmp_text):,} characters"
    ]


def inspect_font_resources(reader: PdfReader) -> tuple[list[str], list[str]]:
    """Allow only unembedded Base-14 Helvetica and Courier font resources."""

    failures: list[str] = []
    observed_fonts: set[str] = set()
    seen_resources: set[tuple[Any, ...]] = set()
    seen_fonts: set[tuple[Any, ...]] = set()
    font_file_keys = ("/FontFile", "/FontFile2", "/FontFile3")

    def object_marker(value: Any, resolved: Any) -> tuple[Any, ...]:
        if isinstance(value, IndirectObject):
            return ("indirect", value.idnum, value.generation)
        return ("direct", id(resolved))

    def inspect_descriptor(descriptor_value: Any, context: str) -> None:
        descriptor = dictionary(descriptor_value)
        for key in font_file_keys:
            if descriptor.get(key) is not None:
                failures.append(f"{context} embeds a font through {key}")

    def inspect_font(font_value: Any, context: str) -> None:
        font = dictionary(font_value)
        marker = object_marker(font_value, font)
        if marker in seen_fonts:
            return
        seen_fonts.add(marker)
        base_font = str(font.get("/BaseFont", "")).strip()
        subtype = str(font.get("/Subtype", "")).strip()
        observed_fonts.add(base_font or "(missing)")

        if base_font not in APPROVED_BASE14_FONTS:
            failures.append(
                f"{context} uses non-approved font {base_font or '(missing)'!r}"
            )
        if subtype != "/Type1":
            failures.append(
                f"{context} uses unsupported font subtype "
                f"{subtype or '(missing)'!r}"
            )

        inspect_descriptor(font.get("/FontDescriptor"), context)
        for descendant_value in array(font.get("/DescendantFonts")):
            descendant = dictionary(descendant_value)
            inspect_descriptor(descendant.get("/FontDescriptor"), context)

    def walk_resources(resources_value: Any, context: str) -> None:
        resources = dictionary(resources_value)
        marker = object_marker(resources_value, resources)
        if marker in seen_resources:
            return
        seen_resources.add(marker)

        fonts = dictionary(resources.get("/Font"))
        for resource_name, font_value in fonts.items():
            inspect_font(font_value, f"{context} font {resource_name}")

        xobjects = dictionary(resources.get("/XObject"))
        for resource_name, xobject_value in xobjects.items():
            xobject = dictionary(xobject_value)
            if str(xobject.get("/Subtype", "")) == "/Form":
                walk_resources(
                    xobject.get("/Resources"),
                    f"{context} form XObject {resource_name}",
                )

        patterns = dictionary(resources.get("/Pattern"))
        for resource_name, pattern_value in patterns.items():
            pattern = dictionary(pattern_value)
            if pattern.get("/Resources") is not None:
                walk_resources(
                    pattern.get("/Resources"),
                    f"{context} pattern {resource_name}",
                )

    try:
        for page_number, page in enumerate(reader.pages, start=1):
            walk_resources(page.get("/Resources"), f"page {page_number}")
    except Exception as exc:
        failures.append(f"font-resource inspection failed: {type(exc).__name__}")

    # Check every indirect object, including unreachable objects, so an embedded
    # font stream cannot remain hidden outside the current page resource graph.
    references = {
        (idnum, generation)
        for generation, entries in reader.xref.items()
        if generation != 65535
        for idnum in entries
        if idnum != 0
    }
    references.update((idnum, 0) for idnum in reader.xref_objStm)

    def inspect_direct_values(value: Any, context: str, seen: set[int]) -> None:
        resolved = dereference(value)
        if isinstance(resolved, (DictionaryObject, ArrayObject)):
            marker = id(resolved)
            if marker in seen:
                return
            seen.add(marker)
        if isinstance(resolved, DictionaryObject):
            for key in font_file_keys:
                if resolved.get(key) is not None:
                    failures.append(f"{context} contains embedded font key {key}")
            for child in resolved.values():
                if not isinstance(child, IndirectObject):
                    inspect_direct_values(child, context, seen)
        elif isinstance(resolved, ArrayObject):
            for child in resolved:
                if not isinstance(child, IndirectObject):
                    inspect_direct_values(child, context, seen)

    for idnum, generation in sorted(references):
        try:
            indirect = IndirectObject(idnum, generation, reader)
            inspect_direct_values(
                indirect.get_object(),
                f"PDF object {idnum} {generation}",
                set(),
            )
        except Exception as exc:
            failures.append(
                f"PDF object {idnum} {generation} could not be inspected for "
                f"embedded fonts: {type(exc).__name__}"
            )

    checks = [
        "font resources: "
        + (", ".join(sorted(observed_fonts)) if observed_fonts else "(none)")
    ]
    if not observed_fonts:
        failures.append("PDF exposes no page font resources")
    return failures, checks


def validate_source_disclosures(source_path: Path) -> tuple[list[str], list[str]]:
    """Scan a release source file for the same disclosure classes as the PDF."""

    label = f"source {source_path.name!r}"
    if not source_path.is_file():
        return [f"{label} is missing or is not a regular file"], []
    try:
        source_text = source_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{label} could not be read as UTF-8: {type(exc).__name__}"], []
    return disclosure_failures(source_text, label), [f"{label} disclosure scan: clean"]


def search_surface(value: str) -> str:
    """Normalize prose for stable required/forbidden content checks."""

    return re.sub(
        r"\s+",
        " ",
        value.replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-"),
    ).strip().casefold()


def content_contract_failures(
    text: str,
    label: str,
    spec: dict[str, Any],
    *,
    companion: bool = False,
) -> list[str]:
    """Check the shared and edition-specific reader-content contract."""

    failures: list[str] = []
    folded = search_surface(text)
    required_text = (
        COMPANION_COMMON_REQUIRED_TEXT
        + tuple(spec["companion_required_text"])
        if companion
        else COMMON_REQUIRED_TEXT + tuple(spec["required_text"])
    )
    for required in required_text:
        if search_surface(required) not in folded:
            failures.append(f"{label} is missing required text: {required!r}")
    for forbidden in spec["forbidden_text"]:
        if search_surface(forbidden) in folded:
            failures.append(
                f"{label} contains content forbidden for "
                f"{spec['edition_name']}: {forbidden!r}"
            )
    return failures


HTTPS_URL_PATTERN = re.compile(r"https://[^\s<>\[\]\"']+", re.IGNORECASE)


def extract_https_urls(text: str) -> set[str]:
    """Extract HTTPS URLs from a Markdown or plain-text source."""

    links: set[str] = set()
    for match in HTTPS_URL_PATTERN.finditer(text):
        # Markdown destinations and prose commonly leave closing punctuation
        # adjacent to a URL. None of the approved sources need these suffixes.
        candidate = match.group(0).rstrip(").,;:")
        parsed = urlsplit(candidate)
        if parsed.scheme.lower() == "https" and parsed.netloc:
            links.add(candidate)
    return links


def validate_link_contract(
    links: Iterable[str],
    label: str,
    spec: dict[str, Any],
) -> tuple[list[str], list[str]]:
    """Validate link authorities and required authoritative-source coverage."""

    failures: list[str] = []
    normalized_links: set[str] = set()
    for uri in links:
        parsed = urlsplit(uri)
        try:
            port = parsed.port
        except ValueError:
            failures.append(f"{label} contains a malformed HTTPS-link port")
            continue
        hostname = (parsed.hostname or "").rstrip(".").lower()
        if (
            parsed.scheme.lower() != "https"
            or hostname not in APPROVED_LINK_HOSTS
            or parsed.username is not None
            or parsed.password is not None
            or port is not None
        ):
            failures.append(
                f"{label} contains a disallowed or malformed external-link authority"
            )
            continue
        normalized_links.add(uri.casefold())

    if len(normalized_links) < spec["min_https_links"]:
        failures.append(
            f"{label} requires at least {spec['min_https_links']} unique HTTPS "
            f"source links; found {len(normalized_links)}"
        )

    required_fragments = (
        COMMON_REQUIRED_LINK_FRAGMENTS
        + tuple(spec["required_link_fragments"])
    )
    for fragment in required_fragments:
        if not any(fragment.casefold() in uri for uri in normalized_links):
            failures.append(
                f"{label} is missing required authoritative link fragment: "
                f"{fragment!r}"
            )

    return failures, [
        f"{label} unique approved HTTPS links: {len(normalized_links)}"
    ]


def validate_accessible_companion(
    path: Path,
    spec: dict[str, Any],
) -> tuple[list[str], list[str]]:
    """Check the edition-specific accessible Markdown companion."""

    label = f"{spec['edition_name']} accessible companion"
    failures: list[str] = []
    checks: list[str] = []
    if path.as_posix().casefold() != (ROOT / spec["accessible_doc"]).as_posix().casefold():
        failures.append(
            f"{label} must use repository path {spec['accessible_doc']!r}"
        )
    if not path.is_file():
        return [f"{label} is missing: {path}"], checks
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [
            f"{label} could not be read as UTF-8: {type(exc).__name__}"
        ], checks

    failures.extend(content_contract_failures(text, label, spec, companion=True))
    failures.extend(disclosure_failures(text, label))
    link_failures, link_checks = validate_link_contract(
        extract_https_urls(text),
        label,
        spec,
    )
    failures.extend(link_failures)
    checks.extend(link_checks)
    checks.append(f"{label} text: {len(text):,} characters")
    return failures, checks


def inspect_active_content_and_links(reader: PdfReader) -> tuple[list[str], list[str]]:
    """Return unsafe-content findings and external URI links."""

    failures: list[str] = []
    links: list[str] = []
    catalog = dictionary(reader.trailer.get("/Root"))
    names = dictionary(catalog.get("/Names"))

    if catalog.get("/OpenAction") is not None:
        failures.append("catalog contains /OpenAction")
    if catalog.get("/AA") is not None:
        failures.append("catalog contains additional actions (/AA)")
    if catalog.get("/AcroForm") is not None:
        failures.append("catalog contains an AcroForm")
    if catalog.get("/AF") is not None:
        failures.append("catalog contains associated files (/AF)")
    if names.get("/JavaScript") is not None:
        failures.append("name tree contains JavaScript")
    if names.get("/EmbeddedFiles") is not None:
        failures.append("name tree contains embedded files")
    if catalog.get("/Collection") is not None:
        failures.append("catalog defines a PDF portfolio/collection")
    failures.extend(inspect_outline_actions(catalog))

    for page_number, page in enumerate(reader.pages, start=1):
        page_object = dictionary(page)
        if page_object.get("/AA") is not None:
            failures.append(f"page {page_number} contains additional actions (/AA)")
        if page_object.get("/AF") is not None:
            failures.append(f"page {page_number} contains associated files (/AF)")

        for annotation_ref in array(page_object.get("/Annots")):
            annotation = dictionary(annotation_ref)
            subtype = str(annotation.get("/Subtype", ""))
            if subtype != "/Link":
                failures.append(
                    f"page {page_number} contains unsupported annotation subtype "
                    f"{subtype or '(missing)'!r}"
                )
            if subtype == "/FileAttachment":
                failures.append(f"page {page_number} contains a file attachment")
            if annotation.get("/AA") is not None:
                failures.append(
                    f"page {page_number} contains an annotation with additional actions"
                )
            file_spec = dictionary(annotation.get("/FS"))
            if annotation.get("/EF") is not None or file_spec.get("/EF") is not None:
                failures.append(f"page {page_number} annotation embeds a file stream")

            action = dictionary(annotation.get("/A"))
            if action_contains_javascript(action):
                failures.append(f"page {page_number} contains a JavaScript action")
            if action.get("/Next") is not None:
                failures.append(
                    f"page {page_number} contains an annotation with a chained action"
                )

            action_type = str(action.get("/S", ""))
            if action_type and action_type not in {"/URI", "/GoTo"}:
                failures.append(
                    f"page {page_number} contains unsupported action type {action_type!r}"
                )

            uri_value = action.get("/URI")
            if uri_value is None:
                continue
            uri = str(dereference(uri_value)).strip()
            parsed = urlsplit(uri)
            if parsed.scheme.lower() != "https" or not parsed.netloc:
                failures.append(
                    f"page {page_number} has a non-HTTPS or malformed external link "
                    "(URI redacted)"
                )
                continue
            try:
                port = parsed.port
            except ValueError:
                failures.append(
                    f"page {page_number} has a malformed external-link port "
                    "(URI redacted)"
                )
                continue
            hostname = (parsed.hostname or "").rstrip(".").lower()
            if (
                hostname not in APPROVED_LINK_HOSTS
                or parsed.username is not None
                or parsed.password is not None
                or port is not None
            ):
                failures.append(
                    f"page {page_number} has a disallowed external-link authority "
                    "(URI and host redacted)"
                )
                continue
            links.append(uri)

    return failures, links


def validate_tracked_pdf_set(root: Path) -> tuple[list[str], list[str]]:
    """Require the Git index to contain exactly the intended release PDFs."""

    failures: list[str] = []
    checks: list[str] = []
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached", "--", "*.pdf"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        return [
            "could not enumerate tracked PDFs with Git: "
            f"{type(exc).__name__}"
        ], checks

    tracked = {
        Path(line.strip()).as_posix()
        for line in result.stdout.splitlines()
        if line.strip()
    }
    missing = sorted(EXPECTED_REPOSITORY_PDFS - tracked)
    unexpected = sorted(tracked - EXPECTED_REPOSITORY_PDFS)
    if missing:
        failures.append(
            f"expected tracked release PDF(s) missing: {', '.join(missing)}"
        )
    if unexpected:
        failures.append(f"unexpected tracked PDF(s): {', '.join(unexpected)}")
    checks.append(
        "tracked PDFs: " + (", ".join(sorted(tracked)) if tracked else "(none)")
    )

    try:
        all_result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached", "-z"],
            check=True,
            capture_output=True,
        )
        all_tracked = {
            Path(item.decode("utf-8", errors="strict")).as_posix()
            for item in all_result.stdout.split(b"\0")
            if item
        }
    except (OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        failures.append(
            "could not enumerate the complete tracked release set: "
            f"{type(exc).__name__}"
        )
        return failures, checks

    missing_docs = sorted(EXPECTED_ACCESSIBLE_DOCS - all_tracked)
    if missing_docs:
        failures.append(
            "expected tracked accessible companion(s) missing: "
            + ", ".join(missing_docs)
        )
    if BUILDER_SOURCE not in all_tracked:
        failures.append(f"expected tracked builder is missing: {BUILDER_SOURCE}")
    legacy = sorted(LEGACY_RELEASE_ARTIFACTS & all_tracked)
    if legacy:
        failures.append(
            "legacy release artifact(s) remain tracked: " + ", ".join(legacy)
        )
    checks.append(
        "tracked accessible companions: "
        + ", ".join(sorted(EXPECTED_ACCESSIBLE_DOCS & all_tracked))
    )
    return failures, checks


def validate_tracked_text_disclosures(root: Path) -> tuple[list[str], list[str]]:
    """Scan every tracked release-text file without echoing matched content."""

    failures: list[str] = []
    checks: list[str] = []
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached", "-z"],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        return [f"could not enumerate tracked text files: {type(exc).__name__}"], checks

    try:
        tracked = [
            Path(item.decode("utf-8", errors="strict")).as_posix()
            for item in result.stdout.split(b"\0")
            if item
        ]
    except UnicodeError as exc:
        return [
            "could not decode tracked file names as UTF-8: "
            f"{type(exc).__name__}"
        ], checks
    candidates = [
        rel
        for rel in tracked
        if rel not in TRACKED_TEXT_EXCLUSIONS
        and (Path(rel).name in TRACKED_TEXT_NAMES or Path(rel).suffix in TRACKED_TEXT_SUFFIXES)
    ]
    for rel in candidates:
        source_failures, _source_checks = validate_source_disclosures(root / rel)
        failures.extend(source_failures)
    checks.append(
        f"tracked release-text disclosure scan: {len(candidates)} file(s), "
        f"{len(TRACKED_TEXT_EXCLUSIONS)} reviewed third-party exclusion(s)"
    )
    return failures, checks


def validate_index_worktree_alignment(root: Path) -> tuple[list[str], list[str]]:
    """Require tracked worktree content to match the Git index exactly."""

    try:
        result = subprocess.run(
            ["git", "-C", str(root), "diff", "--quiet", "--"],
            check=False,
            capture_output=True,
        )
    except OSError as exc:
        return [
            "could not compare the Git index with the tracked worktree: "
            f"{type(exc).__name__}"
        ], []

    if result.returncode == 0:
        return [], ["Git index and tracked worktree content: identical"]
    if result.returncode == 1:
        return [
            "tracked files differ between the Git index and worktree; "
            "stage the intended versions or restore unintended edits before "
            "treating this as a final release check"
        ], []
    return [
        "could not compare the Git index with the tracked worktree: "
        f"Git exited with status {result.returncode}"
    ], []


def edition_spec_for_path(pdf_path: Path) -> dict[str, Any] | None:
    """Return the edition contract selected by an exact release basename."""

    for spec in EDITION_SPECS.values():
        if pdf_path.name == spec["filename"]:
            return spec
    return None


def validate(
    pdf_path: Path,
    spec: dict[str, Any],
) -> tuple[list[str], list[str]]:
    """Validate one edition PDF and return findings and informational checks."""

    failures: list[str] = []
    checks: list[str] = []
    label = f"{spec['edition_name']} PDF"

    if pdf_path.name != spec["filename"]:
        failures.append(
            f"{label} expected filename {spec['filename']!r}, "
            f"got {pdf_path.name!r}"
        )
    if not pdf_path.is_file():
        return [f"{label} does not exist: {pdf_path}"], checks

    size = pdf_path.stat().st_size
    if size < 40_000:
        failures.append(f"{label} is unexpectedly small ({size:,} bytes)")
    if size > 20_000_000:
        failures.append(f"{label} is unexpectedly large ({size:,} bytes)")
    checks.append(f"{label} file size: {size:,} bytes")

    try:
        reader = PdfReader(pdf_path, strict=True)
    except Exception as exc:
        return failures + [
            f"{label} parsing failed in strict mode: {exc}"
        ], checks

    if reader.is_encrypted:
        failures.append(f"{label} is encrypted")

    page_count = len(reader.pages)
    if not spec["min_pages"] <= page_count <= spec["max_pages"]:
        failures.append(
            f"{label} expected {spec['min_pages']}-{spec['max_pages']} pages, "
            f"found {page_count}"
        )
    checks.append(f"{label} page count: {page_count}")

    metadata = reader.metadata or {}
    title = str(metadata.get("/Title", "")).strip()
    author = str(metadata.get("/Author", "")).strip()
    subject = str(metadata.get("/Subject", "")).strip()
    creator = str(metadata.get("/Creator", "")).strip()
    keywords = str(metadata.get("/Keywords", "")).strip()
    if title != spec["title"]:
        failures.append(
            f"{label} expected title {spec['title']!r}, got {title!r}"
        )
    if author != EXPECTED_AUTHOR:
        failures.append(
            f"{label} expected author {EXPECTED_AUTHOR!r}, got {author!r}"
        )
    if not subject:
        failures.append(f"{label} metadata is missing a subject")
    elif (
        spec["edition_name"].casefold() not in subject.casefold()
        or "LG Monitor App".casefold() not in subject.casefold()
    ):
        failures.append(
            f"{label} metadata subject does not identify its edition and "
            "LG Monitor App scope"
        )
    if EXPECTED_AUTHOR.casefold() not in creator.casefold():
        failures.append(f"{label} metadata creator does not identify the author")
    if (
        spec["edition_name"].casefold() not in keywords.casefold()
        or "LG Monitor App".casefold() not in keywords.casefold()
    ):
        failures.append(
            f"{label} metadata keywords do not identify its edition and scope"
        )
    checks.append(
        f"{label} metadata title/author: {title!r} / {author!r}"
    )

    catalog = dictionary(reader.trailer.get("/Root"))
    language = str(dereference(catalog.get("/Lang", ""))).strip()
    if language.lower() != EXPECTED_LANGUAGE.lower():
        failures.append(
            f"{label} expected language {EXPECTED_LANGUAGE!r}, got {language!r}"
        )
    viewer_preferences = dictionary(catalog.get("/ViewerPreferences"))
    if bool(viewer_preferences.get("/DisplayDocTitle")) is not True:
        failures.append(f"{label} does not request display of its document title")
    checks.append(f"{label} document language: {language or '(missing)'}")

    xmp_failures, xmp_checks = inspect_xmp_metadata(catalog)
    failures.extend(f"{label}: {failure}" for failure in xmp_failures)
    checks.extend(f"{label}: {check}" for check in xmp_checks)

    try:
        outline_count = count_outline_items(reader.outline)
    except Exception as exc:
        failures.append(f"{label} outline could not be read: {exc}")
        outline_count = 0
    if outline_count < 4:
        failures.append(f"{label} has fewer than four outline/bookmark entries")
    checks.append(f"{label} outline entries: {outline_count}")

    active_failures, links = inspect_active_content_and_links(reader)
    failures.extend(f"{label}: {failure}" for failure in active_failures)
    font_failures, font_checks = inspect_font_resources(reader)
    failures.extend(f"{label}: {failure}" for failure in font_failures)
    checks.extend(f"{label}: {check}" for check in font_checks)
    link_failures, link_checks = validate_link_contract(links, label, spec)
    failures.extend(link_failures)
    checks.extend(link_checks)

    try:
        text = normalized_text(reader)
    except ValueError as exc:
        failures.append(f"{label}: {exc}")
        text = ""

    metadata_text = " ".join(str(value) for value in metadata.values())
    disclosure_surface = f"{text}\n{metadata_text}"
    failures.extend(content_contract_failures(text, label, spec))
    failures.extend(
        disclosure_failures(disclosure_surface, f"{label} text or metadata")
    )

    checks.append(f"{label} extracted text: {len(text):,} characters")
    return failures, checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "pdf",
        nargs="*",
        type=Path,
        help=(
            "edition PDF(s) to validate; each must retain its exact release "
            "basename (default: both checked-in release PDFs)"
        ),
    )
    parser.add_argument(
        "--check-tracked-pdf-set",
        action="store_true",
        help=(
            "also require exactly the two release PDFs, both accessible "
            "companions and the shared builder in the Git index; reject legacy "
            "release artifacts; also require tracked worktree/index alignment"
        ),
    )
    parser.add_argument(
        "--check-tracked-text-disclosures",
        action="store_true",
        help=(
            "also scan all tracked release-text files for private-session or "
            "workstation disclosures; also requires all tracked worktree content "
            "to match the index; intended for CI and the final staged release check"
        ),
    )
    parser.add_argument(
        "--source",
        action="append",
        type=Path,
        help=(
            "release source file to scan for disclosures; repeat for multiple files "
            f"(the shared {BUILDER_SOURCE} is always scanned)"
        ),
    )
    args = parser.parse_args()

    requested_pdfs = args.pdf or [
        ROOT / spec["filename"] for spec in EDITION_SPECS.values()
    ]
    failures: list[str] = []
    checks: list[str] = []
    checked_editions: set[str] = set()
    for requested in requested_pdfs:
        pdf_path = requested if requested.is_absolute() else Path.cwd() / requested
        pdf_path = pdf_path.resolve()
        spec = edition_spec_for_path(pdf_path)
        if spec is None:
            expected = ", ".join(sorted(EXPECTED_REPOSITORY_PDFS))
            failures.append(
                f"cannot infer edition from PDF basename {pdf_path.name!r}; "
                f"expected one of: {expected}"
            )
            continue
        edition_key = next(
            key for key, value in EDITION_SPECS.items() if value is spec
        )
        if edition_key in checked_editions:
            failures.append(
                f"duplicate {spec['edition_name']} PDF input: {pdf_path}"
            )
            continue
        checked_editions.add(edition_key)
        pdf_failures, pdf_checks = validate(pdf_path, spec)
        failures.extend(pdf_failures)
        checks.extend(pdf_checks)
        companion_path = (ROOT / spec["accessible_doc"]).resolve()
        companion_failures, companion_checks = validate_accessible_companion(
            companion_path,
            spec,
        )
        failures.extend(companion_failures)
        checks.extend(companion_checks)

    sources = [Path(BUILDER_SOURCE), *(args.source or [])]
    seen_sources: set[Path] = set()
    for source in sources:
        source_path = (
            source if source.is_absolute() else ROOT / source
        ).resolve()
        if source_path in seen_sources:
            continue
        seen_sources.add(source_path)
        source_failures, source_checks = validate_source_disclosures(source_path)
        failures.extend(source_failures)
        checks.extend(source_checks)
    if args.check_tracked_pdf_set:
        repository_failures, repository_checks = validate_tracked_pdf_set(ROOT)
        failures.extend(repository_failures)
        checks.extend(repository_checks)
    if args.check_tracked_text_disclosures:
        disclosure_failures_found, disclosure_checks = (
            validate_tracked_text_disclosures(ROOT)
        )
        failures.extend(disclosure_failures_found)
        checks.extend(disclosure_checks)
    if args.check_tracked_pdf_set or args.check_tracked_text_disclosures:
        alignment_failures, alignment_checks = validate_index_worktree_alignment(ROOT)
        failures.extend(alignment_failures)
        checks.extend(alignment_checks)
    print("LG monitor companion-software guides public-release validation")
    for check in checks:
        print(f"[INFO] {check}")
    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}", file=sys.stderr)
        print(f"Validation failed with {len(failures)} finding(s).", file=sys.stderr)
        return 1

    print("[PASS] Requested PDFs satisfy automated public-release checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
