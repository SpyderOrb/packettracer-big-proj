# Network build sheet

This document specifies the target design. See [Validation](VALIDATION.md) for implemented and tested behavior.

## Design in brief

Kraków HQ supports 44 staff and hosts IT and shared services; Katowice supports 16 staff and Rzeszów 12. Use representative PCs instead of modelling every employee. Segment by trust and function: Management, IT, Users, Servers, and Guest at HQ; Management, Users, and Guest at each branch.

HQ uses a two-tier collapsed core: `HQ-L3` combines distribution/core functions and supplies VLAN gateways through switch virtual interfaces (SVIs). `HQ-SW1` and `HQ-SW2` provide Layer 2 access. `HQ-R1` connects to HQ-L3 over a routed Ethernet link and handles WAN routing and NAT/PAT. At each branch, the router still provides VLAN gateways through one 802.1Q trunk (router-on-a-stick). [Cisco campus design guide](https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html)

The three site routers retain their shared Ethernet transit for OSPF area 0. `WAN-SW` is an abstraction of Layer 2 transport between sites; only router transit ports share VLAN 900. Corporate client VLANs remain local to each site. No provider core, MPLS, VPN, or WAN redundancy is implemented. HQ-R1 remains the sole simulated Internet exit.

Each HQ access switch has its own two-member LACP trunk to HQ-L3: Po1 serves HQ-SW1 and Po2 serves HQ-SW2. There is no direct HQ-SW1–HQ-SW2 cable. Make HQ-L3 the STP root and HQ-SW1 secondary for HQ VLANs. Test loss of one member in each bundle. One HQ-L3 is a single point of failure; a secondary STP root does not provide a backup VLAN gateway. The FastEthernet bundles are chosen for simulator practice, with no throughput claim. Additional Layer 2 protections remain optional after the core baseline.

## Devices and links

| Names | Target model | Role |
|---|---|---|
| `HQ-L3` | 3560-24PS | HQ collapsed core, SVI gateways, DHCP relay, inter-VLAN ACLs and OSPF |
| `HQ-R1` | 2911 | HQ WAN/Internet edge, OSPF and NAT/PAT |
| `KAT-R1`, `RZE-R1` | 2911 | Branch VLAN gateways, DHCP relay, ACLs and OSPF |
| `ISP-R1` | 2911 | Simulated ISP, outside corporate OSPF |
| `HQ-SW1`, `HQ-SW2`, `KAT-SW1`, `RZE-SW1` | 2960-24TT | Corporate Layer 2 access switches |
| `WAN-SW` | 2960-24TT | Shared transit, access VLAN 900, no management IP |
| `HQ-SRV1`, `EXT-SRV1` | Server-PT | Internal DHCP/DNS/HTTP; external DNS/HTTP respectively |
| `HQ-PC1`, `HQ-PC2`, `IT-PC1`, `HQ-GUEST1`, `KAT-PC1`, `KAT-GUEST1`, `RZE-PC1`, `RZE-GUEST1` | PC-PT | Eight representative clients |

**20 devices, 21 physical links.** Port-channels are logical interfaces and do not add cables. `G` means GigabitEthernet; `F` means FastEthernet.

