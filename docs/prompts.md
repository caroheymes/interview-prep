# Antisèche des commandes et prompts

Ce document rassemble la séquence complète des messages à envoyer dans Antigravity après avoir dupliqué `TEMPLATE_GENERATE_ROADMAP` vers votre dossier mission (par exemple `C:\Users\Admin\Documents\MALT\11_NomClient`).

## Préparation avant d'ouvrir le chat

Collez le texte brut de l'annonce dans `00_inputs/offre.md`, ajustez si besoin 2 ou 3 lignes dans `00_inputs/cadrage_livrable.md` (interlocuteurs, thème, schéma requis), puis ouvrez ce nouveau dossier comme workspace dans Antigravity.

## Message 1 (Temps 1 automatique: enquête Deep Recon)

Sélectionnez **Gemini 4 Neon (High)** et envoyez:

```text
Exécute @workflows/workflow_01_recon.py sur le workspace courant.
```

Attendez la notification de fin. Lisez `_bmad-output/planning-artifacts/01_deep_recon.md`, vérifiez la mise à jour de `docs/methodo.md`, puis lancez `/compact`.

## Message 2 (Temps 2 interactif: brainstorming et verrouillage des specs)

Basculez sur **Claude Opus 5.5 (High)** et envoyez:

```text
Lis @00_inputs/offre.md et @_bmad-output/planning-artifacts/01_deep_recon.md, puis lance un bmad-brainstorming interactif pour qu'on tranche ensemble l'angle d'attaque et les 3 POCs avant de rédiger le Brief, le PRFAQ et le PRD.
```

Échangez librement avec l'agent jusqu'à valider vos arbitrages. Vous pouvez aussi envoyer `/grill-me` à ce stade si vous voulez que l'agent vous challenge point par point avant de figer vos décisions.

Dès que vos choix sont arrêtés, envoyez:

```text
Nos arbitrages sont figés. Rédige 02_product_brief.md (Mary), 03_prfaq.md et 04_prd.md dans _bmad-output/planning-artifacts/, passe chacun de ces trois fichiers dans le serveur MCP ai-remover (clean_invisible_unicode, analyze_ai_density, humanize_text), et mets à jour docs/methodo.md (Étapes 2.1 à 2.4).
```

Relisez ces trois fichiers, puis lancez `/compact`.

## Message 3 (Temps 3 automatique: architecture, stress-test, roadmap et deck)

Basculez sur **Claude Sonnet 5.5 (High)** (ou **Claude Opus 5.5 Medium**) et envoyez:

```text
Exécute @workflows/workflow_02_build.py sur le workspace courant.
```

Le workflow produit automatiquement `05_architecture.md`, `06_stress_test.md`, `07_epics_roadmap.md`, `index.html`, `README.md` et met à jour `docs/methodo.md`.

## Message 4 (Schéma transparent et contrôle avant publication)

Basculez sur **Gemini 3.8 Flash (Medium)** et envoyez:

```text
Génère architecture.png sur fond transparent à partir de @_bmad-output/planning-artifacts/05_architecture.md (via MCP Eraser.io ou MCP Draw.io -t), mets à jour la Phase 5A dans docs/methodo.md, puis vérifie index.html et README.md.
```

## Message 5 (Temps 4 automatique: publication GitHub teaser et anonymisation)

Basculez sur **Claude Sonnet 5.5 (High)** (ou **Gemini 4 Neon Medium**) et envoyez:

```text
Exécute @workflows/workflow_03_publish.py sur le workspace courant.
```

Si vous souhaitez caviarder à partir d'une autre slide que la slide 5 (par exemple la slide 6), utilisez plutôt:

```text
Exécute @workflows/workflow_03_publish.py sur le workspace courant avec l'argument {"start_slide": 6}.
```

Le dossier `github/` contient alors la version prête pour GitHub Pages: `github/index.html` (slides 1 à 4 publiques, texte caviardé en SHA-256 flouté à partir de la slide 5), `github/architecture.png` et `github/README.md` entièrement anonymisé avec vos coordonnées de prise de contact.
