# Gemini CLI Playbook
## GitHub-Automated Blog aufsetzen — Schritt für Schritt

> **Ziel:** Vollständige Blog-Pipeline in einer Session aufsetzen  
> **Tool:** Gemini CLI (google-gemini/gemini-cli)  
> **System:** Intel Celeron · 512MB RAM · Windows/Linux  
> **Zeit:** ca. 2–3 Stunden für initiales Setup

---

## Inhaltsverzeichnis

1. [Voraussetzungen & Installation](#1-voraussetzungen--installation)
2. [Gemini CLI Grundlagen](#2-gemini-cli-grundlagen)
3. [Repository einrichten](#3-repository-einrichten)
4. [Hugo installieren & konfigurieren](#4-hugo-installieren--konfigurieren)
5. [Context-Dateien erstellen](#5-context-dateien-erstellen)
6. [GitHub Actions Workflows bauen](#6-github-actions-workflows-bauen)
7. [API-Keys konfigurieren](#7-api-keys-konfigurieren)
8. [Frontend einrichten](#8-frontend-einrichten)
9. [Ersten Post durch die Pipeline jagen](#9-ersten-post-durch-die-pipeline-jagen)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Voraussetzungen & Installation

### Was du brauchst (alles kostenlos)

Bevor du startest, sorge dafür, dass folgende Accounts existieren:

- **GitHub Account** (github.com) — falls noch nicht vorhanden
- **Google AI Studio** (aistudio.google.com) — mit deinem Google AI Pro Account einloggen
- **Serper.dev** (serper.dev) → Account erstellen → API Key kopieren
- **Unsplash Developers** (unsplash.com/developers) → App erstellen → Access Key kopieren
- **Buttondown** (buttondown.email) → Account erstellen (kostenlos)
- **Formspree** (formspree.io) → Account erstellen → ein Formular anlegen

### Node.js installieren (für Gemini CLI)

Gemini CLI braucht Node.js 18+. Auf deinem Celeron-System:

**Windows:**
```
1. nodejs.org → "LTS" Version herunterladen
2. Installer ausführen
3. Standardeinstellungen belassen
```

**Linux/WSL:**
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Prüfen:**
```bash
node --version    # sollte v18.x.x oder höher zeigen
npm --version     # sollte 9.x.x oder höher zeigen
```

### Gemini CLI installieren

```bash
npm install -g @google/gemini-cli
```

**Prüfen:**
```bash
gemini --version
```

### Git installieren (falls nicht vorhanden)

**Windows:** git-scm.com → Download → Installer  
**Linux:** `sudo apt-get install git`

```bash
# Git konfigurieren (einmalig)
git config --global user.name "Dein Name"
git config --global user.email "deine@email.com"
```

### GitHub CLI installieren (sehr empfohlen)

```bash
# Linux:
sudo apt install gh

# Windows: github.com/cli/cli → Download
```

```bash
# Mit GitHub verbinden:
gh auth login
# → "GitHub.com" → "HTTPS" → Browser öffnet sich → Einloggen
```

---

## 2. Gemini CLI Grundlagen

### Mit API Key authentifizieren

```bash
# Deinen Gemini API Key aus aistudio.google.com/apikey holen
gemini auth --api-key DEIN_API_KEY

# Alternativ als Umgebungsvariable (empfohlen für Scripting):
export GEMINI_API_KEY="DEIN_API_KEY"
```

### Basis-Syntax

```bash
# Einfache Anfrage:
gemini "Schreibe mir ein Haiku über Mykorrhiza"

# Mit Modell-Spezifikation:
gemini --model gemini-1.5-pro "Dein Prompt"
gemini --model gemini-1.5-flash "Dein Prompt"    # Schneller, günstiger

# Mit Datei als Kontext:
gemini --file context/system-identity.md "Schreibe einen Post über ..."

# Mit mehreren Dateien:
gemini --file context/system-identity.md --file context/blog-memory.json "..."

# Output in Datei schreiben:
gemini "..." > output.md

# Interaktiver Chat-Modus:
gemini chat
```

### Nützliche Flags

```bash
--model          # Modell wählen (gemini-1.5-pro, gemini-1.5-flash)
--file           # Datei als Kontext hinzufügen (wiederholbar)
--temperature    # Kreativität 0.0–2.0 (Standard: 1.0)
--max-tokens     # Maximale Ausgabelänge
--json           # Output als JSON (für Scripting)
--quiet          # Nur Output, keine Meta-Informationen
```

### Erster Test — System Identity generieren lassen

```bash
gemini --model gemini-1.5-pro "
Erstelle eine system-identity.md Datei für einen Blog mit folgenden Eigenschaften:

Nische: Regenerative Wirtschaft und Ökosysteme
Von Forschung bis Anwendung, von Technologie bis Soil Science
Vibe: Natural Solarpunk x Avantgarde Prestige

Die Datei soll enthalten:
- Wer der Blog ist (2-3 Absätze)
- Ton und Stimme (konkrete Regeln)
- Verbotenes (was nie erscheinen darf)
- Zielgruppe
- Beispielsätze die den Ton zeigen

Format: Markdown, ca. 800 Tokens
" > context/system-identity.md
```

---

## 3. Repository einrichten

### Neues GitHub Repository erstellen

```bash
# Mit GitHub CLI:
gh repo create dein-blog-name \
  --public \
  --description "Regenerative Wirtschaft & Ökosysteme Blog" \
  --clone

cd dein-blog-name
```

**Oder manuell:** GitHub.com → New Repository → Public → Clone URL kopieren → `git clone URL`

### Ordnerstruktur anlegen

```bash
# Alle nötigen Ordner erstellen:
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p context/agent-prompts
mkdir -p content/de/posts
mkdir -p content/en/posts
mkdir -p _drafts
mkdir -p _distribution
mkdir -p assets/images
mkdir -p static/favicon
mkdir -p layouts/partials
mkdir -p config

# Leere Placeholder-Dateien erstellen (Git trackt keine leeren Ordner):
touch _drafts/.gitkeep
touch _distribution/.gitkeep
touch assets/images/.gitkeep
```

### GitHub Discussions aktivieren

Das brauchst du für Giscus (Kommentarsystem):

1. Dein Repo auf GitHub.com öffnen
2. **Settings** → **Features** → **Discussions** → Checkbox aktivieren

### Dependabot aktivieren

```bash
cat > .github/dependabot.yml << 'EOF'
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "chore"
EOF
```

---

## 4. Hugo installieren & konfigurieren

### Hugo Binary herunterladen

**Linux/WSL:**
```bash
# Aktuelle Version prüfen: github.com/gohugoio/hugo/releases
HUGO_VERSION="0.121.2"

wget "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
tar -xzf hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz
sudo mv hugo /usr/local/bin/
rm hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz

# Prüfen:
hugo version
```

**Windows:**
```
github.com/gohugoio/hugo/releases → hugo_extended_X.X.X_windows-amd64.zip
→ Entpacken → hugo.exe in einen PATH-Ordner kopieren (z.B. C:\Windows\System32)
```

### Hugo Site initialisieren

```bash
# Im Repo-Ordner:
hugo new site . --force    # --force weil Ordner schon existiert
```

### Theme installieren (Blowfish)

```bash
# Als Git Submodule (empfohlen):
git submodule add -b main https://github.com/nunocoracao/blowfish.git themes/blowfish

# Oder ohne Submodule:
git clone https://github.com/nunocoracao/blowfish.git themes/blowfish
```

### Hugo Basis-Konfiguration

```bash
# Alte config.toml entfernen, neue Struktur anlegen:
rm -f config.toml hugo.toml

# Gemini generiert die Konfiguration:
gemini --model gemini-1.5-flash "
Erstelle eine Hugo-Konfigurationsdatei (hugo.toml) für:

- Blog-Name: Rə:Generate
- baseURL: https://martyr92.github.io/regenerate-blog/ (oder custom domain)
- Zweisprachig: Deutsch (primary) und Englisch
- Theme: blowfish
- Taxonomien: tags, categories, series
- Output: HTML, RSS, JSON (für Pagefind)
- Autoren-Name: [Martin Reiter]

Gib nur die TOML-Datei aus, keinen erklärenden Text.
" > hugo.toml
```

**Bearbeite `hugo.toml` manuell** und ersetze Platzhalter:
- `USERNAME` → dein GitHub Username
- `REPO-NAME` → dein Repo-Name
- `[DEIN BLOG NAME]` → dein Blog-Titel
- `[DEIN NAME]` → dein Name

### Lokale Vorschau testen

```bash
hugo server -D
# Öffne im Browser: http://localhost:1313
# -D zeigt auch Draft-Posts
# Strg+C zum Beenden
```

---

## 5. Context-Dateien erstellen

Das ist der wichtigste Schritt — diese Dateien sind das "Gehirn" des Systems.

### system-identity.md (mit Gemini generieren, dann anpassen)

```bash
gemini --model gemini-1.5-pro "
Erstelle eine system-identity.md für einen Blog mit:
- Nische: Regenerative Wirtschaft und Ökosysteme (von Forschung bis Anwendung, von Tech bis Soil)
- Vibe: Natural Solarpunk x Avantgarde Prestige
- Zielgruppe: Wissenschaftler:innen, Unternehmer:innen, Designer:innen, Aktivist:innen die zwischen Theorie und Praxis operieren

Struktur:
1. Wer wir sind (2-3 kraftvolle Absätze)
2. Ton und Stimme (5-7 konkrete Regeln)
3. Verbotenes (was nie erscheinen darf)
4. Zielgruppe (präzise Beschreibung)
5. Tonbeispiele (3 Sätze die den Stil zeigen)

Ca. 800 Tokens. Nur Markdown, kein Meta-Text.
" > context/system-identity.md

# WICHTIG: Datei öffnen und personalisieren!
# Gemini gibt einen guten Entwurf — du kennst deinen Blog besser.
```

### blog-memory.json (Startversion)

```bash
cat > context/blog-memory.json << 'EOF'
{
  "version": "1.0",
  "last_updated": "2025-01-15",
  "total_posts": 0,
  "posts": [],
  "recurring_themes": [],
  "avoid_repetition": []
}
EOF
```

### series-registry.json

```bash
cat > context/series-registry.json << 'EOF'
{
  "version": "1.0",
  "last_updated": "2025-01-15",
  "series": []
}
EOF
```

### ontology.json (mit Gemini generieren)

```bash
gemini --model gemini-1.5-pro "
Erstelle eine ontology.json für einen Blog über Regenerative Wirtschaft und Ökosysteme.

Der Blog verbindet:
- Soil Science und Mykologie mit Wirtschaftssystemen
- Regenerative Landwirtschaft mit Finanzmodellen
- Open Source Technologie mit Naturprinzipien
- Systemdenken mit konkreter Praxis

Erstelle ein JSON mit:
- 5 Haupt-Domänen, jeweils mit 4-6 spezifischen Tags
- Jede Domäne mit kurzer Beschreibung
- Cross-Domain Tags für Querschnittsthemen
- Felder: domains (object), cross-domain-tags (array), version, last_updated

Nur JSON ausgeben, kein erklärender Text.
" > context/ontology.json
```

### visual-style-guide.md

```bash
gemini --model gemini-1.5-pro "
Erstelle eine visual-style-guide.md für KI-Bildgenerierung (Google Imagen) für einen Blog mit dem Vibe 'Natural Solarpunk x Avantgarde Prestige' im Themenbereich Regenerative Wirtschaft.

Enthalte:
1. Kern-Ästhetik (Beschreibung in 2-3 Sätzen)
2. Farb-Palette (beschreibend, keine Hex-Codes)
3. Kompositions-Prinzipien (5 Regeln)
4. 8 Referenz-Prompts für typische Post-Themen:
   - Mykorrhiza-Netzwerke
   - Kreislaufwirtschaft
   - Regenerative Landwirtschaft
   - Ökosystem-Diagramm
   - Boden-Querschnitt wissenschaftlich
   - Urbane Regeneration
   - Technologie-Natur-Hybrid
   - Gemeinschafts-Wirtschaft
5. Verbotene Ästhetiken (Corporate Flat Design etc.)

Format: Markdown mit Code-Blöcken für die Prompts.
" > context/visual-style-guide.md
```

### Agent-Prompts generieren

```bash
# Writer-Agent Prompt:
gemini --model gemini-1.5-pro --file context/system-identity.md "
Erstelle einen detaillierten System-Prompt nach "best practices 2026" für einen KI-Agenten (writer-agent), der Blog-Posts schreibt.

Der Agent:
- Liest system-identity.md (bereits als Kontext übergeben)
- Erhält research-queue.json Einträge als Input
- Schreibt 1.500-3.000 Wörter lange Artikel
- Generiert vollständiges Hugo Front Matter
- Integriert [VERIFY]-Tags für nicht belegte Claims
- Prüft series-registry.json auf offene Serien

Schreibe den Prompt als Anweisung an den Agenten (du-Form).
Konkret, nicht abstrakt. Ca. 600 Tokens.
" > context/agent-prompts/writer-v1.md

# Editor-Agent Prompt:
gemini --model gemini-1.5-flash --file context/system-identity.md "
Erstelle einen System-Prompt nach "best practices 2026" für einen editor-agent der Blog-Posts prüft.

Der Agent prüft:
- Ton-Konsistenz mit system-identity.md
- [VERIFY]-Tags (Claims ohne Quellennachweis)
- Interne Konsistenz mit blog-memory.json
- EU AI Act Compliance (ai_assisted Flag)
- DSGVO: keine personenbezogenen Daten ohne Kontext
- Tag-Konsistenz mit ontology.json

Output: GitHub PR mit Inline-Kommentaren und Empfehlung approved/needs-revision.
Ca. 400 Tokens.
" > context/agent-prompts/editor-v1.md
```

---

## 6. GitHub Actions Workflows bauen

### Workflow 1 — research-agent

```bash
# Gemini generiert den Workflow:
gemini --model gemini-1.5-pro "
Erstelle eine vollständige GitHub Actions Workflow YAML-Datei für einen research-agent basierend auf best practices 2026.

Anforderungen:
- Name: Research Agent
- Trigger: Cron Mo+Do 06:00 UTC, workflow_dispatch
- Runner: ubuntu-latest
- Python Script das Gemini API aufruft
- Umgebungsvariablen: GEMINI_API_KEY, SERPER_API_KEY (aus secrets)
- GITHUB_TOKEN für commit
- Retry-Logik: 3 Versuche, 60s Pause (nick-fields/retry@v2)
- Script: 
  1. Liest context/ontology.json für Suchthemen
  2. Sucht via Serper API (JSON-Output)
  3. Sucht via OpenAlex API (kostenlos, kein Key nötig)
  4. Ruft Gemini 1.5 Flash auf für Relevanz-Scoring und Zusammenfassung
  5. Schreibt Ergebnis in context/research-queue.json
  6. Git commit + push
- Error Handling: Bei Fehler → GitHub Actions Step Summary mit Fehlermeldung

Vollständige YAML, kein erklärender Text.
" > .github/workflows/research-agent.yml
```

**Nach der Generierung prüfen:**
```bash
# YAML-Syntax validieren (lokal):
cat .github/workflows/research-agent.yml

# Auf offensichtliche Fehler prüfen:
# - secrets.GEMINI_API_KEY referenziert?
# - Python-Script-Pfad korrekt?
# - Git-User für Commit konfiguriert?
```

### Workflow 2 — writer-agent

```bash
gemini --model gemini-1.5-pro "
Erstelle eine GitHub Actions Workflow YAML für einen writer-agent basierend auf best practices 02/2026.

Anforderungen:
- Trigger: workflow_run (nach research-agent), issues (label 'write:'), workflow_dispatch
- Python Script das:
  1. context/system-identity.md liest
  2. context/blog-memory.json liest  
  3. context/series-registry.json liest
  4. context/research-queue.json liest (top 3 relevante Items)
  5. Gemini 2.5 Pro aufruft mit allen Context-Dateien + Auftrag
  6. Hugo Front Matter generiert (inkl. ai_assisted: true, ai_model: gemini-1.5-pro)
  7. Post in _drafts/YYYY-MM-DD-generierter-titel.md speichert
  8. Git commit + push
- Secrets: GEMINI_API_KEY, GITHUB_TOKEN
- Retry-Logik: 3 Versuche

Vollständige YAML.
" > .github/workflows/writer-agent.yml
```

### Workflow 3 — editor-agent

```bash
gemini --model gemini-1.5-pro "
Erstelle GitHub Actions Workflow YAML für einen editor-agent basierend auf best practices 02/2026.

Anforderungen:
- Trigger: push auf _drafts/** 
- Script:
  1. Geändertes File in _drafts/ identifizieren
  2. Gemini 2.5 Pro aufrufen mit context/agent-prompts/editor-v1.md + Post-Inhalt + blog-memory.json
  3. Prüft ai_assisted Flag: wenn nicht vorhanden, auf 'true' setzen (muss vom Mensch geprüft werden)
  4. Erstellt GitHub Pull Request mit:
     - Base: main
     - Head: editor/post-slug-DATUM
     - PR-Beschreibung: Zusammenfassung der editor-Kommentare
  5. Fügt Inline Review-Kommentare hinzu (GitHub Review API)
- Secrets: GEMINI_API_KEY, GITHUB_TOKEN
- Label wird automatisch auf PR gesetzt: 'editor-review'

Vollständige YAML.
" > .github/workflows/editor-agent.yml
```

### Workflow 4 — staging-agent

```bash
gemini --model gemini-1.5-pro "
Erstelle GitHub Actions Workflow YAML für einen staging-agent basierend auf best practices 02/2026.

Anforderungen:
- Trigger: pull_request (opened, synchronize) mit Label 'editor-review'
- Steps:
  1. Hugo installieren (binary download, Version als Variable)
  2. Hugo Build auf PR-Branch ausführen
  3. Pagefind Index bauen: npx pagefind --source public
  4. Auf GitHub Pages 'preview' Environment deployen (separate Branch oder subdirectory)
  5. Broken Links prüfen: htmlproofer oder lychee
  6. Lighthouse CI ausführen (Performance, Accessibility Score)
  7. PR-Kommentar mit:
     - Preview-URL
     - Lighthouse Scores
     - Broken Links (falls vorhanden)
- Auto-approve nach 48h wenn kein 'veto' Label: separate workflow oder timer

Vollständige YAML.
" > .github/workflows/staging-agent.yml
```

### Workflow 5 — publish-agent

```bash
gemini --model gemini-1.5-pro "
Erstelle GitHub Actions Workflow YAML für einen publish-agent basierend auf best practices 02/2026.

Anforderungen:
- Trigger: 
  A) pull_request merged (wenn PR aus editor-branch)
  B) schedule: täglich prüfen ob PR > 48h offen und kein 'veto' Label → auto-merge
- Steps bei Publish:
  1. Hugo production build (HUGO_ENV: production, minify: true)
  2. Pagefind Index bauen
  3. Deploy auf GitHub Pages (actions/deploy-pages@v4)
  4. sitemap.xml validieren
  5. Triggert distribution-agent und memory-agent via workflow_dispatch
- Secrets: GITHUB_TOKEN
- Fehler: Notification in ursprünglichem Issue

Vollständige YAML.
" > .github/workflows/publish-agent.yml
```

### Workflows 6-8 auf einen Schlag

```bash
# Distribution Agent:
gemini --model gemini-1.5-flash "
Erstelle GitHub Actions Workflow YAML für distribution-agent basierend auf best practices 02/2026.
Trigger: workflow_dispatch (vom publish-agent aufgerufen) mit input 'post_slug'.
Script: Liest veröffentlichten Post, ruft Gemini 2.5 Flash auf für:
1. Mastodon-Post (max 500 Zeichen, DE, 3 Hashtags)
2. LinkedIn-Post (300 Wörter, professionell)  
3. Newsletter-Teaser (150 Wörter)
Output: _distribution/YYYY-MM-DD-postslug.md mit allen drei Versionen.
Git commit + push. Secrets: GEMINI_API_KEY, GITHUB_TOKEN.
" > .github/workflows/distribution-agent.yml

# Memory Agent:
gemini --model gemini-1.5-flash "
GitHub Actions Workflow für memory-agent basierend auf best practices 02/2026.
Trigger: workflow_dispatch (vom publish-agent).
Script: 
1. Liest veröffentlichten Post Front Matter
2. Fügt Eintrag zu context/blog-memory.json hinzu (max 20 Posts, älteste raus)
3. Updated context/series-registry.json wenn Post zu einer Serie gehört
4. Prüft ob neue Tags in context/ontology.json fehlen → als 'proposed: true' hinzufügen
5. Bereinigt context/research-queue.json (genutzte Items markieren)
Git commit + push. Secrets: GITHUB_TOKEN.
" > .github/workflows/memory-agent.yml

# Rollback:
gemini --model gemini-1.5-flash "
GitHub Actions Workflow für rollback basierend auf best practices 02/2026.
Trigger: issues (labeled) - wenn Label mit 'rollback:' beginnt.
Script: Extrahiert Post-Slug aus Label-Name, findet Commit mit 'Publish: SLUG', führt git revert aus, pusht.
Secrets: GITHUB_TOKEN.
" > .github/workflows/rollback.yml
```

### Issue Template generieren

```bash
gemini --model gemini-1.5-flash "
Erstelle eine GitHub Issue Template YAML-Datei für neue Blog-Posts basierend auf best practices 02/2026.
Datei: .github/ISSUE_TEMPLATE/new-post.yml

Felder:
- title (required): Post-Titel
- series (optional): Serie-Name
- series_order (optional): Episode-Nummer  
- angle (required, textarea): Hauptthese des Posts
- language (required, dropdown): de / en / de+en
- sources (optional, textarea): Quellen-Links, DOIs
- target_publish (optional): Ziel-Veröffentlichungsdatum
- additional_notes (optional, textarea): Sonstige Hinweise

Labels automatisch setzen: write:
" > .github/ISSUE_TEMPLATE/new-post.yml
```

---

## 7. API-Keys konfigurieren

### Gemini API Key holen

1. Öffne [aistudio.google.com](https://aistudio.google.com)
2. Oben links: **Get API Key**
3. **Create API key** → Projekt wählen oder neu erstellen
4. Key kopieren und **sicher aufbewahren**

### Alle Keys in GitHub hinterlegen

```bash
# Mit GitHub CLI — komfortabel, kein Browser nötig:

gh secret set GEMINI_API_KEY
# → Einfügen, Enter

gh secret set SERPER_API_KEY
# → Von serper.dev Dashboard

gh secret set UNSPLASH_ACCESS_KEY
# → Von unsplash.com/developers

gh secret set BUTTONDOWN_API_KEY
# → Von buttondown.email → Settings → API Key

gh secret set FORMSPREE_ENDPOINT
# → Von formspree.io → dein Formular → Endpoint URL

# Prüfen ob alle gesetzt:
gh secret list
```

### Lokale .env für Entwicklung

```bash
# .env Datei (NIEMALS commiten!)
cat > .env << 'EOF'
GEMINI_API_KEY=dein_key_hier
SERPER_API_KEY=dein_key_hier
UNSPLASH_ACCESS_KEY=dein_key_hier
EOF

# .gitignore erweitern:
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

---

## 8. Frontend einrichten

### GitHub Pages aktivieren

```bash
# Leeren main-Branch initial pushen:
git add .
git commit -m "Initial setup"
git push origin main
```

Dann auf GitHub.com:
1. Repo → **Settings** → **Pages**
2. Source: **GitHub Actions** (nicht "Deploy from branch")
3. Das war's — GitHub Pages ist jetzt per Action steuerbar

### Giscus einrichten

```bash
# Giscus konfigurieren:
# 1. github.com/apps/giscus → Install → dein Repo auswählen
# 2. giscus.app → Repo eingeben → Konfiguration generieren
# 3. Script-Tag kopieren

# Partial erstellen (Gemini füllt den Template-Code):
gemini --model gemini-1.5-flash "
Erstelle layouts/partials/comments.html für Hugo mit Giscus.
Platzhalter für: REPO_OWNER, REPO_NAME, REPO_ID, CATEGORY_ID.
Theme: preferred_color_scheme (passt sich Dark/Light Mode an).
Mapping: pathname.
Nur HTML-Code, kein erklärender Text.
" > layouts/partials/comments.html
```

### AI-Disclosure Partial

```bash
cat > layouts/partials/ai-disclosure.html << 'HTMLEOF'
{{ if .Params.ai_assisted }}
{{ if eq .Params.ai_assisted "true" }}
<div class="ai-disclosure" style="font-size:0.85em; opacity:0.75; margin-top:2rem; padding:0.5rem; border-left:2px solid currentColor;">
  ✦ Dieser Artikel wurde mit KI-Unterstützung ({{ .Params.ai_model }}) erstellt und redaktionell geprüft. 
  <a href="/de/datenschutz/#ki-einsatz">Mehr erfahren</a>
</div>
{{ else if eq .Params.ai_assisted "partial" }}
<div class="ai-disclosure" style="font-size:0.85em; opacity:0.75; margin-top:2rem; padding:0.5rem; border-left:2px solid currentColor;">
  ✦ Teile dieses Artikels entstanden mit KI-Unterstützung.
</div>
{{ end }}
{{ end }}
HTMLEOF
```

### Structured Data Partial

```bash
gemini --model gemini-1.5-flash "
Erstelle layouts/partials/structured-data.html für Hugo.
JSON-LD Schema.org Article Markup.
Felder: headline (Title), datePublished, dateModified, author (Site.Params.author), publisher (Site.Title + Logo), description, ai_assisted als additionalProperty wenn vorhanden.
Nur HTML mit eingebettetem script-Tag, kein erklärender Text.
" > layouts/partials/structured-data.html
```

### Umami Analytics

```bash
cat > layouts/partials/analytics.html << 'HTMLEOF'
{{- if not .Site.IsServer -}}
<script defer 
  src="https://analytics.umami.is/script.js" 
  data-website-id="DEINE-UMAMI-WEBSITE-ID">
</script>
{{- end -}}
HTMLEOF
```

Registriere dich auf [umami.is](https://umami.is), füge deine Domain hinzu und trage die Website-ID ein.

### robots.txt

```bash
cat > static/robots.txt << 'EOF'
User-agent: *
Allow: /

# AI Training Opt-Out (optional aber empfehlenswert)
User-agent: GPTBot
Disallow: /
User-agent: Google-Extended
Disallow: /

Sitemap: https://yourdomain.com/sitemap.xml
EOF
```

---

## 9. Ersten Post durch die Pipeline jagen

### Alles committen und pushen

```bash
git add .
git status    # Prüfen was hinzugefügt wird

git commit -m "feat: initial blog setup with agent pipeline

- Hugo configuration with Blowfish theme
- 8 GitHub Actions workflows
- Context management system
- Frontend partials (Giscus, AI disclosure, Structured Data)
- Issue templates and label system"

git push origin main
```

### GitHub Actions prüfen

1. GitHub.com → Dein Repo → **Actions** Tab
2. Du solltest die Workflows sehen
3. Auf einen Workflow klicken → **Run workflow** (falls `workflow_dispatch`)

### Ersten Post manuell testen

```bash
# Direkt mit Gemini CLI einen Test-Post generieren:
gemini --model gemini-1.5-pro \
  --file context/system-identity.md \
  --file context/ontology.json \
  "
Schreibe einen vollständigen Blog-Post für einen deutschen Blog über Regenerative Wirtschaft.

Thema: Mykorrhiza-Netzwerke als Modell für dezentrale Wirtschaftssysteme

Anforderungen:
- 1.500-2.000 Wörter
- Hugo Front Matter am Anfang (title, date, draft: false, language: de, tags aus der ontology.json, ai_assisted: true, ai_model: gemini-1.5-pro, description)
- Wissenschaftlich fundiert aber zugänglich
- [VERIFY] Tags wo Fakten ohne Quelle
- Strukturiert mit H2 und H3 Überschriften
- Schlusssatz der zur nächsten Serie-Episode überleitet

Nur den Markdown-Post ausgeben, kein erklärender Text darum.
" > _drafts/$(date +%Y-%m-%d)-mykorrhiza-wirtschaft.md

# Post anschauen:
cat _drafts/$(date +%Y-%m-%d)-mykorrhiza-wirtschaft.md | head -50
```

### Lokale Vorschau des Posts

```bash
hugo server -D
# Browser: http://localhost:1313
# Du siehst den Draft-Post unter "Drafts"
```

### Test-Pipeline triggern

```bash
# Post committen → triggert editor-agent:
git add _drafts/
git commit -m "draft: mykorrhiza wirtschaft post [writer-agent-test]"
git push

# GitHub Actions Tab beobachten → editor-agent läuft
# Nach ein paar Minuten: Pull Request erscheint
```

### Ersten PR reviewen und mergen

```bash
# PRs anzeigen:
gh pr list

# PR im Detail ansehen:
gh pr view 1

# PR im Browser öffnen:
gh pr view 1 --web

# Staging-Preview-Link im PR-Kommentar finden
# Post prüfen, Kommentare lesen

# Wenn zufrieden — mergen:
gh pr merge 1 --merge
```

---

## 10. Troubleshooting

### Häufige Probleme und Lösungen

**Problem: Gemini API gibt Fehler 429 (Rate Limit)**
```bash
# In jedem Python-Script sicherstellen:
import time
import random

def call_gemini_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = call_gemini(prompt)
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time * 60)  # 60, 120, 240 Sekunden
            else:
                raise e
```

**Problem: Hugo Build schlägt fehl**
```bash
# Lokal debuggen:
hugo --verbose 2>&1 | head -50

# Häufigste Ursache: Ungültiges Front Matter YAML
# Prüfen:
cat _drafts/dein-post.md | head -20
# YAML-Syntax validieren: yamllint.com
```

**Problem: GitHub Actions hat keinen Schreibzugriff auf Repo**
```yaml
# In jeder workflow.yml unter 'permissions' hinzufügen:
permissions:
  contents: write
  pull-requests: write
  issues: write
```

**Problem: Gemini CLI findet keine Context-Dateien**
```bash
# Immer absolute oder relative Pfade prüfen:
ls -la context/     # Existieren die Dateien?

# Im GitHub Action: Working Directory prüfen:
- name: Debug
  run: ls -la && ls -la context/
```

**Problem: Hugo Page erscheint nicht auf GitHub Pages**
```bash
# baseURL in hugo.toml prüfen:
# Für username.github.io/repo-name: 
baseURL = "https://username.github.io/repo-name/"

# Für Custom Domain:
baseURL = "https://yourdomain.com/"

# CNAME File in static/ für Custom Domain:
echo "yourdomain.com" > static/CNAME
```

**Problem: Giscus Kommentare erscheinen nicht**
```bash
# Checklist:
# 1. GitHub Discussions im Repo aktiviert? → Repo Settings → Features
# 2. giscus App hat Zugriff auf Repo? → github.com/apps/giscus
# 3. REPO_ID und CATEGORY_ID im HTML korrekt?
# 4. Lokaler Hugo Server zeigt keine Giscus (nur auf Live-Site)
```

**Problem: GitHub Actions Minutes gehen aus**
```bash
# Verbrauch prüfen:
# GitHub.com → Settings → Billing → Actions

# Sparen durch:
# 1. research-agent auf 1× pro Woche reduzieren
# 2. Gemini Flash statt Pro wo möglich
# 3. Jobs mit 'if' conditions bedingt ausführen
```

### Gemini CLI Debug-Tricks

```bash
# Zeigt was gesendet wird (Verbose Mode):
GEMINI_DEBUG=true gemini "test"

# Token-Verbrauch schätzen (vor dem echten Call):
gemini --count-tokens --file context/system-identity.md "schreibe einen post über..."

# Modell-Verfügbarkeit prüfen:
gemini models list

# Interaktiver Chat zum Testen von Prompts:
gemini chat --model gemini-1.5-pro
# Dann context/system-identity.md inhalt pasten und testen
```

### Nützliche Gemini CLI One-Liner

```bash
# Post-Qualität prüfen:
gemini --file context/system-identity.md --file _drafts/mein-post.md \
  "Bewerte diesen Post auf einer Skala 1-10 für: Ton-Konsistenz, Fachlichkeit, Lesbarkeit, Originalität. Kurze Begründung jeweils."

# Tag-Vorschläge:
gemini --file context/ontology.json --file _drafts/mein-post.md \
  "Welche Tags aus der Ontologie passen zu diesem Post? Schlage maximal 5 vor."

# SEO-Beschreibung generieren:
gemini --file _drafts/mein-post.md \
  "Generiere eine SEO-Meta-Description für diesen Post. Maximal 160 Zeichen. Nur den Text, nichts anderes."

# Übersetzung EN:
gemini --model gemini-1.5-pro --file _drafts/mein-post-de.md \
  "Übersetze diesen deutschen Blog-Post ins Englische. Behalte den Stil, Überschriften, Front Matter (ändere language: en). Nur das übersetzte Markdown." \
  > content/en/posts/$(date +%Y-%m-%d)-translated-title.md

# Social Media Texte:
gemini --file content/de/posts/mein-post.md \
  "Schreibe: 1) Mastodon-Post (max 500 Zeichen, 3 Hashtags) 2) LinkedIn-Post (300 Wörter, professionell). Trenne mit '---'."
```

---

## Abschluss-Checkliste

### Vor dem ersten Live-Post:

- [ ] Hugo lokal gebaut und Vorschau funktioniert (`hugo server -D`)
- [ ] Alle 6 API Keys in GitHub Secrets hinterlegt (`gh secret list`)
- [ ] GitHub Pages aktiviert (Settings → Pages → GitHub Actions)
- [ ] GitHub Discussions aktiviert (für Giscus)
- [ ] `context/system-identity.md` personalisiert (nicht nur Gemini-Entwurf)
- [ ] `context/ontology.json` geprüft und angepasst
- [ ] Impressum und Datenschutzseite erstellt (manuell!)
- [ ] `baseURL` in `hugo.toml` korrekt gesetzt
- [ ] Ersten Test-Post durch lokale Vorschau geprüft
- [ ] Dependabot aktiviert (`.github/dependabot.yml` committed)
- [ ] `robots.txt` nach deinen Präferenzen angepasst

### Nach dem ersten Live-Post:

- [ ] GitHub Pages URL funktioniert
- [ ] AI-Disclosure im Footer sichtbar
- [ ] Giscus Kommentarfeld erscheint
- [ ] Pagefind Suche funktioniert
- [ ] RSS Feed erreichbar (yourdomain.com/index.xml)
- [ ] Sitemap korrekt (yourdomain.com/sitemap.xml)
- [ ] Google Search Console: Domain registrieren + Sitemap einreichen

---

*Playbook Version 1.0*  
*Gemini CLI: github.com/google-gemini/gemini-cli*  
*Bei Problemen: GitHub Issues oder Gemini CLI Dokumentation*