| Device / port | Peer / port | Cable | Intended use |
|---|---|---|---|
| HQ-R1 G0/0 | HQ-L3 G0/1 | Copper Straight-Through | Routed /30 link; no VLAN trunk |
| KAT-R1 G0/0 | KAT-SW1 G0/1 | Copper Straight-Through | Katowice VLAN trunk |
| RZE-R1 G0/0 | RZE-SW1 G0/1 | Copper Straight-Through | Rzeszów VLAN trunk |
| HQ-L3 F0/1 | HQ-SW1 F0/23 | Copper Cross-Over | Po1 member 1 |
| HQ-L3 F0/2 | HQ-SW1 F0/24 | Copper Cross-Over | Po1 member 2 |
| HQ-L3 F0/3 | HQ-SW2 F0/23 | Copper Cross-Over | Po2 member 1 |
| HQ-L3 F0/4 | HQ-SW2 F0/24 | Copper Cross-Over | Po2 member 2 |
| HQ-R1 G0/1 | WAN-SW F0/1 | Copper Straight-Through | OSPF transit, access VLAN 900 |
| KAT-R1 G0/1 | WAN-SW F0/2 | Copper Straight-Through | OSPF transit, access VLAN 900 |
| RZE-R1 G0/1 | WAN-SW F0/3 | Copper Straight-Through | OSPF transit, access VLAN 900 |
| HQ-R1 G0/2 | ISP-R1 G0/0 | Copper Cross-Over | Internet edge |
| ISP-R1 G0/1 | EXT-SRV1 FastEthernet0 | Copper Cross-Over | External services LAN |

Use Copper Straight-Through for the nine endpoint links below, with endpoint port `FastEthernet0`.

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

VLAN IDs repeat across sites; their IP subnets do not. Corporate site prefixes are `10.10.0.0/16` (HQ), `10.20.0.0/16` (KAT), and `10.30.0.0/16` (RZE). These are allocation containers, not interface masks or required OSPF summaries. HQ gateway `.1` resides on `HQ-L3 interface Vlan<VLAN>`; branch gateway `.1` resides on router subinterface `G0/0.<VLAN>`.

| Site | VLAN / name | Subnet | Gateway | Assignment |
|---|---|---|---|---|
| HQ | 10 MGMT | 10.10.10.0/28 | 10.10.10.1 | HQ-L3 .1; SW1 .2; SW2 .3, static SVIs |
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

Use VLAN 999 as an unused native/parking VLAN with no IP interface or clients. HQ Po1 and Po2 allow 10,20,30,40,50,999; branch trunks allow 10,30,50,999. Match native VLAN 999 at both ends, including branch router trunks. Configure LACP `mode active` and consistent trunk settings on each bundle and its members; use group 1 at both Po1 ends and group 2 at both Po2 ends. Check the 3560 trunk-encapsulation syntax with CLI help before forcing trunk mode. Shut unused access ports, including HQ-SW1 G0/1. Management is reserved for device administration.

| Network | Subnet | Addresses |
|---|---|---|
| Shared OSPF transit | 10.255.0.0/29 | HQ G0/1 .1; KAT G0/1 .2; RZE G0/1 .3 |
| HQ core–edge | 10.255.1.0/30 | HQ-R1 G0/0 .1; HQ-L3 G0/1 .2 |
| HQ–ISP | 198.51.100.0/30 | ISP G0/0 .1; HQ G0/2 .2 |
| External services | 203.0.113.0/24 | ISP G0/1 .1; EXT-SRV1 .10, gateway .1 |

