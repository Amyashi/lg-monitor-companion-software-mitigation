# LG Monitor Companion Software: Cleanup and Recurrence Mitigation

## Windows 11 Home runbook

Author: Amyashi

Version 1.0.0. Reviewed 2026-07-29.

This is the substantive, screen-reader-friendly companion to the Windows 11
Home PDF. Follow the numbered steps in order.

This independent, unofficial guide is not an LG Electronics or Microsoft
publication, endorsement, support channel, incident-response substitute,
security certification, or guarantee. Use it only on a PC you own or are
authorized to administer. Review every command, path, expected result, and undo
instruction before running an elevated command.

**Home validation status:** This edition is documentation-derived and
structurally validated, but it has not been field-tested on a Windows 11 Home
machine. Confirm every effective result locally and stop on any mismatch.

## Documented example and exact target

This procedure was developed from an LG 45GR95QE-B case involving:

- Microsoft Store product **LG Monitor App Installer**;
- Store ID `9PM9N6F47JB8`;
- Store publisher **LG Electronics Inc.**;
- Windows package name `LGElectronics.LGMonitorApp`; and
- the separate LG **OnScreen Control** desktop application.

The monitor model is provenance, not an eligibility rule. Other LG monitors
can use different applications, package identities, installers, firmware
tools, or delivery paths. Before acting:

1. Open the [official LG support site][2] and find the page for the exact
   monitor model.
2. Open [Microsoft Store product 9PM9N6F47JB8][1].
3. Confirm the Store page says **LG Monitor App Installer** and the publisher
   is **LG Electronics Inc.**
4. Continue only if Windows reports the exact package name
   `LGElectronics.LGMonitorApp` and its installed publisher identity is
   expected.

If the exact package is absent, its Store reference does not match, its
installed publisher is unexpected, or a different LG-named package appears,
stop. Never substitute another package name into these commands.

OnScreen Control is not the Store package. Decide whether to keep or remove it
as a separate action.

## The ordered Home path

1. Pass the authority, firmware, physical-control, and recovery gates.
2. Confirm Windows 11 Home and capture the before-state.
3. Set the Home Device Installation Settings preference.
4. Remove only the exact Store package from current and future users.
5. Decide separately whether to keep OnScreen Control.
6. Restart once and verify.
7. Stop when every core result passes.
8. Use the failure or undo branch only when needed.

Windows 11 Home does not include the tested local AppLocker-management path
used in the Pro runbook. This Home runbook intentionally contains no AppLocker
implementation. Do not install third-party Group Policy Editor, Local Security
Policy, or AppLocker hacks.

---

## 1. Before you start

### Action

Pass every gate before changing Windows:

- Open **Settings -> Accounts -> Access work or school**.
- Confirm no organization manages the PC.
- Confirm no LG monitor firmware update is running.
- Record the exact monitor model and open its official LG support page.
- Confirm a working remote or physical control path, or deliberately accept
  losing software-only monitor controls.
- Preserve a current data backup and a tested administrator sign-in.
- Understand that policy/state exports do not reinstall removed software.

### Expected result

Continue only when:

- this is a personally administered Windows 11 Home PC;
- the PC is not domain-, MDM-, or CSP-managed;
- no firmware update is active;
- the official recovery source is known;
- the physical or alternate control decision is understood; and
- the backup and administrator sign-in have been tested.

### Restart?

No.

### If it fails

Stop. Use the responsible administrator's managed-device workflow, allow the
firmware update to finish, restore a working control path, or establish
recovery before continuing.

### Undo

No Windows setting has changed yet.

---

## 2. Step 0 - confirm Home and capture the before-state

Open **Windows PowerShell 5.1 as Administrator**. Keep the same window open
through Step 2.

### Run this

