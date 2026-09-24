"""Backup restoration service."""

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path

from backup_manager.config import HASH_CHUNK_SIZE, MANIFEST_NAME

logger = logging.getLogger(__name__)


def _safe_target(destination: Path, member_name: str) -> Path:
    """Return a safe extraction target and block path traversal."""
    target = (destination / member_name).resolve()

    try:
        target.relative_to(destination)
    except ValueError as exc:
        raise ValueError(
            f"Unsafe archive path detected: {member_name}"
        ) from exc

    return target


def restore_backup(archive: Path, destination: Path) -> int:
    """Restore files from a backup archive safely."""
    archive = archive.resolve()
    destination = destination.resolve()

    if not archive.exists():
        raise FileNotFoundError(
            f"Backup does not exist: {archive}"
        )

    if not archive.is_file():
        raise ValueError(
            f"Backup is not a file: {archive}"
        )

    destination.mkdir(parents=True, exist_ok=True)

    restored = 0

    try:
        with zipfile.ZipFile(archive, "r") as zip_file:
            # Validate the archive before extracting anything.
            bad_member = zip_file.testzip()

            if bad_member is not None:
                raise ValueError(
                    f"Backup is corrupted or invalid: {archive}"
                )

            members = zip_file.infolist()

            with tempfile.TemporaryDirectory(
                prefix="backup_restore_",
                dir=destination.parent,
            ) as temp_dir:
                staging = Path(temp_dir).resolve()

                for info in members:
                    if info.filename == MANIFEST_NAME:
                        continue

                    target = _safe_target(
                        staging,
                        info.filename,
                    )

                    if info.is_dir():
                        target.mkdir(
                            parents=True,
                            exist_ok=True,
                        )
                        continue

                    target.parent.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                    with zip_file.open(info, "r") as source:
                        with target.open("wb") as output:
                            while True:
                                chunk = source.read(
                                    HASH_CHUNK_SIZE
                                )

                                if not chunk:
                                    break

                                output.write(chunk)

                    restored += 1

                # Only copy files to the final destination after
                # the complete archive has been extracted successfully.
                for item in staging.rglob("*"):
                    relative = item.relative_to(staging)
                    final_target = destination / relative

                    if item.is_dir():
                        final_target.mkdir(
                            parents=True,
                            exist_ok=True,
                        )
                    else:
                        final_target.parent.mkdir(
                            parents=True,
                            exist_ok=True,
                        )
                        shutil.copy2(item, final_target)

    except zipfile.BadZipFile as exc:
        logger.error(
            "Invalid or corrupted backup: %s",
            archive,
        )

        raise ValueError(
            f"Backup is corrupted or invalid: {archive}"
        ) from exc

    logger.info(
        "Restored backup: %s | files=%d",
        archive,
        restored,
    )

    return restored