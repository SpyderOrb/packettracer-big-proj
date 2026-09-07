# Network build sheet

**State:** working design, not implemented or tested. This is the active source for topology, addressing, and traffic intent. Target device models and port labels require confirmation in Packet Tracer 9.0.1 before configuration.

## Design in brief

Kraków HQ supports 44 staff and hosts IT and shared services; Katowice supports 16 staff and Rzeszów 12. Use representative PCs instead of modelling every employee. Segment by trust and function: Management, IT, Users, Servers, and Guest at HQ; Management, Users, and Guest at each branch.

Each site router provides VLAN gateways through one 802.1Q trunk (router-on-a-stick). Three routers share an Ethernet transit subnet for OSPF area 0. `WAN-SW` represents the lab transit medium, not a managed corporate access switch or a real carrier/VPN. HQ provides the sole Internet exit. This avoids WAN modules and keeps the build uniform.

Two HQ switches use one two-member LACP EtherChannel. Make `HQ-SW1` the STP root and `HQ-SW2` secondary for HQ VLANs. Test loss of one member link; do not claim switch, router, or WAN failover. DHCP snooping, DAI, and further Layer 2 protections are optional follow-ups after the core baseline and simulator support checks.

![Planned topology, not validation evidence](topology.png)

## Devices and links

| Names | Target model | Role |
|---|---|---|
| `HQ-R1`, `KAT-R1`, `RZE-R1` | 2911 | Site gateways and OSPF; HQ also runs NAT/PAT |
| `ISP-R1` | 2911 | Simulated ISP, outside corporate OSPF |
| `HQ-SW1`, `HQ-SW2`, `KAT-SW1`, `RZE-SW1` | 2960-24TT | Corporate Layer 2 access switches |
| `WAN-SW` | 2960-24TT | Shared transit, access VLAN 900, no management IP |
| `HQ-SRV1`, `EXT-SRV1` | Server-PT | Internal DHCP/DNS/HTTP; external DNS/HTTP respectively |
| `HQ-PC1`, `HQ-PC2`, `IT-PC1`, `HQ-GUEST1`, `KAT-PC1`, `KAT-GUEST1`, `RZE-PC1`, `RZE-GUEST1` | PC-PT | Eight representative clients |

