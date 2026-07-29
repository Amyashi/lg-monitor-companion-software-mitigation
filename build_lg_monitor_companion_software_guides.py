import argparse
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT_FILENAMES = {
    "home": "LG_Monitor_Companion_Software_Mitigation_Windows_11_Home_v1.0.0.pdf",
    "pro": "LG_Monitor_Companion_Software_Mitigation_Windows_11_Pro_v1.0.0.pdf",
}

PAGE_W, PAGE_H = landscape(letter)
MARGIN_X = 28
TOP = 42
BOTTOM = 34
CONTENT_W = PAGE_W - (2 * MARGIN_X)

NAVY = colors.HexColor("#0B162A")
NAVY_2 = colors.HexColor("#14243D")
INK = colors.HexColor("#1C2738")
MUTED = colors.HexColor("#5C6A7D")
TEAL = colors.HexColor("#107D79")
TEAL_BRIGHT = colors.HexColor("#13B8A6")
BLUE = colors.HexColor("#3467D2")
GREEN = colors.HexColor("#237D60")
AMBER = colors.HexColor("#8C6A2B")
CORAL = colors.HexColor("#B04C56")
PURPLE = colors.HexColor("#715AC3")
LIGHT = colors.HexColor("#F4F7FA")
LIGHT_BLUE = colors.HexColor("#EAF1FF")
LIGHT_GREEN = colors.HexColor("#EAF8F2")
LIGHT_AMBER = colors.HexColor("#FFF6E3")
LIGHT_CORAL = colors.HexColor("#FDEDEF")
LIGHT_PURPLE = colors.HexColor("#F1EDFF")
GRID = colors.HexColor("#D8E0EA")
WHITE = colors.white

GUIDE_VERSION = "1.0.0"
PREPARED = "29 July 2026"
ACTIVE_EDITION = "pro"


def is_pro():
    return ACTIVE_EDITION == "pro"


def edition_name():
    return "Windows 11 Pro" if is_pro() else "Windows 11 Home"


def short_title():
    return f"LG MONITOR COMPANION-SOFTWARE MITIGATION - {edition_name().upper()}"


def pdf_title():
    return (
        "LG Monitor Companion-Software Cleanup and Recurrence Mitigation - "
        f"{edition_name()} Edition"
    )

REFS = {
    "device": (
        1,
        "Prevent device metadata retrieval from the network",
        "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-deviceinstallation#preventdevicemetadatafromnetwork",
    ),
    "requirements": (
        2,
        "AppLocker requirements and supported Windows editions",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/requirements-to-use-applocker",
    ),
    "kb": (
        3,
        "KB5024351: removal of Windows edition checks for AppLocker",
        "https://support.microsoft.com/en-us/servicing/os/windows/2023/02/kb5024351-removal-of-windows-edition-checks-for-applocker",
    ),
    "create_appx": (
        4,
        "Create an AppLocker rule for packaged apps",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/create-a-rule-for-packaged-apps",
    ),
    "precedence": (
        5,
        "AppLocker allow and deny actions",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/understanding-applocker-allow-and-deny-actions-on-rules",
    ),
    "appidsvc": (
        6,
        "Configure the Application Identity service",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/configure-the-application-identity-service",
    ),
    "events": (
        7,
        "Use Event Viewer with AppLocker",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/using-event-viewer-with-applocker",
    ),
    "overview": (
        8,
        "AppLocker overview and defense-in-depth guidance",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/applocker-overview",
    ),
    "get_appx": (
        9,
        "Get-AppxPackage",
        "https://learn.microsoft.com/en-us/powershell/module/appx/get-appxpackage?view=windowsserver2025-ps",
    ),
    "remove_appx": (
        10,
        "Remove-AppxPackage",
        "https://learn.microsoft.com/en-us/powershell/module/appx/remove-appxpackage?view=windowsserver2025-ps",
    ),
    "get_prov": (
        11,
        "Get-AppxProvisionedPackage",
        "https://learn.microsoft.com/en-us/powershell/module/dism/get-appxprovisionedpackage?view=windowsserver2025-ps",
    ),
    "remove_prov": (
        12,
        "Remove-AppxProvisionedPackage",
        "https://learn.microsoft.com/en-us/powershell/module/dism/remove-appxprovisionedpackage?view=windowsserver2025-ps",
    ),
    "pua": (
        13,
        "Detect and block potentially unwanted applications",
        "https://learn.microsoft.com/en-us/defender-endpoint/detect-block-potentially-unwanted-apps-microsoft-defender-antivirus",
    ),
    "compat": (
        14,
        "Microsoft Defender Antivirus compatibility modes",
        "https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility",
    ),
    "get_policy": (
        15,
        "Get-AppLockerPolicy",
        "https://learn.microsoft.com/en-us/powershell/module/applocker/get-applockerpolicy?view=windowsserver2025-ps",
    ),
    "set_policy": (
        16,
        "Set-AppLockerPolicy",
        "https://learn.microsoft.com/en-us/powershell/module/applocker/set-applockerpolicy?view=windowsserver2025-ps",
    ),
    "audit_enforce": (
        17,
        "Deploy AppLocker policies by using Enforce rules",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/deploy-applocker-policies-by-using-the-enforce-rules-setting",
    ),
    "test_policy": (
        18,
        "Test-AppLockerPolicy",
        "https://learn.microsoft.com/en-us/powershell/module/applocker/test-applockerpolicy?view=windowsserver2025-ps",
    ),
    "default_rules": (
        19,
        "Create AppLocker default rules",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/create-applocker-default-rules",
    ),
    "delete_rule": (
        20,
        "Delete an AppLocker rule",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/delete-an-applocker-rule",
    ),
    "device_apps": (
        21,
        "Automatic installation for UWP device apps",
        "https://learn.microsoft.com/en-us/windows-hardware/drivers/devapps/auto-install-for-uwp-device-apps",
    ),
    "inf_addsoftware": (
        22,
        "INF AddSoftware directive",
        "https://learn.microsoft.com/en-us/windows-hardware/drivers/install/inf-addsoftware-directive",
    ),
    "lg_support": (
        23,
        "LG product support, manuals, software and drivers",
        "https://www.lg.com/us/support",
    ),
    "lg_osc": (
        24,
        "LG Monitor OnScreen Control: update monitor software",
        "https://www.lg.com/us/support/help-library/lg-monitor-onscreen-control-how-to-update-monitor-software--20154629827481",
    ),
    "store_app": (
        25,
        "Microsoft Store: LG Monitor App Installer",
        "https://apps.microsoft.com/detail/9pm9n6f47jb8",
    ),
    "driver_container": (
        26,
        "Driver Package Container Metadata",
        "https://learn.microsoft.com/en-us/windows-hardware/drivers/install/driver-package-container-metadata",
    ),
    "system_tools": (
        27,
        "System Configuration tools in Windows",
        "https://support.microsoft.com/en-us/windows/experience/system-configuration-tools-in-windows",
    ),
}


def register_fonts():
    pdfmetrics.registerFont(pdfmetrics.Font("Segoe", "Helvetica", "WinAnsiEncoding"))
    pdfmetrics.registerFont(
        pdfmetrics.Font("Segoe-Bold", "Helvetica-Bold", "WinAnsiEncoding")
    )
    pdfmetrics.registerFont(
        pdfmetrics.Font("Segoe-Italic", "Helvetica-Oblique", "WinAnsiEncoding")
    )
    pdfmetrics.registerFont(pdfmetrics.Font("Consolas", "Courier", "WinAnsiEncoding"))
    pdfmetrics.registerFontFamily(
        "Segoe",
        normal="Segoe",
        bold="Segoe-Bold",
        italic="Segoe-Italic",
        boldItalic="Segoe-Bold",
    )
    pdfmetrics.registerFontFamily(
        "Consolas",
        normal="Consolas",
        bold="Consolas",
        italic="Consolas",
        boldItalic="Consolas",
    )


register_fonts()

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="PageTitle",
        fontName="Segoe-Bold",
        fontSize=19,
        leading=22,
        textColor=NAVY,
        spaceAfter=4,
        keepWithNext=1,
    )
)
styles.add(
    ParagraphStyle(
        name="PageIntro",
        fontName="Segoe",
        fontSize=9.1,
        leading=11.8,
        textColor=MUTED,
        spaceAfter=9,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        fontName="Segoe",
        fontSize=8.3,
        leading=10.8,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="BodySmall",
        fontName="Segoe",
        fontSize=7.4,
        leading=9.5,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyTiny",
        fontName="Segoe",
        fontSize=6.85,
        leading=8.25,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="HeaderWhite",
        fontName="Segoe-Bold",
        fontSize=7.3,
        leading=8.5,
        textColor=WHITE,
    )
)
styles.add(
    ParagraphStyle(
        name="Callout",
        fontName="Segoe",
        fontSize=8.2,
        leading=10.6,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="CardTitle",
        fontName="Segoe-Bold",
        fontSize=9.4,
        leading=11.2,
        textColor=NAVY,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CardBody",
        fontName="Segoe",
        fontSize=7.75,
        leading=10.0,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="RunCode",
        fontName="Consolas",
        fontSize=6.55,
        leading=7.7,
        textColor=colors.HexColor("#E8F0FA"),
    )
)
styles.add(
    ParagraphStyle(
        name="RunCodeCompact",
        fontName="Consolas",
        fontSize=6.2,
        leading=7.1,
        textColor=colors.HexColor("#E8F0FA"),
    )
)
styles.add(
    ParagraphStyle(
        name="Source",
        fontName="Segoe",
        fontSize=6.85,
        leading=8.45,
        textColor=INK,
        spaceAfter=2,
    )
)


