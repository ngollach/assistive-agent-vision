# MCP Integration Plan

## Purpose
This project uses an MCP-readiness layer to prepare for safe external tool integration.

The assistive agent may eventually connect to MCP servers for:
- Reading local files
- Reading Google Drive files
- Creating optional Google Docs summaries
- Saving optional evaluation reports
- Exporting user-approved summaries

## Security Rules
1. Read-only access is allowed only for approved tools.
2. Write and export actions require explicit user confirmation.
3. User images must not be saved or exported without approval.
4. API keys and credentials must never be hardcoded.
5. MCP servers should run with least privilege.
6. Public MCP servers must not receive sensitive user data.
7. Tool calls should be logged for auditability.

## Approved Read-Only Tool Types
- filesystem_read
- google_drive_read
- google_docs_read

## Write / Export Tool Types
These require human confirmation:
- google_drive_write
- google_docs_write
- google_sheets_write

## Capstone Explanation
This layer demonstrates MCP-style tool governance before connecting real external systems. It follows a safe-by-default design where read tools are limited and write/export actions are blocked unless the user confirms.