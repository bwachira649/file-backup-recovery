"""Application configuration."""

from pathlib import Path

APP_NAME = "File Backup & Recovery System"
APP_VERSION = "1.0.0"

MANIFEST_NAME = "backup_manifest.json"
HASH_ALGORITHM = "sha256"
HASH_CHUNK_SIZE = 1024 * 1024

BACKUP_PREFIX = "backup_"
BACKUP_SUFFIX = ".zip"

LOG_DIRECTORY = Path("logs")
LOG_FILE = LOG_DIRECTORY / "backup_manager.log"