def ref(key):
    number, _title, url = REFS[key]
    return f" <link href='{url}' color='#315FC4'><b>[{number:02d}]</b></link>"


def para(text, style="Body"):
    return Paragraph(text, styles[style])


def plain(text, style="Body"):
    return Paragraph(escape(text), styles[style])


class CoverHero(Flowable):
    def __init__(self):
        super().__init__()
        self.width = CONTENT_W
        self.height = 258

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setFillColor(NAVY)
        c.roundRect(0, 0, w, h, 15, fill=1, stroke=0)
        c.setFillColor(NAVY_2)
        c.circle(w - 82, h - 56, 67, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#173656"))
        c.circle(w - 48, 62, 64, fill=1, stroke=0)
        c.setFillColor(TEAL_BRIGHT)
        c.roundRect(34, h - 41, 128, 5, 2.5, fill=1, stroke=0)

        c.setFont("Segoe-Bold", 9.4)
        c.setFillColor(TEAL_BRIGHT)
        c.drawString(35, h - 60, "WINDOWS 11 ACTION RUNBOOK")

        title = c.beginText(35, h - 96)
        title.setFont("Segoe-Bold", 23)
        title.setLeading(27)
        title.setFillColor(WHITE)
        title.textLine("LG Monitor Companion-Software")
        title.textLine("Cleanup and Recurrence")
        title.textLine("Mitigation")
        c.drawText(title)

        sub = c.beginText(35, 79)
        sub.setFont("Segoe", 10.5)
        sub.setLeading(15)
        sub.setFillColor(colors.HexColor("#D7E4F3"))
        sub.textLine(f"{edition_name()} Edition")
        sub.textLine("Preflight -> confirm exact LG package -> remove -> restart -> verify")
        sub.textLine(
            "Optional recurrence controls appear only when this edition supports the tested path"
            if is_pro()
            else "Home path: cleanup, recurrence reduction, verification and recovery"
        )
        c.drawText(sub)

        c.setFillColor(WHITE)
        c.setFont("Segoe-Bold", 29)
        c.drawCentredString(w - 82, h - 60, "11")
        c.setFont("Segoe-Bold", 8)
        c.setFillColor(colors.HexColor("#B8CCE5"))
        c.drawCentredString(w - 82, h - 77, "PRO" if is_pro() else "HOME")

        c.setFillColor(colors.HexColor("#D8E7F7"))
        c.setFont("Segoe-Bold", 7.2)
        c.drawString(
            35,
            31,
            f"Author: Amyashi | v{GUIDE_VERSION} | Reviewed {PREPARED}",
        )
        c.setFont("Segoe", 6.5)
        c.drawString(
            35,
            20,
            (
                "Original observed case: Windows 11 Pro; revalidate the package and delivery path locally."
                if is_pro()
                else "Home status: documentation-derived and structurally validated; not field-tested on Windows 11 Home."
            ),
        )
        c.drawString(
            35,
            9,
            "Independent, unofficial and unaffiliated; not endorsed by LG or Microsoft; not support, certification or a guarantee. Guide materials: CC BY-NC-ND 4.0; see LICENSE.md.",
        )


def page_heading(number, title, intro):
    return [
        para(f"{number}. {title}", "PageTitle"),
        para(intro, "PageIntro"),
    ]


def callout(label, body, accent=AMBER, bg=LIGHT_AMBER):
    table = Table(
        [[para(f"<b>{escape(label)}</b>", "Callout"), para(body, "Callout")]],
        colWidths=[122, CONTENT_W - 122],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.7, accent),
                ("LINEBEFORE", (0, 0), (0, -1), 5, accent),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def card(title, body, accent=BLUE, bg=LIGHT_BLUE, width=(CONTENT_W - 12) / 2):
    table = Table(
        [[para(title, "CardTitle")], [para(body, "CardBody")]],
        colWidths=[width],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.8, accent),
                ("LINEABOVE", (0, 0), (-1, 0), 4, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def two_cards(left, right):
    table = Table([[left, right]], colWidths=[CONTENT_W / 2, CONTENT_W / 2])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, 0), 6),
                ("LEFTPADDING", (1, 0), (1, 0), 6),
                ("RIGHTPADDING", (1, 0), (1, 0), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def code_card(title, code, accent=BLUE, width=CONTENT_W, compact=False):
    lines = code.strip("\n").splitlines() or [""]
    data = [[para(escape(title), "HeaderWhite")]]
    code_style = styles["RunCodeCompact"] if compact else styles["RunCode"]
    data.extend([[Preformatted(line, code_style)]] for line in lines)
    table = Table(
        data,
        colWidths=[width],
        hAlign="LEFT",
        repeatRows=1,
        splitByRow=1,
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), accent),
                ("BACKGROUND", (0, 1), (-1, -1), NAVY_2),
                ("BOX", (0, 0), (-1, -1), 0.8, accent),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, 0), 5),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
                ("TOPPADDING", (0, 1), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 0),
                ("LINEABOVE", (0, 1), (-1, -1), 0.35, accent),
            ]
        )
    )
    return table


def standard_table(headers, rows, widths, tiny=False):
    body_style = "BodyTiny" if tiny else "BodySmall"
    data = [[para(escape(header), "HeaderWhite") for header in headers]]
    for row in rows:
        data.append(
            [
                value if isinstance(value, Flowable) else para(value, body_style)
                for value in row
            ]
        )
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.45, GRID),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for index in range(1, len(data)):
        commands.append(
            ("BACKGROUND", (0, index), (-1, index), WHITE if index % 2 else LIGHT)
        )
    table.setStyle(TableStyle(commands))
    return table


def page_header_footer(c: canvas.Canvas, _doc):
    page = c.getPageNumber()
    c.setTitle(pdf_title())
    c.setAuthor("Amyashi")
    c.setCreator("Amyashi - generated from the accompanying ReportLab source")
    c.setSubject(
        f"Ordered {edition_name()} cleanup, recurrence mitigation, verification "
        "and recovery runbook for the LG Monitor App package"
    )
    c.setKeywords(
        f"LG Monitor App, {edition_name()}, AppLocker, device metadata, "
        "Defender PUA, OnScreen Control"
    )
    c._doc.Catalog.Lang = PDFString("en-US")
    c.setViewerPreference("DisplayDocTitle", "true")
    c.showOutline()
    if page == 1:
        return
    c.saveState()
    c.setStrokeColor(GRID)
    c.setLineWidth(0.5)
    c.line(MARGIN_X, PAGE_H - 27, PAGE_W - MARGIN_X, PAGE_H - 27)
    c.setFont("Segoe-Bold", 7)
    c.setFillColor(NAVY)
    c.drawString(MARGIN_X, PAGE_H - 18, short_title())
    c.setFont("Segoe", 6.8)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 18, f"Reviewed {PREPARED}")

    c.line(MARGIN_X, 22, PAGE_W - MARGIN_X, 22)
    c.setFont("Segoe", 6.7)
    c.drawString(
        MARGIN_X,
        11,
        f"Amyashi | Independent and unaffiliated | CC BY-NC-ND 4.0 guide material | v{GUIDE_VERSION}",
    )
    c.setFont("Segoe-Bold", 6.8)
    c.drawRightString(PAGE_W - MARGIN_X, 11, f"PAGE {page}")
    c.restoreState()


def cover_page():
    advanced = (
        "Use AppLocker only after the exact tested package actually returns. "
        "Leave that returned package installed, reconfirm its full identity, "
        "start in <b>Audit only</b>, and enforce only after every gate passes."
        if is_pro()
        else
        "Windows 11 Home does not include the tested local AppLocker-management "
        "path used in the Pro guide. Do not install third-party Group Policy or "
        "Local Security Policy hacks. Use the failure ladder if the package returns."
    )
    home_validation = (
        ""
        if is_pro()
        else "<b>Home validation status:</b> This edition is documentation-derived and structurally validated, but has not been field-tested on a Windows 11 Home machine. Confirm each effective result locally and stop on mismatch. "
    )
    return [
        Spacer(1, 13),
        CoverHero(),
        Spacer(1, 12),
        two_cards(
            card(
                "Core path",
                "<b>0.</b> Preflight and capture state<br/>"
                "<b>1.</b> Apply this edition's metadata control<br/>"
                "<b>2.</b> Remove only the exact LG package<br/>"
                "<b>2A.</b> Decide about LG OnScreen Control separately<br/>"
                "<b>3.</b> Restart once and verify<br/>"
                "<b>4.</b> Stop when every core result passes",
                TEAL,
                LIGHT_GREEN,
            ),
            card(
                "Recurrence path" if is_pro() else "Home boundary",
                advanced,
                BLUE,
                LIGHT_BLUE,
            ),
        ),
        Spacer(1, 7),
        callout(
            "READ BEFORE USE",
            "Use only on a personally administered PC or with the responsible administrator's approval. All-user package removal affects every current user and future-user provisioning and requires reinstallation to undo. Confirm that no firmware update is running and that a working remote, physical control path or accepted loss of software-only controls exists.",
            CORAL,
            LIGHT_CORAL,
        ),
        Spacer(1, 6),
        callout(
            "DOCUMENTED EXAMPLE AND ELIGIBILITY",
            home_validation
            + "This procedure was developed from an LG 45GR95QE-B case involving the Microsoft Store product <b>LG Monitor App Installer</b> "
            "(Store ID <font name='Consolas'>9PM9N6F47JB8</font>, package <font name='Consolas'>LGElectronics.LGMonitorApp</font>) "
            "and the separate LG OnScreen Control desktop application. Other LG monitor models can use different software or delivery paths. "
            "Confirm the exact model's official LG support page and stop if the exact package is absent, its Store publisher is not LG Electronics Inc., "
            "or a different LG-named package appears. Never substitute another package name into these commands."
            + ref("store_app")
            + ref("lg_support"),
            AMBER,
            LIGHT_AMBER,
        ),
    ]


