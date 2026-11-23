# Document de reprise: industrialisation du pipeline d'analyse d'offre et API LLMOps

Date de sauvegarde: 2026-11-19
Dossier de référence: `C:\Users\Admin\Documents\TEMPLATE_GENERATE_ROADMAP`

## Ce qui est déjà construit et validé

Le dossier `TEMPLATE_GENERATE_ROADMAP` est autonome, nettoyé et prêt à être dupliqué pour chaque nouvelle offre d'emploi ou de mission.

### Arborescence active

```text
TEMPLATE_GENERATE_ROADMAP/
├── 00_inputs/
│   ├── offre.md                             # Emplacement vide prêt pour le texte brut de l'annonce
│   ├── mon_profil.md                        # Profil Career-Ops (Caroline Heymes) pré-rempli
│   └── cadrage_livrable.md                  # Thème swiss, 15 slides index.html, outils MCP Eraser/Draw.io
├── _bmad-output/
│   └── planning-artifacts/                  # Reçoit 01_deep_recon.md à 07_epics_roadmap.md
├── docs/
│   ├── methodo.md                           # Registre de traçabilité de tous les skills BMad/ECC + MCP ai-remover
│   └── prompts.md                           # Antisèche complète des 5 messages prêts à copier-coller
├── github/                                  # Reçoit index.html caviardé, architecture.png et README.md anonymisé
├── workflows/
│   ├── workflow_01_recon.py                 # Temps 1 auto: identification + 5 pistes Deep Recon + ai-remover
│   ├── workflow_02_build.py                 # Temps 3 auto: Architecture, 5 Elicitations, Roadmap, index.html, README + ai-remover
│   ├── workflow_03_publish.py               # Temps 4 auto: caviardage SHA-256 + github/README.md anonymisé + ai-remover
│   └── caviarder-presentation.mjs           # Script Node.js sans dépendance (testé OK sur deck Accor: 103 blocs, 0 fuite)
├── PLAYBOOK_ANALYSE_OFFRE.md                # Guide complet de la méthodologie et choix des modèles Antigravity
└── reprise.md                               # Ce document de reprise
```

### Architecture méthodologique figée (4 temps)

Le pipeline sépare volontairement l'automatisation de la réflexion humaine afin de préserver la valeur du brainstorming BMad:

| Temps | Mode | Contenu | Modèle Antigravity recommandé |
| :--- | :--- | :--- | :--- |
| Temps 1 | Automatique (`workflow_01_recon.py`) | Identification cible + 5 pistes `bmad-deep-recon` en parallèle (MR, DR, CR, TS, UV) + passe MCP `ai-remover` | Gemini 4 Neon (High) |
| Temps 2 | Interactif (chat Antigravity) | `bmad-brainstorming` (et `/grill-me` si besoin), puis verrouillage de `02_product_brief.md` (Mary), `03_prfaq.md` et `04_prd.md` + `ai-remover` | Claude Opus 5.5 (High) |
| Temps 3 | Automatique (`workflow_02_build.py`) | `bmad-architecture` (`AD-01..07`), 5 ateliers `bmad-advanced-elicitation` en parallèle (`24`, `9`, `59`, `21`, `22`), Epics/Roadmap T1-T4 + RACI, `index.html`, `README.md` + `ai-remover` | Claude Sonnet 5.5 (High) ou Opus 5.5 (Medium) |
| Finition | Court (chat Antigravity) | Génération `architecture.png` sur fond transparent (MCP Eraser.io ou Draw.io `-t`) et vérification visuelle | Gemini 3.8 Flash (Medium) |
| Temps 4 | Automatique (`workflow_03_publish.py`) | Caviardage SHA-256 + flou dès la slide 5 (`github/index.html`), copie `github/architecture.png`, rédaction de `github/README.md` 100% anonymisé + `ai-remover` | Claude Sonnet 5.5 (High) ou Gemini 4 Neon (Medium) |

