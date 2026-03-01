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
4. [Die 10 Agenten](#4-die-10-agenten)
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
│  [research] → [writer] → [image] → [editor] → [visual] → [designer] → [staging]  │
│                                                                         ↓         │
│  [memory] ← [distribution] ← [publish] ←───────────────────────────────┘         │
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
│   │   ├── image-agent.yml          # Agent 3
│   │   ├── editor-agent.yml         # Agent 4
│   │   ├── visual-agent.yml         # Agent 5
│   │   ├── staging-agent.yml        # Agent 7 (Designer integrated as Agent 6)
│   │   ├── publish-agent.yml        # Agent 8
│   │   ├── distribution-agent.yml   # Agent 9
│   │   ├── memory-agent.yml         # Agent 10
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
│       ├── image-v1.md
│       ├── editor-v1.md
│       ├── visual-v1.md
│       ├── designer-v1.md
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

## 4. Die 10 Agenten

Detailed Standard Operating Procedures (SOPs) for each agent can be found in the [`.planning/SOPs/`](./.planning/SOPs/) directory.

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
  [3] image-agent
        │ assets/images/ (Diagramme)
        ▼
  [4] editor-agent
        │ PR mit Inline-Kommentaren
        ▼
  [5] visual-agent
        │ assets/images/ (Hero) + Alt-Texte
        ▼
  [6] designer-agent
        │ Design-Compliance Report
        ▼
  [7] staging-agent
        │ Preview-Deploy (du reviewst)
        ▼
  [8] publish-agent ◄── Trigger: Dein Merge ODER Auto nach 48h
        │ Live auf GitHub Pages
        ├── [9] distribution-agent → _distribution/*.md
        └── [10] memory-agent → context/*.json aktualisiert
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

---

### Agent 2 — `writer-agent`

**Datei:** `.github/workflows/writer-agent.yml`

**Trigger:**
- Nach Abschluss von `research-agent` (workflow_run)
- GitHub Issue mit Label `write:` (Issue-Titel = Post-Titel)
- Manuell: `workflow_dispatch` mit Parameter

**Gemini-Modell:** `gemini-1.5-pro` (höchste Qualität für Haupttext)

**Aufgaben:**
1. Prüft `series-registry.json` auf offene Serien → schlägt Fortsetzung vor
2. Schreibt Langform-Artikel (1.500–3.000 Wörter) in Ziel-Sprache
3. Generiert Hugo Front Matter vollständig
4. Setzt `ai_assisted: true` im Front Matter
5. Integriert `[VERIFY]`-Tags für nicht belegte Claims
6. Flaggt technische Daten für den `image-agent` mit `[DIAGRAM: ...]`
7. Legt Draft in `_drafts/YYYY-MM-DD-titel.md` ab

---

### Agent 3 — `image-agent`

**Datei:** `.github/workflows/image-agent.yml`

**Trigger:** Nach Abschluss von `writer-agent` (workflow_run)

**Gemini-Modell:** `gemini-3.1-flash-image-preview`

**Aufgaben:**
1. Extrahiert technische Daten (ROI, Prozentwerte, System-Beziehungen) aus dem Draft und der research-queue.
2. Generiert hochpräzise 4K-Diagramme und Infografiken im "Organic Precision" Stil.
3. Nutzt `thinking_level: HIGH` für optimale Platzierung von Beschriftungen.
4. Speichert WebP-Assets in `assets/images/YYYY/postname/`.
5. Fügt Diagramm-Referenzen (`![Diagramm](...)`) automatisch in den Markdown-Draft ein.

---

### Agent 4 — `editor-agent`

**Datei:** `.github/workflows/editor-agent.yml`

**Trigger:** Push auf `_drafts/**` (inkl. Commits von `image-agent`)

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

---

### Agent 5 — `visual-agent`

**Datei:** `.github/workflows/visual-agent.yml`

**Trigger:** Nach editor-agent (workflow_run bei PR-Erstellung)

**Gemini-Modell:** `gemini-1.5-pro` (für Prompt-Generierung) + Imagen API (für Bildgenerierung)

**Aufgaben:**
1. Liest Post-Inhalt und extrahiert visuelle Kernthemen
2. Konsultiert `context/visual-style-guide.md` für Stil-Konsistenz
3. Generiert Hero-Image + 1–2 Inline-Illustrationen (künstlerisch)
4. Konvertiert alle Bilder zu WebP (optimiert)
5. Generiert Alt-Texte automatisch
6. Legt Bilder in `assets/images/YYYY/postname/` ab

---

### Agent 6 — `designer-agent`

**Datei:** Integriert in `staging-agent.yml`

**Trigger:** PR-Erstellung / Staging-Phase

**Aufgaben:**
1. Prüft Layout und Typografie gegen **ReNatureForce Brand Guidelines v4.0**.
2. Validiert die Einhaltung der Fibonacci-Skala für Abstände und φ-Proportionen.
3. Überwacht die Farbratios (60/30/10) im Front Matter.
4. Flaggt verbotene Begriffe (z.B. "Solarpunk" in externen Texten).
5. Erstellt einen detaillierten Compliance-Report als PR-Kommentar.

---

### Agent 7 — `staging-agent`

**Datei:** `.github/workflows/staging-agent.yml`

**Trigger:** PR-Erstellung durch editor-agent

**Aufgaben:**
1. Checkt PR-Branch aus
2. Führt Hugo Build durch
3. Deployt auf `preview`-Branch
4. Führt Lighthouse CI durch
5. Integriert den Report von `designer-agent` in den PR-Kommentar.

---

### Agent 8 — `publish-agent`

**Datei:** `.github/workflows/publish-agent.yml`

**Trigger:** Dein Merge ODER Auto-Merge nach 48h

**Aufgaben:**
1. Merged PR in `main`
2. Hugo Production Build
3. Deployt auf GitHub Pages
4. Triggert distribution-agent und memory-agent

---

### Agent 9 — `distribution-agent`

**Datei:** `.github/workflows/distribution-agent.yml`

**Trigger:** Nach publish-agent (workflow_run)

**Aufgaben:**
Generiert plattformspezifische Texte (LinkedIn, Mastodon, Newsletter) basierend auf dem finalen Post.

---

### Agent 10 — `memory-agent`

**Datei:** `.github/workflows/memory-agent.yml`

**Trigger:** Nach publish-agent (workflow_run)

**Aufgaben:**
1. Fügt veröffentlichten Post zu `context/blog-memory.json` hinzu
2. Aktualisiert Serien-Status und Ontologie
3. Committet Änderungen in `context/`

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
  Dateien: research-queue.json · visual-style-guide.md · ReNatureForce_BrandGuidelines_v4.md

Layer 3 — WORKING MEMORY (ephemeral)
  Generierungsprozess des aktuellen Agenten
```

---

## 8. Compliance & Rechtliches

### EU AI Act & Brand Consistency

Das System gewährleistet nicht nur rechtliche Compliance (KI-Kennzeichnung), sondern auch **Brand-Compliance** durch den `designer-agent`. Jede Abweichung von der visuellen Identität wird vor der Veröffentlichung gemeldet.

---

## 14. Maintenance & Monitoring

### GitHub Actions Minuten-Budget (10 Agenten)

| Agent | Frequenz | Geschätzte Dauer | Monatlich |
|---|---|---|---|
| research-agent | 2× pro Woche | ~5 min | ~40 min |
| writer-agent | 4× pro Monat | ~8 min | ~32 min |
| image-agent | 4× pro Monat | ~5 min | ~20 min |
| editor-agent | 4× pro Monat | ~5 min | ~20 min |
| visual-agent | 4× pro Monat | ~10 min | ~40 min |
| staging-agent (incl. Designer) | 4× pro Monat | ~7 min | ~28 min |
| publish-agent | 4× pro Monat | ~3 min | ~12 min |
| distribution-agent | 4× pro Monat | ~3 min | ~12 min |
| memory-agent | 4× pro Monat | ~2 min | ~8 min |
| **Gesamt** | | | **~212 min** |

Budget: 2.000 min/Monat → Weiterhin massiver Spielraum ✓

---

*Dokumentation Version 1.1 — Aktualisiert für die 10-Agenten-Pipeline*