def preflight_page():
    system_check = r"""
# Run in Windows PowerShell 5.1 as Administrator.
$ErrorActionPreference = 'Stop'
$ExpectedEdition = '__EXPECTED_EDITION__'
$Os = Get-CimInstance Win32_OperatingSystem
$Computer = Get-CimInstance Win32_ComputerSystem
$Identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$Principal = [Security.Principal.WindowsPrincipal]$Identity
$IsAdmin = $Principal.IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)

[pscustomobject]@{
    WindowsEdition = $Os.Caption
    Version = $Os.Version
    Build = $Os.BuildNumber
    Administrator = $IsAdmin
    DomainJoined = $Computer.PartOfDomain
}
if (-not $IsAdmin) { throw 'STOP: reopen PowerShell as Administrator.' }
if ($Computer.PartOfDomain) { throw 'STOP: use the managed-device workflow.' }
if ($Os.Caption -notmatch [regex]::Escape($ExpectedEdition)) {
    throw "STOP: this is the $ExpectedEdition guide; detected $($Os.Caption)."
}

$RunId = '{0}-{1}' -f (Get-Date -Format 'yyyyMMdd-HHmmss'),
    ([guid]::NewGuid().ToString('N').Substring(0,8))
$RunDir = Join-Path ([Environment]::GetFolderPath('Desktop')) "LG-Run-$RunId"
New-Item -ItemType Directory -Path $RunDir -ErrorAction Stop | Out-Null
$RunDir
"""
    system_check = system_check.replace("__EXPECTED_EDITION__", edition_name())
    capture = r"""
$Package = 'LGElectronics.LGMonitorApp'
$ExpectedPublisher = 'CN=4A5401D9-32C2-486E-A8CB-EFECB124AF89'
$ExpectedPublisherId = 'cfnzzhwkr8z5w'
$ExpectedFamily = "${Package}_${ExpectedPublisherId}"
$Types = 'Main','Framework','Resource','Bundle','Optional'
$MetaPath = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Device Metadata'
$MetaName = 'PreventDeviceMetadataFromNetwork'
$Meta = [ordered]@{ KeyExisted = Test-Path -LiteralPath $MetaPath
                   ValueExisted = $false; Value = $null; Kind = $null }
if ($Meta.KeyExisted) {
    $Key = Get-Item -LiteralPath $MetaPath
    $Props = Get-ItemProperty -LiteralPath $MetaPath
    $Meta.ValueExisted = $Props.PSObject.Properties.Name -contains $MetaName
    if ($Meta.ValueExisted) {
        $Meta.Value = $Props.$MetaName
        $Meta.Kind = [string]$Key.GetValueKind($MetaName)
    }
}
[pscustomobject]$Meta | Export-Clixml "$RunDir\Metadata-Before.clixml"

Get-AppxPackage -AllUsers -Name $Package -PackageTypeFilter $Types |
    Export-Clixml "$RunDir\Registered-Before.clixml"
Get-AppxProvisionedPackage -Online |
    Where-Object DisplayName -eq $Package |
    Export-Clixml "$RunDir\Provisioned-Before.clixml"
Get-MpPreference | Select-Object PUAProtection |
    Export-Clixml "$RunDir\Defender-Before.clixml"
Get-ChildItem -LiteralPath $RunDir |
    Select-Object Name,Length,LastWriteTime
"""
    if not is_pro():
        capture = r"""
$Package = 'LGElectronics.LGMonitorApp'
$Types = 'Main','Framework','Resource','Bundle','Optional'
Start-Process SystemPropertiesHardware.exe
# Hardware > Device Installation Settings: note the selected Yes/No option.
$HomeChoice = Read-Host 'Type the exact selected Yes/No option'
if ([string]::IsNullOrWhiteSpace($HomeChoice)) {
    throw 'STOP: record the Home preference before continuing.'
}
[pscustomobject]@{ DeviceInstallationSettingsChoice = $HomeChoice } |
    Export-Clixml "$RunDir\Device-Installation-Settings-Before.clixml"
Get-AppxPackage -AllUsers -Name $Package -PackageTypeFilter $Types |
    Export-Clixml "$RunDir\Registered-Before.clixml"
Get-AppxProvisionedPackage -Online |
    Where-Object DisplayName -eq $Package |
    Export-Clixml "$RunDir\Provisioned-Before.clixml"
Get-MpPreference | Select-Object PUAProtection |
    Export-Clixml "$RunDir\Defender-Before.clixml"
Get-ChildItem -LiteralPath $RunDir |
    Select-Object Name,Length,LastWriteTime
"""
    story = page_heading(
        "1",
        "Step 0 - preflight and preserve the before-state",
        "Complete this page before changing Windows. Keep the same elevated PowerShell window open through the cleanup step.",
    )
    story += [
        callout(
            "PHYSICAL AND RECOVERY CHECK",
            "Confirm that <b>no LG monitor firmware update is running</b>. Record the exact monitor model and open its official LG support page. Confirm a working remote or physical control path, or deliberately accept losing software-only controls. Policy backups do not reinstall removed software."
            + ref("lg_support")
            + ref("lg_osc"),
            CORAL,
            LIGHT_CORAL,
        ),
        Spacer(1, 8),
        two_cards(
            code_card(
                "A - CONFIRM EDITION, ADMINISTRATOR AND DOMAIN STATE",
                system_check,
                TEAL,
                (CONTENT_W / 2) - 6,
            ),
            code_card(
                "B - CAPTURE THE EXACT CORE BEFORE-STATE",
                capture,
                BLUE,
                (CONTENT_W / 2) - 6,
            ),
        ),
        Spacer(1, 8),
        callout(
            "GO / STOP",
            "Open every saved file, then copy the complete <font name='Consolas'>LG-Run-...</font> folder to separate administrator-controlled storage. "
            + (
                "Record the current Local Group Policy state before changing it. "
                if is_pro()
                else
                "Record the current Device Installation Settings choice before changing it. "
            )
            + "Open <b>Settings &gt; Accounts &gt; Access work or school</b>. Continue only when the edition matches this guide, Administrator is True, DomainJoined is False, no organization manages the PC, the recovery copy opens, and the exact Store product and publisher have been confirmed. Unknown package or publisher identity means stop.",
            AMBER,
            LIGHT_AMBER,
        ),
    ]
    return story


