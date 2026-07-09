# AI Cyber Defense Ops — Course Notes & Projects

My Hands-on notes, tools, and detection engineering projects built while completing 
the AI Cyber Defense Ops course by JustHacking and Women in CyberSecurity. This repo documents how I use Claude and Claude 
Code as force multipliers for blue team work: threat hunting, detection engineering, 
incident response, and purple teaming, while keeping analyst judgment squarely 
in the loop.

## About This Repo

AI tools are moving fast in security operations, and I wanted hands-on reps 
building real workflows with them rather than just reading about it. This repo 
tracks that process: what I built, what worked, what didn't, and what I learned 
about integrating AI safely into a SOC/IR workflow.

A guiding principle throughout: AI assists in analysis, it does not replace an 
analyst's judgment on security decisions. Every tool here is built with that 
boundary in mind.

## Skills & Tools Demonstrated

- Detection Engineering: building parsers and enrichment tools for security telemetry
- Log/Event Analysis: Sysmon, Windows Event Logs, SIEM data
- Scripting: Python, working toward automating repetitive analyst tasks
- AI-Assisted Workflows: Claude Code, prompt engineering for security use cases
- Version Control: Git/GitHub workflows for tracking security tooling

## Course Modules & Progress

| Module | Topic | Status |
|--------|-------|--------|
| 1 | The Claude Ecosystem | ✅ Complete |
| 2 | Building Your First Security Tool (Sysmon Parser) | 🔄 In Progress |
| 3 | *(add as you go)* | ⬜ Not Started |
| 3 | *(add as you go)* | ⬜ Not Started |
| 3 | *(add as you go)* | ⬜ Not Started |
| 3 | *(add as you go)* | ⬜ Not Started |
| 3 | *(add as you go)* | ⬜ Not Started |
| 3 | *(add as you go)* | ⬜ Not Started |
| 3 | *(add as you go)* | ⬜ Not Started |

## Featured Projects

- Sysmon Event Parser — extracts key detection fields (Image, CommandLine, 
  ParentImage, User, IntegrityLevel) from raw Sysmon XML into clean JSON. 
  [`/module-2-sysmon-parser`](./module-2-sysmon-parser)

## Notes & Methodology

I'm approaching each exercise as an iterative build with Claude Code rather than 
expecting one-shot results, describing the task, reviewing output, refining, 
and documenting what I'd do differently. Notes on process and lessons learned 
live alongside each project folder.

## About Me

Security Operations / Incident Response analyst with a focus on detection 
engineering and Python-based tooling. Currently exploring how AI-assisted 
development can speed up blue team workflows without cutting analysts out 
of the decision loop.

- 🔗 [LinkedIn](https://www.linkedin.com/in/kathleenfell/)
- 🌐 [Website](https://www.katmarie.com)
- 🦋 [Bluesky](https://bsky.app/profile/cyberseckat.bsky.social)

## Notes & Methodology

Each exercise is built iteratively rather than one-shotted. For the Sysmon 
parser, for example, the field selection wasn't arbitrary, Image, CommandLine, 
ParentImage, User, and IntegrityLevel were chosen because they cover the core 
who/what/how/privilege questions an analyst asks first when triaging a 
process-creation event.
