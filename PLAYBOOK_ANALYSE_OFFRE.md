# Playbook d'analyse d'offre et production de livrable exécutif

Ce playbook standardise la transformation d'une offre d'emploi ou de mission en un dossier stratégique complet et en une présentation interactive autonome `index.html` prête pour une publication sur GitHub Pages (15 slides, schéma d'architecture intégré et mode teaser pour l'entretien). Il repose sur un modèle hybride en trois temps qui combine deux workflows Python natifs (`run_workflow`), un sas de réflexion interactive au milieu pour figer les spécifications dans `_bmad-output/planning-artifacts/`, et une traçabilité complète des skills utilisés dans `docs/methodo.md`.

## Architecture hybride en 3 temps

Automatiser de bout en bout supprime la valeur principale de BMad: le dialogue humain avec `bmad-brainstorming` pour trancher les angles et verrouiller les spécifications. Ce playbook sépare donc la mécanique factuelle de la décision stratégique.

| Temps | Mode d'exécution | Ce qui s'y passe | Livrable produit |
| :--- | :--- | :--- | :--- |
| Temps 1 (Enquête) | Automatique via `workflows/workflow_01_recon.py` | Identification entreprise + 5 pistes `bmad-deep-recon` en parallèle (MR, DR, CR, TS, UV) + trace dans `docs/methodo.md` | `_bmad-output/planning-artifacts/01_deep_recon.md` |
| Temps 2 (Réflexion et specs) | Interactif dans le chat Antigravity | `bmad-brainstorming` (et `/grill-me` si besoin), puis `bmad-product-brief`, `bmad-prfaq` et `bmad-prd` + trace dans `docs/methodo.md` | `02_product_brief.md`, `03_prfaq.md`, `04_prd.md` figés |
| Temps 3 (Build et durcissement) | Automatique via `workflows/workflow_02_build.py` | `bmad-architecture` (`AD-01..07`), 5 ateliers `bmad-advanced-elicitation` en parallèle, Epics/Roadmap T1-T4, `index.html`, `README.md` + trace dans `docs/methodo.md` | `05_architecture.md`, `06_stress_test.md`, `07_epics_roadmap.md`, `index.html`, `README.md` |
| Temps 4 (Publication GitHub) | Automatique via `workflows/workflow_03_publish.py` | Caviardage SHA-256 + flou dès la slide 5 (`caviarder-presentation.mjs`), copie `architecture.png` et rédaction de `github/README.md` 100% anonymisé | `github/index.html`, `github/architecture.png`, `github/README.md` |

## Principes de choix des modèles Antigravity

Choisissez le modèle en fonction de la nature cognitive de l'étape, et ajustez l'effort de raisonnement (Low, Medium, High, XHigh) pour maîtriser vos quotas et votre vitesse d'exécution.

| Famille et niveau | Usage principal dans ce playbook | Pourquoi ce choix |
| :--- | :--- | :--- |
| Gemini 4 Neon ou Argon (Medium / High) | Temps 1 (workflow Recon), consolidation de gros volumes documentaires | Grande fenêtre de contexte, synthèse rapide de sources multiples, excellente tenue sur les recherches web |
| Claude Opus 5.5 (Medium / High) | Temps 2 (`bmad-brainstorming`, PRFAQ, PRD) et Temps 3 (Advanced Elicitation) | Qualité rédactionnelle en français, finesse d'argumentation métier, rigueur sur les postures critiques |
| Claude Sonnet 5.5 (Medium / High) | Temps 2 (Product Brief), Temps 3 (Architecture, Epics/Roadmap, Deck HTML) | Meilleur ratio vitesse/précision pour structurer des spécifications, cadrer des invariants et coder du HTML propre |
| Gemini 3.8 Flash (Medium) ou Sonnet (Low) | Relectures, nettoyages typographiques, vérifications de cohérence | Coût en quota très faible pour les contrôles mécaniques en fin de parcours |

Utilisez `/compact` après le Temps 1 puis après le Temps 2. Vous repartez ainsi avec un contexte léger tout en conservant la vérité dans les fichiers Markdown sur disque.

