-- BrandSight — Supabase schema
-- Run in Supabase SQL Editor: Dashboard → SQL → New query

CREATE TABLE IF NOT EXISTS videos (
    id              SERIAL PRIMARY KEY,
    filename        VARCHAR(255) NOT NULL,
    storage_path    TEXT NOT NULL,
    duration_sec    DOUBLE PRECISION NOT NULL,
    fps             DOUBLE PRECISION,
    total_frames    INTEGER,
    annotated_path  TEXT,
    status          VARCHAR(20) DEFAULT 'pending',
    processed_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS detections (
    id              SERIAL PRIMARY KEY,
    video_id        INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    brand           VARCHAR(50) NOT NULL,
    confidence      DOUBLE PRECISION NOT NULL,
    frame_number    INTEGER NOT NULL,
    timestamp_sec   DOUBLE PRECISION NOT NULL,
    bbox_x          DOUBLE PRECISION NOT NULL,
    bbox_y          DOUBLE PRECISION NOT NULL,
    bbox_w          DOUBLE PRECISION NOT NULL,
    bbox_h          DOUBLE PRECISION NOT NULL,
    crop_path       TEXT
);

CREATE TABLE IF NOT EXISTS brand_summary (
    id              SERIAL PRIMARY KEY,
    video_id        INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    brand           VARCHAR(50) NOT NULL,
    visible_seconds DOUBLE PRECISION NOT NULL,
    visibility_pct  DOUBLE PRECISION NOT NULL,
    detection_count INTEGER NOT NULL,
    avg_confidence  DOUBLE PRECISION,
    UNIQUE (video_id, brand)
);

CREATE TABLE IF NOT EXISTS competitive_analysis (
    id                  SERIAL PRIMARY KEY,
    video_id            INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE UNIQUE,
    dominant_brand      VARCHAR(50) NOT NULL,
    coca_cola_seconds   DOUBLE PRECISION NOT NULL,
    pepsi_seconds       DOUBLE PRECISION NOT NULL,
    coca_cola_pct       DOUBLE PRECISION NOT NULL,
    pepsi_pct           DOUBLE PRECISION NOT NULL,
    visibility_gap_sec  DOUBLE PRECISION NOT NULL,
    balance_label       VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS marketing_reports (
    id              SERIAL PRIMARY KEY,
    video_id        INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    model_name      VARCHAR(100),
    prompt_version  VARCHAR(20),
    report_text     TEXT NOT NULL,
    report_path     TEXT,
    generated_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_detections_video_id ON detections(video_id);
CREATE INDEX IF NOT EXISTS idx_detections_brand ON detections(brand);
