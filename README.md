# Préparation stratégique et technique d'un poste Data Scientist Senior Pricing (Opérateur HPA Européen)

Ce dépôt documente la méthode complète utilisée pour transformer une offre de poste Data Scientist Senior Pricing & Revenue Management (80 lignes) en une feuille de route produit, architecture et gouvernance prête pour un débriefing d'équipe technique, puis recalée à chaud après un premier entretien réel de 33 minutes avec le Responsable Data d'Opérateur HPA Européen (Client Cible).

L'objectif de ce travail dépasse la simple préparation d'entretien. Il démontre comment une démarche structurée (méthode BMad, workflows automatisés, exigences contrôlées ASD-STE100 et boucle de recalage terrain) produit des livrables vérifiables, sans remplissage et directement exploitables en contexte professionnel.

---

## Aperçu animé de la démarche (dessin animé 2D)

[![Découvrir la démarche BMad + ECC en dessin animé 2D](./demarche_cartoon_thumb.png)](./demarche_cartoon.mp4)

Voir la vidéo cartoon 2D (33 s, MP4 H.264): [demarche_cartoon.mp4](./demarche_cartoon.mp4)  
Voir la version démonstration complète avec défilement live d'`index.html` (48 s): [demarche_demo.mp4](./demarche_demo.mp4)

---

## 1. Pourquoi cette démarche change la qualité de l'output

Une préparation classique consiste à relire une offre et à improviser des idées génériques en entretien ("remplacer le prestataire par un XGBoost"). Cette approche produit des angles morts majeurs face à un interlocuteur technique qui vit les contraintes réelles du terrain.

La démarche appliquée ici inverse la logique en quatre temps tracés dans [docs/methodo.md](./docs/methodo.md).

### Temps 1: enquête factuelle multi-pistes avant toute hypothèse (`workflow_01_recon.py`)
Cinq pistes de recherche parallèles (`bmad-deep-recon`: marché, domaine HPA, concurrence européenne, stack technique et parties prenantes) ont été consolidées dans [01_deep_recon.md](./_bmad-output/planning-artifacts/01_deep_recon.md) à partir de sources publiques 2025-2026 vérifiées (Eurostat, INSEE, S&P Global Ratings, Éditeur PMS/PMS central, littérature RM, textes juridiques Omnibus, DMA et AI Act). Chaque piste sépare strictement les faits sourcés des hypothèses de travail à auditer.

### Temps 2: arbitrages humains et verrouillage produit (sas interactif)
Plutôt que de déléguer les choix stratégiques à une génération automatique, quatre jalons interactifs ont fixé la colonne vertébrale du dossier:
1. Un brainstorming ciblé (`bmad-brainstorming`) pour rejeter la logique de "3 POCs isolés" au profit d'une feuille de route globale incarnant le profil hybride métier et MLOps.
2. Un Product Brief ([02_product_brief.md](./_bmad-output/planning-artifacts/02_product_brief.md)) cadrant quatre lignes rouges non négociables (conservation de PMS central, zéro bascule en juillet-août, débrayage tracé en une ligne, sobriété cloud).
3. Un document Working Backwards à horizon 12 mois ([03_prfaq.md](./_bmad-output/planning-artifacts/03_prfaq.md)) incluant les objections difficiles de la Direction financière, du DPO, des équipes Tech/Data et des Revenue Managers.
4. Un PRD exécutif ([04_prd.md](./_bmad-output/planning-artifacts/04_prd.md)) décliné dans une version 2 rédigée selon les principes **ASD-STE100** ([04_prd_v2_asdste100.md](./_bmad-output/planning-artifacts/04_prd_v2_asdste100.md)): vocabulaire contrôlé unique, 28 exigences fonctionnelles et 10 exigences non fonctionnelles atomiques à la voix active, grille de scoring sur 100 points, 5 critères éliminatoires, North-Star Metric, contre-métriques, 4 kill-switches et annexe technique sur SHAP, Random Forest, XGBoost, RFF et optimisation des hyperparamètres.

