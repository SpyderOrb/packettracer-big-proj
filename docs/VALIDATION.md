# Validation

**Reviewed 2026-09-13:** HQ VLANs, LACP, VLAN 30 STP roles, five SVIs, IT–Server traffic and the routed HQ link have supporting evidence. Authenticated SSH 2.0 sessions to HQ-SW1 and HQ-SW2 also work. Branch routing, services, remaining SSH targets, policy enforcement and failover tests remain pending. No complete clean baseline is validated.

The lab author ran the Packet Tracer checks. This record reviews supplied screenshots and configuration captures; expected results are separate from observed behavior. A planned diagram, configuration capture or saved file alone is not a passed traffic test.

## Checkpoints

No `.pkt` is currently published. The local v02 was reopened and its gateway/repeated server pings passed, but the file was subsequently resaved. The current bytes have not been matched to those tests; a new save/reopen check is required before publishing a downloadable checkpoint.

| State | Identity | Evidence / limitation |
|---|---|---|
| v02 when reviewed | 127,932 bytes; SHA-256 `d10e59c6821e72489f9bf50efca593dd6acd9ec9f8ed0dfdd4dca408b4c6b96b` | [HQ-L3](evidence/2026-09-13_v02_hq_l3_reopen.png) and [named checkpoint/pings](evidence/2026-09-13_v02_it_pc1_reopen_ping.png). SVI Protocol column cropped; full export equality unverified |
| v02 after resave | 128,136 bytes; SHA-256 `021b36db37aff721a5386ae53b4f765babf3c0e4be0d3acac944f8fc835f464e` | Retained locally; internal changes and repeat validation unconfirmed |

Other results below are working-session evidence unless explicitly tied to the reviewed file identity. The final clean baseline requires the complete test checklist.

## Verified results

