# Supabase setup — ISSUE-03

**Owner:** B (SM) · **Day:** 1  
**Goal:** Live Supabase project with all BrandSight tables, Storage bucket for crops, and secrets shared securely with the team.

Related: [KANBAN.md](./KANBAN.md) · [sql/schema.sql](../sql/schema.sql) · [sql/storage.sql](../sql/storage.sql)

---

## 1. Create project

1. Go to [supabase.com/dashboard](https://supabase.com/dashboard) → **New project**
2. Name: `brandsight` (or team name)
3. Database password: generate and **save in team password manager** (not Git, not Slack plain text)
4. Region: closest to deploy (e.g. `eu-west-1`)
5. Plan: **Free**

Wait until the project status is **Active** (~2 min).

---

## 2. Run database schema

1. Dashboard → **SQL Editor** → **New query**
2. Copy the full contents of [`sql/schema.sql`](../sql/schema.sql)
3. Click **Run**
4. Expected: success, no errors (uses `CREATE TABLE IF NOT EXISTS`)

**Tables created:**

| Table | Purpose |
|-------|---------|
| `videos` | Uploaded / analyzed videos |
| `detections` | Per-frame logo detections |
| `brand_summary` | Visibility seconds / % per brand |
| `competitive_analysis` | Coca-Cola vs Pepsi dominance |
| `marketing_reports` | AI-generated reports |

5. **Table Editor** → confirm all 5 tables appear

---

## 3. Create Storage bucket for crops

1. **SQL Editor** → run [`sql/storage.sql`](../sql/storage.sql)  
   **or** Dashboard → **Storage** → **New bucket** → name `brandsight-crops`, **private**
2. Verify the bucket appears under **Storage**

The app uploads bbox crops to `brandsight-crops/{video_id}/{brand}_{index}.jpg` and stores a `storage:…` URI in `detections.crop_path`.

---

## 4. Get `DATABASE_URL` (Session pooler)

1. **Project Settings** → **Database**
2. **Connection string** → URI
3. Mode: **Session pooler** (port `5432`) — required for Streamlit / server apps
4. Copy string; replace `[YOUR-PASSWORD]` with your DB password

Example shape:

```
postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
```

SQLAlchemy accepts this as-is; the app auto-adds `+psycopg2` if needed.

---

## 5. Get Storage API credentials

1. **Project Settings** → **API**
2. Copy **Project URL** → `SUPABASE_URL`
3. Copy **service_role** key → `SUPABASE_SERVICE_ROLE_KEY` (**never expose in frontend / Git**)

---

## 6. Local `.env` (each teammate)

```bash
cp .env.example .env
```

Edit `.env` — set at minimum:

```bash
DATABASE_URL=...
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_SERVICE_ROLE_KEY=...
```

**Never commit `.env`.**

---

## 7. Verify from your machine

```bash
pip install -r requirements.txt
python -m scripts.check_db
python -m scripts.check_storage
```

Expected output:

```
Connection OK
Schema OK — 5 tables: videos, detections, brand_summary, competitive_analysis, marketing_reports
OK: Storage bucket 'brandsight-crops' is available
```

If schema check fails, re-run `sql/schema.sql` in the SQL Editor.

---

## 8. Share credentials with team (secure channel)

Share via **team password manager**, **encrypted note**, or **DM** — not:

- Git / GitHub issues / PR comments
- Public Slack channels
- Screenshots with password visible

| Secret | Who needs it |
|--------|----------------|
| `DATABASE_URL` (Session pooler) | A, B, C — Day 1 |
| `SUPABASE_URL` | A, B, C — Day 1+ |
| `SUPABASE_SERVICE_ROLE_KEY` | A, B, C — Day 1+ (backend only) |
| Supabase dashboard login | B (SM) |

---

## 9. Close ISSUE-03

- [ ] Supabase project live
- [ ] All 5 tables in Table Editor
- [ ] `brandsight-crops` bucket created
- [ ] `python -m scripts.check_db` passes
- [ ] `python -m scripts.check_storage` passes
- [ ] `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` shared with A and C
- [ ] Update [KANBAN.md](./KANBAN.md) ISSUE-03 → **Done**

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Connection refused` | Use **Session pooler** URI, not direct connection |
| `password authentication failed for user "postgres"` | Pooler username must be **`postgres.[project-ref]`**, not `postgres`. Copy URI from Dashboard → Database → **Session pooler** |
| `password authentication failed` (correct username) | Wrong DB password, or special chars not URL-encoded (`@` → `%40`, `#` → `%23`). Reset password in Project Settings → Database |
| Missing tables | Re-run `sql/schema.sql`; check SQL Editor error panel |
| Bucket not found | Re-run `sql/storage.sql` or create bucket in Dashboard → Storage |
| Crop upload fails | Confirm `SUPABASE_SERVICE_ROLE_KEY` (not anon key) and bucket name `brandsight-crops` |
| SSL errors | Ensure URI is from Supabase dashboard (includes SSL by default) |
| IPv6 issues on pooler | Try **Transaction pooler** temporarily for local test only |

---

_Configuración en español: mismos pasos; el SM (B) ejecuta y comparte credenciales por canal seguro._
