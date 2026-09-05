# Validation

**Network results: not run.** The build-sheet review is not Packet Tracer evidence. Each result below must identify the actual tested checkpoint, expected behavior, observed behavior, and supporting evidence.

## Checks during the build

| ID | Check and method | Expected result | Actual / evidence |
|---|---|---|---|
| B1 | Open, save, and reopen v01; inspect devices and cables | 19 named devices, 19 links; actual models/ports match the build sheet | Not run / — |
| B2 | `show vlan brief`, `show interfaces trunk`, gateway tests with temporary static client IPs | Correct access VLANs, allowed/native VLANs, and local gateways | Not run / — |
| B3 | `show spanning-tree`, `show etherchannel summary`; disable one Po1 member, test HQ-PC2 → HQ gateway, then restore | HQ-SW1 root; two bundled members; gateway access survives a single member failure and restoration | Not run / — |
| B4 | SSH from IT-PC1 to every corporate management IP | Successful SSH after routed reachability exists; Telnet disabled | Not run / — |
| B5 | `show ip ospf neighbor`, `show ip route`; test HQ/branch paths | Three routers share transit; each has two FULL neighbors, remote VLAN routes, branches have HQ-originated default | Not run / — |
| B6 | Renew every DHCP client and inspect address, mask, gateway, DNS | Leases fit the six pools; corporate and guest DNS settings differ correctly | Not run / — |
| B7 | Resolve and browse internal/external names from applicable clients | Corporate clients reach intranet and external web; guests resolve external web through external DNS | Not run / — |
| B8 | Generate external HTTP/ICMP; `show ip nat translations`, `show ip nat statistics` | HQ and both branch client sources translate to 198.51.100.2 | Not run / — |
| B9 | Test TP-01–TP-13 using the coverage table below | All required permits and denies have evidence and an explained cause | Not run / — |
| B10 | Save device startup configs and checkpoint; close/reopen; export configs; repeat service and policy checks | Reloaded file retains configuration and services; exports match that exact checkpoint | Not run / — |

Run relevant checks immediately after each configuration slice. B4 needs routed connectivity for branch management and is completed when that path exists. B5 may have a transient DR election period; record the settled neighbor state. Command support must be checked on the actual model; record a supported alternative if needed.

## Policy coverage

Use the individual TP IDs in result entries even where the table groups their setup. Repeat checks at both branches and all three guest zones. For a limited permit, also try an unlisted protocol with a known working destination service or use ACL evidence to establish the intended denial.

| Rules | Representative check |
|---|---|
| TP-01, TP-02 | HQ-PC1, KAT-PC1, RZE-PC1: internal DNS and HTTP work; unlisted server access is denied |
| TP-03, TP-04, TP-05 | IT-PC1: DNS/HTTP/ICMP to HQ-SRV1; SSH/ICMP to all seven corporate network devices; ICMP to corporate user PCs |
| TP-06 | Each corporate user site: external HTTP and ICMP work through PAT |
| TP-07, TP-08 | Each guest: DHCP and external DNS/HTTP/ICMP work; tests to internal server, user, IT, and management zones are denied |
| TP-09, TP-10, TP-11 | Corporate users: management access, new access to IT, and cross-zone user access are denied; replies to permitted IT diagnostics still work |
| TP-12 | External source: no internal service publication; record edge ACL/NAT state and the actual attempted inbound path |
| TP-13 | Pick an unlisted routed pair, such as IT → Guest; show intended denial |

A failed ping alone does not establish ACL enforcement. Check the service, routing, and return path, then collect ACL counters if supported or Packet Tracer Simulation Mode evidence. A timeout caused by a missing route or a disabled service is not an ACL pass. For TP-12, distinguish lack of a NAT mapping from an explicit ACL drop; use a separate verification copy if a temporary route is needed to isolate ACL behavior.

## Recording results

Append short entries here as checks are executed; keep raw output and screenshots in `docs/evidence/`. Use filenames such as `v02_B3_etherchannel.txt`. Include the policy ID in the filename for a policy test. Capture test endpoint addresses at execution time because DHCP leases may change.

For screenshots, keep device names, relevant port labels, or the command and its full result readable. Use one overview plus close-ups when the whole topology is too dense. For text output, include the device prompt, command, and complete response. Failed checks and CLI errors are useful evidence: preserve them before making a correction, then capture the new result under a different filename.

If the user runs a check and Codex reviews its output, record that execution source. Do not describe an evidence review as Codex opening or operating the `.pkt`. Keep the checkpoint filename consistent across the report, configuration exports, and screenshots.

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
