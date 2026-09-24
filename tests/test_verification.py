import json
import zipfile
from pathlib import Path

from backup_manager.services.backup import create_backup
from backup_manager.services.verification import verify_backup


def test_verify_valid_backup(tmp_path: Path):
    source = tmp_path / "source"
    backups = tmp_path / "backups"

    source.mkdir()

    (source / "file.txt").write_text(
        "integrity test",
        encoding="utf-8",
    )

    archive = create_backup(
        source,
        backups,
    )

    valid, message = verify_backup(archive)

    assert valid is True
    assert "verified successfully" in message


def test_verify_detects_modified_content(
    tmp_path: Path,
):
    source = tmp_path / "source"
    backups = tmp_path / "backups"

    source.mkdir()

    (source / "file.txt").write_text(
        "original",
        encoding="utf-8",
    )

    archive = create_backup(
        source,
        backups,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as original_zip:

        manifest = json.loads(
            original_zip.read(
                "backup_manifest.json"
            ).decode("utf-8")
        )

        files = {
            name: original_zip.read(name)
            for name in original_zip.namelist()
            if name != "backup_manifest.json"
        }

    # Intentionally corrupt the stored hash.
    manifest["files"][0]["sha256"] = "0" * 64

    with zipfile.ZipFile(
        archive,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as modified_zip:

        for name, data in files.items():
            modified_zip.writestr(name, data)

        modified_zip.writestr(
            "backup_manifest.json",
            json.dumps(
                manifest,
                indent=2,
            ),
        )

    valid, message = verify_backup(archive)

    assert valid is False
    assert "Hash mismatch" in message