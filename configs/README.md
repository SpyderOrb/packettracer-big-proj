# Device configurations

One current capture per device. Configuration files describe the supplied state; the [validation record](../docs/VALIDATION.md) identifies what was tested and which checkpoint was used.

| Device | Capture | Reviewed scope / limitation |
|---|---|---|
| HQ-L3 | [HQ-L3.cfg](HQ-L3.cfg) | VLAN gateways, LACP/STP, routed G0/1 at 10.255.1.2/30, core-edge OSPF, SSH v2 and IT-only VTY ACL; complete capture with account credential redacted |
| HQ-R1 | [HQ-R1.cfg](HQ-R1.cfg) | Routed G0/0 at 10.255.1.1/30, core-edge OSPF, SSH v2, admin privilege 15 and IT-only VTY ACL; account credential redacted; final end marker missing |
| HQ-SW1 | [HQ-SW1.cfg](HQ-SW1.cfg) | Vlan10 .2/28, gateway .1, SSH v2, IT-only VTY ACL, access VLANs, Po1 and secondary STP priority; account and enable credentials redacted |
| HQ-SW2 | [HQ-SW2.cfg](HQ-SW2.cfg) | Vlan10 .3/28, gateway .1, SSH v2, IT-only VTY ACL, access VLANs and Po2; account and enable credentials redacted |

Reviewed 2026-09-14. HQ-L3 and both access-switch captures are complete. HQ-L3 includes explicit account privilege 15. SW1/SW2 omit that account parameter but now include enable secrets: their tested administrative workflow is SSH login followed by password-authenticated enable. Both report privilege 15 after the author's reported reopen check; see [Validation](../docs/VALIDATION.md). Exact export equality with a reopened .pkt is not independently established. The earlier v02 was resaved after review and remains unverified. New HQ-L3/HQ-R1 captures include process 1, area 0, the planned router IDs and point-to-point core-edge interfaces. HQ-R1 also includes the corrected IT-only VTY ACL. Its opening lines are now present, but the final `end` marker is missing. The latest working file was saved after these tests; its exact configuration correspondence and persistence have not been verified by reopening. Missing commands have not been reconstructed; other device exports and server settings remain pending.

## Restore notes

- Account credential lines in all four device captures and enable-secret lines in SW1/SW2 are replaced with `! REDACTED` comments. Exact originals are retained privately. Before enabling `login local`, recreate the local admin account through the console. HQ-L3 and HQ-R1 use account privilege 15; SW1/SW2 also require an enable secret for the verified remote elevation workflow. Public copies are not ready-to-restore backups.
- Before applying switch captures to a fresh device, create VLANs **10 MGMT, 20 IT, 30 USERS, 40 SERVERS, 50 GUEST and 999 PARKING** from the [design](../docs/NETWORK.md#vlans-and-addressing). VLAN definitions are absent from these captures; normal-range VLAN data can reside separately in `vlan.dat`. [Cisco VLAN storage guide](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-2940-series-switches/109304-manage-vlandat.html)
- Use the matching model and inspect the complete capture before applying it. HQ management, SSH and core-edge OSPF are represented. DHCP relay, PAT and the full routed traffic policy remain unconfigured.
- Server-PT settings must be recorded separately when configured; IOS exports do not include them.

## Save and export

1. Run `copy running-config startup-config` on changed devices, then save the Packet Tracer working file separately.
2. Copy **all** of `show running-config`, including the opening configuration lines through the final `end`. Exclude prompts and pagination markers; record any redaction.
3. Preserve the previous export before replacing `<hostname>.cfg`. Record the checkpoint and its relevant verification results in [Validation](../docs/VALIDATION.md).
