# Validation

**Status:** complete layout screenshot, HQ-L3 inventory and VLAN creation on all three HQ switches recorded; checkpoint persistence and end-to-end network validation pending. Each result must distinguish expected behavior from observed output and identify its checkpoint or working-file context.

## Checks during the build

| ID | Check and method | Expected result | Actual / evidence |
|---|---|---|---|
| B1 | Save/reopen the first complete HQ-L3 checkpoint; inspect devices, ports and model support | 20 named devices, 21 physical links; HQ-L3 is 3560-24PS; four LACP candidate links and no direct HQ-SW1–HQ-SW2 link; exact model/port differences recorded | Partial — full 20-device/21-link screenshot and HQ-L3 output reviewed; checkpoint/reopen and remaining support checks pending; see dated reviews below |
| B2 | `show vlan brief`, `show interfaces trunk`, `show ip interface brief`, `show ip route`; gateway and core–edge tests | HQ gateways on HQ-L3 SVIs; branch gateways on router subinterfaces; correct allowed/native VLANs; HQ-L3 G0/1 and HQ-R1 G0/0 use the /30 as routed interfaces, not a trunk | Partial — VLAN IDs/names observed on HQ-L3, HQ-SW1 and HQ-SW2; trunks, SVIs and routed-link tests pending; see dated VLAN reviews below |
| B3 | `show spanning-tree`, `show etherchannel summary`; independently disable/restore one Po1 member and one Po2 member | HQ-L3 root; two bundled members per channel; HQ-PC1 → 10.10.30.1 survives Po1 member loss, HQ-PC2 → 10.10.30.1 survives Po2 member loss; both bundles fully restored | Not run / — |
| B4 | SSH from IT-PC1 to every corporate management IP | Successful SSH after routed reachability exists; Telnet disabled | Not run / — |
| B5 | `show ip ospf neighbor`, `show ip ospf interface`, `show ip route`; test HQ/branch paths | HQ-R1 has 3 FULL neighbors, HQ-L3 has 1, each branch has 2; /29 broadcast and /30 point-to-point types match design; HQ-R1 learns HQ VLAN routes through HQ-L3; HQ-L3 and branches learn the HQ-R1-originated default | Not run / — |
| B6 | Renew every DHCP client; inspect address/mask/gateway/DNS and relay placement | Six pools work; HQ relay on HQ-L3 SVIs 30/50 and branch relay on G0/0.30/.50; no client relay on HQ-R1; corporate/guest DNS settings match design | Not run / — |
| B7 | Resolve and browse internal/external names from applicable clients | Corporate clients reach intranet and external web; guests resolve external web through external DNS | Not run / — |
| B8 | Generate external HTTP/ICMP; inspect HQ-R1 `show ip nat translations`, `show ip nat statistics` and return routes | HQ traffic through HQ-L3 and both branches translate to 198.51.100.2; HQ-R1 G0/0 and G0/1 inside, G0/2 outside; no NAT on HQ-L3 | Not run / — |
| B9 | Test TP-01–TP-13 using the coverage table below | All required permits and denies have evidence and an explained cause | Not run / — |
| B10 | Save device startup configs and checkpoint; close/reopen; export configs; repeat service and policy checks | Reloaded file retains configuration and services; exports match that exact checkpoint | Not run / — |

Run relevant checks immediately after each configuration slice. B4 needs routed connectivity for branch management and is completed when that path exists. B5 may have a transient DR election period; record the settled neighbor state. Command support must be checked on the actual model; record a supported alternative if needed.

The 2026-09-08 full overview shows all 20 devices and 21 physical links, including the WAN and simulated Internet. Earlier separate site views cover 17 devices and 16 links. B1 remains incomplete until a matching checkpoint is checked and reopened; preserve an existing checkpoint and use the next unused number when necessary.

