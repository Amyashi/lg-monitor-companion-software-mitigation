# LG Monitor Companion Software: Cleanup and Recurrence Mitigation

## Windows 11 Pro runbook

Author: Amyashi

Version 1.0.0. Reviewed 2026-07-29.

This is the substantive, screen-reader-friendly companion to the Windows 11 Pro
PDF. Follow the numbered steps in order.

This independent, unofficial guide is not an LG Electronics or Microsoft
publication, endorsement, support channel, incident-response substitute,
security certification, or guarantee. Use it only on a PC you own or are
authorized to administer. Review every command, path, expected result, and undo
instruction before running an elevated command.

The original observed and field-tested case used Windows 11 Pro. Revalidate the
current package identity, publisher, delivery path, and effective results on
the target PC.

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

## The ordered Pro path

Complete the core path first:

1. Pass the authority, firmware, physical-control, and recovery gates.
2. Confirm Windows 11 Pro and capture the before-state.
3. Enable the documented device-metadata policy.
4. Remove only the exact Store package from current and future users.
5. Decide separately whether to keep OnScreen Control.
6. Restart once and verify.
7. Stop when every core result passes.

Use the optional AppLocker path only after the exact tested package actually
returns. Leave that returned package installed, reconfirm its complete identity,
then begin the Audit-only path. Never reinstall an unwanted package merely to
create a rule, and do not skip the core path to create a proactive rule.

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

The local AppLocker procedure later in this runbook does not manage AppLocker
CSP. Microsoft states that `Get-AppLockerPolicy` has no knowledge of CSP policy
and can return incorrect data for CSP-deployed policy; `Set-AppLockerPolicy`
cannot interact with AppLocker CSP.[15][16]

### Expected result

Continue only when:

- this is a personally administered Windows 11 Pro PC;
- the PC is not domain-, MDM-, or CSP-managed;
- effective policy authority is understood;
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

## 2. Step 0 - confirm Pro and capture the before-state

Open **Windows PowerShell 5.1 as Administrator**. Keep the same window open
through Step 2.

### Run this

```powershell
$ErrorActionPreference = 'Stop'
$ExpectedEdition = 'Windows 11 Pro'
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
$MetaPath = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Device Metadata'
$MetaName = 'PreventDeviceMetadataFromNetwork'
$Meta = [ordered]@{
    KeyExisted = Test-Path -LiteralPath $MetaPath
    ValueExisted = $false
    Value = $null
    Kind = $null
}

if ($Meta.KeyExisted) {
    $Key = Get-Item -LiteralPath $MetaPath
    $Props = Get-ItemProperty -LiteralPath $MetaPath
    $Meta.ValueExisted = $Props.PSObject.Properties.Name -contains $MetaName
    if ($Meta.ValueExisted) {
        $Meta.Value = $Props.$MetaName
        $Meta.Kind = [string]$Key.GetValueKind($MetaName)
    }
}
[pscustomobject]$Meta |
    Export-Clixml "$RunDir\Metadata-Before.clixml"

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

Before continuing:

1. Open `gpedit.msc`.
2. Go to **Computer Configuration -> Administrative Templates -> System ->
   Device Installation**.
3. Record whether **Prevent automatic download of applications associated with
   device metadata** is **Not Configured**, **Enabled**, or **Disabled**.
4. Save a sanitized screenshot with the recovery copy if useful.

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

- `WindowsEdition` contains `Windows 11 Pro`.
- `Administrator = True`.
- `DomainJoined = False`.
- Every saved file reports `Readable = True`.
- The separate recovery copy opens.
- The original Local Group Policy state is recorded.
- Any installed target shows the exact package name and one consistent,
  expected signed publisher identity.

Zero package results mean the exact target is already absent. Do not reinstall
it merely to complete this guide or create an AppLocker reference.

### Restart?

No.

### If it fails

- Wrong edition: use the Windows 11 Home runbook when Home is installed.
- Domain or organization management: stop and contact the responsible
  administrator.
- Unexpected publisher or package identity: stop and investigate.
- Unreadable recovery copy: recreate and test it before any change.

### Undo

No Windows setting or package state has changed.

---

## 3. Step 1 - enable the documented metadata policy

### Do this

1. Open `gpedit.msc`.
2. Go to **Computer Configuration -> Administrative Templates -> System ->
   Device Installation**.
3. Open **Prevent automatic download of applications associated with device
   metadata**.
4. Select **Enabled**.
5. Select **Apply**, then **OK**.

### Run this

```powershell
gpupdate /target:computer /force