The two external ranges are documentation addresses used only inside the simulation. [IETF RFC 5737](https://www.rfc-editor.org/rfc/rfc5737)

## Routing and services

- Enable `ip routing` on HQ-L3. Its G0/1 is a routed port (`no switchport`), addressed `10.255.1.2/30`; HQ-R1 G0/0 is `10.255.1.1/30`, with no VLAN subinterfaces. HQ-L3 supplies SVIs 10,20,30,40,50. An SVI needs its VLAN and an active forwarding member/trunk to become operational. [Cisco 3560 routing guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst3560/software/release/15-0_1_se/configuration/guide/scg3560/swiprout.html)
- OSPF process 1, area 0 runs on four devices. Router IDs are `10.255.255.1` (HQ-R1), `.2` (KAT-R1), `.3` (RZE-R1), and `.4` (HQ-L3); these are identifiers, not assigned interface addresses. HQ-L3 advertises HQ VLAN networks and the core–edge /30; HQ-R1 advertises the /30 and shared /29; each branch advertises its local VLANs and the /29. Use passive interfaces by default, with only the adjacencies listed below enabled. Keep ISP-R1 and the external networks outside corporate OSPF.
- Use OSPF point-to-point network type on both ends of the HQ core–edge /30 after confirming command support. The shared /29 retains broadcast network type and DR/BDR election.
- HQ-R1 has a default route via `198.51.100.1` and originates that default into OSPF while it exists. HQ-L3 and both branches learn it. HQ-R1 must learn all HQ VLAN routes back through HQ-L3. The shared transit still permits direct branch-to-branch routing; access policy applies at each site's routing boundary.
- HQ-R1 PAT overloads G0/2 (outside); G0/0 toward HQ-L3 and G0/1 toward WAN-SW are inside. HQ-L3 performs no NAT. A NAT source list selects corporate client source prefixes for translation; it does not replace traffic-filtering ACLs. Do not publish internal services with static translations.
- HQ-SRV1 supplies the same six DHCP pools: three Users and three Guest pools. Relay to `10.10.40.10` from HQ-L3 SVIs 30/50 and from branch router subinterfaces G0/0.30/G0/0.50. HQ-R1 has no client DHCP relay role. Management, IT, and Servers remain static.
- Corporate clients use DNS `10.10.40.10`. Guests use external DNS `203.0.113.10`. Internal DNS has `intranet.lab.example → 10.10.40.10` and `www.lab.example → 203.0.113.10`; external DNS has only the latter. Serve HTTP on both servers. Use the same corporate DNS for IT-PC1.
- Manage HQ-L3 at `10.10.10.1`, HQ-SW1/SW2 at `.2`/`.3`, and HQ-R1 at `10.255.1.1`. Branch router/switch management stays at `10.20.10.1/.2` and `10.30.10.1/.2`. Apply TP-04 and TP-09 to all eight management targets, explicitly including HQ-R1's transit address. Restrict corporate device SSH to HQ IT. ISP-R1 and WAN-SW remain simulation infrastructure without corporate remote-management requirements.

| OSPF device | Non-passive interfaces | Expected FULL neighbors |
|---|---|---|
| HQ-L3 | G0/1 | HQ-R1 (1) |
| HQ-R1 | G0/0, G0/1 | HQ-L3, KAT-R1, RZE-R1 (3) |
| KAT-R1 | G0/1 | HQ-R1, RZE-R1 (2) |
| RZE-R1 | G0/1 | HQ-R1, KAT-R1 (2) |

## Traffic policy

TP-01–TP-13 define the required policy; verification is tracked separately. Use DNS (UDP/TCP 53), HTTP (TCP 80), SSH (TCP 22), and ICMP as specified; confirm simulator behavior before writing final ACLs. Enforce HQ inter-VLAN policy on HQ-L3 SVIs and branch policy on branch router subinterfaces; apply Internet-edge filtering on HQ-R1. In particular, HQ Users-to-Servers traffic is routed entirely on HQ-L3, so an ACL on HQ-R1 cannot enforce TP-01.

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

## Build order

1. Assemble and name the devices using the tables above. Confirm model, interface and feature support in the installed simulator; save and reopen the topology.
2. Build local networks: HQ VLANs, access ports, LACP/STP, SVIs and the routed HQ link; branch VLANs and router subinterfaces. Add management addressing and SSH.
3. Connect the sites with OSPF, then configure DHCP relay, DNS/HTTP and HQ PAT.
4. Apply TP-01–TP-13 and verify permitted traffic, denied traffic and service regressions.
5. Save a clean baseline, export matching configurations, and reproduce four incidents in separate copies: wrong access VLAN, OSPF adjacency failure, missing DHCP relay and an ACL blocking a required service.

After each working slice, run the relevant [tests](VALIDATION.md#test-checklist), save device startup configurations and a numbered `.pkt`, export configurations, and record the result. Preserve earlier checkpoints. Reserve `packet-tracer/HQ-Branches-NOC-Lab.pkt` for the fully validated baseline.