### Temps 3: architecture, stress-test adversarial et livrables exécutifs (`workflow_02_build.py`)
Le second workflow a enchaîné la conception de l'architecture cible et de ses sept invariants `AD-01` à `AD-07` ([05_architecture.md](./_bmad-output/planning-artifacts/05_architecture.md)), cinq ateliers de stress-test adversarial en parallèle (`First Principles`, `Stakeholder Round Table`, `Pre-mortem`, `Red Team vs Blue Team`, `Shark Tank Pitch`) consolidés dans [06_stress_test.md](./_bmad-output/planning-artifacts/06_stress_test.md), la structuration macro en Epics, trimestres T1-T4 et matrice RACI ([07_epics_roadmap.md](./_bmad-output/planning-artifacts/07_epics_roadmap.md)), ainsi que l'assemblage de la présentation autonome [index.html](./index.html).

### Boucle terrain: preuve par l'entretien réel et recalage chirurgical
Après l'entretien de 33 minutes avec [HR] (Responsable de l'équipe Data chez Client Cible), l'enregistrement a été transcrit localement via `faster-whisper` ([00_inputs/transcribe_whisper.py](./00_inputs/transcribe_whisper.py)) et synthétisé dans [00_inputs/notes_entretien_responsable_data.md](./00_inputs/notes_entretien_responsable_data.md).

