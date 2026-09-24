from pathlib import Path

import pytest

from backup_manager.services.backup import create_backup
from backup_manager.services.restore import (
    _safe_target,
    restore_backup,
)


def test_restore_backup(tmp_path: Path):
    source = tmp_path / "source"
    backups = tmp_path / "backups"
    restored = tmp_path / "restored"

    (source / "documents").mkdir(parents=True)

    original = source / "documents" / "file.txt"

    original.write_text(
        "important test data",
        encoding="utf-8",
    )

    archive = create_backup(
        source,
        backups,
    )

    count = restore_backup(
        archive,
        restored,
    )

    assert count == 1

    restored_file = (
        restored / "documents" / "file.txt"
    )

    assert restored_file.read_text(
        encoding="utf-8"
    ) == "important test data"


def test_restore_blocks_path_traversal(
    tmp_path: Path,
):
    destination = tmp_path / "restored"

    destination.mkdir()

    with pytest.raises(ValueError):
        _safe_target(
            destination,
            "../../outside.txt",
        )