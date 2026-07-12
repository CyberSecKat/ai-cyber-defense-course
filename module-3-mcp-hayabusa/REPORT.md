# AI Cyber Defense Ops — Module 3 Progress Report
## MCP: Wrapping Security CLIs — Phase 1: Environment Setup & Tool Validation

**Analyst:** CyberSecKat
**Course:** AI Cyber Defense Ops
**Module:** 3 — Model Context Protocol (MCP) — Wrapping Security CLIs
**Date:** July 11, 2026

---

## Introduction

Module 2 of this course focused on building a Sysmon parser by having an AI assistant (Claude) write Python code directly. That approach works, but it has a recurring cost: every time the parser needs to run, the assistant has to re-read the script, re-establish context, and execute it from scratch. There is no persistent capability — just a one-off script that gets reused by re-explaining it.

Module 3 addresses that limitation using the **Model Context Protocol (MCP)**, an open standard that lets an AI assistant invoke external tools directly, the same way an analyst would invoke a CLI utility without needing to re-learn its syntax every session. Once an MCP server is built and registered, its tools are available to the assistant persistently — across sessions and across projects — without re-reading a single line of implementation code.

The tool selected for this module is **Hayabusa**, an open-source Windows Event Log (EVTX) fast forensics timeline generator and Sigma-based threat hunting tool developed by Yamato Security. Hayabusa was chosen because it reflects a realistic SOC/DFIR workflow: an analyst receives EVTX files from a potentially compromised host, needs to triage tens or hundreds of thousands of raw events down to a manageable set of actionable detections, and frequently needs to re-run that triage with different parameters as an investigation develops.

The objective of this module is to build a Python-based MCP server that wraps Hayabusa's command-line interface, register it with both Claude Code and Claude Desktop, and validate that an AI assistant can invoke Hayabusa scans as a native tool call rather than as a manually-copied command.

This report documents that build in phases, starting with environment setup and tool validation.

---

## Phase 1: Environment Setup & Tool Validation

### Objective

Before wrapping any CLI tool in an MCP server, the tool itself must be confirmed to work correctly in isolation. Phase 1 focused exclusively on installing Hayabusa, obtaining representative test data, and running a baseline scan to validate that the tool, its detection rule set, and the local environment were all functioning correctly — independent of any AI tooling.

### Environment

