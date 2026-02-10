"""Ransomware Simulation Config"""
import os

class RansomConfig:
    EXTENSIONS = [".doc", ".docx", ".xls", ".xlsx", ".pdf", ".jpg", ".png",
                  ".txt", ".csv", ".sql", ".db", ".bak", ".zip"]
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ENCRYPTED_EXT = ".locked"
    KEY_SIZE = 32  # AES-256
    NOTE_FILENAME = "RECOVERY_README.txt"
    SAFE_MODE = True  # Never encrypt without this flag
    LOG_FILE = "ransim.log"