$Path = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Device Metadata'
$Name = 'PreventDeviceMetadataFromNetwork'
$Value = Get-ItemPropertyValue -Path $Path -Name $Name `
    -ErrorAction SilentlyContinue

[pscustomobject]@{
    WindowsEdition = (Get-CimInstance Win32_OperatingSystem).Caption
    MetadataPolicyValue =
        if ($null -eq $Value) { '(not set)' } else { $Value }
}
```

### Expected result

- `WindowsEdition` contains `Windows 11 Pro`.
- `MetadataPolicyValue = 1`.

This policy concerns applications associated with device metadata. It is not a
universal block for:

- manual Microsoft Store acquisition;
- Windows Update drivers;
- OEM provisioning;
- Driver Package Container Metadata;
- driver-INF `AddSoftware`; or
- conventional Win32 installers.[21][22][26]

Microsoft marks the legacy device-metadata path as deprecated. The policy is
one layer, not proof that every current or future delivery path is blocked.

### Restart?

Not yet. Continue to Step 2.

### If it fails

Reopen Local Group Policy, confirm **Enabled**, refresh policy, and check once
more. Stop if another authority reverses or controls the setting.

### Undo

Use the same Local Group Policy page to restore exactly the state recorded in
Step 0. Run:

```powershell
gpupdate /target:computer /force
```

Restart and verify the affected peripheral workflow.

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
$Meta = Get-ItemPropertyValue `
    -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Device Metadata' `
    -Name PreventDeviceMetadataFromNetwork -ErrorAction SilentlyContinue
$Defender = Get-MpComputerStatus

