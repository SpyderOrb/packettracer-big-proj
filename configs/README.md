# Device configurations

One current capture per device. Configuration files describe the supplied state; the [validation record](../docs/VALIDATION.md) identifies what was tested and which checkpoint was used.

| Device | Capture | Reviewed scope / limitation |
|---|---|---|
| HQ-L3 | [HQ-L3.cfg](HQ-L3.cfg) | VLAN gateways, DHCP relay, inbound GUEST_HQ_IN on Vlan50, LACP/STP, routed G0/1 at 10.255.1.2/30, core-edge OSPF, SSH v2 and IT-only VTY ACL; complete capture with account credential redacted |
| HQ-R1 | [HQ-R1.cfg](HQ-R1.cfg) | Routed G0/0 at 10.255.1.1/30, core-edge and shared-WAN OSPF, G0/1 at 10.255.0.1/29, ISP edge/default origination and PAT with seven-subnet ACL 20, SSH v2, admin privilege 15 and IT-only VTY ACL; account credential redacted; complete capture |
| HQ-SW1 | [HQ-SW1.cfg](HQ-SW1.cfg) | Vlan10 .2/28, gateway .1, SSH v2, IT-only VTY ACL, access VLANs, Po1 and secondary STP priority; account and enable credentials redacted |
| HQ-SW2 | [HQ-SW2.cfg](HQ-SW2.cfg) | Vlan10 .3/28, gateway .1, SSH v2, IT-only VTY ACL, access VLANs and Po2; account and enable credentials redacted |
| KAT-R1 | [KAT-R1.cfg](KAT-R1.cfg) | Complete Sep 18 capture: inbound GUEST_KAT_IN on G0/0.50, DHCP relay, VLAN 10/30/50 gateways and native unaddressed VLAN 999; WAN /29 addressing and OSPF area 0 with passive LANs; SSH v2, IT-only ACL 10 on VTY 0–15; account/enable credentials redacted |
| KAT-SW1 | [KAT-SW1.cfg](KAT-SW1.cfg) | Complete capture: access VLANs 30/50, G0/1 trunk, management 10.20.10.2/28 and gateway 10.20.10.1; SSH v2, IT-only ACL 10 on VTY 0–15; account/enable credentials redacted |
| RZE-R1 | [RZE-R1.cfg](RZE-R1.cfg) | Complete Sep 18 capture: inbound GUEST_RZE_IN on G0/0.50, DHCP relay, VLAN 10/30/50 gateways and native unaddressed VLAN 999; WAN /29 addressing and OSPF area 0 with passive LANs; SSH v2, IT-only ACL 10 on VTY 0–15; account/enable credentials redacted |
| RZE-SW1 | [RZE-SW1.cfg](RZE-SW1.cfg) | Complete capture: access VLANs 30/50, G0/1 trunk, management 10.30.10.2/28 and gateway 10.30.10.1; SSH v2, IT-only ACL 10 on VTY 0–15; account/enable credentials redacted |
| WAN-SW | [WAN-SW.cfg](WAN-SW.cfg) | Complete capture: Fa0/1–3 access VLAN 900; no management IP |
| ISP-R1 | [ISP-R1.cfg](ISP-R1.cfg) | Complete capture: G0/0 198.51.100.1/30, G0/1 203.0.113.1/24; simulation infrastructure outside corporate OSPF |

Reviewed 2026-09-18. All ten captures are complete through `end`; the Sep 17 KAT-R1 re-export restores its initially missing opening lines. The four OSPF devices use the planned addresses, masks, router IDs and area 0 network statements. HQ-R1 enables both routed adjacencies; branches enable only G0/1. LAN interfaces are passive. Both HQ core-edge interfaces explicitly use point-to-point; the shared WAN uses the default Ethernet network type. WAN-SW assigns Fa0/1–3 to access VLAN 900.

All eight corporate captures include SSH v2, IT-only ACL 10 and restrictions on VTY 0–15. Branch login/privilege checks and reported server/Telnet refusals are recorded in [Validation](../docs/VALIDATION.md). Selected reported v03 reopen checks show restored HQ-R1 adjacencies and RZE SSH access, including switch enable elevation. Full persistence and exact export equality with the reopened file remain unverified. Credential-bearing originals are retained privately; public copies are redacted.

Sep 17 relay review: HQ-L3 and RZE-R1 exports are complete and all three routing devices include the two required helper statements. KAT-R1 was subsequently re-exported with version/global opening lines; missing lines were not reconstructed. Server-PT pool/DNS/HTTP settings require separate evidence in [Validation](../docs/VALIDATION.md).

Sep 18 edge review: HQ-R1/ISP-R1 captures match the tested edge addressing and routing. HQ-R1 retains IT-only management and translates seven client subnets through G0/2. Selected restart/service/PAT checks are recorded in Validation; exact export equality with reopened bytes is not established.

Sep 18 Guest review: fresh HQ-L3/KAT-R1/RZE-R1 captures contain the eight planned ACEs and inbound Guest interface bindings. Other non-credential settings match the previous captures, including relay, OSPF and management ACL 10. Guest flow evidence and remaining TP-07/TP-08 checks are recorded in Validation; other zone policies remain pending.

## Restore notes

- Account credential lines in the eight corporate captures, and captured enable-secret lines are replaced with `! REDACTED` comments. Exact originals are retained privately. Before enabling `login local`, recreate the local admin account through the console. HQ-L3 and HQ-R1 use account privilege 15; retain enable secrets for the verified access-switch elevation workflow after reopening. Public copies are not ready-to-restore backups.
- Before applying switch captures to a fresh device, create the site-specific VLANs: **HQ: 10 MGMT, 20 IT, 30 USERS, 40 SERVERS, 50 GUEST, 999 PARKING; branches: 10 MGMT, 30 USERS, 50 GUEST, 999 PARKING** from the [design](../docs/NETWORK.md#vlans-and-addressing). For WAN-SW, create VLAN 900 (captured name WAN_TRANSMIT). VLAN definitions are absent from these captures; normal-range VLAN data can reside separately in `vlan.dat`. [Cisco VLAN storage guide](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-2940-series-switches/109304-manage-vlandat.html)
- Use the matching model and inspect the complete capture before applying it. HQ management, SSH and core-edge OSPF are represented. DHCP relay is present on HQ-L3 Vlan30/50 and branch G0/0.30/.50. HQ PAT and conditional default origination are configured; Guest ACLs are configured; the remaining routed traffic policies are pending.
- Server-PT settings must be recorded separately when configured; IOS exports do not include them.

## Save and export

1. Run `copy running-config startup-config` on changed devices, then save the Packet Tracer working file separately.
2. Export **Running Config** through Config → GLOBAL → Settings → Export, or copy all of `show running-config` through the final `end`. Exclude prompts and pagination markers; record any redaction.
3. Preserve the previous export before replacing `<hostname>.cfg`. Record the checkpoint and its relevant verification results in [Validation](../docs/VALIDATION.md).