def metadata_page():
    verify = r"""
$Path = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Device Metadata'
$Name = 'PreventDeviceMetadataFromNetwork'
$Value = Get-ItemPropertyValue -Path $Path -Name $Name `
    -ErrorAction SilentlyContinue
[pscustomobject]@{
    WindowsEdition = (Get-CimInstance Win32_OperatingSystem).Caption
    MetadataPolicyValue = if ($null -eq $Value) { '(not set)' } else { $Value }
}
"""
    pro_steps = (
        "<b>1.</b> Open <font name='Consolas'>gpedit.msc</font>.<br/>"
        "<b>2.</b> Go to Computer Configuration &gt; Administrative Templates &gt; "
        "System &gt; Device Installation.<br/>"
        "<b>3.</b> Open <b>Prevent automatic download of applications associated "
        "with device metadata</b>.<br/>"
        "<b>4.</b> Select <b>Enabled</b>, then Apply and OK.<br/>"
        "<b>5.</b> Run <font name='Consolas'>gpupdate /target:computer /force</font>.<br/>"
        "<b>6.</b> Run the verification block. Expected policy value: <b>1</b>."
    )
    home_steps = (
        "<b>1.</b> Run <font name='Consolas'>SystemPropertiesHardware.exe</font> "
        "or open Control Panel &gt; System &gt; Advanced system settings &gt; Hardware.<br/>"
        "<b>2.</b> Select <b>Device Installation Settings</b>.<br/>"
        "<b>3.</b> Choose the option that does not automatically download "
        "manufacturer apps and custom icons, then save.<br/>"
        "<b>4.</b> Reopen the dialog and confirm that the choice persisted."
    )
    story = page_heading(
        "2",
        "Step 1 - reduce metadata-associated app retrieval",
        (
            "Use the supported Local Group Policy setting, verify it, and record the exact undo."
            if is_pro()
            else
            "Use the Windows 11 Home Device Installation Settings preference, then reopen it to verify the saved choice."
        ),
    )
    if is_pro():
        story += [
            card(
                "DO THIS - WINDOWS 11 PRO",
                pro_steps + "<br/><br/><b>Undo:</b> restore the exact Local Group Policy state recorded in Step 0, refresh policy, and verify again." + ref("device"),
                BLUE,
                LIGHT_BLUE,
                width=CONTENT_W,
            ),
            Spacer(1, 10),
            code_card("VERIFY THE EFFECTIVE REGISTRY RESULT", verify, TEAL),
            Spacer(1, 10),
            standard_table(
                ["PASS RESULT", "IF IT DOES NOT MATCH", "RESTART?"],
                [[
                    "<font name='Consolas'>MetadataPolicyValue = 1</font>",
                    "Reopen Local Group Policy, confirm Enabled, refresh Group Policy and recheck. Stop if another authority reverses it.",
                    "No restart yet. Continue to package cleanup.",
                ]],
                [190, 396, 150],
            ),
        ]
    else:
        story += [
            two_cards(
                card(
                    "DO THIS - WINDOWS 11 HOME",
                    home_steps + ref("system_tools"),
                    AMBER,
                    LIGHT_AMBER,
                ),
                card(
                    "EXPECTED RESULT AND UNDO",
                    "<b>Pass:</b> the dialog reopens with the chosen preference still selected. "
                    "This is not the Pro policy and no Pro registry value is expected.<br/><br/>"
                    "<b>Undo:</b> reopen the same dialog and restore the exact choice recorded in Step 0.<br/><br/>"
                    "<b>Restart?</b> Not yet. Continue to package cleanup.",
                    GREEN,
                    LIGHT_GREEN,
                ),
            ),
        ]
    story += [
        Spacer(1, 10),
        callout(
            "CONTROL BOUNDARY",
            (
                "This policy concerns applications associated with device metadata. "
                if is_pro()
                else
                "The Home control is a broader, weaker user preference; it is not equivalent to the documented Pro policy. "
            )
            + "Neither control is a universal block for Microsoft Store/manual acquisition, Windows Update drivers, OEM provisioning, "
            "Driver Package Container Metadata, driver-INF <font name='Consolas'>AddSoftware</font> or conventional Win32 installers. "
            "Microsoft also marks the legacy device-metadata path as deprecated."
            + ref("device_apps")
            + ref("driver_container")
            + ref("inf_addsoftware"),
            AMBER,
            LIGHT_AMBER,
        ),
    ]
    return story


def removal_page():
    removal = r"""
$Package = 'LGElectronics.LGMonitorApp'
$ExpectedPublisher = 'CN=4A5401D9-32C2-486E-A8CB-EFECB124AF89'
$ExpectedPublisherId = 'cfnzzhwkr8z5w'
$ExpectedFamily = "${Package}_${ExpectedPublisherId}"
$Types = 'Main','Framework','Resource','Bundle','Optional'
$Targets = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
$Provisioned = @(Get-AppxProvisionedPackage -Online -ErrorAction Stop |
    Where-Object DisplayName -eq $Package)
$Targets | Select-Object Name,Publisher,PublisherId,PackageFamilyName,PackageFullName
$Provisioned | Select-Object DisplayName,PublisherId,PackageName
if ($Targets.Count -eq 0 -and $Provisioned.Count -eq 0) {
    'Already clean: no registered or provisioned target was found.'
} else {
    if (@($Targets | Where-Object {
        $_.Publisher -ne $ExpectedPublisher -or
        $_.PublisherId -ne $ExpectedPublisherId -or
        $_.PackageFamilyName -ne $ExpectedFamily
    }).Count -gt 0) {
        throw 'STOP: registered signer or package family is not the tested identity.'
    }
    if (@($Provisioned | Where-Object {
        $_.PublisherId -ne $ExpectedPublisherId
    }).Count -gt 0) {
        throw 'STOP: provisioned publisher ID is not the tested identity.'
    }

    $Confirm = Read-Host "Type REMOVE to remove only $Package from all users"
    if ($Confirm -cne 'REMOVE') { throw 'STOP: removal was not confirmed.' }

    if ($Targets.Count -gt 0) {
        $Bundles = @(Get-AppxPackage -AllUsers -Name $Package `
            -PackageTypeFilter Bundle -ErrorAction Stop)
        $Mains = @(Get-AppxPackage -AllUsers -Name $Package `
            -PackageTypeFilter Main -ErrorAction Stop)
        $Parents = if ($Bundles.Count -gt 0) { $Bundles } else { $Mains }
        if ($Parents.Count -eq 0) {
            throw 'STOP: child packages exist without a removable parent.'
        }
        $Parents | Sort-Object PackageFullName -Unique | ForEach-Object {
            Remove-AppxPackage -Package $_.PackageFullName -AllUsers `
                -ErrorAction Stop
        }
    }

    $Provisioned | ForEach-Object {
        Remove-AppxProvisionedPackage -Online -AllUsers `
            -PackageName $_.PackageName -ErrorAction Stop | Out-Null
    }
}
"""
    verify = r"""
$Package = 'LGElectronics.LGMonitorApp'
$Types = 'Main','Framework','Resource','Bundle','Optional'
$Registered = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
$Provisioned = @(Get-AppxProvisionedPackage -Online -ErrorAction Stop |
    Where-Object DisplayName -eq $Package)
[pscustomobject]@{
    RegisteredPackageCount = $Registered.Count
    ProvisionedPackageCount = $Provisioned.Count
}
"""
    right_column = Table(
        [
            [
                code_card(
                    "B - VERIFY BOTH STORES OF PACKAGE STATE",
                    verify,
                    TEAL,
                    (CONTENT_W / 2) - 6,
                )
            ],
            [
                card(
                    "STEP 2A - DECIDE ABOUT LG ONSCREEN CONTROL",
                    "<b>Action:</b> Keep OnScreen Control if you use it for firmware, "
                    "presets or settings. Remove it only through <b>Settings &gt; Apps "
                    "&gt; Installed apps</b>, only when no firmware update is running "
                    "and another accepted control path works.<br/><br/>"
                    "<b>Expected result:</b> the chosen remote, physical or software "
                    "control path works and no firmware update was interrupted.<br/><br/>"
                    "<b>Restart:</b> no separate restart now; continue to Step 3.<br/><br/>"
                    "<b>If it fails / undo:</b> stop. Reinstall only the official "
                    "model-specific LG version, then retest the functions you use."
                    + ref("lg_osc")
                    + ref("lg_support"),
                    BLUE,
                    LIGHT_BLUE,
                    (CONTENT_W / 2) - 6,
                )
            ],
        ],
        colWidths=[(CONTENT_W / 2) - 6],
        hAlign="LEFT",
    )
    right_column.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, 0), 0),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
                ("TOPPADDING", (0, 1), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 0),
            ]
        )
    )
    story = page_heading(
        "3",
        "Step 2 - remove the exact LG package",
        f"This {edition_name()} procedure targets only LGElectronics.LGMonitorApp. Zero packages at the start means already clean, not an error.",
    )
    story += [
        callout(
            "IDENTITY AND RECOVERY GATE",
            "Before running removal, open Microsoft Store product <font name='Consolas'>9PM9N6F47JB8</font> and confirm <b>LG Monitor App Installer</b>, publisher <b>LG Electronics Inc.</b> "
            "The command then displays the exact installed name, publisher, publisher ID, family and full package identity before asking for <font name='Consolas'>REMOVE</font>. "
            "It fails closed unless the registered signer is <font name='Consolas'>CN=4A5401D9-32C2-486E-A8CB-EFECB124AF89</font>, "
            "the publisher ID is <font name='Consolas'>cfnzzhwkr8z5w</font> and the family is <font name='Consolas'>LGElectronics.LGMonitorApp_cfnzzhwkr8z5w</font>. "
            "These are tested identity values, not a promise about a future LG release. Stop and revalidate if the Store reference or any installed identity differs, or if another LG package appears. "
            "This is an all-user action: it removes registrations for current users and provisioning for future users. Never substitute another package name, "
            "delete WindowsApps files manually, or reinstall an absent package merely to create a rule."
            + ref("store_app")
            + ref("get_appx")
            + ref("remove_appx"),
            CORAL,
            LIGHT_CORAL,
        ),
        Spacer(1, 2),
        two_cards(
            code_card(
                "A - REMOVE EXISTING REGISTRATIONS AND FUTURE-USER PROVISIONING",
                removal,
                BLUE,
                (CONTENT_W / 2) - 6,
                compact=True,
            ),
            right_column,
        ),
        Spacer(1, 2),
        callout(
            "PASS RESULT",
            "Both counts are <b>0</b>. Registered removal clears existing users; provisioning removal clears the online image used for future users. Both checks are required." + ref("remove_appx") + ref("get_prov") + ref("remove_prov"),
            GREEN,
            LIGHT_GREEN,
        ),
    ]
    return story


