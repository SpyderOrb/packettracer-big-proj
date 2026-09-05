# Project instructions for Codex

## Purpose and language

Build a practical Cisco Packet Tracer portfolio for Junior NOC, Network Support, and Junior Network Engineer roles. Write project documentation, explanations within project files, configuration comments, diagram labels, evidence captions, and incident reports in **English**. Communicate with the user in chat in **Russian**, as explicitly requested.

## Start each session

1. Read `README.md`, `.project/STATUS.md`, `.project/DECISIONS.md`, and the latest `.project/CHANGELOG.md` entry.
2. Read only the sections of `docs/NETWORK.md` and `docs/VALIDATION.md` needed for the current block.
3. State the current block and concrete deliverable before editing.

The five-block roadmap lives in `.project/STATUS.md`. The old twelve-phase plan is archived and no longer controls the workflow.

## Work in practical increments

- Complete one block, or a small working slice of it, per session.
- Use the loop: configure, test, save a checkpoint, export configurations, record the result.
- Keep planning in `docs/NETWORK.md`; use its device, interface, VLAN, subnet, and policy identifiers consistently.
- Keep one full configuration per device in `configs/`. Do not split a device's configuration across technology folders.
- Update `.project/STATUS.md` and `.project/CHANGELOG.md` after material changes. Record architecture changes in `.project/DECISIONS.md` and update the build sheet.
- Keep the README focused on the reviewer. Avoid duplicate plans, empty topic folders, and documents without a practical purpose.
- Keep `.project/archive/` unchanged as historical material. Do not treat archived instructions or status as current.

## Evidence and checkpoints

- Never invent Packet Tracer results. A proposed configuration or a generated diagram is not validation evidence.
- Do not claim a `.pkt` file was tested unless it was opened and the documented checks were run.
- Confirm device and feature support in the installed Packet Tracer version before relying on it. Label untested model and interface selections explicitly.
- Record expected and actual results separately, with the tested checkpoint and supporting output or screenshots.
- Save clean milestones as `packet-tracer/checkpoints/HQ-Branches-NOC-Lab_vNN_description.pkt`; preserve older checkpoints.
- Keep deliberate faults under `incidents/IR-NNN/`, alongside the report. Never overwrite the clean baseline with a fault copy.
- Assign `packet-tracer/HQ-Branches-NOC-Lab.pkt` only to the validated baseline.

## Completion standard

Deliver a validated clean `.pkt`, matching full device configurations, a readable topology and addressing plan, repeatable checks with evidence, and four reproduced incidents with recovery reports. Then prepare a concise portfolio description and update the Network/NOC CV using verified lab work only; visually and ATS-check the exported CV.
