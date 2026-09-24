import json
import zipfile
from pathlib import Path

from backup_manager.config import MANIFEST_NAME
from backup_manager.services.backup import (
    create_backup,
    list_backups,
)


def test_create_backup(tmp_path: Path):
    source = tmp_path / "source"
    destination = tmp_path / "backups"

    (source / "documents").mkdir(parents=True)

    (source / "documents" / "readme.txt").write_text(
        "backup test",
        encoding="utf-8",
    )

    archive = create_backup(
        source,
        destination,
    )

    assert archive.exists()
    assert archive.suffix == ".zip"

    with zipfile.ZipFile(archive) as zip_file:
        assert "documents/readme.txt" in zip_file.namelist()
        assert MANIFEST_NAME in zip_file.namelist()

        manifest = json.loads(
            zip_file.read(MANIFEST_NAME).decode("utf-8")
        )

    assert manifest["file_count"] == 1
    assert manifest["files"][0]["path"] == (
        "documents/readme.txt"
    )


def test_list_backups(tmp_path: Path):
    source = tmp_path / "source"
    destination = tmp_path / "backups"

    source.mkdir()

    create_backup(
        source,
        destination,
    )

    backups = list_backups(destination)

    assert len(backups) == 1