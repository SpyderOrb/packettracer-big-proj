"""Exercise the static audit with isolated copies of the published captures."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_configs", ROOT / "scripts/check-configs.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ConfigurationAuditTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="noc-config-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copytree(ROOT / "configs", self.root / "configs")

    def replace(self, device, old, new):
        path = self.root / "configs" / f"{device}.cfg"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count(old), 1, "Mutation must target exactly one command")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def assert_rejected(self, expected):
        self.assertIn(expected, CHECKER.audit(self.root))

    def test_published_captures_pass(self):
        self.assertEqual(CHECKER.audit(self.root), [])

    def test_ir001_wrong_client_vlan_is_rejected(self):
        self.replace("HQ-SW1", " switchport access vlan 30", " switchport access vlan 50")
        self.assert_rejected("HQ-SW1/FastEthernet0/1: expected access VLAN 30")

    def test_endpoint_trunk_mode_is_rejected(self):
        self.replace("HQ-SW2", " switchport access vlan 50\n switchport mode access\n",
                     " switchport access vlan 50\n switchport mode trunk\n")
        self.assert_rejected("HQ-SW2/FastEthernet0/1: expected static access mode")

    def test_endpoint_shutdown_is_rejected(self):
        self.replace("RZE-SW1", "\ninterface FastEthernet0/1\n",
                     "\ninterface FastEthernet0/1\n shutdown\n")
        self.assert_rejected("RZE-SW1/FastEthernet0/1: endpoint port is shut down")

    def test_ir002_passive_wan_is_rejected(self):
        self.replace("KAT-R1", " no passive-interface GigabitEthernet0/1\n", "")
        self.assert_rejected("KAT-R1: OSPF passive-interface policy mismatch")

    def test_ospf_enabled_on_client_vlan_is_rejected(self):
        self.replace("HQ-L3", " passive-interface default\n",
                     " passive-interface default\n no passive-interface Vlan30\n")
        self.assert_rejected("HQ-L3: OSPF passive-interface policy mismatch")

    def test_missing_ospf_passive_default_is_rejected(self):
        self.replace("HQ-R1", " passive-interface default\n", "")
        self.assert_rejected("HQ-R1: OSPF passive-interface policy mismatch")

    def test_unplanned_ospf_process_is_rejected(self):
        self.replace("ISP-R1", "\nend", "\nrouter ospf 1\n passive-interface default\nend")
        self.assert_rejected("ISP-R1: OSPF process inventory mismatch")

    def test_allow_all_replacing_service_permit_is_rejected(self):
        self.replace("KAT-R1",
                     " permit tcp 10.20.30.0 0.0.0.31 host 10.10.40.10 eq www",
                     " permit ip any any")
        self.assert_rejected("KAT-R1/USERS_KAT_IN: unrestricted IP permit")

    def test_allow_all_with_logging_is_rejected(self):
        self.replace("KAT-R1",
                     " permit tcp 10.20.30.0 0.0.0.31 host 10.10.40.10 eq www",
                     " permit ip any any log")
        self.assert_rejected("KAT-R1/USERS_KAT_IN: unrestricted IP permit")

    def test_early_deny_with_unchanged_rule_count_is_rejected(self):
        self.replace("KAT-R1",
                     " permit tcp 10.20.30.0 0.0.0.31 host 10.10.40.10 eq www",
                     " deny ip any any")
        self.assert_rejected("KAT-R1/USERS_KAT_IN: catch-all deny before the final rule")

    def test_extra_static_nat_mapping_is_rejected(self):
        self.replace("HQ-R1", "\nend",
                     "\nip nat inside source static tcp 10.10.40.10 80 198.51.100.2 80\nend")
        self.assert_rejected("HQ-R1: NAT translation rules mismatch")

    def test_nat_on_branch_router_is_rejected(self):
        self.replace("KAT-R1", "\nend",
                     "\nip nat inside source list 20 interface GigabitEthernet0/1 overload\nend")
        self.assert_rejected("KAT-R1: NAT translation rules mismatch")

    def test_nat_role_on_core_switch_is_rejected(self):
        self.replace("HQ-L3", "\ninterface GigabitEthernet0/1\n",
                     "\ninterface GigabitEthernet0/1\n ip nat inside\n")
        self.assert_rejected("HQ-L3: NAT interface roles mismatch")

    def test_cli_reports_failure_without_success_output(self):
        (self.root / "scripts").mkdir()
        script = self.root / "scripts/check-configs.py"
        shutil.copyfile(ROOT / "scripts/check-configs.py", script)
        self.replace("HQ-R1", "\nend",
                     "\nip nat inside source static tcp 10.10.40.10 80 198.51.100.2 80\nend")
        result = subprocess.run([sys.executable, str(script)], cwd=self.root,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: HQ-R1: NAT translation rules mismatch", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
