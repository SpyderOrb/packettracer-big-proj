# Changelog

## 2026-09-05 — Prepared the documentation snapshot for publication

- Included the README, network build sheet, validation checklist, diagram, configuration export guide, incident template, and current working notes in the publication scope.
- Removed machine-specific paths and links to local-only archives from published documents. Preserved the previous working documents locally before editing.
- Added ignore rules for local planning archives, agent state, credentials, and proprietary installers. Kept placeholders for the future checkpoint and evidence directories.
- Checked the exact 14-file Git snapshot: all 22 internal links/anchors resolve within it. Secret-pattern and machine-specific-path scans found no matches; local archive hashes remained unchanged.
- Kept the project explicitly in Block 1: no `.pkt`, runtime test result, completed incident, or CV achievement is claimed.

## 2026-09-05 — Simplified the workflow and documented review steps

- Replaced twelve phases with five practical blocks and consolidated design/addressing into one build sheet.
- Defined the target 19-device topology, 19 links, 11 VLAN subnets, three transit/external subnets, and six DHCP pools; reviewed the address ranges and port assignments statically.
- Retained TP-01–TP-13 and added a repeatable validation checklist. All network results remain not run.
- Added a planned topology diagram, full-configuration export instructions, and screenshot/command-output evidence requirements.
- Established English project files and Russian chat; separated user-executed Packet Tracer checks from evidence review.

## 2026-08-31 — Defined the routed traffic policy

- Specified permitted services, guest isolation, HQ IT management access, and default-deny routed zone boundaries.
- Identified DHCP, routing control, gateway operation, and reply traffic as required infrastructure exceptions.

## 2026-08-30 — Initialized the lab

- Defined one headquarters in Kraków and branches in Katowice and Rzeszów, with representative endpoints sized for a fictional company of about 72 staff.
- Created the project workspace and agreed to preserve clean checkpoints separately from intentional faults.
