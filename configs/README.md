# Device configurations

One complete running-configuration capture per IOS device. These are redacted reference configurations, not ready-to-restore backups. The [validation record](../docs/VALIDATION.md) identifies runtime evidence, author-reported outcomes and the associated saved states.

| Device | Capture | Configuration scope |
|---|---|---|
| HQ-L3 | [HQ-L3.cfg](HQ-L3.cfg) | Five VLAN gateways and inbound zone ACLs; DHCP relay; LACP/STP; routed core–edge link; OSPF; SSH |
| HQ-R1 | [HQ-R1.cfg](HQ-R1.cfg) | Core–edge and shared-WAN OSPF; conditional default origination; seven-subnet PAT list; ISP_IN; SSH |
| HQ-SW1 | [HQ-SW1.cfg](HQ-SW1.cfg) | Management 10.10.10.2/28; access VLANs; Po1; secondary STP priority; SSH |
| HQ-SW2 | [HQ-SW2.cfg](HQ-SW2.cfg) | Management 10.10.10.3/28; access VLANs; Po2; SSH |
| KAT-R1 | [KAT-R1.cfg](KAT-R1.cfg) | VLAN 10/30/50 gateways and inbound zone ACLs; native VLAN 999; DHCP relay; WAN OSPF; SSH |
| KAT-SW1 | [KAT-SW1.cfg](KAT-SW1.cfg) | Management 10.20.10.2/28; access VLANs 30/50; G0/1 trunk; SSH |
| RZE-R1 | [RZE-R1.cfg](RZE-R1.cfg) | VLAN 10/30/50 gateways and inbound zone ACLs; native VLAN 999; DHCP relay; WAN OSPF; SSH |
| RZE-SW1 | [RZE-SW1.cfg](RZE-SW1.cfg) | Management 10.30.10.2/28; access VLANs 30/50; G0/1 trunk; SSH |
| WAN-SW | [WAN-SW.cfg](WAN-SW.cfg) | Fa0/1–3 in access VLAN 900; no management IP |
| ISP-R1 | [ISP-R1.cfg](ISP-R1.cfg) | G0/0 198.51.100.1/30 and G0/1 203.0.113.1/24; outside corporate OSPF |

All ten captures end with `end`. All eight corporate devices restrict VTY 0–15 to SSH with local login and IT-only ACL 10. The [ACL placement map](../docs/NETWORK.md#acl-placement) lists all twelve named filters, their interfaces and rule counts.

The Sep 20 [baseline export review](../docs/VALIDATION.md#baseline-and-incidents) found all ten non-credential command sets matched the preceding reviewed captures. The same section records six representative reopen checks and four incident recoveries. Historical checks do not establish exhaustive coverage or validate a subsequently modified `.pkt`; use the [recorded checkpoint identities](../docs/VALIDATION.md#checkpoints).

## Restore notes

Rebuild in a separate Packet Tracer file using the [device and cabling plan](../docs/NETWORK.md#devices-and-links) and [build order](../docs/NETWORK.md#build-order). Inspect each capture before applying it through the device console. A rebuild from these files has not been independently validated.

1. **Create VLANs on the switches.** HQ: 10 MGMT, 20 IT, 30 USERS, 40 SERVERS, 50 GUEST, 999 PARKING. Branches: 10 MGMT, 30 USERS, 50 GUEST, 999 PARKING. WAN-SW: 900 WAN_TRANSMIT. VLAN definitions are absent from these captures; normal-range VLAN data can reside separately in `vlan.dat`. Follow the [addressing and trunk plan](../docs/NETWORK.md#vlans-and-addressing). [Cisco VLAN storage guide](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-2940-series-switches/109304-manage-vlandat.html)
2. **Recreate credentials locally.** `! REDACTED` comments replace account and captured enable-secret lines. Recreate `admin` before enabling `login local`. The four Layer 3 devices use account privilege 15; access switches use the recorded login/enable workflow. Set the required enable secrets through the console and keep them out of public exports.
3. **Restore SSH prerequisites.** Apply the captured hostname and `ip domain-name lab.example`, then generate RSA host keys on a fresh corporate device with `crypto key generate rsa`; use CLI help for supported syntax and modulus sizes. The captures do not contain the host keys. Retain `ip ssh version 2`, local authentication and ACL 10 on both VTY groups (0–4 and 5–15). Check `show ip ssh` and a fresh login from IT-PC1 before relying on remote access. [Cisco SSH setup](https://www.cisco.com/c/en/us/support/docs/security-vpn/secure-shell-ssh/4145-ssh.html)
4. **Apply and inspect the device configuration.** Follow the build order and check command acceptance, intended active interfaces, native/allowed VLANs, port-channel members, addressing and routes. On fresh routers, enable the intended active interfaces with `no shutdown` where needed. Preserve the [ACL order and inbound attachments](../docs/NETWORK.md#acl-placement), six DHCP helpers and NAT interface roles.
5. **Configure endpoints and Server-PT services separately.** IOS exports do not include these settings. Use the [addressing table](../docs/NETWORK.md#vlans-and-addressing) for static hosts and DHCP start addresses/lease counts, and [routing and services](../docs/NETWORK.md#routing-and-services) for DNS and HTTP. HQ-SRV1 supplies six DHCP pools; Users use internal DNS and Guests use external DNS. Check the [corrected pool table](../docs/evidence/2026-09-17_dhcp_pools_corrected.png). EXT-SRV1 uses 203.0.113.10/24, gateway 203.0.113.1 and self DNS; its DNS service contains only `www.lab.example → 203.0.113.10`.
6. **Validate the rebuilt state.** Run relevant [baseline and policy checks](../docs/VALIDATION.md#test-checklist), including allowed services, a denied path and management access. Save device startup configurations and the `.pkt`, then run a representative reopen batch. Record new evidence against the rebuilt file's identity.

## Save and export

1. Run `copy running-config startup-config` on changed devices, then save the Packet Tracer working file separately.
2. Export **Running Config** through Config → GLOBAL → Settings → Export, or copy all of `show running-config` through the final `end`. Exclude prompts and pagination markers; record any redaction.
3. Preserve the original privately before replacing `<hostname>.cfg`, then redact credentials in the public copy. Record the checkpoint identity and relevant verification results in [Validation](../docs/VALIDATION.md#recording-a-new-result).