## Arborescence standard d'une mission

Dupliquez ce dossier template pour chaque nouvelle offre (par exemple `C:/Users/Admin/Documents/MALT/11_NomClient/`):

```text
11_NomClient/
├── 00_inputs/
│   ├── offre.md                             # Texte brut de l'annonce, sans reformulation
│   ├── mon_profil.md                        # Votre profil Career-Ops (déjà pré-rempli)
│   └── cadrage_livrable.md                  # Contraintes visuelles, thème swiss, outils schéma
├── _bmad-output/
│   └── planning-artifacts/
│       ├── 01_deep_recon.md                 # Généré par workflow_01_recon.py
│       ├── 02_product_brief.md              # Figé pendant le Temps 2 interactif
│       ├── 03_prfaq.md                      # Figé pendant le Temps 2 interactif
│       ├── 04_prd.md                        # Figé pendant le Temps 2 interactif
│       ├── 05_architecture.md               # Généré par workflow_02_build.py
│       ├── 06_stress_test.md                # Généré par workflow_02_build.py
│       └── 07_epics_roadmap.md              # Généré par workflow_02_build.py
├── docs/
│   └── methodo.md                           # Trace complète de tous les skills BMad et ECC utilisés
├── github/                                  # Dossier prêt à publier sur GitHub Pages (version teaser)
│   ├── index.html                           # Copie caviardée SHA-256 + flou dès la slide 5
│   ├── architecture.png                     # Copie du schéma d'architecture (si généré)
│   └── README.md                            # Vitrine 100% anonymisée (zéro nom d'entreprise)
├── workflows/
│   ├── workflow_01_recon.py                 # Workflow automatique Temps 1
│   ├── workflow_02_build.py                 # Workflow automatique Temps 3
│   ├── workflow_03_publish.py               # Workflow automatique Temps 4 (publication GitHub)
│   └── caviarder-presentation.mjs           # Script Node.js de caviardage SHA-256 sans dépendance
├── PLAYBOOK_ANALYSE_OFFRE.md                # Ce guide
├── README.md                                # Vitrine GitHub (généré en Phase 5C, inclut architecture.png si requis)
├── architecture.png                         # Schéma d'architecture exporté sur fond transparent
└── index.html                               # Deck final interactif (15 slides, GitHub Pages)
```

## Exécution pas à pas

Remplacez `<DOSSIER>` par le chemin absolu de votre mission (par exemple `C:/Users/Admin/Documents/MALT/11_NomClient`). Collez d'abord le texte de l'annonce dans `00_inputs/offre.md` et adaptez `00_inputs/cadrage_livrable.md`.

### Temps 1: Lancer le workflow automatique de reconnaissance

Modèle conseillé dans le sélecteur: **Gemini 4 Neon (High)**.

```text
Exécute le workflow @/workflows/workflow_01_recon.py avec l'argument {"dossier": ""}.
```

À la fin de l'exécution, parcourez `/_bmad-output/planning-artifacts/01_deep_recon.md` et vérifiez la trace dans /docs/methodo.md`, puis passez `/compact`.

### Temps 2: Sas interactif (brainstorming et verrouillage des specs)

Modèle conseillé: **Claude Opus 5.5 (High)** pour le brainstorming, le PRFAQ et le PRD (ou **Claude Sonnet 5.5 High** sur le Product Brief).

#### Étape 2.1: Brainstorming et arbitrages stratégiques

```text
Entrées: @/00_inputs/offre.md et @/_bmad-output/planning-artifacts/01_deep_recon.md
Skill: `bmad-brainstorming`

Lance une session interactive courte pour challenger les angles d'attaque issus du Deep Recon.
Pose-moi des questions ciblées pour m'aider à trancher:
1. L'angle de différenciation prioritaire face aux autres candidats.
2. Les 3 POCs pilotes les plus crédibles et mesurables sur 12 mois.
3. Les contraintes politiques ou techniques à respecter absolument.
Ne rédige aucun livrable final tant que nous n'avons pas validé ces arbitrages ensemble.
En fin de session, mets à jour la ligne Étape 2.1 dans /docs/methodo.md.
```

