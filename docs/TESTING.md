# Testing

## Overview

The File Backup & Recovery System uses automated tests to verify core functionality and security-related behavior.

The test suite is written with `pytest` and uses temporary directories and files so that tests do not modify real user data.

## Testing Framework

The project uses:

- Python
- pytest
- Python `tempfile` functionality through pytest's `tmp_path` fixture

Install the development testing dependency with:

```bash
python -m pip install -r requirements.txt
```

## Running the Test Suite

From the project root, run:

```bash
python -m pytest
```

The project's `pyproject.toml` configures pytest to discover tests in:

```text
tests/
```

## Test Organization

```text
tests/
├── test_backup.py
├── test_hashing.py
├── test_restore.py
└── test_verification.py
```

## Backup Tests

`test_backup.py` verifies backup creation and backup listing.

### Backup Creation

The test:

1. Creates a temporary source directory
2. Creates test files
3. Creates a backup
4. Confirms that the ZIP archive exists
5. Confirms that the expected files are stored
6. Confirms that the backup manifest exists
7. Checks manifest information

### Backup Listing

The listing test verifies that created backup archives can be discovered by the application.

## Hashing Tests

`test_hashing.py` verifies SHA-256 file hashing.

The test creates a temporary text file and compares the calculated SHA-256 hash with the expected hash.

This confirms that the hashing utility produces the expected result.

## Restore Tests

`test_restore.py` verifies the restoration process.

### Normal Restoration

The test:

1. Creates temporary source data
2. Creates a backup
3. Restores the backup
4. Confirms that the expected file exists
5. Confirms that restored content matches the original content

### Path Traversal Protection

The security test attempts to use an unsafe path:

```text
../../outside.txt
```

The application is expected to reject this path.

The test passes when a `ValueError` is raised.

This verifies an important security control in the restoration process.

## Verification Tests

`test_verification.py` verifies backup integrity checking.

### Valid Backup

The test creates a valid backup and confirms that verification succeeds.

### Modified Backup

The test intentionally modifies the SHA-256 hash stored in the backup manifest.

The verification process should detect the mismatch and report that the backup is invalid.

This demonstrates that the application can detect unexpected changes to backup contents.

## Test Isolation

Tests use pytest's `tmp_path` fixture.

Temporary directories are created automatically for each test.

This means the tests do not depend on project directories such as:

```text
backups/
restored/
test-data/
```

and do not require access to personal files.

## Expected Result

A successful test run should display output similar to:

```text
============================= test session starts =============================
...
passed
...
============================== X passed in ... ================================
```

The exact number and execution time may change as the test suite evolves.

## Manual Testing

In addition to automated tests, the application should be manually tested through its command-line interface.

A basic manual workflow is:

### 1. Create test data

```bash
mkdir test-data
```

Create sample files inside the directory.

### 2. Create a backup

```bash
python -m backup_manager.main backup test-data backups
```

### 3. List backups

```bash
python -m backup_manager.main list backups
```

### 4. Verify the backup

```bash
python -m backup_manager.main verify backups/BACKUP_FILE.zip
```

### 5. Restore the backup

```bash
python -m backup_manager.main restore backups/BACKUP_FILE.zip restored
```

### 6. Compare restored files

Confirm that the restored files contain the same expected data as the original test files.

### 7. Review logging

Check:

```text
logs/backup_manager.log
```

to confirm that important operations were recorded.

### 8. Delete the test backup

After testing is complete, a backup can be removed using:

```bash
python -m backup_manager.main delete backups/BACKUP_FILE.zip
```

## Cross-Platform Testing

The project is designed for:

- Windows
- Linux
- macOS

Testing should be performed on each available operating system to confirm that filesystem operations, virtual environments, package installation, and command-line behavior work correctly.

The development workflow for this project is:

```text
Windows Development
        │
        ▼
Automated Tests
        │
        ▼
Manual CLI Testing
        │
        ▼
Linux Verification
        │
        ▼
macOS Compatibility Consideration
        │
        ▼
GitHub Publication
```

## Testing Goals

The testing process is intended to verify:

- Correct backup creation
- Correct backup listing
- Correct file hashing
- Correct restoration
- Integrity verification
- Detection of modified backup data
- Path traversal protection
- Expected error handling
- Cross-platform compatibility

## Test Philosophy

The project follows a practical testing approach:

> Test normal behavior, test failure conditions, and test security-sensitive behavior.

Automated tests provide repeatable verification of core functionality, while manual testing confirms that the complete command-line workflow works as expected.