def verify_page():
    verify = r"""
$Package = 'LGElectronics.LGMonitorApp'
$Types = 'Main','Framework','Resource','Bundle','Optional'
$Edition = (Get-CimInstance Win32_OperatingSystem).Caption
$Registered = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
$Provisioned = @(Get-AppxProvisionedPackage -Online -ErrorAction Stop |
    Where-Object DisplayName -eq $Package)
$Meta = Get-ItemPropertyValue `
    -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Device Metadata' `
    -Name PreventDeviceMetadataFromNetwork -ErrorAction SilentlyContinue

[pscustomobject]@{
    WindowsEdition = $Edition
    RegisteredPackageCount = $Registered.Count
    ProvisionedPackageCount = $Provisioned.Count
    MetadataPolicyValue = if ($null -eq $Meta) { '(not set)' } else { $Meta }
    DefenderRealTime = (Get-MpComputerStatus).RealTimeProtectionEnabled
}
"""
    if not is_pro():
        verify = r"""
$Package = 'LGElectronics.LGMonitorApp'
$Types = 'Main','Framework','Resource','Bundle','Optional'
$Registered = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
$Provisioned = @(Get-AppxProvisionedPackage -Online -ErrorAction Stop |
    Where-Object DisplayName -eq $Package)
[pscustomobject]@{
    WindowsEdition = (Get-CimInstance Win32_OperatingSystem).Caption
    RegisteredPackageCount = $Registered.Count
    ProvisionedPackageCount = $Provisioned.Count
    DefenderRealTime = (Get-MpComputerStatus).RealTimeProtectionEnabled
}
"""
    story = page_heading(
        "4",
        "Step 3 - restart once, then verify",
        "Restart Windows now. Sign in normally, wait for the desktop to settle, then run the block in an elevated Windows PowerShell 5.1 window.",
    )
    story += [
        code_card("POST-RESTART CORE VERIFICATION", verify, TEAL),
        Spacer(1, 10),
        standard_table(
            ["CHECK", f"{edition_name().upper()} PASS", "IF IT DOES NOT MATCH"],
            [
                ["Registered package", "0", "Return to Section 3; display identity again and stop on any mismatch."],
                ["Provisioned package", "0", "Return to Section 3; do not delete WindowsApps files manually."],
                [
                    "Metadata control",
                    "Policy value = 1" if is_pro() else "Recorded Home preference is still selected",
                    "Return to Section 2 and restore or reapply through the same control surface.",
                ],
                [
                    "Defender health",
                    "True when Microsoft Defender is the active antivirus",
                    "Identify the active antivirus authority before changing PUA settings.",
                ],
                [
                    "Monitor baseline",
                    "Every recorded function actually used still works",
                    f"Restore only the smallest changed layer; use Section {10 if is_pro() else 7}.",
                ],
            ],
            [170, 210, 356],
        ),
        Spacer(1, 10),
        two_cards(
            card(
                "Everything passed",
                "<b>Stop here.</b> The core mitigation is complete. "
                + (
                    "Do not enable AppLocker or change Defender without a documented requirement. "
                    if is_pro()
                    else
                    "Do not add third-party policy tools or change Defender without a documented requirement. "
                )
                + "Record the date and keep the recovery folder.",
                GREEN,
                LIGHT_GREEN,
            ),
            card(
                "Something failed",
                "Continue to the failure ladder on the next page. Preserve the exact output and time. Do not repeat removal blindly, add broad exclusions or delete application folders.",
                AMBER,
                LIGHT_AMBER,
            ),
        ),
        Spacer(1, 8),
        callout(
            "FUNCTIONAL MONITOR CHECK",
            "Compare against the pre-change baseline for this exact LG model: native resolution, intended maximum refresh rate, adaptive sync if supported, HDR if supported and used, audio, USB hub or KVM, input switching, firmware access and the chosen remote/physical/software control path. A clean package count is not a pass if a used monitor function was unintentionally lost.",
            BLUE,
            LIGHT_BLUE,
        ),
    ]
    return story


def failure_page():
    recurrence_action = (
        "Record the time, edition, package identity and observed delivery path. "
        "Reconfirm the Pro metadata policy value without assuming it caused the return."
        if is_pro()
        else
        "Record the time, edition, package identity and observed delivery path. "
        "Reopen Device Installation Settings and confirm the recorded Home preference persisted."
    )
    recurrence_gate = (
        "If repeat prevention is required, leave the exact returned package installed long "
        "enough to use as its own signed AppLocker reference, then continue to Section 6."
        if is_pro()
        else
        "Remove only the reconfirmed exact package again. If recurrence continues, collect "
        "the time and source and contact LG or Microsoft support. Do not install Group Policy "
        "or Local Security Policy hacks."
    )
    rows = [
        [
            "Registered or provisioned count is nonzero",
            "Display package name, publisher, type and full name again. Close the app; confirm other users are signed out; rerun only the exact removal block.",
            "Still nonzero: stop and inspect package state. Never delete WindowsApps manually.",
        ],
        [
            "The exact package returns later",
            recurrence_action,
            recurrence_gate,
        ],
        [
            "A different LG-named package appears",
            "Stop. Record its full name, family, publisher and delivery time.",
            "Do not substitute its name into this guide. Use the exact monitor model's official LG support page and obtain product-specific guidance.",
        ],
        [
            "OnScreen Control was needed",
            "Use the official LG support source to reinstall the intended version.",
            "Recheck firmware/settings access and the full monitor functional baseline.",
        ],
        [
            "A different app or device is affected",
            "Restore the edition-specific metadata setting through the same control plane used to change it.",
            "Restart and verify the recorded before-state.",
        ],
        [
            "DefenderRealTime is False",
            "Check whether another antivirus is active or the PC is managed.",
            "Do not change PUA settings until the antivirus authority is understood." + ref("compat"),
        ],
    ]
    story = page_heading(
        "5",
        "Use the failure ladder - do not skip ahead",
        (
            "Choose the row matching the observed result. The optional AppLocker path begins "
            "only after the exact tested package actually returns, not from uncertainty."
            if is_pro()
            else
            "Choose the row matching the observed result. Windows 11 Home uses the documented "
            "cleanup and verification path; do not add unofficial policy tools."
        ),
    )
    story += [
        standard_table(
            ["OBSERVED RESULT", "NEXT ACTION", "DECISION GATE"],
            rows,
            [190, 350, 196],
        ),
    ]
    if is_pro():
        story += [
            Spacer(1, 8),
            callout(
                "APPLOCKER ENTRY GATE",
                "Continue only when Section 5 recorded an actual return of the exact signed <font name='Consolas'>LGElectronics.LGMonitorApp</font> package, the tested local AppLocker console and cmdlets are available, the PC is personally managed, the current Appx policy is empty or fully understood, a complete local/effective policy backup exists, and you accept the compatibility testing burden. If the package is absent, the standard path is already clean; do not reinstall it just to create a rule.",
                CORAL,
                LIGHT_CORAL,
            ),
            Spacer(1, 8),
            callout(
                "WHAT APPLOCKER IS - AND IS NOT",
                "Microsoft documents AppLocker configuration and enforcement on current Windows 11 editions, but describes it as defense-in-depth rather than a security boundary. This runbook uses one narrow packaged-app deny, not a general application-control design. Do not adapt it by substituting another package name."
                + ref("requirements")
                + ref("kb")
                + ref("overview"),
                BLUE,
                LIGHT_BLUE,
            ),
        ]
    else:
        story += [
            Spacer(1, 8),
            callout(
                "HOME EDITION BOUNDARY",
                "Microsoft documents AppLocker support on current Windows 11 editions, but this guide deliberately omits the tested local authoring workflow because standard Home installations cannot be assumed to include the required local console and cmdlets. Do not install third-party Group Policy, Local Security Policy or AppLocker hacks. A returning package is evidence to trace the delivery path, not permission to improvise an enforcement rule."
                + ref("requirements")
                + ref("kb"),
                BLUE,
                LIGHT_BLUE,
            ),
        ]
    return story


