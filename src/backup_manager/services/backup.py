"""Backup creation and backup listing."""

import json
import logging
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from backup_manager.config import (
    APP_NAME,
    APP_VERSION,
    BACKUP_PREFIX,
    BACKUP_SUFFIX,
    HASH_ALGORITHM,
    MANIFEST_NAME,
)
from backup_manager.utils.hashing import sha256_file

logger = logging.getLogger(__name__)


def create_backup(source: Path, destination: Path) -> Path:
    """Create a timestamped ZIP backup containing a verification manifest."""
    source = source.resolve()
    destination = destination.resolve()

    if not source.exists():
        raise FileNotFoundError(
            f"Source directory does not exist: {source}"
        )

    if not source.is_dir():
        raise NotADirectoryError(
            f"Source is not a directory: {source}"
        )

    destination.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive = destination / (
        f"{BACKUP_PREFIX}{timestamp}{BACKUP_SUFFIX}"
    )

    files = sorted(
        path for path in source.rglob("*") if path.is_file()
    )

    manifest = {
        "application": APP_NAME,
        "version": APP_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "hash_algorithm": HASH_ALGORITHM,
        "source_name": source.name,
        "file_count": len(files),
        "files": [],
    }

    for path in files:
        relative = path.relative_to(source).as_posix()

        manifest["files"].append(
            {
                "path": relative,
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    with zipfile.ZipFile(
        archive,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zip_file:

        for path in files:
            relative = path.relative_to(source).as_posix()
            zip_file.write(path, relative)

        zip_file.writestr(
            MANIFEST_NAME,
            json.dumps(manifest, indent=2),
        )

    logger.info(
        "Created backup: %s | files=%d",
        archive,
        len(files),
    )

    return archive


def list_backups(directory: Path) -> list[Path]:
    """Return backup archives sorted newest first."""
    directory = directory.resolve()

    if not directory.exists():
        return []

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Not a directory: {directory}"
        )

    return sorted(
        directory.glob(
            f"{BACKUP_PREFIX}*{BACKUP_SUFFIX}"
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def delete_backup(archive: Path) -> None:
    """Delete one backup archive."""
    archive = archive.resolve()

    if not archive.exists():
        raise FileNotFoundError(
            f"Backup does not exist: {archive}"
        )

    if not archive.is_file():
        raise ValueError(
            f"Backup is not a file: {archive}"
        )

    archive.unlink()

    logger.info("Deleted backup: %s", archive)