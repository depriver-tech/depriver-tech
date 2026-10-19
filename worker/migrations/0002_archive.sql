CREATE TABLE IF NOT EXISTS archive_files (
 id TEXT PRIMARY KEY,
 object_key TEXT NOT NULL UNIQUE,
 title TEXT NOT NULL,
 description TEXT NOT NULL DEFAULT '',
 filename TEXT NOT NULL,
 category TEXT NOT NULL CHECK (category IN ('documents','images','applications','archives')),
 extension TEXT NOT NULL,
 size INTEGER NOT NULL CHECK (size > 0),
 status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','published')),
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX IF NOT EXISTS archive_public_order ON archive_files(status, created_at DESC, id DESC);