On HQ-L3, capture version/port information and confirm CLI support for `ip routing`, `interface vlan`, `no switchport`, `router ospf`, `ip ospf network point-to-point`, `ip helper-address`, ACLs and LACP before configuration. Use CLI help to check trunk-encapsulation syntax. Command acceptance is only a support check; B2–B9 establish behavior. For B3, capture baseline, single-member failure and recovery separately for each bundle; this tests member-link resilience, not core-switch or gateway failover.

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

## Recording results

Append short entries here as checks are executed; keep raw output and screenshots in `docs/evidence/`. Use filenames such as `v02_B3_etherchannel.txt`. Include the policy ID in the filename for a policy test. Capture test endpoint addresses at execution time because DHCP leases may change.

### 2026-09-07 — Site layout and HQ-L3 inventory review

- **Execution/review:** lab author ran the commands and supplied screenshots; review covered the visible output and site layouts. Screenshots are preserved without image edits. The version output is cropped; only visible fields are recorded.
- **Working-file context:** `HQ-Branches-NOC-Lab_working_l3.pkt`, 103,965 bytes; SHA-256 `a89ce62431e0037881da161946f9b85070e7a7d266cda6c216a3a9ee9fcfe869`. Saving was reported and file presence/hash checked. The file was not opened during review; screenshot-to-file consistency and reopen persistence remain unverified. This is not a published or validated checkpoint.

| Check | Expected | Observed | Evidence |
|---|---|---|---|
| HQ layout | Nine devices, ten cables; separate HQ-L3 access pairs | Named devices and visible cabling match the HQ design; amber indicators remain on one link in each pair | [HQ](evidence/2026-09-07_hq_topology.png) |
| Branch layouts | Four devices and three cables per branch | Models, names and visible router/switch port labels match; router-to-switch indicators are now green in both views | [Katowice](evidence/2026-09-07_kat_topology.png), [Rzeszow](evidence/2026-09-07_rze_topology.png) |
| HQ-L3 inventory | 3560-24PS with the required physical ports | Visible model WS-C3560-24PS; C3560-ADVIPSERVICESK9-M, IOS 12.2(37)SE1; F0/1–24 and G0/1–2 listed | [Version](evidence/2026-09-07_hq_l3_version.png), [Interfaces](evidence/2026-09-07_hq_l3_interfaces.png) |
| Used HQ-L3 interfaces | F0/1–4 and G0/1 operational | These five ports show up/up; addresses unassigned. Other physical ports show down/down; Vlan1 is administratively down/down | [Interfaces](evidence/2026-09-07_hq_l3_interfaces.png) |
| HQ-L3 CDP port pairs | G0/1 → router G0/0; F0/1–4 → switch F0/23, F0/24, F0/23, F0/24 | All five local/remote port-number pairs match; router platform C2900 and switch platform 2960. Neighbor IDs are still Router/Switch, so switch identities require hostname confirmation | [CDP](evidence/2026-09-07_hq_l3_cdp.png) |

**Result:** partial B1 evidence only. VLAN gateways, LACP operation, routing, DHCP, NAT, ACLs, full-topology completeness and save/reopen persistence have not passed validation. Set unique IOS hostnames during configuration and recapture CDP before accepting named peer identities.

### 2026-09-08 — HQ-L3 VLAN creation

- **Execution/review:** lab author executed `show vlan brief`; review covers the supplied [original screenshot](evidence/2026-09-08_hq_l3_vlans.png). No configuration was applied during review.
- **Expected:** HQ-L3 has VLANs 10 MGMT, 20 IT, 30 USERS, 40 SERVERS, 50 GUEST and 999 PARKING, all active.
- **Observed:** all six IDs/names match and show `active`; the prompt is `HQ-L3#`. Their port columns are empty. VLAN 1 lists Fa0/1–24 and Gig0/1–2. This confirms local VLAN creation, not port assignment, trunking, SVI reachability or inter-VLAN routing.
- **Save context:** no matching saved checkpoint has been verified; the screenshot does not identify the open filename. Startup configuration and saved VLAN-database persistence have not been checked.
- **Result:** the HQ-L3 VLAN-creation slice matches its expected output; B2 remains partial. The following entry covers matching VLANs on HQ-SW1 and HQ-SW2. B3 and the remaining network behavior checks are not run.