[pscustomobject]@{
    WindowsEdition = (Get-CimInstance Win32_OperatingSystem).Caption
    RegisteredPackageCount = $Registered.Count
    ProvisionedPackageCount = $Provisioned.Count
    MetadataPolicyValue =
        if ($null -eq $Meta) { '(not set)' } else { $Meta }
    DefenderRealTime = $Defender.RealTimeProtectionEnabled
}
```

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

- `WindowsEdition` contains `Windows 11 Pro`.
- `RegisteredPackageCount = 0`.
- `ProvisionedPackageCount = 0`.
- `MetadataPolicyValue = 1`.
- `DefenderRealTime = True` when Microsoft Defender is the active antivirus.
- Every required monitor function passes.
- The OnScreen Control state matches the user's decision.

If every core result passes, stop. The core mitigation is complete. Do not add
AppLocker or change Defender solely to make the guide look more complete.

### Restart?

No additional restart is required when everything passes.

### If it fails

Use the first matching failure branch below.

### Undo

Reverse only the layer causing the problem; do not undo successful,
unrelated layers.

---

## 7. Core failure and undo branches

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
3. Reconfirm `MetadataPolicyValue = 1`.
4. Review Store, Windows Update, OEM, driver, and manual-install activity.
5. Do not assume which delivery path was responsible.

If repeat prevention is required, leave the returned signed package installed
temporarily and continue to the optional AppLocker path.

### Failure branch C - an unexpected LG package appears

Stop. Do not change `$Package` to match it. Identify the exact product,
publisher, purpose, and official source first. This runbook authorizes actions
only against `LGElectronics.LGMonitorApp`.

### Failure branch D - OnScreen Control was needed

Reinstall only the intended version from the exact model's official LG support
page. Recheck the full monitor baseline and package inventory.

### Failure branch E - another application or peripheral is affected

Restore the original Local Group Policy state through `gpedit.msc`, refresh
policy, restart, and verify both the affected peripheral and the LG monitor
baseline.

### Failure branch F - Defender real-time protection is false

Determine whether another antivirus is active or the PC is managed. Do not
change Defender PUA settings until antivirus authority is understood.

---

## 8. Optional AppLocker - decision, backup, and Audit only

AppLocker is not part of a successful core cleanup. Microsoft documents it as
defense in depth, not a security boundary.[8]

### Continue only when all gates pass

- Failure branch B recorded an actual return of the exact signed
  `LGElectronics.LGMonitorApp` package, and that returned package remains
  installed.
- Store product `9PM9N6F47JB8` still identifies **LG Monitor App Installer**,
  publisher **LG Electronics Inc.**
- The PC is personally managed.
- AppLocker is not managed through MDM/CSP.
- Current local and effective Appx policy is empty or fully understood.
- `secpol.msc`, `Get-AppLockerPolicy`, and `Test-AppLockerPolicy` are present.
- A complete local/effective policy backup can be opened off-device.
- The default signed-packaged-app allow for Everyone will be preserved.
- The compatibility-testing and Application Identity service trade-offs are
  accepted.

If any gate fails, stop. Do not install third-party policy-editor hacks and do
not reinstall an absent package merely to create a reference.

### Back up and inspect

```powershell
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
if ($Missing.Count) {
    throw "STOP: missing AppLocker tools: $Missing"
}

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
```

Copy the complete `LG-AppLocker-...` folder to separate
administrator-controlled storage. Reopen both XML files. Stop if any
collection, effective rule, domain policy, or CSP/MDM control is unfamiliar.

### Configure only the Packaged app collection

1. Open `secpol.msc`.
2. Go to **Application Control Policies -> AppLocker**.
3. Inspect every collection and **AppLocker Properties** before editing.
4. Under **Packaged app Rules**, choose **Create Default Rules** only when no
   prior Appx design exists.
5. Require **Allow Everyone to install and run all signed packaged apps**.
6. Open **AppLocker Properties**.
7. Configure only **Packaged app Rules** as **Audit only**.
8. Leave EXE, MSI, Script, and DLL collections unchanged.

Microsoft states that the protected Application Identity service cannot be
returned to Manual with `sc.exe` and recommends a system backup before changing
its startup type.[6] Continue only after accepting this persistent
service-state change.

```powershell
sc.exe config appidsvc start=auto
Start-Service AppIDSvc
gpupdate /target:computer /force

Get-CimInstance Win32_Service -Filter "Name='AppIDSvc'" |
    Select-Object Name,State,StartMode
```

### Expected result

- `State = Running`.
- `StartMode = Auto`.
- Packaged app Rules is visibly **Audit only**.
- EXE, MSI, Script, and DLL collections are unchanged.

### Restart?

No. Continue in Audit only.

### If it fails

Do not create or enforce the target rule. Restore only changes made during this
section when their prior state and supported recovery method are known.

### Undo

Return only Packaged app Rules to its recorded prior mode and remove only
guide-created rules. Keep `AppIDSvc` running unless a tested, supported recovery
method exists; do not try to return it to Manual with `sc.exe`.

---

## 9. Optional AppLocker - create the exact deny and test

Keep Packaged app Rules in **Audit only**.

### Create the rule

1. Under **Packaged app Rules**, select **Create New Rule**.
2. Permissions: **Deny / Everyone**.
3. Condition: **Publisher**.
4. Reference: installed packaged app **LG Monitor App Installer**.
5. Scope: package name `LGElectronics.LGMonitorApp`, all versions, no
   exceptions.
6. Name: **Block LG Monitor App Installer**.
7. Preserve the default signed-package allow. Create one narrow deny only.

Do not browse manually into `WindowsApps`.

### Export Audit policy and simulate installed packages

```powershell
$ALRun = '<paste exact LG-AppLocker-... folder path>'
$Package = 'LGElectronics.LGMonitorApp'
$RuleName = 'Block LG Monitor App Installer'
$Types = 'Main','Framework','Resource','Bundle','Optional'
$AuditStarted = Get-Date
$AuditStarted | Export-Clixml "$ALRun\Audit-Started.clixml"

