-- BrandSight — Supabase Storage bucket for bbox crops (ISSUE-03 / ISSUE-10)
-- Run in SQL Editor after schema.sql, or create the bucket in Dashboard → Storage.

INSERT INTO storage.buckets (id, name, public)
VALUES ('brandsight-crops', 'brandsight-crops', false)
ON CONFLICT (id) DO NOTHING;