```powershell
$ErrorActionPreference = 'Stop'
$ExpectedEdition = 'Windows 11 Home'
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

if (-not $IsAdmin) {
    throw 'STOP: reopen Windows PowerShell as Administrator.'
}
if ($Computer.PartOfDomain) {
    throw 'STOP: use the managed-device workflow.'
}
if ($Os.Caption -notmatch [regex]::Escape($ExpectedEdition)) {
    throw "STOP: this is the $ExpectedEdition guide; detected $($Os.Caption)."
}

$RunId = '{0}-{1}' -f (Get-Date -Format 'yyyyMMdd-HHmmss'),
    ([guid]::NewGuid().ToString('N').Substring(0,8))
$RunDir = Join-Path ([Environment]::GetFolderPath('Desktop')) "LG-Run-$RunId"
New-Item -ItemType Directory -Path $RunDir -ErrorAction Stop | Out-Null

$Package = 'LGElectronics.LGMonitorApp'
$Types = 'Main','Framework','Resource','Bundle','Optional'

Get-AppxPackage -AllUsers -Name $Package -PackageTypeFilter $Types |
    Export-Clixml "$RunDir\Registered-Before.clixml"
Get-AppxProvisionedPackage -Online |
    Where-Object DisplayName -eq $Package |
    Export-Clixml "$RunDir\Provisioned-Before.clixml"
Get-MpPreference | Select-Object PUAProtection |
    Export-Clixml "$RunDir\Defender-Before.clixml"

Get-AppxPackage -AllUsers -Name $Package -PackageTypeFilter $Types |
    Select-Object Name,Publisher,PublisherId,PackageFamilyName,PackageFullName
Get-AppxProvisionedPackage -Online |
    Where-Object DisplayName -eq $Package |
    Select-Object DisplayName,PublisherId,PackageName

Get-ChildItem -LiteralPath $RunDir |
    Select-Object Name,Length,LastWriteTime
$RunDir
```

Before continuing, run `SystemPropertiesHardware.exe` and select **Device
Installation Settings**. The longer path is **Control Panel -> System and
Security -> System -> Advanced system settings -> Hardware -> Device
Installation Settings**. Record the current choice. A sanitized screenshot
saved in the `LG-Run-...` folder is acceptable.

Open each saved `.clixml` file:

```powershell
Get-ChildItem -LiteralPath $RunDir -Filter '*.clixml' |
    ForEach-Object {
        Import-Clixml -LiteralPath $_.FullName -ErrorAction Stop | Out-Null
        [pscustomobject]@{ File = $_.Name; Readable = $true }
    }
```

Copy the complete `LG-Run-...` folder to separate,
administrator-controlled storage and reopen the copy.

### Expected result

- `WindowsEdition` contains `Windows 11 Home`.
- `Administrator = True`.
- `DomainJoined = False`.
- Every saved file reports `Readable = True`.
- The separate recovery copy opens.
- The original Device Installation Settings choice is recorded.
- Any installed target shows the exact package name and one consistent,
  expected signed publisher identity.

Zero package results mean the exact target is already absent. Do not reinstall
it merely to complete this guide.

### Restart?

No.

### If it fails

- Wrong edition: use the Windows 11 Pro runbook when Pro is installed.
- Domain or organization management: stop and contact the responsible
  administrator.
- Unexpected publisher or package identity: stop and investigate.
- Unreadable recovery copy: recreate and test it before any change.

### Undo

No Windows setting or package state has changed.

---

## 3. Step 1 - set the Windows 11 Home preference

### Do this

1. Run `SystemPropertiesHardware.exe`.[13] Alternatively, open **Control Panel ->
   System and Security -> System -> Advanced system settings -> Hardware**.
2. Select **Device Installation Settings**.
3. Choose the option that does not automatically download manufacturer
   applications and custom icons.
4. Save the choice.
5. Reopen the dialog.

### Expected result

The dialog reopens with the chosen preference still selected.

This is a broader, weaker Home preference. It is not the documented Pro policy,
and no Pro policy-registry value is expected. Do not force the Pro-only policy
onto Home and do not install third-party policy-editor hacks.

This preference is not a universal block for:

- manual Microsoft Store acquisition;
- Windows Update drivers;
- OEM provisioning;
- Driver Package Container Metadata;
- driver-INF `AddSoftware`; or
- conventional Win32 installers.[8][9][10]

### Restart?

Not yet. Continue to Step 2.

### If it fails

If the option is missing, managed, or does not persist, stop. Do not use an
undocumented registry substitute.

### Undo

Reopen the same dialog and restore the exact choice recorded in Step 0.
Restart, then verify the affected peripheral workflow.

---

## 4. Step 2 - remove only the exact LG Store package

### All-user and identity warning

This action affects every Windows account:

- `Remove-AppxPackage -AllUsers` removes installed registrations for the exact
  target from all current user accounts; and
- `Remove-AppxProvisionedPackage -AllUsers` removes online provisioning so the
  exact target is not automatically staged for future user profiles.

Reinstallation is required to undo software removal. Before typing `REMOVE`,
open Store product `9PM9N6F47JB8` and reconfirm **LG Monitor App Installer**,
publisher **LG Electronics Inc.** The command displays the installed package
name, publisher, publisher ID, family, and full identity.

The tested signed identity is:

- publisher: `CN=4A5401D9-32C2-486E-A8CB-EFECB124AF89`;
- publisher ID: `cfnzzhwkr8z5w`; and
- package family: `LGElectronics.LGMonitorApp_cfnzzhwkr8z5w`.