| Area / date | Expected | Observed / evidence |
|---|---|---|
| Layout and model · Sep 7–9 | 20 devices / 21 links; HQ-L3 3560-24PS | [Overview](evidence/2026-09-09_full_topology.png) matches counts; [version](evidence/2026-09-07_hq_l3_version.png) identifies WS-C3560-24PS, IOS 12.2(37)SE1. [Interfaces](evidence/2026-09-07_hq_l3_interfaces.png) and [CDP](evidence/2026-09-07_hq_l3_cdp.png) match port numbers; CDP still uses default neighbor names |
| HQ access VLANs · Sep 9 | SW1 Fa1/2/3 → VLAN 30/20/40; SW2 Fa1/2 → VLAN 50/30 | [SW1](evidence/2026-09-09_hq_sw1_access_vlans.png) and [SW2](evidence/2026-09-09_hq_sw2_access_vlans.png) match; trunk native 999, allowed/active/forwarding lists 10,20,30,40,50,999 |
| LACP and STP · Sep 9 | Po1/Po2 SU with two P members; HQ-L3 root for VLAN 30 | [HQ-L3 after restart](evidence/2026-09-09_hq_l3_lacp_stp_after_restart.png) shows both bundles and only Po1/Po2 in STP. [Po1 roles](evidence/2026-09-09_hq_po1_stp_review.txt) is a labeled manual transcription: HQ-L3 base priority 24576, SW1 28672 and Po1 Root FWD. [SW2](evidence/2026-09-09_hq_po2_checks.png) shows Po2 Root FWD |
| HQ SVIs · Sep 13 | Five planned .1 gateways up/up with connected routes | [SVIs/routes](evidence/2026-09-13_hq_l3_svi_routes.png): VLANs 10/20/30/40/50 up/up, connected /28, /28, /26, /28, /27; startup-save acknowledgment visible |
| IT ↔ Server · Sep 13 | Both endpoints reach their own gateway and peer, 4/4 | [IT-PC1](evidence/2026-09-13_it_pc1_gateway_peer_ping.png): 10.10.20.10/28, gateway .20.1. [HQ-SRV1](evidence/2026-09-13_hq_srv1_gateway_peer_ping.png): 10.10.40.10/28, gateway .40.1. All four gateway/peer tests 4/4. Self-pings excluded from network-path evidence |
| HQ routed link · Sep 13 | .2/30 on HQ-L3 G0/1, .1/30 on HQ-R1 G0/0; up/up and peer pings 5/5 | [HQ-L3](evidence/2026-09-13_hq_l3_routed_link.png) and [HQ-R1](evidence/2026-09-13_hq_r1_routed_link.png) match addresses, connected 10.255.1.0/30 and bidirectional 5/5. No default route yet; client-to-edge routing untested |
| HQ switch management · Sep 13 | IT-PC1 reaches HQ-SW1 10.10.10.2 and HQ-SW2 10.10.10.3, 4/4 | [Management pings](evidence/2026-09-13_hq_management_ping.png): both destinations reply 4/4, 0% loss, TTL 254. Source identity follows the supplied test context; the capture does not show source addressing or the open checkpoint. Saved-state persistence remains untested |
| HQ-SW1 SSH · Sep 13 | IT-PC1 authenticates to 10.10.10.2 and runs a command | [SSH session](evidence/2026-09-13_hq_sw1_ssh_login.png): login as admin reaches HQ-SW1 privileged EXEC; remote show ip interface reports Vlan10 10.10.10.2/28 up/up. Source follows test context. [SSH status](evidence/2026-09-13_hq_sw1_ssh_version.png) confirms version 2.0, authentication timeout 120 seconds and 3 retries. VTY source filtering and checkpoint persistence remain unverified |
| HQ-SW2 SSH · Sep 13 | IT-PC1 authenticates to 10.10.10.3 and verifies SSH 2.0 | [Login and SSH status](evidence/2026-09-13_hq_sw2_ssh_login_version.png): login as admin reaches HQ-SW2 privileged EXEC; SSH enabled, version 2.0, timeout 120 seconds, 3 retries. Source follows test context. VTY source filtering and checkpoint persistence remain unverified |
| HQ access-switch Telnet · Sep 13 | No Telnet login on 10.10.10.2 or 10.10.10.3 | [Telnet attempts](evidence/2026-09-13_hq_switches_telnet_closed.png): both attempts report Open, then Connection closed by foreign host, with no login prompt. PASS for observed denial of Telnet login; updated exports confirm transport input ssh on both VTY ranges. Source follows the IT-PC1 test context |
| HQ access-switch privilege · Sep 13 | Administrative sessions report privilege level 15 | Author reports `Current privilege level is 15` on both HQ-SW1 and HQ-SW2. User-reported result only: no supporting screenshot or raw output supplied; current exports predate this report |
| Configuration review · Sep 13 | Captures match observed operation and intended management settings | [Four captures](../configs/README.md): updated SW1/SW2 include correct Vlan10 /28 addresses, default gateway, SSH v2, login local, transport input ssh and access-class 10 in on both VTY ranges. ACL 10 permits only 10.10.20.0/28. Earlier interface/STP settings are unchanged. Public account credential lines are redacted; exports matching the later privilege report remain pending. HQ-L3/HQ-R1 opening lines remain incomplete |

## Troubleshooting observations

These are setup observations, not the four completed incident exercises.

| Observation | Follow-up / outcome |
|---|---|
| Po1 [VLAN-mask warning](evidence/2026-09-09_hq_l3_po1_vlan_mismatch.png) and [suspended members](evidence/2026-09-09_hq_l3_po1_suspended.png) | Later [HQ-L3](evidence/2026-09-09_hq_l3_po1_trunk.png) and [SW1](evidence/2026-09-09_hq_sw1_po1_trunk.png) show SU/P. The exact corrective sequence was not captured |
| SW1 initially had no forwarding VLANs; later became VLAN 30 root | [SW1 forwarding/root output](evidence/2026-09-09_hq_sw1_po1_forwarding.png), followed by [intended root-role verification](evidence/2026-09-09_hq_po1_stp_review.txt). Cause of the initial empty list is unconfirmed |
| HQ-L3 listed Po2 and its physical members separately in STP | [Before](evidence/2026-09-09_hq_po2_checks.png) and [after reported restart](evidence/2026-09-09_hq_l3_lacp_stp_after_restart.png): extra rows disappeared; cause unconfirmed |
| Initial ping loss | Earlier working-session IT → Server test was 3/4; later bidirectional tests passed. In [v02](evidence/2026-09-13_v02_it_pc1_reopen_ping.png), server ping was 3/4 then 4/4. The [routed-link capture](evidence/2026-09-13_hq_l3_routed_link.png) also begins with a cropped 4/5 summary, then shows peer ping 5/5. No packet capture establishes the loss cause |

## Test checklist

Partial means only the listed subchecks passed. Keep B1–B10 identifiers for future results.

