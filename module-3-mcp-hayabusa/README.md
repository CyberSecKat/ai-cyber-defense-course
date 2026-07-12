# MCP: Wrapping Security CLIs — Hayabusa

A Python MCP (Model Context Protocol) server that wraps the [Hayabusa](https://github.com/Yamato-Security/hayabusa) 
CLI, so an AI assistant can scan Windows Event Logs and pull Sigma-based 
detections as a native tool call instead of a manually-copied command.

## What it does

Registers three MCP capabilities backed by the Hayabusa binary:

- **`scan_evtx`** — runs a Hayabusa `csv-timeline` scan over a directory of 
  `.evtx` files at a given minimum severity and returns a preview of the 
  resulting detection timeline.
- **`update_hayabusa_rules`** — updates Hayabusa's bundled Sigma rule set.
- **`hayabusa://last-scan`** — a resource exposing the full CSV timeline from 
  the most recently run scan.

## Implementation

- `server.py` — the MCP server implementation.

## Full write-up

See [REPORT.md](REPORT.md) for the full analyst notes: why Hayabusa was 
chosen, setup/validation steps, and ongoing progress on this module.
