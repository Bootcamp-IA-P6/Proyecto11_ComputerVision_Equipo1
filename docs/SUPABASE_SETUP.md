# Supabase setup — ISSUE-03

**Owner:** B (SM) · **Day:** 1  
**Goal:** Live Supabase project with all BrandSight tables; `DATABASE_URL` shared securely with the team.

Related: [KANBAN.md](./KANBAN.md) · [sql/schema.sql](../sql/schema.sql)

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

## 3. Get `DATABASE_URL` (Session pooler)

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

## 4. Local `.env` (each teammate)

```bash
cp .env.example .env
```

Edit `.env` — set `DATABASE_URL` only for ISSUE-03 (other keys can wait).

**Never commit `.env`.**

---

## 5. Verify from your machine

```bash
pip install -r requirements.txt
python -m scripts.check_db
```

Expected output:

```
Connection OK
Schema OK — 5 tables: videos, detections, brand_summary, competitive_analysis, marketing_reports
```

If schema check fails, re-run `sql/schema.sql` in the SQL Editor.

---

## 6. Share credentials with team (secure channel)

Share via **team password manager**, **encrypted note**, or **DM** — not:

- Git / GitHub issues / PR comments
- Public Slack channels
- Screenshots with password visible

**Minimum to share:**

| Secret | Who needs it |
|--------|----------------|
| `DATABASE_URL` (Session pooler) | A, B, C — Day 1 |
| Supabase dashboard login | B (SM); optional read for others |

**Optional (ISSUE-11 — crops in cloud):**

| Secret | When |
|--------|------|
| `SUPABASE_URL` | Day 4+ |
| `SUPABASE_SERVICE_ROLE_KEY` | Day 4+ — **service role, never in frontend** |

---

## 7. Optional — Storage bucket `brandsight-crops`

**Option A — Dashboard**

1. **Storage** → **New bucket**
2. Name: `brandsight-crops`
3. Public: **off** (use signed URLs or app-side access)

**Option B — SQL**

Run [`sql/storage.sql`](../sql/storage.sql) in SQL Editor.

---

## 8. Close ISSUE-03

- [ ] Supabase project live
- [ ] All 5 tables in Table Editor
- [ ] `python -m scripts.check_db` passes on SM machine
- [ ] `DATABASE_URL` shared with A and C
- [ ] Optional: `brandsight-crops` bucket created
- [ ] Update [KANBAN.md](./KANBAN.md) ISSUE-03 → **Done**

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Connection refused` | Use **Session pooler** URI, not direct connection |
| `password authentication failed for user "postgres"` | Pooler username must be **`postgres.[project-ref]`**, not `postgres`. Copy URI from Dashboard → Database → **Session pooler** |
| `password authentication failed` (correct username) | Wrong DB password, or special chars not URL-encoded (`@` → `%40`, `#` → `%23`). Reset password in Project Settings → Database |
| Missing tables | Re-run `sql/schema.sql`; check SQL Editor error panel |
| SSL errors | Ensure URI is from Supabase dashboard (includes SSL by default) |
| IPv6 issues on pooler | Try **Transaction pooler** temporarily for local test only |

---

_Configuración en español: mismos pasos; el SM (B) ejecuta y comparte `DATABASE_URL` por canal seguro._
