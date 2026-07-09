# Sysmon Event Parser

Parses Sysmon Event ID 1 (process creation) XML into clean JSON, pulling out 
the fields that actually matter for triage — and flagging known discovery 
techniques when they show up.

## What it does

Raw Sysmon events arrive as noisy XML — a lot of metadata wrapped around a 
handful of fields an analyst actually needs. This tool strips that down to 
five core fields:

- **Image** — what process executed
- **CommandLine** — what arguments were passed
- **ParentImage** — what spawned this process
- **User** — who ran it
- **IntegrityLevel** — what privilege level it ran at

On top of that, it checks the `ParentImage` → `Image` pair against a set of 
known discovery-technique patterns and adds a `detection_flag` field when one 
matches.

## Why these fields

These five answer the first questions any analyst asks when triaging a 
process-creation event: who ran what, what spawned it, and at what privilege 
level. `Image` and `CommandLine` tell you what actually ran. `ParentImage` 
tells you the lineage — whether this came from a normal parent (like 
`explorer.exe`) or something that should raise an eyebrow (like `cmd.exe` or 
`powershell.exe`). `User` and `IntegrityLevel` tell you who did it and how much 
access they had. Strip away everything else in the XML and these five are 
what's left when you actually need to make a call fast.

## Why the detection logic

The base assignment asked for field extraction. But extraction alone doesn't 
tell you if something's worth looking at, it just organizes the noise. So 
this parser goes a step further and checks for a specific pattern: shell 
processes (`cmd.exe`, `powershell.exe`) spawning known discovery binaries. 
Right now it flags:

| Parent → Child | Technique |
|---|---|
| `cmd.exe`/`powershell.exe` → `whoami.exe` | T1033 — System Owner/User Discovery |
| `cmd.exe`/`powershell.exe` → `net.exe`/`net1.exe` | T1087 — Account Discovery |
| `cmd.exe`/`powershell.exe` → `systeminfo.exe` | T1082 — System Information Discovery |

These are all early-stage recon techniques attackers use right after gaining 
a foothold — before lateral movement or privilege escalation. Catching this 
pattern at the parsing stage means an analyst sees the flag immediately, 
instead of having to recognize the technique manually from a wall of process 
names.

The logic is a plain dictionary lookup on purpose — no black-box scoring, 
nothing hidden. An analyst reading this code can see exactly why something 
got flagged, and adjust the rules directly.

## Sample input → output

**Input** (`sample_event.xml`, a real Sysmon Event ID 1):
```xml
<Data Name="Image">C:\Windows\System32\whoami.exe</Data>
<Data Name="CommandLine">whoami  /groups</Data>
<Data Name="ParentImage">C:\Windows\System32\cmd.exe</Data>
<Data Name="User">CONDEF\Administrator</Data>
<Data Name="IntegrityLevel">High</Data>
```

**Output:**
```json
{
  "Image": "C:\\Windows\\System32\\whoami.exe",
  "CommandLine": "whoami  /groups",
  "ParentImage": "C:\\Windows\\System32\\cmd.exe",
  "User": "CONDEF\\Administrator",
  "IntegrityLevel": "High",
  "detection_flag": "cmd.exe spawned whoami.exe (T1033)"
}
```

## Usage
