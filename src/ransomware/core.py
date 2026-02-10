"""Ransomware Simulation Engine - RESEARCH ONLY"""
import os, hashlib, json, time
from datetime import datetime

class RansomSim:
    def __init__(self, config):
        self.config = config
        self.key = os.urandom(config.KEY_SIZE)
        self.encrypted_files = []
        self.log = []
    
    def simulate_encrypt(self, target_dir, dry_run=True):
        """Simulate encryption - dry_run=True only lists files"""
        if not self.config.SAFE_MODE:
            raise RuntimeError("SAFE_MODE must be enabled for simulation")
        
        targets = self._find_targets(target_dir)
        self._log(f"Found {len(targets)} target files in {target_dir}")
        
        for filepath in targets:
            if dry_run:
                self._log(f"[DRY-RUN] Would encrypt: {filepath}")
                self.encrypted_files.append(filepath)
            else:
                self._encrypt_file(filepath)
        
        return {"files_found": len(targets), "dry_run": dry_run}
    
    def _find_targets(self, directory):
        targets = []
        for root, dirs, files in os.walk(directory):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in self.config.EXTENSIONS:
                    path = os.path.join(root, f)
                    if os.path.getsize(path) <= self.config.MAX_FILE_SIZE:
                        targets.append(path)
        return targets
    
    def _encrypt_file(self, filepath):
        """XOR-based simulation encryption"""
        with open(filepath, "rb") as f:
            data = f.read()
        keystream = (self.key * (len(data) // len(self.key) + 1))[:len(data)]
        encrypted = bytes(a ^ b for a, b in zip(data, keystream))
        with open(filepath + self.config.ENCRYPTED_EXT, "wb") as f:
            f.write(encrypted)
        self.encrypted_files.append(filepath)
        self._log(f"Encrypted: {filepath}")
    
    def decrypt_file(self, filepath):
        if not filepath.endswith(self.config.ENCRYPTED_EXT):
            raise ValueError("Not an encrypted file")
        with open(filepath, "rb") as f:
            data = f.read()
        keystream = (self.key * (len(data) // len(self.key) + 1))[:len(data)]
        decrypted = bytes(a ^ b for a, b in zip(data, keystream))
        orig_path = filepath[:-len(self.config.ENCRYPTED_EXT)]
        with open(orig_path, "wb") as f:
            f.write(decrypted)
        self._log(f"Decrypted: {orig_path}")
    
    def generate_report(self):
        return {"timestamp": str(datetime.now()), "files_encrypted": len(self.encrypted_files),
                "key_hash": hashlib.sha256(self.key).hexdigest()[:16], "log": self.log[-20:]}
    
    def _log(self, msg):
        entry = f"[{datetime.now().isoformat()}] {msg}"
        self.log.append(entry)
        print(entry)
