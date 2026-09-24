from pathlib import Path

from backup_manager.utils.hashing import sha256_file


def test_sha256_file(tmp_path: Path):
    file = tmp_path / "hello.txt"

    file.write_text(
        "hello world",
        encoding="utf-8",
    )

    assert sha256_file(file) == (
        "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    )