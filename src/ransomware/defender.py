"""Ransomware defense and detection"""
import os, time, hashlib, json
from datetime import datetime

class RansomDefender:
    def __init__(self, watch_dirs=None):
        self.watch_dirs = watch_dirs or []
        self.baseline = {}
        self.alerts = []
    
    def create_baseline(self, directory):
        baseline = {}
        for root, dirs, files in os.walk(directory):
            for f in files:
                path = os.path.join(root, f)
                try:
                    stat = os.stat(path)
                    baseline[path] = {"size": stat.st_size, "mtime": stat.st_mtime,
                                      "hash": hashlib.md5(open(path,"rb").read(4096)).hexdigest()}
                except: pass
        self.baseline[directory] = baseline
        return len(baseline)
    
    def check_changes(self, directory):
        if directory not in self.baseline:
            return {"error": "no baseline"}
        changes = {"modified": [], "deleted": [], "new": [], "suspicious": []}
        current = set()
        for root, dirs, files in os.walk(directory):
            for f in files:
                path = os.path.join(root, f)
                current.add(path)
                if path in self.baseline[directory]:
                    old = self.baseline[directory][path]
                    stat = os.stat(path)
                    if stat.st_mtime != old["mtime"]:
                        changes["modified"].append(path)
                else:
                    changes["new"].append(path)
        for path in self.baseline[directory]:
            if path not in current:
                changes["deleted"].append(path)
        mass = len(changes["modified"]) + len(changes["deleted"])
        if mass > 10:
            changes["suspicious"].append(f"Mass file changes detected: {mass} files")
        return changes
