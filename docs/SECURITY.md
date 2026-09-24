# Security Considerations

## Overview

Security is an important part of the File Backup & Recovery System.

The application handles files and archive contents, so it includes safeguards designed to reduce common risks associated with backup and restoration operations.

## 1. ZIP Path Traversal Protection

The restoration process validates every path stored inside a backup archive before extracting it.

A malicious archive could contain a path such as:

```text
../../outside.txt
```

Without validation, extracting such a file could write data outside the selected restoration directory.

The application resolves the target path and verifies that it remains inside the requested destination directory.

Unsafe paths are rejected with an error.

## 2. Backup Integrity Verification

Every backup contains a `backup_manifest.json` file.

The manifest records information about each backed-up file, including:

- Relative file path
- File size
- SHA-256 hash

During verification, the application recalculates the SHA-256 hash of each stored file and compares it with the value recorded in the manifest.

This helps detect unexpected modification or corruption of backup contents.

## 3. ZIP CRC Verification

The verification process also uses the ZIP archive's built-in CRC checks.

The application runs a ZIP integrity test before performing manifest-based verification.

This provides an additional layer of archive integrity checking.

## 4. File Size Verification

The manifest records the original size of each backed-up file.

During verification, the application compares the recorded size with the size of the file stored in the archive.

A size mismatch causes verification to fail.

## 5. Manifest Validation

The backup manifest is required for successful integrity verification.

The application checks that:

- The manifest exists
- The manifest contains valid JSON
- Required file information can be read
- Manifest entries correspond to files in the archive

Invalid or incomplete manifest data causes verification to fail.

## 6. Safe Test Data

Automated tests use temporary directories and files rather than real user data.

This reduces the risk of accidentally modifying or deleting personal files during testing.

The project's `.gitignore` also excludes test-related directories such as:

```text
test-data/
backups/
restored/
```

## 7. Controlled Backup Deletion

Backup deletion requires explicit confirmation by default.

For example:

```text
Delete 'backup.zip'? Type 'yes' to confirm:
```

The `--yes` option is available for controlled automation where confirmation is intentionally bypassed.

## 8. Error Handling

The application handles expected filesystem and application errors instead of allowing them to produce uncontrolled failures.

Examples include:

- Missing source directories
- Missing backup archives
- Invalid directories
- Permission errors
- Invalid archive files
- Unsafe archive paths
- Invalid manifest data

Errors are displayed to the user and recorded in the application log where appropriate.

## 9. Logging

Important application events are recorded in:

```text
logs/backup_manager.log
```

Logging can assist with troubleshooting and understanding application activity.

The log directory is excluded from version control through `.gitignore`.

## 10. Local Operation

The application operates locally and does not require:

- A cloud account
- A remote database
- An external backup server
- An internet connection

This reduces the number of external services involved in normal backup operations.

## Security Limitations

The current implementation does not provide encryption for backup archives.

Therefore, sensitive backup files should be protected using appropriate operating-system permissions and secure storage.

The application also does not currently provide:

- Password-protected backups
- Backup encryption
- Cloud security controls
- Multi-user authentication
- Role-based access control
- Secure remote storage

These are outside the current project's scope.

## Security Testing

Security-related behavior is tested using automated tests.

The test suite includes a path traversal test that verifies that an unsafe archive path is rejected.

Example test scenario:

```text
../../outside.txt
```

The expected behavior is for the application to raise an error instead of allowing the path to escape the restoration directory.

## Security Principle

The project follows a simple security principle:

> Validate data before acting on it.

Archive paths, backup files, manifests, and filesystem operations are validated before potentially destructive or security-sensitive actions are performed.