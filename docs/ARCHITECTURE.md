# System Architecture

## Overview

The File Backup & Recovery System uses a modular Python architecture based on a `src/` package layout.

The application separates command-line interaction, backup operations, restoration, verification, configuration, hashing, and logging into dedicated modules.

This separation makes the project easier to understand, test, maintain, and extend.

## Architecture

```text
User
  │
  ▼
Command-Line Interface
src/backup_manager/main.py
  │
  ├── Backup Service
  │     └── services/backup.py
  │
  ├── Restore Service
  │     └── services/restore.py
  │
  ├── Verification Service
  │     └── services/verification.py
  │
  ├── Configuration
  │     └── config.py
  │
  └── Utilities
        ├── utils/hashing.py
        └── utils/logging_config.py
```

## Components

### `main.py`

The main command-line interface.

Responsibilities include:

- Parsing command-line arguments
- Selecting the requested operation
- Calling the appropriate service
- Displaying results to the user
- Handling application-level errors
- Returning appropriate exit codes

Supported commands include:

- `backup`
- `restore`
- `verify`
- `list`
- `delete`

### `services/backup.py`

Responsible for creating and managing backup archives.

Responsibilities include:

- Validating source directories
- Finding files to back up
- Creating timestamped ZIP archives
- Generating the backup manifest
- Calculating SHA-256 hashes
- Listing existing backups
- Deleting backup archives

### `services/restore.py`

Responsible for restoring files from backup archives.

Responsibilities include:

- Validating the backup archive
- Creating the restoration directory
- Extracting backed-up files
- Preventing ZIP path traversal
- Recording restoration activity

### `services/verification.py`

Responsible for checking backup integrity.

Verification includes:

1. Checking that the archive is a valid ZIP file
2. Running ZIP CRC integrity checks
3. Confirming that the backup manifest exists
4. Checking that manifest files exist in the archive
5. Comparing SHA-256 hashes
6. Comparing recorded and actual file sizes

### `utils/hashing.py`

Provides reusable SHA-256 hashing functions.

The module supports:

- Hashing files
- Hashing byte data

File hashing is performed in chunks rather than loading the entire file into memory at once.

### `utils/logging_config.py`

Configures application logging.

Logs are stored in:

```text
logs/backup_manager.log
```

The logging system records important application events and failures.

### `config.py`

Contains shared application configuration such as:

- Application name
- Application version
- Manifest filename
- Hashing algorithm
- Hashing chunk size
- Backup filename format
- Log directory
- Log filename

Keeping these values in one module reduces duplication and makes configuration easier to maintain.

## Backup Workflow

The backup process follows this sequence:

```text
Source Directory
       │
       ▼
Validate Source
       │
       ▼
Find Files
       │
       ▼
Calculate SHA-256 Hashes
       │
       ▼
Create Backup Manifest
       │
       ▼
Create ZIP Archive
       │
       ▼
Store Files + Manifest
       │
       ▼
Log Operation
```

## Verification Workflow

```text
Backup ZIP
    │
    ▼
Validate ZIP
    │
    ▼
Run CRC Check
    │
    ▼
Read Manifest
    │
    ▼
Check Files
    │
    ▼
Calculate SHA-256
    │
    ▼
Compare Hashes
    │
    ▼
Compare File Sizes
    │
    ▼
Return Verification Result
```

## Restoration Workflow

```text
Backup ZIP
    │
    ▼
Validate Archive
    │
    ▼
Create Destination
    │
    ▼
Validate Archive Paths
    │
    ▼
Extract Files
    │
    ▼
Log Operation
```

## Testing Architecture

Automated tests are located in the `tests/` directory.

Each major component has dedicated tests:

```text
tests/
├── test_backup.py
├── test_hashing.py
├── test_restore.py
└── test_verification.py
```

The project uses `pytest` for automated testing.

The tests use temporary directories and files so that testing does not require modifying real user data.

## Design Principles

The project follows several practical software-development principles:

### Separation of Responsibilities

Each module has a specific responsibility rather than placing all functionality in one large file.

### Reusable Components

Hashing, logging, configuration, backup, restoration, and verification functionality are separated into reusable modules.

### Security by Design

The restoration process validates archive paths before writing files to disk to reduce the risk of path traversal attacks.

### Testability

Core operations are implemented as functions that can be tested independently from the command-line interface.

### Cross-Platform Design

The application uses Python's standard library and `pathlib` for filesystem operations, supporting Windows, Linux, and macOS.

### Maintainability

The `src/` package structure, configuration module, service separation, documentation, and automated tests provide a foundation for future improvements.

## Future Extensions

The architecture can be extended to support features such as:

- Backup encryption
- Incremental backups
- Scheduled backups
- Backup retention policies
- Cloud storage integration
- Backup compression options
- Restore previews
- Configuration files
- Additional integrity algorithms