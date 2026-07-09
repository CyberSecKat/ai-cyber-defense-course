# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repo tracks coursework for the **AI Cyber Defense Ops** course (JustHacking / Women in CyberSecurity). It documents hands-on blue team tooling built with Claude Code: detection engineering, log/event parsing, threat hunting, incident response, and purple teaming. The author is a SOC/IR analyst using this repo to build reps with AI-assisted development, not just read about it.

**Guiding principle:** AI assists in analysis; it does not replace analyst judgment on security decisions. Every tool built here should preserve that boundary — favor transparent, inspectable logic over black-box automation, especially in anything that touches detection logic or triage decisions.

## Working Methodology

Each module/exercise is built **iteratively**, not one-shotted: describe the task, review Claude's output, refine, and document what worked/didn't. When implementing a module:
- Prefer incremental changes the user can review between steps over large one-shot generations, especially for detection logic.
- When choosing which fields/data to extract or which logic to implement, explain the analyst reasoning behind the choice (e.g., why a given Sysmon field matters for triage), not just the mechanics — this repo is a learning record as much as a tool collection.
- Notes on process and lessons learned live alongside each project folder (e.g., a module's own README/notes file) — check for one before assuming there isn't any project-specific context.

## Structure & Conventions

- Each course module lives in its own top-level directory named `module-N-<topic>` (e.g. `module-2-sysmon-parser`).
- **Python** is the primary language for tooling in this repo.
- The root `README.md` tracks overall course/module progress and links to featured projects — update the module status table and "Featured Projects" section there when a module reaches a working state.

## Commands

No shared build/lint/test tooling exists yet at the repo root. As modules are built out, check the individual module directory first for its own README, scripts, or dependency file (`requirements.txt`, etc.) before assuming a convention — each module may introduce its own run/test commands as it's built.