### 2026-09-08 — HQ access-switch VLAN creation

- **Execution/review:** lab author configured HQ-SW1 and HQ-SW2, ran `wr` and `show vlan brief`, and supplied screenshots. Review covers the original [HQ-SW1 output](evidence/2026-09-08_hq_sw1_vlans.png) and [HQ-SW2 output](evidence/2026-09-08_hq_sw2_vlans.png), preserved without image edits.
- **Expected:** each switch has VLANs 10 MGMT, 20 IT, 30 USERS, 40 SERVERS, 50 GUEST and 999 PARKING, all active, with a matching IOS hostname.
- **Observed:** both outputs match all six IDs/names/statuses and show the correct device prompt. New VLAN port columns are empty; VLAN 1 still lists Fa0/1–24 and Gig0/1–2. Both `wr` commands return `Building configuration... [OK]`.
- **Save context:** the current working file is `HQ-Branches-NOC-Lab_working_l3.pkt`, 121,971 bytes; SHA-256 `6752063f9d3cbc1a445a64f65cfa0adb6dc898e4a9153b672f371ff76c1dc210`. Its on-disk identity was checked, but it was not opened during review. Save-command acknowledgments do not establish screenshot-to-file consistency or VLAN/configuration persistence after reopening; no matching checkpoint has been verified.
- **Result:** VLAN creation is observed on all three HQ switches. B2 remains partial; access-port assignment, trunks, SVIs and routing are pending. LACP support and operation are the next practical slice; B3 has not been run.

### 2026-09-08 — Complete topology overview

- **Execution/review:** lab author supplied the [current Packet Tracer overview](evidence/2026-09-08_full_topology.png); review covers the visible layout. The original screenshot is preserved without image edits.
- **Expected:** 20 devices and 21 cables: HQ with its collapsed core and two separate access-switch pairs, two branches, shared WAN transport, and an ISP router with an external server.
- **Observed:** all 20 devices and 21 cables are visible. Site-router G0/1 ports connect to WAN-SW F0/1, F0/2 and F0/3. HQ-R1 G0/2 connects to ISP-R1 G0/0; ISP-R1 G0/1 connects to EXT-SRV1. The two HQ access pairs remain separate, with no direct HQ-SW1–HQ-SW2 cable. An amber indicator is visible in each pair; no STP/LACP command output diagnoses their state. Some device labels overlap, and endpoint port labels are not shown.
- **Save context:** the screenshot does not identify its open filename. No corresponding checkpoint was opened or tested during review.
- **Result:** visible device/link counts match the build sheet. B1 remains partial pending checkpoint/reopen and remaining support checks. The DNS/HTTP annotation describes an intended service role; it does not verify service operation.

For screenshots, keep device names, relevant port labels, or the command and its full result readable. Use one overview plus close-ups when the whole topology is too dense. For text output, include the device prompt, command, and complete response. Failed checks and CLI errors are useful evidence: preserve them before making a correction, then capture the new result under a different filename.

Record who executed each check and how its result was reviewed. Distinguish direct Packet Tracer testing from inspection of saved output. Keep the checkpoint filename consistent across the report, configuration exports, and screenshots.

```text
Test ID / date / Packet Tracer version:
Checkpoint filename:
Executed by / review method:
Source and destination / method:
Expected:
Observed:
Evidence link:
Result: PASS / FAIL / BLOCKED
```

Do not mark the clean baseline validated until B1–B10 and every TP rule are covered with evidence. The final baseline and text configuration exports must identify the same saved state. Preserve earlier checkpoints.
