-- Additive migration; does not change the engagement tables.
CREATE TABLE IF NOT EXISTS social_accounts (
  platform TEXT PRIMARY KEY CHECK(platform IN ('instagram','linkedin')),
  account_id TEXT NOT NULL,
  label TEXT NOT NULL,
  token TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  connected_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS social_oauth (
  state TEXT PRIMARY KEY,
  platform TEXT NOT NULL,
  expires_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS social_settings (
  id INTEGER PRIMARY KEY CHECK(id = 1),
  enabled INTEGER NOT NULL DEFAULT 0
);
INSERT OR IGNORE INTO social_settings(id) VALUES(1);
CREATE TABLE IF NOT EXISTS social_jobs (
  id TEXT PRIMARY KEY,
  source_slug TEXT NOT NULL,
  platform TEXT NOT NULL CHECK(platform IN ('instagram','linkedin','tiktok')),
  account_id TEXT,
  title TEXT NOT NULL,
  caption TEXT NOT NULL,
  source_url TEXT NOT NULL,
  media TEXT NOT NULL DEFAULT '[]',
  scheduled_at TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft' CHECK(status IN ('draft','scheduled','processing','published','failed','review','cancelled','handoff')),
  attempts INTEGER NOT NULL DEFAULT 0,
  next_attempt_at TEXT,
  container_id TEXT,
  external_id TEXT,
  external_url TEXT,
  error TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(source_slug, platform)
);
CREATE INDEX IF NOT EXISTS social_jobs_due ON social_jobs(status, scheduled_at, next_attempt_at);
CREATE TABLE IF NOT EXISTS social_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_id TEXT NOT NULL,
  action TEXT NOT NULL,
  detail TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL
);