def applocker_prepare_page():
    backup = r"""
# Optional path only. Run in Windows PowerShell 5.1 as Administrator.
$Package = 'LGElectronics.LGMonitorApp'
$ExpectedPublisher = 'CN=4A5401D9-32C2-486E-A8CB-EFECB124AF89'
$ExpectedPublisherId = 'cfnzzhwkr8z5w'
$ExpectedFamily = "${Package}_${ExpectedPublisherId}"
$Types = 'Main','Framework','Resource','Bundle','Optional'
$Target = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
if ($Target.Count -eq 0) {
    throw 'STOP: the returned tested package is not installed.'
}
if (@($Target | Where-Object {
    $_.Publisher -ne $ExpectedPublisher -or
    $_.PublisherId -ne $ExpectedPublisherId -or
    $_.PackageFamilyName -ne $ExpectedFamily
}).Count -gt 0) {
    throw 'STOP: returned signer or package family is not the tested identity.'
}

$Required = 'Get-AppLockerPolicy','Test-AppLockerPolicy'
$Missing = @($Required | Where-Object {
    -not (Get-Command $_ -ErrorAction SilentlyContinue)
})
if ($Missing.Count) { throw "STOP: missing AppLocker tools: $Missing" }

$ALRunId = '{0}-{1}' -f (Get-Date -Format 'yyyyMMdd-HHmmss'),
    ([guid]::NewGuid().ToString('N').Substring(0,8))
$ALRun = Join-Path ([Environment]::GetFolderPath('Desktop')) `
    "LG-AppLocker-$ALRunId"
New-Item -ItemType Directory -Path $ALRun -ErrorAction Stop | Out-Null
Get-AppLockerPolicy -Local -Xml -ErrorAction Stop |
    Set-Content "$ALRun\Local-Before.xml" -Encoding UTF8
Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop |
    Set-Content "$ALRun\Effective-Before.xml" -Encoding UTF8
[xml](Get-Content "$ALRun\Local-Before.xml" -Raw) | Out-Null
[xml](Get-Content "$ALRun\Effective-Before.xml" -Raw) | Out-Null
Get-CimInstance Win32_Service -Filter "Name='AppIDSvc'" -ErrorAction Stop |
    Select-Object Name,State,StartMode |
    Export-Clixml "$ALRun\AppIDSvc-Before.clixml"
$ALRun
"""
    service = r"""
sc.exe config appidsvc start=auto
Start-Service AppIDSvc
gpupdate /target:computer /force
Get-CimInstance Win32_Service -Filter "Name='AppIDSvc'" |
    Select-Object Name,State,StartMode
"""
    rows = [
        ["1", "Open <font name='Consolas'>secpol.msc</font> and go to Application Control Policies &gt; AppLocker.", "If the console is unavailable, stop. Do not install third-party Group Policy hacks."],
        ["2", "Inspect every collection and AppLocker Properties before editing.", "Existing/unfamiliar Appx rules, domain policy or CSP/MDM control: stop."],
        ["3", "Under Packaged app Rules, choose Create Default Rules only when no prior Appx design exists.", "Require the signed-packaged-app allow for Everyone." + ref("default_rules")],
        ["4", "AppLocker Properties &gt; Packaged app Rules: Configured / <b>Audit only</b>.", "Do not configure EXE, MSI, Script or DLL collections."],
        ["5", "Pass the Recovery Gate below, then run the service block.", "Expected: State = Running and StartMode = Auto." + ref("appidsvc")],
    ]
    story = page_heading(
        "6",
        "Optional AppLocker A - back up, inspect, start in Audit only",
        "This section is not part of the successful core path. It applies only after the Section 5 entry gate passes.",
    )
    story += [
        callout(
            "MANAGEMENT BOUNDARY",
            "Current Windows 11 editions support AppLocker, but this tested local GUI path requires <font name='Consolas'>secpol.msc</font> and the AppLocker cmdlets. Stop if either is unavailable and do not install third-party Group Policy hacks. These tools operate on local/Group Policy AppLocker, not AppLocker CSP; effective-policy output can also be incorrect for CSP deployment. Stop on MDM, domain policy or unfamiliar effective policy." + ref("requirements") + ref("get_policy") + ref("set_policy"),
            CORAL,
            LIGHT_CORAL,
        ),
        Spacer(1, 8),
        two_cards(
            code_card(
                "A - EXPORT AND PARSE LOCAL AND EFFECTIVE POLICY",
                backup,
                PURPLE,
                (CONTENT_W / 2) - 6,
            ),
            standard_table(
                ["STEP", "ACTION", "PASS CONDITION"],
                rows,
                [(CONTENT_W / 2 - 6) * 0.10, (CONTENT_W / 2 - 6) * 0.57, (CONTENT_W / 2 - 6) * 0.33],
                tiny=True,
            ),
        ),
        Spacer(1, 9),
        callout(
            "RECOVERY GATE",
            "Copy the complete AppLocker run folder to separate administrator-controlled storage and reopen both XML files. Policy export is not a software reinstall source. Microsoft states that AppIDSvc cannot be returned to Manual with <font name='Consolas'>sc.exe</font> and recommends a system backup before changing its startup type. Continue only when you accept that trade-off, the preexisting policy is understood and the Packaged app collection is visibly Audit only." + ref("appidsvc"),
            AMBER,
            LIGHT_AMBER,
        ),
        Spacer(1, 8),
        code_card("B - ONLY AFTER THE GATE: START AND VERIFY APPLICATION IDENTITY", service, TEAL),
    ]
    return story


def applocker_rule_page():
    test = r"""
$ALRun = '<paste exact LG-AppLocker-... folder path>'
$Package = 'LGElectronics.LGMonitorApp'
$Types = 'Main','Framework','Resource','Bundle','Optional'
$AuditStarted = Get-Date
$AuditStarted | Export-Clixml "$ALRun\Audit-Started.clixml"
gpupdate /target:computer /force
Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop |
    Set-Content "$ALRun\Effective-Audit.xml" -Encoding UTF8

$Target = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
if ($Target.Count -eq 0) { throw 'STOP: signed target package is absent.' }
$All = @(Get-AppxPackage -AllUsers -PackageTypeFilter $Types -ErrorAction Stop)
$TargetDenied = @($Target | Test-AppLockerPolicy `
    -XmlPolicy "$ALRun\Effective-Audit.xml" -User 'S-1-1-0' -Filter Denied)
$DeniedByDefault = @($All | Test-AppLockerPolicy `
    -XmlPolicy "$ALRun\Effective-Audit.xml" -User 'S-1-1-0' `
    -Filter DeniedByDefault)
[pscustomobject]@{
    TargetCount = $Target.Count
    TargetPredictedDenied = $TargetDenied.Count
    InstalledDeniedByDefault = $DeniedByDefault.Count
}
"""
    events = r"""
$ALRun = '<paste exact LG-AppLocker-... folder path>'
$Start = Import-Clixml "$ALRun\Audit-Started.clixml"
$Logs = 'Microsoft-Windows-AppLocker/Packaged app-Execution',
        'Microsoft-Windows-AppLocker/Packaged app-Deployment'
foreach ($Log in $Logs) {
    Get-WinEvent -FilterHashtable @{
        LogName=$Log; Id=8021,8024; StartTime=$Start
    } -ErrorAction SilentlyContinue |
        Select-Object TimeCreated,Id,Message
}
"""
    rows = [
        ["1", "Packaged app Rules &gt; Create New Rule", "Begin only while the collection is Audit only."],
        ["2", "Permissions", "<b>Deny</b> / <b>Everyone</b>."],
        ["3", "Condition", "<b>Publisher</b>."],
        ["4", "Reference", "Use installed packaged app: LG Monitor App Installer."],
        ["5", "Scope", "Package name = <font name='Consolas'>LGElectronics.LGMonitorApp</font>; version = all; no exceptions."],
        ["6", "Name", "<b>Block LG Monitor App Installer</b>."],
        ["7", "Review", "Keep the default signed-package allow. One narrow deny only." + ref("precedence")],
    ]
    story = page_heading(
        "7",
        "Optional AppLocker B - create the exact deny and test it",
        "Create one package-name rule from the installed signed reference. Then predict the result before any enforcement.",
    )
    story += [
        standard_table(
            ["STEP", "WIZARD PAGE", "EXACT VALUE"],
            rows,
            [48, 180, 508],
        ),
        Spacer(1, 9),
        two_cards(
            code_card(
                "A - EXPORT AUDIT POLICY AND SIMULATE INSTALLED PACKAGES",
                test,
                BLUE,
                (CONTENT_W / 2) - 6,
            ),
            code_card(
                "B - AFTER REAL USE, REVIEW WOULD-BE DENIAL EVENTS",
                events,
                AMBER,
                (CONTENT_W / 2) - 6,
            ),
        ),
        Spacer(1, 9),
        callout(
            "DEFINED COMPATIBILITY SESSION",
            "After recording AuditStarted, exercise Start, Settings, Microsoft Store, one built-in Store app, Xbox/Game Bar if used, Discord or other Store apps if applicable, Steam/Epic, mod tools and the normal monitor-control workflow. A zero-event result means little if this workload did not run. Investigate every 8021/8024 event." + ref("events") + ref("test_policy"),
            AMBER,
            LIGHT_AMBER,
        ),
        Spacer(1, 7),
        callout(
            "PASS BEFORE ENFORCEMENT",
            "TargetPredictedDenied must equal TargetCount; InstalledDeniedByDefault must be 0; the target publisher and package name must match; the default signed-package allow must remain; and no required application may have an unexplained would-be denial. Otherwise remain in Audit only.",
            GREEN,
            LIGHT_GREEN,
        ),
    ]
    return story