Total: **19 devices**. Cisco documents three onboard GE ports on the physical 2911; this supports the model choice but does not verify Packet Tracer behavior. [Cisco hardware guide](https://www.cisco.com/c/en/us/td/docs/routers/access/2900/hardware/installation/guide/Hardware_Installation_Guide/Overview.html)

| Device / port | Peer / port | Cable | Intended use |
|---|---|---|---|
| HQ-R1 G0/0 | HQ-SW1 G0/1 | Copper Straight-Through | HQ VLAN trunk |
| KAT-R1 G0/0 | KAT-SW1 G0/1 | Copper Straight-Through | Katowice VLAN trunk |
| RZE-R1 G0/0 | RZE-SW1 G0/1 | Copper Straight-Through | Rzeszów VLAN trunk |
| HQ-SW1 F0/23 | HQ-SW2 F0/23 | Copper Cross-Over | Port-channel 1 member |
| HQ-SW1 F0/24 | HQ-SW2 F0/24 | Copper Cross-Over | Port-channel 1 member |
| HQ-R1 G0/1 | WAN-SW F0/1 | Copper Straight-Through | OSPF transit, access VLAN 900 |
| KAT-R1 G0/1 | WAN-SW F0/2 | Copper Straight-Through | OSPF transit, access VLAN 900 |
| RZE-R1 G0/1 | WAN-SW F0/3 | Copper Straight-Through | OSPF transit, access VLAN 900 |
| HQ-R1 G0/2 | ISP-R1 G0/0 | Copper Cross-Over | Internet edge |
| ISP-R1 G0/1 | EXT-SRV1 FastEthernet0 | Copper Cross-Over | External services LAN |

Select the cable type manually under Connections, then choose the exact ports in the table. `G` means GigabitEthernet and `F` means FastEthernet. Use **Copper Straight-Through** for all nine access links below, with endpoint port `FastEthernet0`. Cable choices follow the [Packet Tracer connection guide](https://tutorials.ptnetacad.net/help/default/connectionsLinks.htm); actual link behavior still needs checking in the installed simulator.

| Switch / port | Endpoint | VLAN | Address |
|---|---|---:|---|
| HQ-SW1 F0/1 | HQ-PC1 | 30 | DHCP |
| HQ-SW1 F0/2 | IT-PC1 | 20 | 10.10.20.10/28, gateway 10.10.20.1 |
| HQ-SW1 F0/3 | HQ-SRV1 | 40 | 10.10.40.10/28, gateway 10.10.40.1 |
| HQ-SW2 F0/1 | HQ-GUEST1 | 50 | DHCP |
| HQ-SW2 F0/2 | HQ-PC2 | 30 | DHCP |
| KAT-SW1 F0/1 | KAT-PC1 | 30 | DHCP |
| KAT-SW1 F0/2 | KAT-GUEST1 | 50 | DHCP |
| RZE-SW1 F0/1 | RZE-PC1 | 30 | DHCP |
| RZE-SW1 F0/2 | RZE-GUEST1 | 50 | DHCP |

## VLANs and addressing

VLAN IDs repeat across sites; their IP subnets do not. Corporate site prefixes are `10.10.0.0/16` (HQ), `10.20.0.0/16` (KAT), and `10.30.0.0/16` (RZE). These are allocation containers, not interface masks or required OSPF summaries. VLAN gateway `.1` resides on router subinterface `G0/0.<VLAN>`.

| Site | VLAN / name | Subnet | Gateway | Assignment |
|---|---|---|---|---|
| HQ | 10 MGMT | 10.10.10.0/28 | 10.10.10.1 | SW1 .2; SW2 .3, static management SVIs |
| HQ | 20 IT | 10.10.20.0/28 | 10.10.20.1 | IT-PC1 .10, static |
| HQ | 30 USERS | 10.10.30.0/26 | 10.10.30.1 | DHCP .10–.62: 53 leases |
| HQ | 40 SERVERS | 10.10.40.0/28 | 10.10.40.1 | HQ-SRV1 .10, static |
| HQ | 50 GUEST | 10.10.50.0/27 | 10.10.50.1 | DHCP .10–.30: 21 leases |
| KAT | 10 MGMT | 10.20.10.0/28 | 10.20.10.1 | SW1 .2, static management SVI |
| KAT | 30 USERS | 10.20.30.0/27 | 10.20.30.1 | DHCP .10–.30: 21 leases |
| KAT | 50 GUEST | 10.20.50.0/28 | 10.20.50.1 | DHCP .2–.14: 13 leases |
| RZE | 10 MGMT | 10.30.10.0/28 | 10.30.10.1 | SW1 .2, static management SVI |
| RZE | 30 USERS | 10.30.30.0/27 | 10.30.30.1 | DHCP .10–.30: 21 leases |
| RZE | 50 GUEST | 10.30.50.0/28 | 10.30.50.1 | DHCP .2–.14: 13 leases |

Use VLAN 999 as an unused native/parking VLAN with no IP interface or clients. HQ trunks allow 10,20,30,40,50,999; branch trunks allow 10,30,50,999. Match native VLAN 999 at both ends, including router trunks. Shut unused access ports. Management means device administration, not company leadership.

| Network | Subnet | Addresses |
|---|---|---|
| Shared OSPF transit | 10.255.0.0/29 | HQ G0/1 .1; KAT G0/1 .2; RZE G0/1 .3 |
| HQ–ISP | 198.51.100.0/30 | ISP G0/0 .1; HQ G0/2 .2 |
| External services | 203.0.113.0/24 | ISP G0/1 .1; EXT-SRV1 .10, gateway .1 |

The two external ranges are documentation addresses used only inside the simulation. [IETF RFC 5737](https://www.rfc-editor.org/rfc/rfc5737)

## Routing and services

- OSPF process 1, area 0; explicit router IDs `10.255.255.1` (HQ), `.2` (KAT), `.3` (RZE). These are identifiers, not assigned interface addresses. Advertise the listed corporate VLAN networks and transit subnet. Make all interfaces passive except G0/1. Keep ISP and external networks outside corporate OSPF.
- HQ has a default route via `198.51.100.1` and originates that default into OSPF while it exists. Branch Internet traffic then exits HQ. The shared transit permits direct branch-to-branch routing; access policy still applies at each site.
- HQ PAT overloads G0/2. G0/1 and the routed HQ client VLAN interfaces are inside-facing. A NAT source list selects addresses for translation; it does not replace traffic-filtering ACLs. Do not publish internal services with static translations.
- HQ-SRV1 supplies six DHCP pools from the table: three Users and three Guest pools. Configure pool start, mask, gateway, DNS, and lease count. Relay those six VLANs to `10.10.40.10`; Management, IT, and Servers use static addresses.
- Corporate clients use DNS `10.10.40.10`. Guests use external DNS `203.0.113.10`. Internal DNS has `intranet.lab.example → 10.10.40.10` and `www.lab.example → 203.0.113.10`; external DNS has only the latter. Serve HTTP on both servers. Use the same corporate DNS for IT-PC1.
- Manage corporate routers through their VLAN 10 address and corporate switches through their management SVI; allow SSH from HQ IT only. ISP-R1 and WAN-SW are simulation infrastructure with no corporate remote-management requirement.

## Traffic policy

The existing TP identifiers are retained. Entries are requirements, not successful tests. Use DNS (UDP/TCP 53), HTTP (TCP 80), SSH (TCP 22), and ICMP as specified; confirm simulator behavior before writing final ACLs.

| Rule | Source → destination | Required behavior |
|---|---|---|
| TP-01 | HQ Users → HQ-SRV1 | Permit DNS and HTTP only |
| TP-02 | Branch Users → HQ-SRV1 | Permit DNS and HTTP only |
| TP-03 | HQ IT → HQ-SRV1 | Permit DNS, HTTP, and diagnostic ICMP |
| TP-04 | HQ IT → corporate Management | Permit SSH and diagnostic ICMP |
| TP-05 | HQ IT → corporate Users | Permit diagnostic ICMP |
| TP-06 | Corporate Users → simulated Internet | Permit HTTP and diagnostic ICMP through HQ PAT |
| TP-07 | Guests → simulated Internet | Permit external DNS, HTTP, and diagnostic ICMP through HQ PAT |
| TP-08 | Guests → internal zones | Deny, except required DHCP infrastructure traffic |
| TP-09 | Corporate Users → Management | Deny |
| TP-10 | Corporate Users → HQ IT | Deny new access; retain replies to permitted IT diagnostics |
| TP-11 | One corporate Users zone → another | Deny new routed access |
| TP-12 | Simulated Internet → internal zones | No unsolicited inbound access or published internal services |
| TP-13 | Other unlisted routed zone pairs | Deny |

Permit the specific DHCP relay exchanges, OSPF control traffic, and replies needed by allowed flows. ARP and local gateway operation must still work. Same-VLAN traffic bypasses routed ACLs: use different routed zones for isolation tests. Ordinary static ACLs do not provide full session tracking; TCP `established` checks flags and does not handle UDP or ICMP replies. Plan those reply rules explicitly. [Cisco ACL behavior](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_data_acl/configuration/15-sy/sec-data-acl-15-sy-book/sec-cfg-ip-filter.html)

## First Packet Tracer checkpoint

1. Open Cisco Packet Tracer 9.0.1. Confirm 2911 and 2960-24TT availability and the port labels above; record differences here before using a substitute.
2. Start with **HQ only: eight devices** — HQ-R1, HQ-SW1, HQ-SW2, HQ-SRV1, HQ-PC1, HQ-PC2, IT-PC1, and HQ-GUEST1. Set these display names and cable the eight HQ-only links from the tables. Display names identify devices on the canvas; IOS hostnames will be configured in Block 2.
3. Save this partial build as `packet-tracer/HQ-Branches-NOC-Lab_working.pkt`, reopen it, and capture `docs/evidence/working_hq_topology.png` with readable names and ports. This is an interim layout review, not a completed B1 test. Use a new working filename if a previous working copy needs preserving.
4. Add the two branches, WAN-SW, ISP-R1, and EXT-SRV1 using the same tables. The complete layout must have **19 devices and 19 links**, grouped as HQ, Katowice, Rzeszów, Transit, and Simulated Internet. Use English labels.
5. In a fresh unconfigured topology, router ports may be administratively down and one parallel switch link may be STP-blocked; this is not yet a connectivity test. Record unexpected observations instead of changing the planned ports to make the indicators green.
6. Save the complete layout as `packet-tracer/checkpoints/HQ-Branches-NOC-Lab_v01_physical-topology.pkt`. Close and reopen that exact file; check device names, ports, and both EtherChannel candidate links.
7. Record **B1** in [Validation](VALIDATION.md) with the checkpoint name and an actual Packet Tracer screenshot. Then begin VLAN/trunk configuration. Later checks follow configure → test → save → export; no separate planning approval round is required for routine configuration.
