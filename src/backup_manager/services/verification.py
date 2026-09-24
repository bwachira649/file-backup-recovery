"""Backup integrity verification."""

import json
import zipfile
from pathlib import Path

from backup_manager.config import MANIFEST_NAME
from backup_manager.utils.hashing import sha256_bytes


def verify_backup(archive: Path) -> tuple[bool, str]:
    """Verify ZIP integrity and SHA-256 hashes."""
    archive = archive.resolve()

    if not archive.exists():
        return False, f"Backup does not exist: {archive}"

    if not archive.is_file():
        return False, f"Backup is not a file: {archive}"

    try:
        with zipfile.ZipFile(archive, "r") as zip_file:

            # First verify the ZIP archive's internal CRC values.
            bad_member = zip_file.testzip()

            if bad_member is not None:
                return False, (
                    f"ZIP CRC verification failed: {bad_member}"
                )

            # The manifest is required for SHA-256 verification.
            if MANIFEST_NAME not in zip_file.namelist():
                return False, "Backup manifest is missing."

            try:
                manifest = json.loads(
                    zip_file.read(MANIFEST_NAME).decode("utf-8")
                )
            except (
                UnicodeDecodeError,
                json.JSONDecodeError,
            ) as exc:
                return False, f"Invalid backup manifest: {exc}"

            members = set(zip_file.namelist())

            for entry in manifest.get("files", []):
                member_name = entry["path"]

                if member_name not in members:
                    return False, (
                        f"Missing file: {member_name}"
                    )

                data = zip_file.read(member_name)
                actual_hash = sha256_bytes(data)

                if actual_hash != entry["sha256"]:
                    return False, (
                        f"Hash mismatch: {member_name}"
                    )

                if len(data) != entry["size"]:
                    return False, (
                        f"Size mismatch: {member_name}"
                    )

            count = manifest.get("file_count", 0)

            return True, (
                "Backup verified successfully. "
                f"Files checked: {count}"
            )

    except zipfile.BadZipFile:
        return False, "Invalid or corrupted ZIP archive."

    except (
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        return False, (
            f"Invalid backup manifest structure: {exc}"
        )