def applocker_enforce_page():
    verify = r"""
$ALRun = '<paste exact LG-AppLocker-... folder path>'
$Package = 'LGElectronics.LGMonitorApp'
$RuleName = 'Block LG Monitor App Installer'
$Types = 'Main','Framework','Resource','Bundle','Optional'
gpupdate /target:computer /force
Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop |
    Set-Content "$ALRun\Effective-Enforced.xml" -Encoding UTF8
[xml]$Policy = Get-Content "$ALRun\Effective-Enforced.xml" -Raw
$Appx = @($Policy.AppLockerPolicy.RuleCollection |
    Where-Object Type -eq 'Appx')
$Target = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
$All = @(Get-AppxPackage -AllUsers -PackageTypeFilter $Types -ErrorAction Stop)
$Denied = @($Target | Test-AppLockerPolicy `
    -XmlPolicy "$ALRun\Effective-Enforced.xml" -User 'S-1-1-0' -Filter Denied)
$DefaultDenied = @($All | Test-AppLockerPolicy `
    -XmlPolicy "$ALRun\Effective-Enforced.xml" -User 'S-1-1-0' `
    -Filter DeniedByDefault)
[pscustomobject]@{
    AppxMode = $Appx.EnforcementMode
    TargetCount = $Target.Count
    TargetPredictedDenied = $Denied.Count
    InstalledDeniedByDefault = $DefaultDenied.Count
}
if ($Target.Count -eq 0 -or $Appx.Count -ne 1 -or
    $Appx.EnforcementMode -ne 'Enabled' -or
    $Denied.Count -ne $Target.Count -or $DefaultDenied.Count -ne 0) {
    throw 'STOP: enforcement precheck failed.'
}

$EnforcementStarted = Get-Date
$EnforcementStarted |
    Export-Clixml "$ALRun\Enforcement-Started.clixml"
Read-Host 'Smoke-test required apps, attempt LG once, then press Enter'

$Logs = 'Microsoft-Windows-AppLocker/Packaged app-Execution',
        'Microsoft-Windows-AppLocker/Packaged app-Deployment'
$DenyEvents = @(foreach ($Log in $Logs) {
    Get-WinEvent -FilterHashtable @{
        LogName=$Log; Id=8022,8025; StartTime=$EnforcementStarted
    } -ErrorAction SilentlyContinue
})
$TargetDenyEvents = @($DenyEvents | Where-Object {
    $_.Message -match [regex]::Escape($Package) -and
    $_.Message -match [regex]::Escape($RuleName)
})
if ($TargetDenyEvents.Count -lt 1) {
    throw 'STOP: no real target deny event was found.'
}
[pscustomobject]@{
    EnforcedTargetDenyEventCount = $TargetDenyEvents.Count
}
$TargetDenyEvents | Select-Object TimeCreated,Id,Message
"""
    rows = [
        ["1", "Review the Section 7 pass criteria again.", "Every condition still passes; recovery XML opens."],
        ["2", "AppLocker Properties &gt; Packaged app Rules: switch only this collection to <b>Enforce rules</b>.", "EXE, MSI, Script and DLL remain unchanged."],
        ["3", "Run the verification block. It stops at a prompt after the policy precheck.", "<font name='Consolas'>AppxMode = Enabled</font>; target denied count equals target count; denied-by-default = 0."],
        ["4", "While the block waits, smoke-test required packaged apps and attempt the LG package once; then press Enter.", "No unrelated block. At least one new 8022/8025 event names the exact package and rule."],
        ["5", "Only now rerun the Section 3 removal block.", "Registered and provisioned counts both return 0."],
        ["6", "Restart and rerun Section 4. In <font name='Consolas'>secpol.msc</font>, recheck the exact deny, default allow and Appx Enforce mode; rerun the Section 6 service query.", "Core checks pass; AppIDSvc is Running/Auto; the intended Appx rules and mode remain."],
    ]
    story = page_heading(
        "8",
        "Optional AppLocker C - enforce, smoke-test, then remove",
        "Enforcement is its own decision. Do not combine the click, cleanup and verification into one opaque action.",
    )
    story += [
        callout(
            "ENFORCEMENT GATE",
            "AppLocker enforcement applies immediately and a deny overrides an allow. If any required app is unexpectedly affected, return the Packaged app collection to Audit only before doing anything else. Do not create a broad exception to make the symptom disappear." + ref("precedence") + ref("audit_enforce"),
            CORAL,
            LIGHT_CORAL,
        ),
        Spacer(1, 8),
        two_cards(
            standard_table(
                ["STEP", "ACTION", "PASS CONDITION"],
                rows,
                [(CONTENT_W / 2 - 6) * 0.09, (CONTENT_W / 2 - 6) * 0.55, (CONTENT_W / 2 - 6) * 0.36],
                tiny=True,
            ),
            code_card(
                "VERIFY, TEST AND CAPTURE THE ENFORCED DENY",
                verify,
                CORAL,
                (CONTENT_W / 2) - 6,
                compact=True,
            ),
        ),
        Spacer(1, 9),
        callout(
            "FINAL APPLOCKER PASS",
            "Require <font name='Consolas'>EnforcedTargetDenyEventCount</font> of at least 1 plus a clean smoke test, not merely predicted denial. The event must name the exact package and rule. After cleanup and restart, use Section 4, the AppLocker UI and the Section 6 service query; do not rerun the target-event block after the target is removed." + ref("events"),
            GREEN,
            LIGHT_GREEN,
        ),
    ]
    return story


def pua_page():
    commands = r"""
$RunDir = '<paste exact LG-Run-... folder path>'
$AuditStartPath = Join-Path $RunDir 'PUA-Audit-Started.clixml'
$Status = Get-MpComputerStatus
$Before = (Get-MpPreference).PUAProtection
$Status | Select-Object AMRunningMode,AntivirusEnabled,
    RealTimeProtectionEnabled
[pscustomobject]@{ PUAProtection = $Before }

# Decision:
# 1: keep blocking; 2: keep Audit; 0: stage Audit only if active/unmanaged.
# Preserve the first audit-start timestamp across reruns.
if ($Before -in 0,2 -and
    -not (Test-Path -LiteralPath $AuditStartPath)) {
    [pscustomobject]@{ Captured=Get-Date; PUAProtection=[int]$Before } |
        Export-Clixml $AuditStartPath
}
if ($Before -eq 0 -and $Status.AMRunningMode -eq 'Normal' -and
    $Status.AntivirusEnabled -and $Status.RealTimeProtectionEnabled) {
    Set-MpPreference -PUAProtection AuditMode
}
(Get-MpPreference).PUAProtection
"""
    events = r"""
$RunDir = '<paste exact LG-Run-... folder path>'
$AuditStartPath = Join-Path $RunDir 'PUA-Audit-Started.clixml'
if (-not (Test-Path -LiteralPath $AuditStartPath)) {
    throw 'STOP: the audit-start record is missing.'
}
$Start = (Import-Clixml $AuditStartPath).Captured
if ($null -eq $Start) { throw 'STOP: invalid audit-start record.' }
Get-WinEvent -FilterHashtable @{
    LogName='Microsoft-Windows-Windows Defender/Operational'
    Id=1160
    StartTime=$Start
} -ErrorAction SilentlyContinue |
    Select-Object TimeCreated,Id,Message
"""
    promote = r"""
Set-MpPreference -PUAProtection Enabled
Update-MpSignature
$ScanRequested = Get-Date
Start-MpScan -ScanType QuickScan
$Status = Get-MpComputerStatus
[pscustomobject]@{
    PUAProtection = (Get-MpPreference).PUAProtection
    QuickScanEndTime = $Status.QuickScanEndTime
    FreshScanCompleted = $Status.QuickScanEndTime -ge $ScanRequested
}
"""
    story = page_heading(
        "9" if is_pro() else "6",
        "Detached option - Defender PUA protection",
        "Stop after the core path passes. This separate, general Windows control is not LG-specific and is not required for package cleanup.",
    )
    story += [
        callout(
            "STOP CONDITIONS - READ BEFORE THE COMMAND",
            "Skip this change when another antivirus is active, Defender is passive, policy is organization-managed, Tamper Protection prevents the write or compatibility is unclear. Do not add broad game-library or application exclusions as a substitute for investigating a specific detection." + ref("pua") + ref("compat"),
            CORAL,
            LIGHT_CORAL,
        ),
        Spacer(1, 8),
        two_cards(
            code_card(
                "CHECK FIRST; NEVER WEAKEN AN ALREADY ENABLED STATE",
                commands,
                PURPLE,
                (CONTENT_W / 2) - 6,
                compact=True,
            ),
            standard_table(
                ["VALUE", "MEANING", "ACTION"],
                [
                    ["0", "Disabled", "If Defender is active and unmanaged, Audit mode is the cautious first change."],
                    ["1", "Enabled / blocking", "Pass. Keep it. Do not lower it to reproduce this guide."],
                    ["2", "Audit mode", "Keep it while testing. Review only events created after the recorded audit start."],
                ],
                [(CONTENT_W / 2 - 6) * 0.14, (CONTENT_W / 2 - 6) * 0.32, (CONTENT_W / 2 - 6) * 0.54],
            ),
        ),
        Spacer(1, 4),
        code_card(
            "IF VALUE IS 2, TEST NORMAL USE, THEN REVIEW ONLY NEW AUDIT EVENTS",
            events,
            TEAL,
            compact=True,
        ),
        Spacer(1, 4),
        two_cards(
            code_card(
                "ONLY AFTER A CLEAN AUDIT: ENABLE, UPDATE, SCAN AND VERIFY",
                promote,
                GREEN,
                (CONTENT_W / 2) - 6,
                compact=True,
            ),
            card(
                "Expected result, restart and recovery",
                "<font name='Consolas'>PUAProtection = 1</font> and "
                "<font name='Consolas'>FreshScanCompleted = True</font>. "
                "No restart is normally required; follow any Windows Security "
                "prompt. If either result fails, remain in Audit mode or restore "
                "the recorded prior value in Rollback. Smart App Control is "
                "separate; this guide neither requires nor changes it.",
                BLUE,
                LIGHT_BLUE,
            ),
        ),
    ]
    return story


