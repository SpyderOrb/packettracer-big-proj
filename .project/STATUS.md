# Working status

Updated: **2026-09-05**. Current block: **1 — Build sheet and topology** (`in progress`).

## Next action

Open Packet Tracer, confirm the target models and ports, then assemble and save the first topology using [the build sheet](../docs/NETWORK.md#first-packet-tracer-checkpoint). Close and reopen `HQ-Branches-NOC-Lab_v01_physical-topology.pkt` and record B1. Proceed to configuration as soon as that passes.

For the first review, save a topology overview and readable port close-ups in `docs/evidence/`, then provide their paths and confirm whether v01 reopened. The [working routine](../README.md#working-with-codex) explains reading order, file locations, and the division between user-executed tests and Codex evidence review.

The documentation restructure and address-plan review are complete. Topology assembly, a `.pkt` save/reopen, and runtime feature support checks remain pending. Those checks require direct interaction with Packet Tracer.

## Five working blocks

| Block | Deliverable and completion condition | State |
|---|---|---|
| 1. Build sheet and topology | Concise design, addressing, actual model/port check, named/cabled devices, saved and reopened v01 (B1) | In progress |
| 2. Local networks and management | VLANs, trunks, STP/EtherChannel, inter-VLAN routing and SSH configured; B2–B3 pass, B4 completed as remote paths become available | Pending |
| 3. Site connectivity and services | OSPF, DHCP relay, DNS and PAT work; B4–B8 pass; save working services checkpoint | Pending |
| 4. Access controls and clean baseline | TP-01–TP-13 enforced; B9–B10 and regression checks pass; full exports match the validated baseline | Pending |
| 5. Incidents and portfolio | Four reproduced incidents and recovery reports; concise README, portfolio/LinkedIn text and updated, visually/ATS-checked CV based on verified work | Pending |

Use a short configure → test → save → export → record loop inside every block. Block completion depends on evidence, not on document count.

## Current artifacts

- [Build sheet](../docs/NETWORK.md), [planned diagram](../docs/topology.png), and [test checklist](../docs/VALIDATION.md): prepared.
- Latest `.pkt` checkpoint / validated baseline: **none / none**.
- Device configuration exports / network test evidence: **none / none**.
- Incident reports: **template only**. Planned faults: wrong access VLAN, OSPF adjacency failure, DHCP relay error, ACL blocking a required service.

## Simulator and publication scope

- Target simulator: Cisco Packet Tracer 9.0.1. Actual model and feature checks remain pending.
- The local package version was checked, but an installation check is not network validation.
- Active documentation, the planned diagram, templates, and these working notes form the repository snapshot.
- Historical planning archives, machine-specific setup notes, local agent state, installers, and credentials are excluded from Git. No active Markdown link depends on excluded files.

## Maintain only these active sources

- `README.md`: reviewer entry point.
- `docs/NETWORK.md`: topology, addressing, service settings and policy.
- `docs/VALIDATION.md`: test expectations and observed results.
- `.project/STATUS.md`, `DECISIONS.md`, `CHANGELOG.md`: working state and history.

The former twelve-phase plan is retained locally as history. The five working blocks above control the build; routine configuration steps do not require another planning approval.
