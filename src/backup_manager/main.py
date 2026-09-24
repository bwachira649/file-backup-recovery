"""Command-line interface for the File Backup & Recovery System."""

import argparse
import logging
import sys
from pathlib import Path

from backup_manager.services.backup import (
    create_backup,
    delete_backup,
    list_backups,
)
from backup_manager.services.restore import restore_backup
from backup_manager.services.verification import verify_backup
from backup_manager.utils.logging_config import configure_logging


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="backup-manager",
        description="File Backup & Recovery System",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    backup_parser = subparsers.add_parser(
        "backup",
        help="Create a new backup",
    )
    backup_parser.add_argument(
        "source",
        help="Directory to back up",
    )
    backup_parser.add_argument(
        "destination",
        help="Directory where the backup will be stored",
    )

    restore_parser = subparsers.add_parser(
        "restore",
        help="Restore files from a backup",
    )
    restore_parser.add_argument(
        "archive",
        help="Path to the backup ZIP file",
    )
    restore_parser.add_argument(
        "destination",
        help="Directory where files will be restored",
    )

    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify backup integrity",
    )
    verify_parser.add_argument(
        "archive",
        help="Path to the backup ZIP file",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List available backups",
    )
    list_parser.add_argument(
        "directory",
        help="Directory containing backup files",
    )

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a backup",
    )
    delete_parser.add_argument(
        "archive",
        help="Path to the backup ZIP file",
    )
    delete_parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip deletion confirmation",
    )

    return parser


def main() -> int:
    """Run the application."""
    configure_logging()

    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "backup":
            archive = create_backup(
                Path(args.source),
                Path(args.destination),
            )

            print(f"Backup created: {archive}")
            return 0

        if args.command == "restore":
            count = restore_backup(
                Path(args.archive),
                Path(args.destination),
            )

            print(f"Restored {count} file(s).")
            return 0

        if args.command == "verify":
            valid, message = verify_backup(
                Path(args.archive)
            )

            print(message)
            return 0 if valid else 1

        if args.command == "list":
            backups = list_backups(
                Path(args.directory)
            )

            if not backups:
                print("No backups found.")
                return 0

            for backup in backups:
                print(backup)

            return 0

        if args.command == "delete":
            archive = Path(args.archive)

            if not args.yes:
                answer = input(
                    f"Delete '{archive}'? "
                    "Type 'yes' to confirm: "
                )

                if answer.strip().lower() != "yes":
                    print("Deletion cancelled.")
                    return 0

            delete_backup(archive)

            print(f"Deleted: {archive}")
            return 0

    except (
        FileNotFoundError,
        NotADirectoryError,
        PermissionError,
        ValueError,
        OSError,
    ) as exc:
        logging.getLogger(__name__).error(
            "Operation failed: %s",
            exc,
        )

        print(
            f"Error: {exc}",
            file=sys.stderr,
        )

        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())