| ID | Method and expected result | State |
|---|---|---|
| B1 | Open saved topology; verify 20 devices, 21 links, exact models/ports and required command support | Partial: layout/model and selected v02 reopen checks; full reopened inventory and named CDP peers pending |
| B2 | VLAN/trunk/interface/route checks; local gateways and HQ /30 work | Partial: HQ results above; HQ switch management pings also pass; remaining endpoints, branch LANs and persistence of recent changes pending |
| B3 | HQ-L3 root; both LACP bundles SU/P. Independently disable/restore one member of each bundle; HQ-PC1/PC2 → 10.10.30.1 remains reachable | Partial: bundling and VLAN 30 roles; other VLAN root roles and member-failure/recovery traffic tests pending |
| B4 | IT-PC1 can SSH to all eight corporate management addresses; Telnet disabled | Partial: HQ-SW1/HQ-SW2 SSH 2.0 logins pass and Telnet attempts close without login; VTY SSH-only/local-login/IT ACL settings match the exports. Privilege 15 is author-reported on both switches; corresponding captures, denied-source testing and other six devices pending |
| B5 | OSPF neighbors FULL: HQ-R1 3, HQ-L3 1, each branch 2; correct /29 broadcast and /30 point-to-point types, learned HQ routes and default | Not run |
| B6 | Renew all six DHCP client groups; correct address/mask/gateway/DNS; relay on HQ-L3 SVIs 30/50 and branch G0/0.30/.50 | Not run |
| B7 | Corporate internal/external DNS and HTTP work; guests resolve external services | Not run |
| B8 | External HTTP/ICMP translated to 198.51.100.2; inspect HQ-R1 NAT translations, statistics and return routes | Not run |
| B9 | Every TP-01–TP-13 permit/deny has evidence and an established cause | Not run |
| B10 | Save/reopen the clean baseline; full device exports match; repeat service, policy and regression checks | Not run |

## Policy coverage

Use the individual TP IDs in result entries even where the table groups their setup. Repeat checks at both branches and all three guest zones. For a limited permit, also try an unlisted protocol with a known working destination service or use ACL evidence to establish the intended denial.

| Rules | Representative check |
|---|---|
| TP-01, TP-02 | HQ-PC1, KAT-PC1, RZE-PC1: internal DNS and HTTP work; unlisted server access is denied |
| TP-03, TP-04, TP-05 | IT-PC1: DNS/HTTP/ICMP to HQ-SRV1; SSH/ICMP to all eight corporate network devices, including HQ-L3 at 10.10.10.1 and HQ-R1 at 10.255.1.1; ICMP to corporate user PCs |
| TP-06 | Each corporate user site: external HTTP and ICMP work through PAT |
| TP-07, TP-08 | Each guest: DHCP and external DNS/HTTP/ICMP work; tests to internal server, user, IT, and management zones are denied |
| TP-09, TP-10, TP-11 | Corporate users: management access (including HQ-R1 at 10.255.1.1), new access to IT, and cross-zone user access are denied; replies to permitted IT diagnostics still work |
| TP-12 | External source: no internal service publication; record edge ACL/NAT state and the actual attempted inbound path |
| TP-13 | Pick an unlisted routed pair, such as IT → Guest; show intended denial |

A failed ping alone does not establish ACL enforcement. Check the service, routing, and return path, then collect ACL counters if supported or Packet Tracer Simulation Mode evidence. A timeout caused by a missing route or a disabled service is not an ACL pass. For TP-12, distinguish lack of a NAT mapping from an explicit ACL drop; use a separate verification copy if a temporary route is needed to isolate ACL behavior.

For HQ inter-VLAN cases, collect the relevant SVI ACL evidence on HQ-L3; HQ Users-to-Servers traffic does not traverse HQ-R1. For branch-originated policy collect branch router evidence, and for Internet-edge behavior collect HQ-R1 evidence. Verify DHCP and permitted reply traffic after applying ACLs.

## Recording a new result

Update the relevant result/checklist row and link the evidence. Retain failures alongside recovery. Include the date, exact checkpoint or working-file context, executor, command/source/destination, expected result and actual result. Capture endpoint addresses at test time.

Screenshots must show readable device names, commands and results. Preserve originals; label any manual transcription. For each new checkpoint, save startup configurations, save and reopen the `.pkt`, run the required checks and export the matching full configurations. The final baseline requires B1–B10 and every TP rule to pass.
