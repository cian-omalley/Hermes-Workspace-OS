# Storage Design

## Purpose
Define how binary/large objects (files, images, videos, generated assets, repo snapshots)
are stored, referenced, and secured.

## Current State
Designed; unimplemented (M6). Backed by **MinIO** (S3-compatible) behind the Storage
provider port, with local FS as a dev default.

## Model
- **Bytes** live in MinIO/object storage; **metadata** lives in Postgres (`assets`,
  `asset_derivatives`).
- **Content-addressed keys:** objects keyed by content hash → automatic deduplication
  (`assets.content_hash` unique per workspace).
- **Derivatives:** thumbnails, page images, transcripts, extracted pages stored as
  `asset_derivatives` referencing the parent asset.
- **Provenance:** uploader, source integration, original filename recorded.

## Access
- Reads/writes via the Storage provider interface (`put/get/delete/presigned_url`).
- **Presigned URLs** for direct client download/upload where supported (avoids proxying
  large files through the API).
- Access is permission-checked; keys are opaque and not guessable.

## Architecture Decisions
1. **Storage behind a port** → MinIO ↔ S3 ↔ GCS ↔ local FS swap with no business-logic
   change (`docs/06`).
2. **Content-addressing** for dedup, integrity, and cache-friendliness.
3. **Separation of bytes and metadata** so queries/search operate on Postgres while bytes
   stream from object storage.

## Alternatives Considered
- **Storing files in Postgres (BYTEA/large objects)** — rejected: bloats the DB, hurts
  backups/performance.
- **Filesystem-only** — fine for single-host dev; not scalable/replicable → MinIO default
  for real deployments (same interface).
- **Third-party managed storage as default** — supported via plugin, but self-host-first
  favors MinIO.

## Future Improvements
Lifecycle policies (tiering/expiry for derivatives), server-side encryption, CDN/presign
tuning, virus-scan-on-write hook, and large-video handling (chunked/streamed transcode).

## Implementation Notes
- Stream uploads to storage; never buffer whole large files in memory.
- Enforce size/type guards and archive-bomb protection before processing (`docs/13`).
- Deleting an asset removes bytes + derivatives + associated embeddings/graph refs.
- **Decision Required:** default bucket layout and retention for derivatives
  (`docs/MISSING_INFORMATION.md`).
