#!/usr/bin/env python3
"""Check published IOS captures against selected documented lab invariants.

Python standard library only. This does not open Packet Tracer, evaluate every
ACL permit, or prove that a saved topology matches these captures.
"""

from pathlib import Path
import re
import sys


DEVICES = (
    "HQ-L3", "HQ-R1", "HQ-SW1", "HQ-SW2", "KAT-R1", "KAT-SW1",
    "RZE-R1", "RZE-SW1", "ISP-R1", "WAN-SW",
)
CORPORATE = DEVICES[:8]
ACL_MAP = {
    "HQ-L3": {
        "MGMT_HQ_IN": ("Vlan10", 4), "IT_HQ_IN": ("Vlan20", 17),
        "USERS_HQ_IN": ("Vlan30", 10), "SERVERS_HQ_IN": ("Vlan40", 27),
        "GUEST_HQ_IN": ("Vlan50", 8),
    },
    "HQ-R1": {"ISP_IN": ("GigabitEthernet0/2", 5)},
    "KAT-R1": {
        "MGMT_KAT_IN": ("GigabitEthernet0/0.10", 4),
        "USERS_KAT_IN": ("GigabitEthernet0/0.30", 10),
        "GUEST_KAT_IN": ("GigabitEthernet0/0.50", 8),
    },
    "RZE-R1": {
        "MGMT_RZE_IN": ("GigabitEthernet0/0.10", 4),
        "USERS_RZE_IN": ("GigabitEthernet0/0.30", 10),
        "GUEST_RZE_IN": ("GigabitEthernet0/0.50", 8),
    },
}
HELPERS = {
    ("HQ-L3", "Vlan30"), ("HQ-L3", "Vlan50"),
    ("KAT-R1", "GigabitEthernet0/0.30"), ("KAT-R1", "GigabitEthernet0/0.50"),
    ("RZE-R1", "GigabitEthernet0/0.30"), ("RZE-R1", "GigabitEthernet0/0.50"),
}
PAT_SOURCES = {
    "10.10.20.0 0.0.0.15", "10.10.30.0 0.0.0.63", "10.10.50.0 0.0.0.31",
    "10.20.30.0 0.0.0.31", "10.20.50.0 0.0.0.15",
    "10.30.30.0 0.0.0.31", "10.30.50.0 0.0.0.15",
}


def audit(root):
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    found = {p.stem for p in (root / "configs").glob("*.cfg")}
    check(found == set(DEVICES), "Expected exactly the ten documented device captures")
    for device in DEVICES:
        path = root / "configs" / f"{device}.cfg"
        if not path.is_file():
            errors.append(f"{device}: missing capture")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        commands = [s.strip() for s in lines if s.strip() and not s.startswith("!")]
        check(bool(commands) and commands[-1] == "end", f"{device}: missing final end")
        check([s for s in commands if s.startswith("hostname ")] == [f"hostname {device}"],
              f"{device}: hostname mismatch")
        check(not any(re.match(r"(?:username |enable (?:secret|password) |password |snmp-server community )", s)
                      for s in commands), f"{device}: unredacted credential command")

        # IOS captures group child commands by indentation, including adjacent ACLs.
        blocks = {}
        current = None
        for line in lines:
            if not line or line.startswith("!"):
                current = None
            elif not line[0].isspace():
                current = line
                check(current not in blocks, f"{device}: duplicate section {current}")
                blocks[current] = []
            elif current is not None:
                blocks[current].append(line.strip())

        interfaces = {k.removeprefix("interface "): v for k, v in blocks.items()
                      if k.startswith("interface ")}
        expected = ACL_MAP.get(device, {})
        acls = {k.removeprefix("ip access-list extended "): v for k, v in blocks.items()
                if k.startswith("ip access-list extended ")}
        check(acls.keys() == expected.keys(), f"{device}: named ACL inventory mismatch")
        bindings = [(iface, s) for iface, body in interfaces.items() for s in body
                    if s.startswith("ip access-group ")]
        wanted = [(iface, f"ip access-group {name} in") for name, (iface, _) in expected.items()]
        check(sorted(bindings) == sorted(wanted), f"{device}: ACL attachment mismatch")
        for name, (_, count) in expected.items():
            rules = acls.get(name, [])
            check(len(rules) == count, f"{device}/{name}: expected {count} rules, got {len(rules)}")
            check(bool(rules) and rules[-1] == "deny ip any any",
                  f"{device}/{name}: missing final explicit deny")

        actual_helpers = [(iface, s) for iface, body in interfaces.items() for s in body
                          if s.startswith("ip helper-address ")]
        wanted_helpers = [(iface, "ip helper-address 10.10.40.10") for dev, iface in HELPERS if dev == device]
        check(sorted(actual_helpers) == sorted(wanted_helpers), f"{device}: DHCP relay mismatch")

        if device in CORPORATE:
            for command in ("ip ssh version 2", "ip domain-name lab.example"):
                check(command in commands, f"{device}: missing {command}")
            check([s for s in commands if s.startswith("access-list 10 ")] ==
                  ["access-list 10 permit 10.10.20.0 0.0.0.15"], f"{device}: SSH source ACL mismatch")
            covered = []
            for header, body in blocks.items():
                if header.startswith("line vty "):
                    match = re.fullmatch(r"line vty (\d+) (\d+)", header)
                    check(match is not None, f"{device}: unexpected VTY header")
                    if match:
                        covered.extend(range(int(match[1]), int(match[2]) + 1))
                    for command in ("access-class 10 in", "login local", "transport input ssh"):
                        check(command in body, f"{device}/{header}: missing {command}")
            check(sorted(covered) == list(range(16)), f"{device}: VTY 0-15 coverage mismatch")

        if device == "HQ-R1":
            check(sorted(s for s in commands if s.startswith("access-list 20 ")) ==
                  sorted(f"access-list 20 permit {s}" for s in PAT_SOURCES), "HQ-R1: PAT sources mismatch")
            check("ip nat inside source list 20 interface GigabitEthernet0/2 overload" in commands,
                  "HQ-R1: missing PAT overload")
            roles = [(iface, s) for iface, body in interfaces.items() for s in body
                     if s in ("ip nat inside", "ip nat outside")]
            check(sorted(roles) == [("GigabitEthernet0/0", "ip nat inside"),
                                    ("GigabitEthernet0/1", "ip nat inside"),
                                    ("GigabitEthernet0/2", "ip nat outside")], "HQ-R1: NAT interface roles mismatch")
    return errors


if __name__ == "__main__":
    findings = audit(Path(__file__).resolve().parents[1])
    for finding in findings:
        print(f"FAIL: {finding}", file=sys.stderr)
    if findings:
        sys.exit(1)
    print("PASS: 10 captures, 12 ACL structures/bindings, 8 SSH/VTY policies, 6 helpers and 7 PAT sources.")
    print("Static checks only; ACL semantics, Packet Tracer runtime and saved-file correspondence are not validated.")