The command fails closed if any installed identity differs. These values record
the tested package; they are not a promise about a future LG release. Stop and
revalidate rather than weakening the check. Never manually delete files from
`C:\Program Files\WindowsApps`.

### Run this

```powershell
$Package = 'LGElectronics.LGMonitorApp'
$ExpectedPublisher = 'CN=4A5401D9-32C2-486E-A8CB-EFECB124AF89'
$ExpectedPublisherId = 'cfnzzhwkr8z5w'
$ExpectedFamily = "${Package}_${ExpectedPublisherId}"
$Types = 'Main','Framework','Resource','Bundle','Optional'
$Targets = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
$Provisioned = @(Get-AppxProvisionedPackage -Online -ErrorAction Stop |
    Where-Object DisplayName -eq $Package)

$Targets |
    Select-Object Name,Publisher,PublisherId,PackageFamilyName,PackageFullName
$Provisioned |
    Select-Object DisplayName,PublisherId,PackageName

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
    if ($Confirm -cne 'REMOVE') {
        throw 'STOP: removal was not confirmed.'
    }

    if ($Targets.Count -gt 0) {
        $Bundles = @(Get-AppxPackage -AllUsers -Name $Package `
            -PackageTypeFilter Bundle -ErrorAction Stop)
        $Mains = @(Get-AppxPackage -AllUsers -Name $Package `
            -PackageTypeFilter Main -ErrorAction Stop)
        $Parents = if ($Bundles.Count -gt 0) { $Bundles } else { $Mains }

        if ($Parents.Count -eq 0) {
            throw 'STOP: child packages exist without a removable parent.'
        }

        $Parents |
            Sort-Object PackageFullName -Unique |
            ForEach-Object {
                Remove-AppxPackage -Package $_.PackageFullName -AllUsers `
                    -ErrorAction Stop
            }
    }

    $Provisioned |
        ForEach-Object {
            Remove-AppxProvisionedPackage -Online -AllUsers `
                -PackageName $_.PackageName -ErrorAction Stop |
                Out-Null
        }
}
```

Verify both stores of package state:

```powershell
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
```

### Expected result

- `RegisteredPackageCount = 0`.
- `ProvisionedPackageCount = 0`.

### Restart?

Not yet. Make the separate OnScreen Control decision first.

### If it fails

Do not repeat removal blindly. Go to **Failure branch A**.

### Undo

Removed software cannot be restored from the state exports. Reinstall only when
intentionally required, using the confirmed Microsoft Store product or the
official LG support page for the exact monitor model. Re-inventory after
installation.

---

## 5. Decide about LG OnScreen Control separately

### Do this

Keep OnScreen Control when it is useful for firmware updates, picture presets,
monitor settings, or another known workflow. Its presence does not invalidate
the Store-package cleanup.

Remove it only when:

- no firmware update is active;
- a working remote or physical control path exists, or the loss is accepted;
  and
- software-only features are not needed.

To remove it:

1. Open **Settings -> Apps -> Installed apps**.
2. Find the exact LG-published **OnScreen Control** entry.
3. Select **Uninstall**.
4. Follow the vendor uninstaller.

If unsure, keep it. Do not manually delete broad `LG` matches; similarly named
software can be unrelated.

### Expected result

The installed-app state matches the decision:

- **Keep:** OnScreen Control still opens and performs the required task.
- **Remove:** its exact Installed Apps entry is absent.

### Restart?

Yes. Restart Windows once after completing the package and OnScreen Control
decisions.

### If it fails

- Uninstaller fails: stop and use the exact application's repair/uninstall
  options or LG support guidance.
- Firmware/settings access was lost: use **Failure branch D**.

### Undo

Reinstall only the intended OnScreen Control version from the official LG
support page for the exact monitor model. Recheck firmware and settings access.

---

## 6. Step 3 - restart once, then verify

After signing in, wait for the desktop to settle. Reopen Windows PowerShell 5.1
as Administrator.

### Run this

```powershell
$Package = 'LGElectronics.LGMonitorApp'
$Types = 'Main','Framework','Resource','Bundle','Optional'
$Registered = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
$Provisioned = @(Get-AppxProvisionedPackage -Online -ErrorAction Stop |
    Where-Object DisplayName -eq $Package)
$Defender = Get-MpComputerStatus

[pscustomobject]@{
    WindowsEdition = (Get-CimInstance Win32_OperatingSystem).Caption
    RegisteredPackageCount = $Registered.Count
    ProvisionedPackageCount = $Provisioned.Count
    DefenderRealTime = $Defender.RealTimeProtectionEnabled
}
```

Reopen Device Installation Settings and confirm the Home preference remains
selected.

Test the actual monitor baseline used on this PC:

- intended resolution;
- intended refresh rate;
- VRR/G-Sync or Adaptive-Sync, if used;
- HDR, if used;
- audio, if used;
- input switching; and
- the chosen remote, physical, or software control path.

Do not assume every LG monitor has the tested example's resolution, refresh
rate, or feature set. Compare against the exact model's LG documentation and
the user's recorded before-state.

### Expected result

- `WindowsEdition` contains `Windows 11 Home`.
- `RegisteredPackageCount = 0`.
- `ProvisionedPackageCount = 0`.
- The Home preference remains selected.
- `DefenderRealTime = True` when Microsoft Defender is the active antivirus.
- Every required monitor function passes.
- The OnScreen Control state matches the user's decision.

If every core result passes, stop. The Home mitigation is complete. Do not add
unsupported policy tools or optional Defender changes merely to make the guide
look more complete.

### Restart?

No additional restart is required when everything passes.

### If it fails

Use the first matching failure branch below.

### Undo

Reverse only the layer causing the problem; do not undo successful,
unrelated layers.

---

## 7. Failure and undo branches

### Failure branch A - registered or provisioned count is nonzero

1. Display package name, publisher, publisher ID, family, type, and full
   identity again.
2. Close the application.
3. Sign out other Windows users.
4. Rerun only the exact removal block once.
5. Recheck both counts.

Still nonzero: stop and inspect package state. Never delete `WindowsApps`
manually.

### Failure branch B - the exact package returns

1. Record the time it returned.
2. Record name, publisher, publisher ID, package type, family, and full
   identity.
3. Reconfirm the Home Device Installation Settings preference.
4. Review Store, Windows Update, OEM, driver, and manual-install activity.
5. Do not assume which delivery path was responsible.

The Home path does not provide the tested local AppLocker implementation. Do
not install policy-editor or AppLocker hacks. Preserve evidence and use the
responsible support or administration channel if stronger recurrence
prevention is required.

### Failure branch C - an unexpected LG package appears

Stop. Do not change `$Package` to match it. Identify the exact product,
publisher, purpose, and official source first. This runbook authorizes actions
only against `LGElectronics.LGMonitorApp`.

### Failure branch D - OnScreen Control was needed

Reinstall only the intended version from the exact model's official LG support
page. Recheck the full monitor baseline and package inventory.

### Failure branch E - another application or peripheral is affected

Restore the original Device Installation Settings choice through the same
dialog. Restart and verify both the affected peripheral and the LG monitor
baseline.

### Failure branch F - Defender real-time protection is false

Determine whether another antivirus is active or the PC is managed. Do not
change Defender PUA settings until antivirus authority is understood.

---

## 8. Detached option - Microsoft Defender PUA evaluation

Potentially unwanted application protection is a general
reputation/behavior layer. It is not an LG-specific rule, is not required for
core cleanup, and does not guarantee classification of an LG package.[11][12]

Stop after the core LG path passes. Continue here only for a separately
documented Windows security requirement.

Skip this section when Microsoft Defender is passive, another antivirus is
active, policy is organization-managed, Tamper Protection prevents the write,
or compatibility is unclear.

### Run this to inspect and start in Audit mode

Set `$RunDir` to the exact recovery folder created in Step 0 if this is a new
PowerShell session.

```powershell
$RunDir = '<paste exact LG-Run-... folder path>'
$AuditStartPath = Join-Path $RunDir 'PUA-Audit-Started.clixml'
$Status = Get-MpComputerStatus
$Before = (Get-MpPreference).PUAProtection

[pscustomobject]@{
    AMRunningMode = $Status.AMRunningMode
    AntivirusEnabled = $Status.AntivirusEnabled
    RealTimeProtectionEnabled = $Status.RealTimeProtectionEnabled
    PUAProtection = $Before
}

if ($Before -in 0,2 -and
    -not (Test-Path -LiteralPath $AuditStartPath)) {
    [pscustomobject]@{
        Captured = Get-Date
        PUAProtection = [int]$Before
    } | Export-Clixml $AuditStartPath
}

if ($Before -eq 0 -and
    $Status.AMRunningMode -eq 'Normal' -and
    $Status.AntivirusEnabled -and
    $Status.RealTimeProtectionEnabled) {
    Set-MpPreference -PUAProtection AuditMode
}

(Get-MpPreference).PUAProtection
```

The first audit-start record is preserved across reruns. Do not delete or
replace it merely to shorten the event-review window.

Interpret the result:

- `0`: remain unchanged when Defender authority is unclear; otherwise the block
  attempts to move an active, unmanaged Defender installation to Audit mode.
- `1`: already blocking; leave it unchanged.
- `2`: Audit mode; test the normal workload before considering Block mode.

After a representative workload in Audit mode:

```powershell
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
```

If required software is unexpectedly detected, remain in Audit mode and
investigate. Do not create broad application, Downloads, or game-library
exclusions.

After a clean review, Block mode can be enabled deliberately:

```powershell
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
```

### Expected result

- `PUAProtection = 1`.
- `FreshScanCompleted = True`.

### Restart?

Normally no. Follow any Windows Security prompt.

### If it fails

Remain in Audit mode or leave the prior state unchanged. Investigate Defender
authority, policy, and compatibility.

### Undo

```powershell
$RunDir = '<paste exact LG-Run-... folder path>'
$Before = Import-Clixml "$RunDir\Defender-Before.clixml"
Set-MpPreference -PUAProtection ([int]$Before.PUAProtection)
(Get-MpPreference).PUAProtection
```

Pass: the value equals the recorded before-state. Smart App Control is
separate; this runbook neither requires nor changes it.

---

## 9. Maintenance, evidence, and scope

After Windows feature/security updates or LG firmware/software changes:

1. Recheck registered and provisioned package counts.
2. Reconfirm the Home Device Installation Settings preference.
3. Recheck Defender/PUA only when that optional layer is used.
4. Reconfirm the exact Store ID, package identity, publisher, and official LG
   support source.
5. Re-run the actual monitor baseline.

| Layer | What it covers |
| --- | --- |
| Home Device Installation Settings | A broader, weaker manufacturer-app preference; not the Pro policy |
| Package removal | Current registrations and online provisioning for the exact identity only |
| Defender PUA | General reputation/behavior decisions; no LG-classification guarantee |
| OnScreen Control removal | Only the selected desktop app; firmware, drivers, and hardware controls remain separate |

Treat current target-PC output as evidence. Documentation does not prove that a
local setting applied. Preserve sanitized summaries only. Never publish
usernames, hostnames, serial numbers, account identifiers, credentials, tokens,
raw recovery exports, or unredacted logs.

## 10. Authoritative references

1. [Microsoft Store: LG Monitor App Installer, Store ID 9PM9N6F47JB8](https://apps.microsoft.com/detail/9pm9n6f47jb8)
2. [LG product support, manuals, software, and drivers](https://www.lg.com/us/support)
3. [LG Monitor OnScreen Control: update monitor software](https://www.lg.com/us/support/help-library/lg-monitor-onscreen-control-how-to-update-monitor-software--20154629827481)
4. [Get-AppxPackage](https://learn.microsoft.com/en-us/powershell/module/appx/get-appxpackage?view=windowsserver2025-ps)
5. [Remove-AppxPackage](https://learn.microsoft.com/en-us/powershell/module/appx/remove-appxpackage?view=windowsserver2025-ps)
6. [Get-AppxProvisionedPackage](https://learn.microsoft.com/en-us/powershell/module/dism/get-appxprovisionedpackage?view=windowsserver2025-ps)
7. [Remove-AppxProvisionedPackage](https://learn.microsoft.com/en-us/powershell/module/dism/remove-appxprovisionedpackage?view=windowsserver2025-ps)
8. [Automatic installation for UWP device apps](https://learn.microsoft.com/en-us/windows-hardware/drivers/devapps/auto-install-for-uwp-device-apps)
9. [Driver Package Container Metadata](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/driver-package-container-metadata)
10. [INF AddSoftware directive](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/inf-addsoftware-directive)
11. [Detect and block potentially unwanted applications](https://learn.microsoft.com/en-us/defender-endpoint/detect-block-potentially-unwanted-apps-microsoft-defender-antivirus)
12. [Microsoft Defender Antivirus compatibility modes](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility)
13. [System configuration tools in Windows](https://support.microsoft.com/en-us/windows/experience/system-configuration-tools-in-windows)

## Publication and rights

Copyright (c) 2026 Amyashi.

This guide is independently authored, unofficial, and unaffiliated. Neither LG
nor Microsoft has endorsed it. Product names are used for identification.

This guide material is licensed under CC BY-NC-ND 4.0 under the
controlled-author terms in [`LICENSE.md`](../LICENSE.md). See that file for
attribution, noncommercial-use, no-derivatives, mixed-content, contribution,
third-party, and warranty terms.

[1]: https://apps.microsoft.com/detail/9pm9n6f47jb8
[2]: https://www.lg.com/us/support
