#!/usr/bin/env python3
"""Ransomware Simulation - SAFE dry-run only"""
from ransomware.config import RansomConfig
from ransomware.core import RansomSim

config = RansomConfig()
sim = RansomSim(config)

# DRY RUN - just lists target files, encrypts nothing
result = sim.simulate_encrypt("/tmp/test_dir", dry_run=True)
print(f"Would affect {result['files_found']} files")
print(sim.generate_report())