gpupdate /target:computer /force
Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop |
    Set-Content "$ALRun\Effective-Audit.xml" -Encoding UTF8

$Target = @(Get-AppxPackage -AllUsers -Name $Package `
    -PackageTypeFilter $Types -ErrorAction Stop)
if ($Target.Count -eq 0) {
    throw 'STOP: signed target package is absent.'
}

$All = @(Get-AppxPackage -AllUsers -PackageTypeFilter $Types `
    -ErrorAction Stop)
$TargetDenied = @($Target | Test-AppLockerPolicy `
    -XmlPolicy "$ALRun\Effective-Audit.xml" `
    -User 'S-1-1-0' -Filter Denied)
$DeniedByDefault = @($All | Test-AppLockerPolicy `
    -XmlPolicy "$ALRun\Effective-Audit.xml" `
    -User 'S-1-1-0' -Filter DeniedByDefault)

[pscustomobject]@{
    TargetCount = $Target.Count
    TargetPredictedDenied = $TargetDenied.Count
    InstalledDeniedByDefault = $DeniedByDefault.Count
}
```

### Run a representative compatibility session

Exercise the applications and workflows actually required on this PC,
including:

- Start and Settings;
- Microsoft Store and one built-in Store app;
- Xbox/Game Bar, if used;
- Discord or other Store apps, if used;
- Steam, Epic, and game launchers;
- mod or monitoring tools; and
- the normal monitor-control workflow.

Review only would-be denial events created after the recorded start:

```powershell
$ALRun = '<paste exact LG-AppLocker-... folder path>'
$Start = Import-Clixml "$ALRun\Audit-Started.clixml"
$Logs = 'Microsoft-Windows-AppLocker/Packaged app-Execution',
        'Microsoft-Windows-AppLocker/Packaged app-Deployment'