## Piste d'évolution actée: passage en API (2 étapes)

La discussion s'est arrêtée sur la conception d'une API autour du SDK Python `google-antigravity` (`pip install google-antigravity`), découpée en deux étapes progressives.

### Étape 1: Moteur local (objectif utilitaire immédiat)

Encapsuler le template derrière une API locale en Docker Compose sans sur-ingénierie:

1. Stack cible: FastAPI (REST + SSE pour suivi en direct), SQLite (état des missions, timestamps, coûts), worker asynchrone Redis/ARQ exécutant le SDK `google-antigravity`.
2. Machine à états par `mission_id`: `POST /missions` (`RECON_RUNNING` -> `AWAITING_BRAINSTORM`), `POST /missions/{id}/brainstorm` (`SPECS_LOCKED`), `POST /missions/{id}/build` (`BUILD_READY`), `POST /missions/{id}/publish` (`PUBLISHED`).
3. Compatibilité disque totale: les fichiers restent écrits au format exact du template (`_bmad-output/planning-artifacts/`, `docs/methodo.md`, `github/`).
4. Intégrations directes: import Python direct du package `ai-remover` dans le worker, appel sous-processus Node.js à `caviarder-presentation.mjs`, et webhook optionnel depuis Career-Ops pour déclencher le Temps 1 sur les offres bien scorées.

### Étape 2: Microservice industriel avec observabilité et eval harness (vitrine Lead IA)

Faire évoluer le moteur local vers une architecture production/portfolio:

1. Découpage en trois services: `api-gateway` (FastAPI, auth, quotas, SSE), `agent-worker` (exécution isolée avec checkpointing par artefact pour reprise sur erreur sans repayer les phases précédentes), `publisher-service` (caviardage SHA-256, anonymisation, contrôle anti-fuite, push GitHub Pages).
2. Observabilité LLMOps: OpenTelemetry + Langfuse auto-hébergé en Docker (traces par span d'agent, tokens, coût exact en euros par mission) + Prometheus/Grafana (taux d'échec par skill, latences p50/p95).
3. Eval harness sur un golden dataset de 3 à 5 offres réelles anonymisées avec deux étages de gates:
   - Évaluateurs déterministes: présence et validité des 7 artefacts BMad, score `ai-remover` (`analyze_ai_density` sous seuil, zéro unicode invisible), contrôle Playwright headless sur `index.html` (0 débordement en 1920x1080, 1440x900 et 390x844), contrôle sécurité `github/` (parité SHA-256 100%, 0 caractère non hexadécimal, 0 occurrence du nom d'entreprise ou de ses marques dans `github/README.md`).
   - Évaluateur LLM-as-a-Judge: cohérence croisée des invariants `AD-01..07` entre architecture, POCs et feuille de route T1-T4, et non-régression à chaque changement de prompt, de skill ou de modèle.

## Questions et prérequis pour la prochaine session

1. Valider le template actuel en réel sur 2 offres via Antigravity pour stabiliser les prompts et récolter les premiers cas du golden dataset.
2. Trancher le mode d'authentification du SDK `google-antigravity` pour l'Étape 1 (Vertex AI via ADC ou clé API Gemini) et le budget plafond par mission.
3. Choisir l'interface souhaitée pour le sas interactif Temps 2 côté API (Swagger/CLI, mini UI Streamlit/Next.js, ou reprise ponctuelle dans Antigravity).
4. Vérifier le chemin du repo local `ai-remover` pour l'importer directement en dépendance Python dans le worker FastAPI.

## Prompt de reprise rapide

Copiez-collez ce message dans une nouvelle conversation pour reprendre exactement au point d'arrêt:

```text
Lis @C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP/reprise.md.
Nous reprenons la conception de l'Étape 1 (moteur local FastAPI + SDK google-antigravity + machine à états sur le template existant). Propose-moi l'arborescence du projet API, le schéma SQLite minimal et les endpoints FastAPI avant de coder.
```
