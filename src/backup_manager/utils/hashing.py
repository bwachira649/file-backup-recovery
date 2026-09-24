"""File hashing utilities."""

import hashlib
from pathlib import Path

from backup_manager.config import HASH_CHUNK_SIZE


def sha256_file(path: Path) -> str:
    """Return the SHA-256 hash of a file."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        while True:
            chunk = file.read(HASH_CHUNK_SIZE)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    """Return the SHA-256 hash of bytes."""
    return hashlib.sha256(data).hexdigest()