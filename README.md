# HQ + Branches NOC Lab

Portfolio-grade Cisco Packet Tracer project for Junior NOC, Network Support, Infrastructure Support, and Junior Network Engineer applications.

## Project objective

Design, build, secure, validate, and troubleshoot a fictional company network consisting of one headquarters site and two branch offices. The result should demonstrate both Cisco CCNA knowledge and an operational NOC mindset: monitoring symptoms, isolating faults, restoring service, documenting evidence, and escalating appropriately.

## Current state

The workspace and documentation structure are initialized. Phase 1 requirements
and architecture are in progress; the company profile, site roles, approximate
scale, and routed traffic policy are defined. See `STATUS.md` for the authoritative
current state.

## Source-of-truth files

- `STATUS.md` — current phase, completed work, blockers, and next action.
- `PROJECT_PLAN.md` — milestone sequence and acceptance criteria.
- `DECISIONS.md` — approved architecture decisions and their rationale.
- `CHANGELOG.md` — chronological record of material changes.
- `PROJECT_BRIEF.md` — business scenario and functional requirements.
- `TRAFFIC_POLICY.md` — intended permitted and denied routed traffic, with reusable test IDs.

## Directory map

```text
addressing/             VLAN, subnet, interface, and endpoint plans
configs/                Device configurations grouped by implementation layer
diagrams/               Logical and physical diagrams
incident-reports/       Troubleshooting scenarios and completed incident reports
packet-tracer/           Final Packet Tracer file and numbered checkpoints
references/             Carefully selected supporting notes
validation/             Test plan, command outputs, screenshots, and evidence
```

## Working workflow

1. Agree on the current phase's requirements.
2. Produce the smallest reviewable artifact.
3. Build or configure the corresponding Packet Tracer portion.
4. Run and record validation checks.
5. Save a numbered checkpoint.
6. Update project status and changelog.

## Resume the project in Codex

The current conversation can continue working on this folder without restarting. For a separate Codex CLI session, start it directly in the project directory:

```bash
codex -C '/home/alex/Database/Network-Lab-Portfolio/HQ-Branches-NOC-Lab'
```

In a new chat, the first request can be:

```text
Read AGENTS.md, README.md, STATUS.md, PROJECT_PLAN.md, and DECISIONS.md.
Continue the current Packet Tracer project phase without repeating completed work.
```

## High-level completion criteria

- End devices receive correct addressing and reach all permitted services.
- VLAN, trunk, STP, EtherChannel, routing, OSPF, DHCP, DNS, NAT/PAT, ACL, SSH, and selected Layer 2 security behavior are verified.
- Prohibited traffic is blocked as designed.
- Device and link failures can be diagnosed through a documented workflow.
- The clean baseline remains separate from intentionally broken troubleshooting copies.