Vous pouvez aussi déclencher `/grill-me` à ce stade si vous souhaitez un interrogatoire plus serré avant de figer vos décisions.

#### Étape 2.2: Figer le Product Brief (Mary)

```text
Entrées: @/00_inputs/offre.md, @/_bmad-output/planning-artifacts/01_deep_recon.md et nos décisions validées en brainstorming.
Skill: `bmad-agent-analyst` (Mary) -> `bmad-product-brief`
Sortie attendue: /_bmad-output/planning-artifacts/02_product_brief.md

Rédige le Product Brief en intégrant exactement les 3 POCs pilotes et les verticaux validés, puis mets à jour la ligne Étape 2.2 dans /docs/methodo.md.
```

#### Étape 2.3: Figer le Working Backwards PRFAQ

```text
Entrées: @/_bmad-output/planning-artifacts/01_deep_recon.md et @/_bmad-output/planning-artifacts/02_product_brief.md
Skill: `bmad-prfaq`
Sortie attendue: /_bmad-output/planning-artifacts/03_prfaq.md

Applique Working Backwards à horizon 12 mois avec un communiqué de presse interne chiffré et une FAQ en deux blocs (externe et interne difficile: Direction, DPO, Tech/Data, Achats), puis mets à jour la ligne Étape 2.3 dans /docs/methodo.md.
```

#### Étape 2.4: Figer le PRD

```text
Entrées: @/_bmad-output/planning-artifacts/02_product_brief.md et @/_bmad-output/planning-artifacts/03_prfaq.md
Skill: `bmad-prd`
Sortie attendue: /_bmad-output/planning-artifacts/04_prd.md

Produis le PRD exécutif incluant obligatoirement:
1. Une grille de scoring sur 100 points (4 axes pondérés, seuils Go/Backlog/No-Go, critères éliminatoires).
2. Les exigences fonctionnelles et non fonctionnelles des 3 POCs pilotes.
3. Le cycle POC en 4 étapes avec North-Star Metric, contre-métriques et kill-switches.
Mets ensuite à jour la ligne Étape 2.4 dans /docs/methodo.md.
```

Relisez rapidement `02_product_brief.md`, `03_prfaq.md` et `04_prd.md`, puis passez `/compact`. Vos spécifications sont désormais figées.

### Temps 3: Lancer le workflow automatique de durcissement et de génération

Modèle conseillé dans le sélecteur: **Claude Sonnet 5.5 (High)** ou **Claude Opus 5.5 (Medium)**.

```text
Exécute le workflow @/workflows/workflow_02_build.py avec les arguments { "reference_deck": "C:/Users/Admin/Documents/MALT/10_14_Accor/presentation.html"}.
```

Le script enchaîne automatiquement `bmad-architecture` (`05_architecture.md`), les 5 ateliers `bmad-advanced-elicitation` en parallèle (`06_stress_test.md`), `bmad-create-epics-and-stories` + `bmad-sprint-planning` (`07_epics_roadmap.md`), la génération de `index.html` via `frontend-slides`, la rédaction du `README.md` (affichant `architecture.png` si un schéma est requis dans `cadrage_livrable.md`) et l'enregistrement final de la trace dans `docs/methodo.md`.

## Temps 4: Publication GitHub publique (teaser caviardé et anonymisé)

Une fois `architecture.png` généré sur fond transparent à la racine (via MCP Eraser.io ou MCP Draw.io `-t`) et `index.html` vérifié, lancez le workflow de publication sur **Claude Sonnet 5.5 (High)** ou **Gemini 4 Neon (Medium)**:

```text
Exécute @workflows/workflow_03_publish.py sur le workspace courant.
```

Ce workflow produit dans `/github/` trois livrables prêts à être poussés sur un dépôt public GitHub Pages: `github/index.html` (slides 1 à 4 publiques, paragraphes, listes et tableaux caviardés en SHA-256 flouté à partir de la slide 5 sans fuite dans le DOM), `github/architecture.png` (si présent à la racine) et `github/README.md` totalement anonymisé avec appel à prise de contact. Il met également à jour la Phase 6 dans `docs/methodo.md`.