Cet échange a validé environ 80 % des hypothèses construites en amont (prestataire externe **Prestataire externe**, cœur **PMS central**, Data Warehouse **BigQuery**, journalisation existante des prix recommandés face aux prix appliqués, contrainte **Omnibus 30 jours** et impossibilité légale d'A/B test individuel). Il a surtout permis d'injecter six ajustements de précision dans [index.html](./index.html) et d'en produire l'export PowerPoint 16:9 haute définition [presentation_pricing_v2.pptx](./presentation_pricing_v2.pptx):
1. Posture recalée sur un **contrepoids constructif envers Prestataire externe** et une automatisation progressive, plutôt qu'une rupture frontale immédiate.
2. Intégration du socle exact confirmé: BigQuery en **architecture médaillon**, maille **Produit x Camping x Semaine** (avril à fin octobre, 218 jours), **quatre grilles marché** (FR/IT/ES, Pays-Bas, UK, Allemagne) et périmètre hébergement + ancillaries (sans yield F&B aujourd'hui).
3. Mise au premier plan des angles morts reconnus en séance: ajout des **données exogènes** (Google Trends, prix concurrents à moins d'1 km, météo, carburant), benchmark **Prophet + régresseurs** face à **XGBoost / Random Forest** pour capter le drift vers le last minute et le report "coolcation", et mesure du contournement inter-grilles (`portail-fr.example` / `portail-pl.example`).
4. Protocole expérimental complet sans A/B test individuel: validation sur **hold-out**, sélection de **10 à 15 campings pilotes volontaires** (Revenue Managers partants pour éviter le rejet manuel) puis **clustering de campings jumeaux** comparant le challenger interne à la baseline Prestataire externe.
5. Répartition réaliste du poste: 80 % pricing et 20 % pipelines/vie d'équipe, avec ouverture phase 2 sur les ancillaries, la recommandation web et le call center.
6. Passe complète de simplification **ASD-STE100** sur les 15 diapositives pour éliminer tout jargon statistique ou cloud opaque à l'oral.

---

## 2. Garanties de qualité et traçabilité

Chaque livrable rédactionnel respecte trois contrôles systématiques documentés dans [docs/methodo.md](./docs/methodo.md):
1. Séparation stricte entre faits publics vérifiés, confirmations d'entretien et hypothèses à auditer.
2. Réécriture claire selon les principes ASD-STE100 (phrases courtes, voix active, seuils mesurables, zéro sigle non expliqué).
3. Passage dans le serveur MCP `ai-remover` (`clean_invisible_unicode` et `analyze_ai_density`) confirmant un score de densité IA de `0.0` (densité faible, zéro cliché IA, zéro caractère Unicode invisible) sur les artefacts Markdown produits.

---

## 3. Carte complète des livrables du dépôt

| Étape | Livrable | Rôle dans la démarche |
| :--- | :--- | :--- |
| Présentation interactive | [index.html](./index.html) | Deck autonome de 15 diapositives (3 thèmes visuels, navigation clavier/molette, marges 1,5 cm, recalé après entretien le Responsable Data) |
| Export PowerPoint | [presentation_pricing_v2.pptx](./presentation_pricing_v2.pptx) | Version 16:9 haute définition des 15 diapositives avec texte complet dans les notes du présentateur |
| Vidéos de la démarche | [demarche_cartoon.mp4](./demarche_cartoon.mp4) et [demarche_demo.mp4](./demarche_demo.mp4) | Dessin animé 2D vectoriel (33 s) et walkthrough complet avec démo live du deck (48 s) |
| Scripts utilitaires | [utils/](./utils/) | Scripts autonomes de transcription Whisper, export PowerPoint et génération vidéo (`html_to_pptx.py`, `record_cartoon_video.py`, `record_demarche_video.py`, `transcribe_whisper.py`) |
| Skills mobilisés | [skills/](./skills/) | Copie locale des 15 fichiers `SKILL.md` (BMad, `frontend-slides`, `manim-video`, `ui-demo`, `remotion-video-creation`) utilisés sur ce dossier |
| Trace méthodologique | [docs/methodo.md](./docs/methodo.md) | Registre horodaté des skills BMad, workflows, contrôles `ai-remover` et arbitrages humains |
| Temps 1 (Recon) | [01_deep_recon.md](./_bmad-output/planning-artifacts/01_deep_recon.md) | Identification cible, 5 pistes d'enquête sourcées 2025-2026 et benchmark de 4 concurrents européens |
| Temps 2 (Produit) | [02_product_brief.md](./_bmad-output/planning-artifacts/02_product_brief.md) | Thèse produit, feuille de route globale en 4 temps et 4 lignes rouges |
| Temps 2 (Working Backwards) | [03_prfaq.md](./_bmad-output/planning-artifacts/03_prfaq.md) | Communiqué interne projeté à M+12 et FAQ externe/interne difficile (Direction, DPO, Tech, RM) |
| Temps 2 (Exigences) | [04_prd.md](./_bmad-output/planning-artifacts/04_prd.md) et [04_prd_v2_asdste100.md](./_bmad-output/planning-artifacts/04_prd_v2_asdste100.md) | PRD v1 conservé + PRD v2 en style ASD-STE100 (28 FR, 10 NFR, scoring /100, kill-switches, annexe SHAP/modèles/hyperparamètres) |
| Temps 3 (Architecture) | [05_architecture.md](./_bmad-output/planning-artifacts/05_architecture.md) | Architecture Spine batch serverless GCP/BigQuery/PMS central et 7 invariants `AD-01` à `AD-07` |
| Temps 3 (Stress-test) | [06_stress_test.md](./_bmad-output/planning-artifacts/06_stress_test.md) | Synthèse de 5 ateliers adversariaux, 4 objections majeures, 3 pivots Plan B et 4 accélérateurs terrain |
| Temps 3 (Roadmap & RACI) | [07_epics_roadmap.md](./_bmad-output/planning-artifacts/07_epics_roadmap.md) | 6 Epics macro, trajectoire T1 à T4 + phase 2 et matrice RACI |
| Retour terrain | [00_inputs/notes_entretien_responsable_data.md](./00_inputs/notes_entretien_responsable_data.md) | Synthèse structurée issue de la transcription locale Whisper (`00_inputs/whisper_raw.txt`) |

---

## 4. Workflows d'orchestration inclus

Le dossier [workflows/](./workflows/) contient les scripts réutilisables qui pilotent cette chaîne de bout en bout: [workflow_01_recon.py](./workflows/workflow_01_recon.py) pour l'enquête parallèle multi-pistes, [workflow_02_build.py](./workflows/workflow_02_build.py) pour l'architecture, le stress-test, la roadmap et le deck HTML, et [workflow_03_publish.py](./workflows/workflow_03_publish.py) pour la génération optionnelle d'une version anonymisée et caviardée destinée à GitHub Pages.
