# GitHub-Automated Blog: Regenerative Economy
## Vollständige Systemdokumentation

> **Nische:** Regenerative Wirtschaft & Ökosysteme — von Forschung bis Anwendung, von Tech bis Soil  
> **Vibe:** Natural Solarpunk × Avantgarde Prestige  
> **Stack:** Hugo · GitHub Actions · Gemini API · GitHub Pages  
> **Constraints:** Intel Celeron · 512MB RAM · Google AI Pro · GitHub Free Tier

---

## Inhaltsverzeichnis

1. [Architektur-Übersicht](#1-architektur-übersicht)
2. [Backend / Frontend Konzept](#2-backend--frontend-konzept)
3. [Repository-Struktur](#3-repository-struktur)
4. [Die 8 Agenten](#4-die-8-agenten)
5. [Context Management](#5-context-management)
6. [API-Keys & Secrets](#6-api-keys--secrets)
7. [Frontend-Konfiguration](#7-frontend-konfiguration)
8. [Compliance & Rechtliches](#8-compliance--rechtliches)
9. [Redaktions-Workflow](#9-redaktions-workflow)
10. [Ontologie & Tagging-System](#10-ontologie--tagging-system)
11. [Zweisprachigkeit](#11-zweisprachigkeit)
12. [Serien-Management](#12-serien-management)
13. [Rollback & Fehlerbehandlung](#13-rollback--fehlerbehandlung)
14. [Maintenance & Monitoring](#14-maintenance--monitoring)

---

## 1. Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────────┐
│                      LOKALES SETUP                              │
│  Antigravity IDE → Git Push / GitHub Issues erstellen           │
│  Hugo Binary (Vorschau: localhost:1313, ~30MB RAM)              │
│  Intel Celeron · 512MB RAM: nur Editor + Git benötigt ✓         │
└───────────────────────────┬─────────────────────────────────────┘
                            │  Push / Cron / Issue-Label-Trigger
┌───────────────────────────▼─────────────────────────────────────┐
│                   GITHUB ACTIONS (Cloud)                        │
│                Ubuntu Runner · 7GB RAM · kostenlos              │
│                                                                 │
│  [research] → [writer] → [editor] → [visual] → [staging]       │
│                                                       ↓         │
│  [memory] ← [distribution] ← [publish] ←─────────────┘         │
└───────────────────────────┬─────────────────────────────────────┘
                            │  Hugo Build → Deploy
┌───────────────────────────▼─────────────────────────────────────┐
│              GITHUB PAGES (Fastly CDN)                          │
│  yourdomain.com · HTTPS automatisch · Global CDN · kostenlos    │
│                                                                 │
│  Hugo Static Site                                               │
│  ├── Pagefind (Client-Side Suche)                               │
│  ├── Giscus (Kommentare via GitHub Discussions)                 │
│  ├── Formspree (Newsletter-Signup)                              │
│  └── Umami Analytics (cookielos, DSGVO-konform)                 │
└─────────────────────────────────────────────────────────────────┘
```

**Leitprinzip:** Git ist die Datenbank. GitHub Actions ist der Server. GitHub Pages ist das Hosting. Kein traditionelles Backend, kein VPS, keine monatlichen Serverkosten.

---

## 2. Backend / Frontend Konzept

### Warum kein klassisches Backend?

Für einen content-getriebenen Blog mit KI-Pipeline ist ein klassisches Backend (Node.js, Python Flask, Datenbank) nicht nur unnötig — es wäre aktiv hinderlich. Die gewählte Architektur bietet:

| Aspekt | Klassisches Backend | Diese Architektur |
|---|---|---|
| Kosten | VPS €5–20/Monat | €0/Monat |
| RAM-Anforderung lokal | Hoch (Server läuft lokal) | ~30MB (nur Hugo Preview) |
| Skalierung | Manuell | Automatisch (CDN) |
| Ausfallsicherheit | Abhängig vom VPS | GitHub SLA 99.9% |
| Versionierung | Zusätzlich nötig | Git ist bereits alles |
| Backup | Separat einrichten | Git = Backup |

### Hugo als Static Site Generator

Hugo ist ein einzelnes Binary (~15MB), kein Node.js, kein Ruby, kein Python. `hugo server` für lokale Vorschau benötigt ~30MB RAM — auf 512MB problemlos.

**Warum Hugo statt Jekyll oder Gatsby:**
- Jekyll: braucht Ruby + Gems → ~200MB RAM, fragile Dependency-Verwaltung
- Gatsby: braucht Node.js + npm → 300MB+ RAM, langsame Builds
- Hugo: ein Binary, Builds in <1 Sekunde, läuft auf jedem System

**Empfohlenes Theme:** [Blowfish](https://blowfish.page) oder [Congo](https://jpanther.github.io/congo/) — beide unterstützen i18n, Dark Mode, Series-Taxonomie und haben ein ästhetisch hochwertiges, anpassbares Design.

### Der "Backend-Ersatz-Stack"

```
Funktion          → Lösung              → Kosten
────────────────────────────────────────────────
Datenbank         → Git Repository      → €0
Server/Compute    → GitHub Actions      → €0 (2000 min/Monat)
Hosting/CDN       → GitHub Pages        → €0
Suche             → Pagefind            → €0 (client-side)
Kommentare        → Giscus              → €0
Newsletter        → Buttondown          → €0 (<100 Subscriber)
Forms             → Formspree           → €0 (<50 Einreichungen/Monat)
Analytics         → Umami (umami.is)    → €0 (hosted free tier)
KI-Generierung    → Gemini API          → Google AI Pro ✓
Bilder            → Gemini Imagen       → Google AI Pro ✓
Stock-Fotos       → Unsplash API        → €0 (50 req/h)
```

---

## 3. Repository-Struktur

```
your-blog/
│
├── .github/
│   ├── workflows/
│   │   ├── research-agent.yml       # Agent 1
│   │   ├── writer-agent.yml         # Agent 2
│   │   ├── editor-agent.yml         # Agent 3
│   │   ├── visual-agent.yml         # Agent 4
│   │   ├── staging-agent.yml        # Agent 5
│   │   ├── publish-agent.yml        # Agent 6
│   │   ├── distribution-agent.yml   # Agent 7
│   │   ├── memory-agent.yml         # Agent 8
│   │   ├── rollback.yml             # Rollback-Workflow
│   │   └── dependabot.yml           # Automatische Security-Updates
│   │
│   └── ISSUE_TEMPLATE/
│       └── new-post.yml             # Strukturiertes Post-Template
│
├── context/                         # KI-Gedächtnis (versioniert in Git)
│   ├── system-identity.md           # Layer 0: Persona, Vibe, Verbotenes
│   ├── blog-memory.json             # Layer 1: Letzte 20 Posts
│   ├── series-registry.json         # Layer 1b: Serien-Status
│   ├── ontology.json                # Layer 1c: Eigenes Tag-System
│   ├── research-queue.json          # Layer 2: Quellen-Pipeline
│   ├── visual-style-guide.md        # Layer 2b: Bild-Prompt-Bibliothek
│   └── agent-prompts/               # Versionierte Agent-Prompts
│       ├── research-v1.md
│       ├── writer-v1.md
│       ├── editor-v1.md
│       ├── visual-v1.md
│       └── distribution-v1.md
│
├── content/
│   ├── de/                          # Deutsche Inhalte
│   │   ├── posts/
│   │   ├── ueber-uns.md
│   │   ├── impressum.md
│   │   └── datenschutz.md
│   └── en/                          # Englische Inhalte
│       ├── posts/
│       └── about.md
│
├── _drafts/                         # Unveröffentlichte Entwürfe
│
├── _distribution/                   # Generierte Social-Media-Texte
│   └── YYYY-MM-DD-postname.md
│
├── assets/
│   └── images/
│       └── YYYY/
│           └── postname/            # Post-spezifische Bilder
│
├── static/
│   ├── robots.txt
│   └── favicon/
│
├── layouts/
│   └── partials/
│       ├── ai-disclosure.html       # KI-Kennzeichnung Footer
│       ├── structured-data.html     # JSON-LD für SEO
│       └── analytics.html           # Umami-Script
│
├── config/
│   ├── hugo.toml                    # Hugo-Konfiguration
│   └── languages.toml               # i18n-Konfiguration
│
└── README.md
```

---

## 4. Die 8 Agenten

### Agenten-Pipeline Übersicht

```
Trigger (Cron/Issue/Push)
        │
        ▼
  [1] research-agent
        │ research-queue.json
        ▼
  [2] writer-agent ◄── Auch: Dein eigener Text aus _drafts/
        │ _drafts/YYYY-MM-DD-titel.md
        ▼
  [3] editor-agent
        │ PR mit Inline-Kommentaren
        ▼
  [4] visual-agent
        │ assets/images/ + Alt-Texte
        ▼
  [5] staging-agent
        │ Preview-Deploy (du reviewst)
        ▼
  [6] publish-agent ◄── Trigger: Dein Merge ODER Auto nach 48h
        │ Live auf GitHub Pages
        ├── [7] distribution-agent → _distribution/*.md
        └── [8] memory-agent → context/*.json aktualisiert
```

---

### Agent 1 — `research-agent`

**Datei:** `.github/workflows/research-agent.yml`

**Trigger:**
- Cron: Montag + Donnerstag, 06:00 UTC
- Manuell: `workflow_dispatch`

**Quellen:**
- Arxiv API (Preprints, kostenlos)
- OpenAlex API (Open-Access Forschung, kostenlos)
- Semantic Scholar API (kostenlos)
- Serper.dev (Google Search, 2.500 req/Monat kostenlos)

**Gemini-Modell:** `gemini-1.5-flash` (schnell, kostengünstig für Massenverarbeitung)

**Aufgaben:**
1. Scrapt Quellen zu Themen aus `context/ontology.json`
2. Bewertet Relevanz für Nische (1–10 Score)
3. Fasst Kernaussagen zusammen
4. Flaggt unverifierbare Claims mit `[VERIFY]`
5. Kategorisiert nach Ontologie-Tags
6. Schreibt Ergebnisse in `context/research-queue.json`

**Halluzinations-Schutz:**
- Nur Quellen mit DOI, arXiv-ID oder verifizierbarer URL werden übernommen
- Alle Claims ohne Quellennachweis werden automatisch mit `[VERIFY]` markiert
- Agent gibt nie Fakten ohne Quelle aus

**Output-Format `research-queue.json`:**
```json
{
  "generated": "2025-01-15T06:00:00Z",
  "items": [
    {
      "id": "arxiv:2501.12345",
      "title": "Mycorrhizal Networks as Economic Infrastructure",
      "source_url": "https://arxiv.org/abs/2501.12345",
      "doi": "10.xxxx/xxxxx",
      "language": "en",
      "relevance_score": 8.5,
      "ontology_tags": ["mycelium-org", "systemic-finance"],
      "summary_de": "...",
      "summary_en": "...",
      "key_claims": ["...", "..."],
      "unverified_claims": ["[VERIFY] ..."]
    }
  ]
}
```

**Retry-Logik:** 3 Versuche mit 60s exponential backoff bei API-Fehlern.

---

### Agent 2 — `writer-agent`

**Datei:** `.github/workflows/writer-agent.yml`

**Trigger:**
- Nach Abschluss von `research-agent` (workflow_run)
- GitHub Issue mit Label `write:` (Issue-Titel = Post-Titel)
- Manuell: `workflow_dispatch` mit Parameter

**Gemini-Modell:** `gemini-1.5-pro` (höchste Qualität für Haupttext)

**Context-Eingabe (in dieser Reihenfolge):**
1. `context/system-identity.md` (Persona, Vibe)
2. `context/blog-memory.json` (Letzte Posts → keine Wiederholungen)
3. `context/series-registry.json` (Offene Serien prüfen)
4. `context/ontology.json` (Tag-System)
5. Relevante Items aus `context/research-queue.json`

**Aufgaben:**
1. Prüft `series-registry.json` auf offene Serien → schlägt Fortsetzung vor
2. Schreibt Langform-Artikel (1.500–3.000 Wörter) in Ziel-Sprache
3. Generiert Hugo Front Matter vollständig
4. Setzt `ai_assisted: true` im Front Matter
5. Integriert `[VERIFY]`-Tags für nicht belegte Claims
6. Legt Draft in `_drafts/YYYY-MM-DD-titel.md` ab

**Hinweis — Deine eigenen Texte:**
Wenn du selbst schreibst, commitest du dein `.md` direkt in `_drafts/`. Der editor-agent erkennt dies und setzt `ai_assisted: false` oder `ai_assisted: partial`. Alle Folge-Agenten (editor, visual, staging, publish) laufen identisch durch — du bekommst dieselbe Qualitätssicherung.

**Hugo Front Matter Template:**
```yaml
---
title: "Titel des Posts"
date: 2025-01-15
draft: false
language: "de"
series: "Mykorrhiza & DAOs"
series_order: 2
tags: ["mycelium-org", "systemic-finance", "soil-tech"]
categories: ["Forschung", "Systemik"]
ai_assisted: true          # true | false | partial
ai_model: "gemini-1.5-pro"
sources:
  - url: "https://arxiv.org/abs/2501.12345"
    doi: "10.xxxx/xxxxx"
description: "SEO-Beschreibung (150–160 Zeichen)"
---
```

---

### Agent 3 — `editor-agent`

**Datei:** `.github/workflows/editor-agent.yml`

**Trigger:** Neues oder geändertes File in `_drafts/` (push)

**Gemini-Modell:** `gemini-1.5-pro`

**Persona:** "Wissenschaftlicher Redakteur trifft Avantgarde-Lektor" — präzise, keine akademische Trockenheit, kohärent mit der Nischen-Stimme.

**Aufgaben:**
1. Prüft Ton-Konsistenz mit `context/system-identity.md`
2. Hebt alle `[VERIFY]`-Tags hervor und kommentiert
3. Prüft interne Konsistenz (widerspricht der Post früheren Posts?)
4. Setzt EU AI Act konforme Kennzeichnung im Front Matter
5. DSGVO-Check: Keine personenbezogenen Daten ohne Kontext
6. Prüft, ob Tags der `context/ontology.json` entsprechen
7. Öffnet GitHub Pull Request mit Inline-Kommentaren

**Output:** GitHub PR mit:
- Inline-Kommentaren zu Schwachstellen
- Zusammenfassung der `[VERIFY]`-Tags
- Empfehlung: `approved` / `needs-revision`

---

### Agent 4 — `visual-agent`

**Datei:** `.github/workflows/visual-agent.yml`

**Trigger:** Nach editor-agent (workflow_run bei PR-Erstellung)

**Gemini-Modell:** `gemini-1.5-pro` (für Prompt-Generierung) + Imagen API (für Bildgenerierung)

**Bild-Quellen (Priorität):**
1. Gemini Imagen (in Google AI Pro enthalten) → KI-generiert, kein Copyright
2. Unsplash API → kostenlos, automatische Attribution

**Aufgaben:**
1. Liest Post-Inhalt und extrahiert visuelle Kernthemen
2. Konsultiert `context/visual-style-guide.md` für Stil-Konsistenz
3. Generiert Imagen-Prompts passend zu "natural solarpunk × Avantgarde prestige"
4. Erstellt Hero-Image + 1–2 Inline-Illustrationen
5. Konvertiert alle Bilder zu WebP (optimiert) mit AVIF-Fallback
6. Generiert Alt-Texte automatisch (Accessibility + SEO)
7. Legt Bilder in `assets/images/YYYY/postname/` ab
8. Fügt Bild-Referenzen in den Draft ein

**Attribution:** Unsplash-Bilder bekommen automatisch Credit-Footer im Post.

**`context/visual-style-guide.md` enthält:**
- Referenz-Prompts für die Nische (Erde, Myzel, Kreislauf, Technologie-Natur-Hybride)
- Verbotene Ästhetiken (Corporate Flat Design, Generic Tech)
- Farb-Paletten und Kompositions-Hinweise
- Versionierte Prompt-Templates

---

### Agent 5 — `staging-agent`

**Datei:** `.github/workflows/staging-agent.yml`

**Trigger:** PR-Erstellung durch editor-agent

**Aufgaben:**
1. Checkt PR-Branch aus
2. Führt Hugo Build durch (production settings)
3. Deployt auf `preview`-Branch → `yourdomain.com/preview/postname`
4. Führt Lighthouse CI durch (Core Web Vitals)
5. Prüft Broken Links (interne + externe)
6. Kommentiert Ergebnisse in den PR

**Du reviewst:** Der Staging-Preview-Link wird automatisch als PR-Kommentar gepostet. Du siehst den Post live, bevor er veröffentlicht wird.

**Auto-Publish Logik:** Wenn du nach 48h kein `veto`-Label auf den PR gesetzt hast, merged `publish-agent` automatisch.

---

### Agent 6 — `publish-agent`

**Datei:** `.github/workflows/publish-agent.yml`

**Trigger:**
- Du mergst den PR manuell
- Auto-Merge nach 48h (wenn kein `veto`-Label)

**Aufgaben:**
1. Merged PR in `main`
2. Hugo Production Build (minified HTML/CSS/JS)
3. Pagefind-Index rebuild (Suche aktualisieren)
4. Deployt auf GitHub Pages
5. Aktualisiert `sitemap.xml`
6. Aktualisiert `feed.xml` (RSS)
7. Triggert distribution-agent und memory-agent

---

### Agent 7 — `distribution-agent`

**Datei:** `.github/workflows/distribution-agent.yml`

**Trigger:** Nach publish-agent (workflow_run)

**Gemini-Modell:** `gemini-1.5-flash`

**Aufgaben:**
Generiert plattformspezifische Texte für manuelles Posting:

1. **Mastodon** (max. 500 Zeichen) — nüchtern, fachlich, mit Hashtags
2. **LinkedIn** (300–500 Wörter) — professioneller Ton, Handlungsrelevanz
3. **Newsletter-Teaser** (150 Wörter) — Neugier wecken, zum Blog führen
4. **RSS** wird automatisch aktualisiert → Buttondown verschickt Newsletter ohne API-Call

**Output:** `_distribution/YYYY-MM-DD-postname.md` mit allen Plattform-Texten. Du öffnest die Datei, kopierst und postest manuell. Kein Social-API-Account nötig.

---

### Agent 8 — `memory-agent`

**Datei:** `.github/workflows/memory-agent.yml`

**Trigger:** Nach publish-agent (workflow_run)

**Gemini-Modell:** `gemini-1.5-flash`

**Aufgaben:**
1. Fügt veröffentlichten Post zu `context/blog-memory.json` hinzu
2. Aktualisiert Serien-Status in `context/series-registry.json`
3. Erweitert `context/ontology.json` bei neuen Tags (mit Vorschlag-Flag)
4. Bereinigt veraltete Items aus `context/research-queue.json`
5. Committet alle Änderungen in `context/`

**Warum das wichtig ist:** Ohne memory-agent weiß der writer-agent nicht, was bereits veröffentlicht wurde. Er würde Themen wiederholen, Serien vergessen und die Ontologie ignorieren. Der memory-agent ist das Langzeit-Gedächtnis des Systems.

---

## 5. Context Management

### Layered Context Architecture

```
Layer 0 — SYSTEM IDENTITY (persistent, ~800 tokens)
  Wer ist der Blog? Was ist verboten? Was ist der Ton?
  Datei: context/system-identity.md

Layer 1 — BLOG MEMORY (rolling, ~2.000 tokens)
  Letzte 20 Posts: Titel, Kernthesen, Tags
  Dateien: blog-memory.json · series-registry.json · ontology.json

Layer 2 — TASK CONTEXT (pro Agent, ~1.500 tokens)
  Aktueller Auftrag + relevante Quellen
  Dateien: research-queue.json · visual-style-guide.md

Layer 3 — WORKING MEMORY (ephemeral)
  Generierungsprozess des aktuellen Agenten
```

**Warum kein RAG / Vektordatenbank?**  
Gemini 1.5 Pro hat 2 Millionen Token Kontextfenster. Der gesamte `context/`-Ordner + der aktuelle Post passen problemlos hinein. RAG (Retrieval-Augmented Generation) wäre bei diesem Scale übertrieben und würde Komplexität ohne Mehrwert hinzufügen.

### `context/system-identity.md` — Beispielstruktur

```markdown
# Blog Identity

## Wer wir sind
Dieser Blog dokumentiert die Schnittstelle zwischen regenerativer Wirtschaft,
Ökosystem-Forschung und technologischer Innovation. Wir verbinden Soil Science
mit Systemtheorie, Mykologie mit DAOs, Permakultur mit Circular Finance.

## Ton und Stimme
- Präzise, aber nie akademisch-trocken
- Poetische Metaphern sind willkommen, wenn sie erhellen, nicht verschleiern
- Keine Corporate-Sprache, keine Buzzword-Anhäufung
- Deutsch und Englisch gleichwertig — kein Anglizismus-Overload im Deutschen

## Verbotenes
- Keine spekulativen Investments empfehlen
- Keine nicht verifizierten wissenschaftlichen Claims ohne [VERIFY]-Flag
- Kein Greenwashing — wenn etwas nicht regenerativ ist, sagen wir es
- Kein AI-Hype ohne kritische Reflexion

## Zielgruppe
Wissenschaftler:innen, Unternehmer:innen, Designer:innen, Aktivist:innen — 
alle, die zwischen Theorie und Praxis operieren und anspruchsvolle Lektüre schätzen.
```

### Prompt-Versionierung

Alle Agent-Prompts liegen als Markdown-Dateien in `context/agent-prompts/`. Git-History ist automatisch die Versionsgeschichte. Wenn ein Agent schlechter wird, reicht `git revert` auf die Prompt-Datei.

```bash
# Prompt-Version zurücksetzen
git log context/agent-prompts/writer-v1.md
git revert <commit-hash>
```

---

## 6. API-Keys & Secrets

### Übersicht aller benötigten Keys

| Variable | Service | Wo erstellen | Kosten |
|---|---|---|---|
| `GEMINI_API_KEY` | Gemini API | aistudio.google.com | Im Google AI Pro Abo |
| `GITHUB_TOKEN` | GitHub Actions | Automatisch verfügbar | Kostenlos |
| `UNSPLASH_ACCESS_KEY` | Unsplash Fotos | unsplash.com/developers | Kostenlos (50 req/h) |
| `SERPER_API_KEY` | Google Search | serper.dev | 2.500 free/Monat |
| `FORMSPREE_ENDPOINT` | Kontaktformular | formspree.io | Kostenlos (<50/Monat) |
| `BUTTONDOWN_API_KEY` | Newsletter | buttondown.email | Kostenlos (<100 Subscriber) |

### Keys in GitHub hinterlegen

1. Repo → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. Name und Value eintragen

**Wichtig:** `GITHUB_TOKEN` ist automatisch verfügbar in allen Actions. Du musst ihn nicht manuell hinterlegen — nur in der Workflow-YAML referenzieren: `${{ secrets.GITHUB_TOKEN }}`.

### Gemini-Modell-Strategie

Nicht alle Agenten brauchen dasselbe Modell:

```
gemini-1.5-pro    → writer-agent, editor-agent (Qualität > Geschwindigkeit)
gemini-1.5-flash  → research-agent, distribution-agent, memory-agent (Effizienz)
gemini-imagen     → visual-agent (Bildgenerierung, in Google AI Pro)
```

**Rate Limit Schutz:** Alle API-Calls haben Retry-Logik:
```yaml
# In jeder workflow YAML:
- name: Call Gemini API with retry
  uses: nick-fields/retry@v2
  with:
    timeout_minutes: 5
    max_attempts: 3
    retry_wait_seconds: 60
    command: python scripts/call_gemini.py
```

---

## 7. Frontend-Konfiguration

### Hugo Basis-Konfiguration

**`config/hugo.toml`:**
```toml
baseURL = "https://yourdomain.com"
title = "Blog-Name"
defaultContentLanguage = "de"
defaultContentLanguageInSubdir = false

[params]
  description = "Regenerative Wirtschaft & Ökosysteme"
  author = "Dein Name"
  
[taxonomies]
  tag = "tags"
  category = "categories"
  series = "series"

[outputs]
  home = ["HTML", "RSS", "JSON"]  # JSON für Pagefind-Suche
```

### Pagefind — Client-Side Suche

Pagefind wird automatisch nach jedem Hugo-Build generiert. Keine externe API, kein Algolia, kein Server.

```yaml
# In publish-agent.yml nach Hugo Build:
- name: Build Pagefind index
  run: npx pagefind --source public --bundle-dir pagefind
```

```html
<!-- In Hugo Template einbinden: -->
<link href="/pagefind/pagefind-ui.css" rel="stylesheet">
<script src="/pagefind/pagefind-ui.js"></script>
<div id="search"></div>
<script>
  new PagefindUI({ element: "#search", showSubResults: true });
</script>
```

### Giscus — Kommentarsystem

Giscus nutzt GitHub Discussions als Kommentar-Backend. Voraussetzung: Discussions im Repo aktivieren.

1. [giscus.app](https://giscus.app) besuchen
2. Repo auswählen → Konfiguration generieren
3. Script-Tag in Hugo-Partial einbinden

```html
<!-- layouts/partials/comments.html -->
<script src="https://giscus.app/client.js"
  data-repo="username/repo"
  data-repo-id="REPO_ID"
  data-category="Announcements"
  data-category-id="CATEGORY_ID"
  data-mapping="pathname"
  data-theme="preferred_color_scheme"
  crossorigin="anonymous"
  async>
</script>
```

### AI-Disclosure Partial

```html
<!-- layouts/partials/ai-disclosure.html -->
{{ if .Params.ai_assisted }}
  {{ if eq .Params.ai_assisted "true" }}
    <div class="ai-disclosure">
      ✦ Dieser Artikel wurde mit KI-Unterstützung ({{ .Params.ai_model }}) erstellt 
      und redaktionell geprüft. <a href="/datenschutz#ki">Mehr erfahren</a>
    </div>
  {{ else if eq .Params.ai_assisted "partial" }}
    <div class="ai-disclosure">
      ✦ Teile dieses Artikels wurden mit KI-Unterstützung erstellt.
    </div>
  {{ end }}
{{ end }}
```

### Structured Data / JSON-LD

```html
<!-- layouts/partials/structured-data.html -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ .Title }}",
  "datePublished": "{{ .Date.Format "2006-01-02" }}",
  "author": {"@type": "Person", "name": "{{ .Site.Params.author }}"},
  "publisher": {
    "@type": "Organization",
    "name": "{{ .Site.Title }}"
  }{{ if .Params.ai_assisted }},
  "additionalProperty": {
    "@type": "PropertyValue",
    "name": "ai-assisted",
    "value": "{{ .Params.ai_assisted }}"
  }{{ end }}
}
</script>
```

---

## 8. Compliance & Rechtliches

### EU AI Act — KI-Kennzeichnung

**Stand 2025:** Der EU AI Act verlangt Kennzeichnung von KI-generiertem Content, der für die Öffentlichkeit bestimmt ist. Das System setzt dies automatisch um:

1. `ai_assisted` Feld im Front Matter (gesetzt by editor-agent)
2. `ai-disclosure.html` Partial im Footer jedes Posts
3. Datenschutzseite erklärt den KI-Einsatz

### DSGVO-Checkliste

| Punkt | Lösung | Status |
|---|---|---|
| Analytics | Umami (cookielos, DSGVO-konform) | ✓ |
| Kommentare | Giscus (GitHub-Login, kein Tracking) | ✓ |
| Newsletter | Buttondown (DSGVO-konform, EU-Server wählbar) | ✓ |
| Kontaktform | Formspree (EU-Server Option) | ✓ |
| CDN | GitHub Pages / Fastly | Datenschutz prüfen |
| Impressum | Statische Seite `content/de/impressum.md` | Manuell erstellen |
| Datenschutzerklärung | `content/de/datenschutz.md` | Manuell erstellen |

### Impressum & Datenschutz

Diese Seiten musst du manuell als statische Hugo-Seiten anlegen (`content/de/impressum.md` und `content/de/datenschutz.md`). Sie liegen außerhalb der Agenten-Pipeline — kein Agent bearbeitet rechtliche Seiten.

---

## 9. Redaktions-Workflow

### GitHub Issues als Redaktionskalender

**Issue-Template `.github/ISSUE_TEMPLATE/new-post.yml`:**
```yaml
name: Neuer Post
description: Post für die Agenten-Pipeline einreichen
title: "[POST] "
labels: ["write:"]
body:
  - type: input
    id: title
    attributes:
      label: Titel
      placeholder: "Mykorrhiza als Finanzinfrastruktur"
    validations:
      required: true
  - type: input
    id: series
    attributes:
      label: Serie (optional)
      placeholder: "Mykorrhiza & DAOs"
  - type: textarea
    id: angle
    attributes:
      label: Angle / These
      placeholder: "Hauptargument des Posts"
  - type: textarea
    id: sources
    attributes:
      label: Quellen (optional)
      placeholder: "arXiv-Links, DOIs, URLs"
  - type: dropdown
    id: language
    attributes:
      label: Sprache
      options: ["de", "en", "de+en"]
```

### Labels-System

```
write:         → Startet writer-agent
research:      → Startet nur research-agent
approved:      → Manuell: Post ist für Publish freigegeben
veto:          → Verhindert Auto-Publish nach 48h
rollback:      → Triggert Rollback-Workflow
translate:     → Startet Übersetzungs-Pipeline
```

### Milestones = Editonsplanung

Erstelle Milestones für jeden Monat (`Januar 2025`, `Februar 2025`) und weise Issues den entsprechenden Milestones zu. Du hast einen vollständigen Redaktionskalender ohne zusätzliches Tool.

### Ablauf eines typischen Posts

```
Tag 0:  Du erstellst Issue mit Label "write:" + Titel + These
Tag 1:  research-agent sammelt Quellen (oder nutzt vorhandene Queue)
Tag 1:  writer-agent schreibt Draft → legt in _drafts/ ab
Tag 1:  editor-agent prüft → öffnet PR mit Kommentaren
Tag 1:  visual-agent generiert Bilder → fügt in PR ein
Tag 1:  staging-agent deployt Preview → du erhältst Link
Tag 2:  Du siehst Preview, liest Kommentare, mergst PR (oder setzt "veto")
Tag 2:  publish-agent deployt → Post ist live
Tag 2:  distribution-agent generiert Social-Texte → du postest manuell
Tag 2:  memory-agent aktualisiert Kontext → System "erinnert" sich
```

---

## 10. Ontologie & Tagging-System

### Warum eine eigene Ontologie?

Standard-Tags wie `sustainability`, `economy`, `technology` sind zu generisch und beschreiben nicht die spezifische Nische. Die eigene Ontologie verbindet "Soil" mit "Code", "Forschung" mit "Anwendung".

### `context/ontology.json` — Startstruktur

```json
{
  "version": "1.0",
  "last_updated": "2025-01-15",
  "domains": {
    "biological-systems": {
      "tags": ["mycelium-org", "soil-carbon", "rhizosphere", "biodiversity-econ"],
      "description": "Biologische Systeme als wirtschaftliche Infrastruktur"
    },
    "economic-systems": {
      "tags": ["circular-material", "systemic-finance", "commons-governance", "doughnut-econ"],
      "description": "Alternative Wirtschaftsmodelle und -theorien"
    },
    "technology-interfaces": {
      "tags": ["soil-tech", "biodigital", "open-source-regen", "sensor-ecology"],
      "description": "Technologie an der Grenze zu natürlichen Systemen"
    },
    "practice-application": {
      "tags": ["regenerative-agriculture", "urban-regen", "circular-design", "bio-materials"],
      "description": "Anwendbare Praktiken und Fallstudien"
    },
    "research-theory": {
      "tags": ["systems-thinking", "complexity-econ", "biomimicry-theory", "post-growth"],
      "description": "Theoretische Grundlagen und Forschungsfelder"
    }
  },
  "cross-domain-tags": ["solarpunk-vision", "avantgarde-praxis", "bridge-research"]
}
```

### Ontologie-Governance

Der memory-agent schlägt neue Tags mit Flag `proposed: true` vor. Du entscheidest bei deinem nächsten Repo-Review, ob der Tag in die Ontologie aufgenommen wird. Kein automatischer Wildwuchs.

---

## 11. Zweisprachigkeit

### Hugo i18n-Konfiguration

```toml
# config/languages.toml
[languages]
  [languages.de]
    languageName = "Deutsch"
    contentDir = "content/de"
    weight = 1
    [languages.de.params]
      description = "Regenerative Wirtschaft & Ökosysteme"
  [languages.en]
    languageName = "English"
    contentDir = "content/en"
    weight = 2
    [languages.en.params]
      description = "Regenerative Economy & Ecosystems"
```

### Übersetzungs-Pipeline

**Trigger:** Issue-Label `translate:` auf einem bestehenden Post-Issue

**Ablauf:**
1. writer-agent schreibt primär in Ziel-Sprache (aus Issue-Parameter)
2. `translation-agent` (Zusatz-Step in writer-agent.yml) übersetzt in zweite Sprache
3. editor-agent prüft beide Versionen
4. Beide landen als separate Dateien in `content/de/` und `content/en/`
5. Hugo verlinkt sie automatisch als Sprachversionen

**Wann übersetzen:**
- Forschungs-Posts: immer EN (internationale Reichweite)
- Praxis-Posts: primär DE, optional EN
- Grundlagen-Posts: beide Sprachen von Anfang an

---

## 12. Serien-Management

### `context/series-registry.json`

```json
{
  "series": [
    {
      "id": "mycelium-daos",
      "title_de": "Mykorrhiza & DAOs",
      "title_en": "Mycorrhiza & DAOs",
      "description": "6-teilige Serie über biologische Netzwerke als Vorlage für dezentrale Organisationen",
      "total_planned": 6,
      "published": [
        {"order": 1, "slug": "2025-01-10-mycelium-networks-intro", "date": "2025-01-10"},
        {"order": 2, "slug": "2025-01-20-dao-governance-soil", "date": "2025-01-20"}
      ],
      "next_episode": {
        "order": 3,
        "working_title": "Nährstoffflüsse als Token-Flows",
        "status": "planned"
      }
    }
  ]
}
```

### Serien-Continuity im writer-agent

Der writer-agent liest `series-registry.json` und berücksichtigt:
- Welche Argumente wurden in früheren Episoden bereits gemacht?
- Wo wurde die Narration unterbrochen?
- Welche Quellen wurden bereits genutzt?

Dadurch entsteht echte inhaltliche Kontinuität über Monate hinweg.

---

## 13. Rollback & Fehlerbehandlung

### Rollback eines Posts

```yaml
# .github/workflows/rollback.yml
name: Rollback Post
on:
  issues:
    types: [labeled]
jobs:
  rollback:
    if: startsWith(github.event.label.name, 'rollback:')
    runs-on: ubuntu-latest
    steps:
      - name: Extract post slug
        run: echo "SLUG=${{ github.event.label.name | replace('rollback:', '') }}" >> $GITHUB_ENV
      - name: Revert post commit
        run: |
          git log --grep="Publish: ${{ env.SLUG }}" --format="%H" | head -1 | xargs git revert --no-commit
          git commit -m "Rollback: ${{ env.SLUG }}"
          git push
```

**Nutzung:** Issue-Label `rollback:2025-01-20-dao-governance-soil` → Post wird automatisch zurückgezogen.

### Fehlerbehandlung in Actions

Alle Agenten senden bei Fehlern eine GitHub Actions Notification und erstellen einen Issue-Kommentar:

```yaml
- name: Notify on failure
  if: failure()
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '❌ Agent fehlgeschlagen. Logs: ' + context.runId
      })
```

### Dependabot für Security-Updates

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

Dependabot hält alle GitHub Actions automatisch auf dem aktuellen Stand — verhindert Security-Lücken durch veraltete Action-Versionen.

---

## 14. Maintenance & Monitoring

### Monatliche Routine (< 30 Minuten)

1. **Ontologie-Review:** Prüfe `context/ontology.json` auf `proposed: true` Tags → bestätigen oder ablehnen
2. **Prompt-Review:** Lies letzte 3 Posts kritisch → passe `context/agent-prompts/writer-v1.md` an falls nötig
3. **Memory-Review:** Öffne `context/blog-memory.json` → prüfe ob Zusammenfassungen stimmen
4. **Action-Minutes:** GitHub → Settings → Billing → prüfe Verbrauch (Limit: 2.000 min/Monat)
5. **Serper-Quota:** serper.dev Dashboard → verbleibende Anfragen prüfen

### GitHub Actions Minuten-Budget

| Agent | Frequenz | Geschätzte Dauer | Monatlich |
|---|---|---|---|
| research-agent | 2× pro Woche | ~5 min | ~40 min |
| writer-agent | 4× pro Monat | ~8 min | ~32 min |
| editor-agent | 4× pro Monat | ~5 min | ~20 min |
| visual-agent | 4× pro Monat | ~10 min | ~40 min |
| staging-agent | 4× pro Monat | ~5 min | ~20 min |
| publish-agent | 4× pro Monat | ~3 min | ~12 min |
| distribution-agent | 4× pro Monat | ~3 min | ~12 min |
| memory-agent | 4× pro Monat | ~2 min | ~8 min |
| **Gesamt** | | | **~184 min** |

Budget: 2.000 min/Monat → ~10× Spielraum. Bei höherer Posting-Frequenz noch kein Problem.

### Lokale Vorschau

```bash
# Hugo installieren (einmalig)
# → https://gohugo.io/installation/ → Binary herunterladen, in PATH legen

# Blog-Repo klonen
git clone https://github.com/username/your-blog

# Lokale Vorschau starten
cd your-blog
hugo server -D    # -D zeigt auch Drafts

# Browser: http://localhost:1313
# RAM-Verbrauch: ~30MB ✓ für 512MB System
```

---

*Dokumentation Version 1.0 — Erstellt für: Regenerative Economy Blog*  
*Stack: Hugo · GitHub Actions · Gemini API · GitHub Pages*  
*Lizenz: Verwende und adaptiere frei für dein Projekt*
