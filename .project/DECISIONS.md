# Decisions

The current build is specified in [NETWORK.md](../docs/NETWORK.md). Accepted design choices are not implementation evidence. Earlier planning notes are retained locally; this table records the current decisions needed to understand and reproduce the lab.

| ID / date | Decision | Reason / status |
|---|---|---|
| D-001 / 2026-08-30 | Keep the topology, configurations, and evidence together in the project repository | Portable and reproducible project layout; local location remains unchanged |
| D-002 / 2026-08-30 | Work gradually and persist state in files | Retained; five practical blocks replace the old phase sequence |
| D-003 / 2026-08-30 | One headquarters and two branches | Useful routing and support scenarios; retained |
| D-004 / 2026-08-30 | Earlier provisional detailed architecture | Superseded by D-010 and the current build sheet |
| D-005 / 2026-08-30 | Kraków 44 staff, Katowice 16, Rzeszów 12; shared HQ services | Retained without unnecessary departmental detail |
| D-006 / 2026-08-30 | Representative endpoints with realistic subnet capacity | Retained; eight PCs represent the client zones and both HQ switches |
| D-007 / 2026-08-30 | Segment by trust/function; Management means infrastructure | Retained |
| D-008 / 2026-08-31 | Default-deny routed zone policy with explicit service, management and infrastructure exceptions | TP-01–TP-13 retained in the build sheet; not yet enforced |
| D-009 / 2026-09-05 | Use English for project documents and explanations within files, and Russian in chat; five working blocks, one build sheet and one validation document | User requested a practical focus, easier reviewer navigation, and clarified the chat language; active |
| D-010 / 2026-09-05 | Router-on-a-stick at each site, one shared Ethernet OSPF transit, HQ Internet exit, two HQ switches with LACP | Avoids WAN modules and duplicate routing methods; limited link redundancy only. Working design; models/commands await simulator checks |
| D-011 / 2026-09-05 | Reuse functional VLAN IDs across separate site prefixes; static infrastructure and six centralized DHCP pools | Makes addressing and repeated configuration easy to explain; ranges statically reviewed |
| D-012 / 2026-09-05 | One complete config export per device; keep fault copies with incident reports | Reviewers can inspect each device's actual state and reproduce faults; active |
| D-013 / 2026-09-05 | Keep DHCP snooping/DAI and further Layer 2 protections optional after the core baseline | Focus on the core configuration and troubleshooting scope; add only after local support checks |
| D-014 / 2026-09-05 | Publish active documentation, diagrams, templates, and current working notes; exclude historical local archives, agent state, installers, and credentials | User authorized commit and push of shareable material; README links must resolve within the published repository |