def rollback_page():
    pua_restore = r"""
$RunDir = '<paste exact LG-Run-... folder path>'
$Before = Import-Clixml "$RunDir\Defender-Before.clixml"
Set-MpPreference -PUAProtection ([int]$Before.PUAProtection)
(Get-MpPreference).PUAProtection
"""
    rows = [
        [
            "Metadata side effect",
            (
                "Restore the prior Local Group Policy state through Local Group Policy, refresh policy and verify."
                if is_pro()
                else
                "Reopen Device Installation Settings and restore the exact choice recorded before the change."
            ),
            "The recorded setting and affected peripheral workflow return.",
        ],
        [
            "PUA compatibility issue",
            "Run the exact-state restore block. Do not create a broad exclusion.",
            "PUAProtection equals the value recorded before the guide.",
        ],
        [
            "Needed LG function was removed",
            "Reinstall only the intended application from the recorded official LG source.",
            "Firmware/settings access works; package state is re-inventoried." + ref("lg_support"),
        ],
    ]
    if is_pro():
        rows = [
            [
                "Unexpected AppLocker block",
                "Immediately set Packaged app Rules back to <b>Audit only</b>, refresh Group Policy, then delete only <b>Block LG Monitor App Installer</b> and refresh again.",
                "Required apps run; exact LG deny is absent. Keep AppIDSvc running while troubleshooting." + ref("delete_rule"),
            ],
            [
                "AppLocker baseline must be restored",
                "Prefer restoring the guide-owned Appx collection, rule and mode manually. Use full local-policy replacement only as the last resort below. Do not try to return AppIDSvc to Manual with sc.exe.",
                "Local policy matches the captured before-state; any retained Automatic service state is documented. Never import Effective-Before.xml." + ref("appidsvc"),
            ],
        ] + rows
    story = page_heading(
        "10" if is_pro() else "7",
        "Rollback - reverse the smallest layer first",
        "Rollback should restore the recorded before-state, not merely make an error disappear. Removed applications require reinstallation.",
    )
    story += [
        standard_table(
            ["PROBLEM", "FIRST RECOVERY ACTION", "PASS RESULT"],
            rows,
            [170, 360, 206],
        ),
        Spacer(1, 9),
    ]
    if is_pro():
        emergency = r"""
# LAST RESORT: local/unmanaged AppLocker only.
# Saved local XML must be known-good; no later AppLocker changes.
$ALRun = '<paste exact LG-AppLocker-... folder path>'
$Backup = Join-Path $ALRun 'Local-Before.xml'
[xml](Get-Content -LiteralPath $Backup -Raw -ErrorAction Stop) | Out-Null
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$Current = Join-Path $ALRun "Local-Before-Emergency-$Stamp.xml"
Get-AppLockerPolicy -Local -Xml -ErrorAction Stop |
    Set-Content $Current -Encoding UTF8
[xml](Get-Content $Current -Raw -ErrorAction Stop) | Out-Null
Set-AppLockerPolicy -XmlPolicy $Backup -WhatIf
$Confirm = Read-Host 'Type REPLACE LOCAL APPLOCKER POLICY to continue'
if ($Confirm -cne 'REPLACE LOCAL APPLOCKER POLICY') {
    throw 'STOP: full-policy replacement was not confirmed.'
}
Set-AppLockerPolicy -XmlPolicy $Backup -ErrorAction Stop
gpupdate /target:computer /force
Get-AppLockerPolicy -Local -Xml -ErrorAction Stop |
    Set-Content "$ALRun\Local-After-Restore.xml" -Encoding UTF8
Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop |
    Set-Content "$ALRun\Effective-After-Restore.xml" -Encoding UTF8
"""
        story += [
            callout(
                "FULL-POLICY REPLACEMENT GATE - READ BEFORE THE COMMAND",
                "Do not use the emergency command on a managed PC, for CSP/MDM policy, after unrelated policy changes or with an unverified backup. It replaces local policy; it is not a merge. Review <font name='Consolas'>-WhatIf</font> output and the newly exported current policy before typing the exact confirmation. Reopen both after-state XML files, compare intended collections, rules and modes, then restart and rerun the relevant functional checks."
                + ref("set_policy"),
                CORAL,
                LIGHT_CORAL,
            ),
            Spacer(1, 8),
            two_cards(
                code_card(
                    "LAST RESORT: FULL LOCAL APPLOCKER RESTORE",
                    emergency,
                    CORAL,
                    (CONTENT_W / 2) - 6,
                ),
                code_card(
                    "RESTORE THE EXACT PRIOR DEFENDER PUA VALUE",
                    pua_restore,
                    PURPLE,
                    (CONTENT_W / 2) - 6,
                ),
            ),
        ]
    else:
        story += [
            code_card(
                "RESTORE THE EXACT PRIOR DEFENDER PUA VALUE",
                pua_restore,
                PURPLE,
            ),
            Spacer(1, 8),
            callout(
                "HOME RECOVERY BOUNDARY",
                "Do not install policy editors or security-policy hacks to reproduce the Pro rollback. Restore only the Home preference, Defender value or LG software layer actually changed, then restart only when the affected workflow requires it.",
                AMBER,
                LIGHT_AMBER,
            ),
        ]
    return story


def references_page():
    rows = []
    keys = list(REFS)
    if not is_pro():
        keys = [
            "requirements",
            "kb",
            "get_appx",
            "remove_appx",
            "get_prov",
            "remove_prov",
            "pua",
            "compat",
            "device_apps",
            "inf_addsoftware",
            "lg_support",
            "lg_osc",
            "store_app",
            "driver_container",
            "system_tools",
        ]
    for key in keys:
        number, title, url = REFS[key]
        rows.append(
            [
                para(f"<b>{number:02d}</b>", "Source"),
                para(escape(title), "Source"),
                para(
                    f"<link href='{url}' color='#315FC4'><b>Open official source</b></link>",
                    "Source",
                ),
            ]
        )
    story = page_heading(
        "11" if is_pro() else "8",
        "Authoritative references",
        f"Microsoft and LG primary documentation reviewed for guide version {GUIDE_VERSION} on {PREPARED}. Current vendor documentation takes precedence if it changes.",
    )
    story += [
        standard_table(
            ["#", "SOURCE", "URL"],
            rows,
            [30, 252, 454],
            tiny=True,
        )
    ]
    return story


def build_story():
    sections = [
        cover_page(),
        preflight_page(),
        metadata_page(),
        removal_page(),
        verify_page(),
        failure_page(),
    ]
    if is_pro():
        sections.extend(
            [
                applocker_prepare_page(),
                applocker_rule_page(),
                applocker_enforce_page(),
            ]
        )
    sections.extend([pua_page(), rollback_page(), references_page()])
    story = []
    for index, section in enumerate(sections):
        story.extend(section)
        if index != len(sections) - 1:
            story.append(PageBreak())
    return story


class GuideDocTemplate(BaseDocTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._outline_counter = 0

    def afterFlowable(self, flowable):
        if isinstance(flowable, CoverHero):
            self.canv.bookmarkPage("cover")
            self.canv.addOutlineEntry(pdf_title(), "cover", level=0, closed=False)
            return
        if isinstance(flowable, Paragraph) and flowable.style.name == "PageTitle":
            self._outline_counter += 1
            key = f"section-{self._outline_counter}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(
                flowable.getPlainText(), key, level=0, closed=False
            )


def build_one(edition: str, output: Path) -> None:
    global ACTIVE_EDITION
    ACTIVE_EDITION = edition
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    frame = Frame(
        MARGIN_X,
        BOTTOM,
        CONTENT_W,
        PAGE_H - TOP - BOTTOM,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="main",
    )
    template = PageTemplate(id="brand", frames=[frame], onPageEnd=page_header_footer)
    doc = GuideDocTemplate(
        str(output),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        pageTemplates=[template],
        title=pdf_title(),
        author="Amyashi",
        subject=(
            f"Ordered {edition_name()} cleanup, recurrence mitigation, verification "
            "and recovery runbook for LG monitor companion software"
        ),
        allowSplitting=1,
        invariant=1,
    )
    doc.build(build_story())
    print(output)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the LG monitor companion-software mitigation runbooks."
    )
    parser.add_argument(
        "--edition",
        choices=("home", "pro", "all"),
        default="all",
        help="edition to build (default: all)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT,
        help="directory for default output filenames",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="custom output PDF; valid only with --edition home or --edition pro",
    )
    args = parser.parse_args(argv)
    if args.edition == "all" and args.output is not None:
        parser.error("--output requires --edition home or --edition pro")
    editions = ("home", "pro") if args.edition == "all" else (args.edition,)
    output_dir = args.output_dir.expanduser().resolve()
    for edition in editions:
        output = (
            args.output
            if args.output is not None
            else output_dir / OUTPUT_FILENAMES[edition]
        )
        build_one(edition, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