| Component | Detail |
|---|---|
| Host OS | Windows |
| Tool | Hayabusa v3.10.0 ("Independence Day Release") |
| Install location | `C:\Tools\hayabusa` |
| Test dataset | [EVTX-to-MITRE-Attack](https://github.com/mdecrevoisier/EVTX-to-MITRE-Attack) (mdecrevoisier) |
| Dataset location | `C:\Tools\sample-evtx\EVTX-to-MITRE-Attack-master` |

The EVTX-to-MITRE-Attack dataset was selected specifically because it is a publicly available, purpose-built collection of Windows Event Logs containing simulated attack techniques mapped to MITRE ATT&CK. This allowed the tool to be validated against realistic, high-signal data without requiring access to a live or compromised endpoint.

### Actions Taken

1. Downloaded the Windows x64 release of Hayabusa (`hayabusa-3.10.0-win-x64.zip`) from the official [Yamato-Security/hayabusa](https://github.com/Yamato-Security/hayabusa) GitHub releases page and extracted it locally.
2. Validated the binary was functional by invoking its built-in help output, confirming the full command set (`csv-timeline`, `json-timeline`, `update-rules`, `search`, `logon-summary`, and others).
3. Downloaded and extracted the EVTX-to-MITRE-Attack sample dataset as a stand-in for evidence collected from a host during an investigation.
4. Executed a baseline `csv-timeline` scan against the full sample dataset using default detection rule settings, with no severity or category filtering applied, to establish an unfiltered baseline.

Command executed:

```powershell
.\hayabusa-3.10.0-win-x64.exe csv-timeline -d C:\Tools\sample-evtx\EVTX-to-MITRE-Attack-master -o test.csv
```

### Results Summary

| Metric | Value |
|---|---|
| Event log files scanned | 293 |
| Total log volume | 74.5 MiB |
| Total detection rules loaded | 4,648 (181 Hayabusa rules + 4,467 Sigma rules) |
| Total events | 12,304 |
| Events with detections | 3,604 |
| Noise reduction | 70.71% |
| Scan duration | 7.885 seconds |
| Output file | `test.csv` (14.8 MiB) |

**Detections by severity (total / unique):**

| Severity | Total | Unique |
|---|---|---|
| Critical | 13 | 8 |
| High | 1,218 | 100 |
| Medium | 840 | 114 |
| Low | 1,293 | 52 |
| Informational | 5,318 | 34 |

**Notable detections observed** (present because they are intentionally embedded in the sample dataset, not indicative of any actual compromise):

- Active Directory Replication from a Non-Machine Account (DCSync-style behavior)
- Antivirus-flagged password dumper signature
- Potential SystemNightmare exploitation attempt
- Sticky Keys–style backdoor execution
- Mimikatz `.kirbi` ticket file creation
- Suspicious service installation paths and PowerShell-based service creation

### Analyst Notes

The scan behaved as expected for a Sigma-based detection engine run against intentionally adversarial sample data. The ~71% noise reduction — 12,304 raw events collapsed to 3,604 events with at least one rule match — is consistent with Hayabusa's stated design goal of letting analysts focus on a small, high-value subset of a much larger log volume rather than reviewing every event manually.

The presence of critical-severity detections (Mimikatz artifacts, SystemNightmare, DCSync-pattern replication) is expected and by design: the EVTX-to-MITRE-Attack dataset exists specifically to give detection tooling something realistic to catch. Their appearance here confirms the rule set is loading and matching correctly, not that any system was compromised.

No issues were encountered with rule loading, channel filtering, or output generation. The tool is confirmed production-ready for the next phase of this module.

### Lessons Learned — SOC Analyst Perspective

Beyond the mechanics of installing and running a tool, this phase reinforced a few things that matter directly to day-to-day SOC work:

- **Triage value is measurable, not theoretical.** Watching 12,304 raw events collapse to 3,604 flagged events in under 8 seconds made the "signal vs. noise" problem concrete in a way that reading about detection engineering doesn't. A 70%+ reduction is the difference between a shift spent scrolling logs and a shift spent actually investigating.
- **Validate the tool before you trust the automation.** Running Hayabusa manually first — before wrapping it in anything AI-driven — meant that when Phase 2 introduces an MCP server calling this same command, any unexpected result can be immediately attributed to the integration layer rather than second-guessed as "maybe Hayabusa is wrong." That separation of concerns is a habit worth carrying into any tool integration, not just this one.
- **Known-bad test data is not the same as a live incident, and conflating the two is a real risk.** Seeing Mimikatz artifacts and SystemNightmare detections fire correctly was reassuring precisely *because* the dataset's contents were already known. In a live investigation, the same output would demand a completely different response posture — a reminder that context (what data am I actually looking at, and why) has to travel with the results, not just the detections themselves.
- **AI-assisted tooling changes the interface, not the judgment.** The entire premise of this module — an AI assistant invoking Hayabusa directly — is about removing friction in *how* a scan gets run, not about deciding *what the results mean*. That interpretation step stays a human/analyst responsibility. This lines up with the guiding principle for this whole repo: AI assists in analysis, it doesn't replace analyst judgment on security decisions.
- **AI is becoming invaluable to blue team defense, specifically because it removes friction rather than removing analysts.** The gap this module is closing — re-explaining a tool's syntax every time it's needed versus having an assistant that can just invoke it — is a small example of a much bigger shift happening in SOC work. Every minute spent context-switching between a terminal, documentation, and a ticketing system is a minute not spent on actual investigation. An AI assistant that can run Hayabusa, summarize thousands of lines of output, and hold the context of an entire investigation across multiple tool calls is a genuine force multiplier for a defender — especially for smaller teams and solo analysts who don't have the luxury of a large SOC to split that workload across.

### Next Steps

With Hayabusa validated as a standalone tool, Phase 2 will scaffold a Python MCP server using the `fastmcp` framework, exposing a `scan_evtx` tool (and a corresponding `last-scan` resource) that lets an AI assistant invoke this exact scan on demand — including selecting a directory, filtering by minimum severity, and reviewing prior results — without needing to re-explain Hayabusa's syntax in every session.

---

*This report is part of an ongoing coursework series for the AI Cyber Defense Ops program. Subsequent phases (MCP server implementation, Claude Code/Desktop integration, and end-to-end validation) will be documented as they are completed.*
