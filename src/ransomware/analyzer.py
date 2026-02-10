"""Ransomware behavior analysis"""
import os, hashlib, json

class RansomAnalyzer:
    KNOWN_SIGNATURES = {
        "WannaCry": "ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa",
        "Petya": "027cc450ef5f8c5f653329641ec1fed91f694e0d229928963b30f6b0d7d3a745",
        "Ryuk": "8b0a5fb13309623c3518473551cb1f55d38d8450129571f9b5c2b169e2a0c5f9",
    }
    
    @staticmethod
    def analyze_file(filepath):
        with open(filepath, "rb") as f:
            data = f.read(1024)
        entropy = RansomAnalyzer._entropy(data)
        return {"path": filepath, "entropy": round(entropy, 2),
                "likely_encrypted": entropy > 7.5, "size": os.path.getsize(filepath)}
    
    @staticmethod
    def check_indicators(directory):
        indicators = {"ransom_notes": [], "encrypted_files": [], "suspicious_exts": []}
        note_patterns = ["readme", "recover", "decrypt", "ransom", "help_decrypt"]
        for root, dirs, files in os.walk(directory):
            for f in files:
                fl = f.lower()
                if any(p in fl for p in note_patterns):
                    indicators["ransom_notes"].append(os.path.join(root, f))
                if f.endswith((".locked", ".encrypted", ".crypto", ".crypt")):
                    indicators["encrypted_files"].append(os.path.join(root, f))
        return indicators
    
    @staticmethod
    def _entropy(data):
        if not data: return 0
        freq = [0] * 256
        for b in data: freq[b] += 1
        import math
        return -sum(p/len(data) * math.log2(p/len(data)) for p in freq if p > 0)
