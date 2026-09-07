# HQ + Branches NOC Lab

Cisco Packet Tracer lab connecting a headquarters in Kraków with branches in Katowice and Rzeszów. Built around network configuration, verification, and incident troubleshooting.

**Status:** site layouts captured; HQ-L3 model and interface checks recorded. Full-network validation and configuration exports pending.

<table>
  <tr>
    <td width="40%"><a href="docs/evidence/2026-09-07_hq_topology.png"><img src="docs/evidence/2026-09-07_hq_topology.png" alt="HQ layout with a 3560-24PS and two access switches" width="100%"></a></td>
    <td width="30%"><a href="docs/evidence/2026-09-07_kat_topology.png"><img src="docs/evidence/2026-09-07_kat_topology.png" alt="Katowice router, access switch and two clients" width="100%"></a></td>
    <td width="30%"><a href="docs/evidence/2026-09-07_rze_topology.png"><img src="docs/evidence/2026-09-07_rze_topology.png" alt="Rzeszow router, access switch and two clients" width="100%"></a></td>
  </tr>
</table>

Separate Packet Tracer site views; open each image for detail. [Full target design](docs/NETWORK.md).

**Planned scope:** HQ collapsed core with SVI gateways, branch router-on-a-stick, VLANs, STP, LACP, OSPF, DHCP/DNS, NAT/PAT, SSH, and ACLs. Internet access is simulated inside the lab.

## Project files

- [Network design and build steps](docs/NETWORK.md)
- [Validation checklist and results](docs/VALIDATION.md)
- [Device configuration exports](configs/README.md)
- [Incident report template](incidents/TEMPLATE.md)

## Reproduce

Use **Cisco Packet Tracer 9.0.1** and follow the build steps. Save numbered milestones in `packet-tracer/checkpoints/`, export their device configurations, and record test evidence in `docs/evidence/`.