foreach ($Log in $Logs) {
    Get-WinEvent -FilterHashtable @{
        LogName=$Log
        Id=8021,8024
        StartTime=$Start
    } -ErrorAction SilentlyContinue |
        Select-Object TimeCreated,Id,Message
}
```

### Expected result before enforcement

- Target predicted-denied count equals target count.
- Installed denied-by-default count is `0`.
- Target publisher and package name match the recorded reference.
- The default signed-package allow remains.
- No required application has an unexplained would-be denial.

Otherwise remain in Audit only.

### Restart?

No.

### If it fails

Remain in Audit only. Do not add a broad exception. Delete only the exact
guide-created deny if the design is abandoned.

### Undo

Delete only **Block LG Monitor App Installer**, refresh Group Policy, and
confirm the default allow and every unrelated rule remain unchanged.

---

## 10. Optional AppLocker - enforce and prove the result

AppLocker enforcement applies immediately, and a deny overrides an allow.[5]

### Do this

1. Review every pass condition in Step 9.
2. Reopen the recovery XML.
3. In **AppLocker Properties**, switch only **Packaged app Rules** to
   **Enforce rules**.
4. Leave EXE, MSI, Script, and DLL unchanged.

### Run this

```powershell
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
$All = @(Get-AppxPackage -AllUsers -PackageTypeFilter $Types `
    -ErrorAction Stop)
$Denied = @($Target | Test-AppLockerPolicy `
    -XmlPolicy "$ALRun\Effective-Enforced.xml" `
    -User 'S-1-1-0' -Filter Denied)
$DefaultDenied = @($All | Test-AppLockerPolicy `
    -XmlPolicy "$ALRun\Effective-Enforced.xml" `
    -User 'S-1-1-0' -Filter DeniedByDefault)

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
```

While the command waits, smoke-test Start, Settings, Store, every required
packaged app, and normal monitor workflows. Attempt the already-installed exact
LG package once, then press Enter.

### Expected result

- `AppxMode = Enabled`.
- Target predicted-denied count equals target count.
- Installed denied-by-default count is `0`.
- `EnforcedTargetDenyEventCount` is at least `1`.
- A returned 8022 or 8025 event names both
  `LGElectronics.LGMonitorApp` and **Block LG Monitor App Installer**.
- Every required unrelated application and monitor workflow passes.

Prediction alone is not proof. Require the real target event before treating
enforcement as observed.

### Restart?

Only after a real block and clean smoke test:

1. Rerun the exact package-removal block from Step 2.
2. Require both package counts to return `0`.
3. Restart.
4. Rerun the core checks.
5. Confirm Appx mode remains **Enforce rules**.
6. Confirm the exact deny and default signed-package allow remain.
7. Confirm `AppIDSvc` remains `Running` and `Auto`.
8. Recheck the actual monitor baseline.

Do not rerun the target-event test after the target package has been removed.

### If it fails

Immediately use the narrow rollback below. Do not add a broad exception.

### Narrow undo

1. Keep `AppIDSvc` running.
2. Return only **Packaged app Rules** to **Audit only**.
3. Run `gpupdate /target:computer /force`.
4. Delete only **Block LG Monitor App Installer**.
5. Refresh Group Policy again.
6. Verify required apps run and the exact deny is absent.

---

## 11. Detached option - Microsoft Defender PUA evaluation

Potentially unwanted application protection is a general
reputation/behavior layer. It is not an LG-specific rule, is not required for
core cleanup, and does not guarantee classification of an LG package.[13][14]

Stop after the core LG path passes. Continue here only for a separately
documented Windows security requirement.

Skip this section when Microsoft Defender is passive, another antivirus is
active, policy is organization-managed, Tamper Protection prevents the write,
or compatibility is unclear.

### Run this to inspect and start in Audit mode

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

## 12. AppLocker last-resort local-policy restore

Prefer manually restoring only the guide-owned Appx collection, exact rule, and
mode. Whole-policy replacement is an emergency fallback, not normal rollback.

Never use full replacement:

- on a managed PC;
- for CSP/MDM policy;
- after unrelated AppLocker changes;
- with an unverified backup; or
- when the current and intended policy scope is not fully understood.

If complete local-policy replacement is explicitly intended:

```powershell
# LAST RESORT: local, unmanaged AppLocker only.
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

$AfterLocal = Join-Path $ALRun 'Local-After-Restore.xml'
$AfterEffective = Join-Path $ALRun 'Effective-After-Restore.xml'
Get-AppLockerPolicy -Local -Xml -ErrorAction Stop |
    Set-Content $AfterLocal -Encoding UTF8
Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop |
    Set-Content $AfterEffective -Encoding UTF8
[xml](Get-Content $AfterLocal -Raw -ErrorAction Stop) | Out-Null
[xml](Get-Content $AfterEffective -Raw -ErrorAction Stop) | Out-Null
Get-Item $Current,$AfterLocal,$AfterEffective
```

Review `-WhatIf` and the newly exported current policy before typing the exact
confirmation. Never import `Effective-Before.xml`; effective policy is
diagnostic, not a restore source.

Afterward, reopen both after-state XML files, restart, and run the functional
checks. Keep `AppIDSvc` Automatic unless a tested, supported recovery method is
available.

---

## 13. Maintenance, evidence, and scope

After Windows feature/security updates or LG firmware/software changes:

1. Recheck registered and provisioned package counts.
2. Reconfirm `MetadataPolicyValue = 1`.
3. When AppLocker is used, recheck service state, Appx mode, the exact deny,
   default allow, required-app compatibility, and real enforcement events.
4. Recheck Defender/PUA only when that optional layer is used.
5. Reconfirm the exact Store ID, package identity, publisher, and official LG
   support source.
6. Re-run the actual monitor baseline.

| Layer | What it covers |
| --- | --- |
| Pro metadata policy | Metadata-associated application retrieval only |
| Package removal | Current registrations and online provisioning for the exact identity only |
| AppLocker | One signed packaged-app identity; not a Win32-installer block or security boundary |
| Defender PUA | General reputation/behavior decisions; no LG-classification guarantee |
| OnScreen Control removal | Only the selected desktop app; firmware, drivers, and hardware controls remain separate |

Treat current target-PC output as evidence. Documentation does not prove that a
local setting applied, and predicted AppLocker results do not prove a real
block. Preserve sanitized summaries only. Never publish usernames, hostnames,
serial numbers, account identifiers, credentials, tokens, raw recovery
exports, or unredacted logs.

## 14. Authoritative references

1. [Microsoft Store: LG Monitor App Installer, Store ID 9PM9N6F47JB8](https://apps.microsoft.com/detail/9pm9n6f47jb8)
2. [LG product support, manuals, software, and drivers](https://www.lg.com/us/support)
3. [LG Monitor OnScreen Control: update monitor software](https://www.lg.com/us/support/help-library/lg-monitor-onscreen-control-how-to-update-monitor-software--20154629827481)
4. [Create an AppLocker rule for packaged apps](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/create-a-rule-for-packaged-apps)
5. [AppLocker allow and deny actions](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/understanding-applocker-allow-and-deny-actions-on-rules)
6. [Configure the Application Identity service](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/configure-the-application-identity-service)
7. [Use Event Viewer with AppLocker](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/using-event-viewer-with-applocker)
8. [AppLocker overview and defense-in-depth guidance](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/applocker-overview)
9. [Get-AppxPackage](https://learn.microsoft.com/en-us/powershell/module/appx/get-appxpackage?view=windowsserver2025-ps)
10. [Remove-AppxPackage](https://learn.microsoft.com/en-us/powershell/module/appx/remove-appxpackage?view=windowsserver2025-ps)
11. [Get-AppxProvisionedPackage](https://learn.microsoft.com/en-us/powershell/module/dism/get-appxprovisionedpackage?view=windowsserver2025-ps)
12. [Remove-AppxProvisionedPackage](https://learn.microsoft.com/en-us/powershell/module/dism/remove-appxprovisionedpackage?view=windowsserver2025-ps)
13. [Detect and block potentially unwanted applications](https://learn.microsoft.com/en-us/defender-endpoint/detect-block-potentially-unwanted-apps-microsoft-defender-antivirus)
14. [Microsoft Defender Antivirus compatibility modes](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility)
15. [Get-AppLockerPolicy](https://learn.microsoft.com/en-us/powershell/module/applocker/get-applockerpolicy?view=windowsserver2025-ps)
16. [Set-AppLockerPolicy](https://learn.microsoft.com/en-us/powershell/module/applocker/set-applockerpolicy?view=windowsserver2025-ps)
17. [Deploy AppLocker policies by using Enforce rules](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/deploy-applocker-policies-by-using-the-enforce-rules-setting)
18. [Test-AppLockerPolicy](https://learn.microsoft.com/en-us/powershell/module/applocker/test-applockerpolicy?view=windowsserver2025-ps)
19. [Create AppLocker default rules](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/create-applocker-default-rules)
20. [Delete an AppLocker rule](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/delete-an-applocker-rule)
21. [Prevent device metadata retrieval from the network](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-deviceinstallation#preventdevicemetadatafromnetwork)
22. [Automatic installation for UWP device apps](https://learn.microsoft.com/en-us/windows-hardware/drivers/devapps/auto-install-for-uwp-device-apps)
23. [INF AddSoftware directive](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/inf-addsoftware-directive)
24. [AppLocker requirements and supported Windows editions](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/requirements-to-use-applocker)
25. [KB5024351: removal of Windows edition checks for AppLocker](https://support.microsoft.com/en-us/servicing/os/windows/2023/02/kb5024351-removal-of-windows-edition-checks-for-applocker)
26. [Driver Package Container Metadata](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/driver-package-container-metadata)

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
