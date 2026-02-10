import unittest, sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ransomware.config import RansomConfig
from ransomware.core import RansomSim
from ransomware.analyzer import RansomAnalyzer
from ransomware.defender import RansomDefender

class TestConfig(unittest.TestCase):
    def test_safe_mode(self):
        self.assertTrue(RansomConfig.SAFE_MODE)
    def test_extensions(self):
        self.assertIn(".pdf", RansomConfig.EXTENSIONS)

class TestRansomSim(unittest.TestCase):
    def test_dry_run(self):
        cfg = RansomConfig()
        sim = RansomSim(cfg)
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "test.txt"), "w").write("hello")
            result = sim.simulate_encrypt(d, dry_run=True)
            self.assertEqual(result["dry_run"], True)

class TestDefender(unittest.TestCase):
    def test_baseline(self):
        d = RansomDefender()
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "a.txt"), "w").write("test")
            count = d.create_baseline(tmp)
            self.assertGreater(count, 0)

if __name__ == "__main__":
    unittest.main()
