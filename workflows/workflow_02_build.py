"""
Workflow 02: Architecture, Advanced Elicitation (5 methodes), Epics/Roadmap, index.html
et trace complete dans docs/methodo.md.

Prerequis:
    Le sas interactif humain (Phase 2) doit etre termine et avoir fige les fichiers suivants
    dans `<dossier>/_bmad-output/planning-artifacts/`:
        - 01_deep_recon.md
        - 02_product_brief.md
        - 03_prfaq.md
        - 04_prd.md

Usage via Antigravity (`run_workflow`):
    Args:
        dossier (str): Chemin absolu du dossier mission. Par defaut, premier workspace actif.
        reference_deck (str): Chemin absolu vers un deck HTML de reference.
"""

from datetime import datetime

dossier = (args.get("dossier") or (WORKSPACES[0] if WORKSPACES else ".")).replace("\\", "/").rstrip("/")
reference_deck = args.get(
    "reference_deck",
    "C:/Users/Admin/Documents/MALT/10_14_Accor/presentation.html",
).replace("\\", "/")

inputs_dir = f"{dossier}/00_inputs"
artifacts_dir = f"{dossier}/_bmad-output/planning-artifacts"

recon_path = f"{artifacts_dir}/01_deep_recon.md"
brief_path = f"{artifacts_dir}/02_product_brief.md"
prfaq_path = f"{artifacts_dir}/03_prfaq.md"
prd_file = args.get("prd_file", "04_prd.md")
prd_path = f"{artifacts_dir}/{prd_file}"
arch_path = f"{artifacts_dir}/05_architecture.md"
stress_path = f"{artifacts_dir}/06_stress_test.md"
roadmap_path = f"{artifacts_dir}/07_epics_roadmap.md"
arch_png_path = f"{dossier}/architecture.png"
deck_path = f"{dossier}/index.html"
readme_path = f"{dossier}/README.md"
methodo_log_path = f"{dossier}/docs/methodo.md"

file_schema = {
    "type": "object",
    "properties": {
        "file_written": {"type": "string"},
        "skills_used": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
    },
    "required": ["file_written", "skills_used", "summary"],
}

log(f"Demarrage Workflow 02 (Build) sur: {dossier}")

# ---------------------------------------------------------------------------
# Phase 3A: Architecture Spine et invariants AD-01..AD-07 (Winston)
# ---------------------------------------------------------------------------
phase("Phase 3A: Architecture Spine (AD-01..AD-07)")

arch_res = await agent(
    prompt=(
        "Lis obligatoirement les skills bmad-agent-architect et bmad-architecture (SKILL.md) "
        f"avant de rediger. Lis ensuite {prfaq_path} et {prd_path}. "
        f"Ecris l'Architecture Spine cible dans {arch_path}. "
        "Le document doit contenir: "
        "1) Une topologie claire des flux ou couloirs d'execution capitalisant sur l'existant, "
        "2) Un tableau de 5 a 7 invariants non negociables numerotes AD-01 a AD-07 "
        "(avec regle d'implementation concrete et risque elimine), "
        "3) Une specification precise du schema d'architecture a generer dans architecture.png "
        "(imperativement sur fond transparent via MCP Eraser.io ou Draw.io -t). "
        f"Passe obligatoirement {arch_path} dans le serveur MCP `ai-remover` "
        "(`clean_invisible_unicode`, `analyze_ai_density`, `humanize_text`) avant de terminer. "
        "Respecte strictement la typographie francaise sans emoji ni tiret cadratin."
    ),
    schema=file_schema,
    role="Architecte (Winston)",
    model="pro",
)
log(f"Architecture ecrite: {arch_res['file_written']}")

# ---------------------------------------------------------------------------
# Phase 3B: BMad Advanced Elicitation (5 ateliers en parallele puis synthese)
# ---------------------------------------------------------------------------
phase("Phase 3B: BMad Advanced Elicitation (5 methodes)")

methodes = [
    ("24_First_Principles", "24: First Principles Analysis (assumptions -> truths -> new approach)"),
    ("09_Stakeholder_Round_Table", "9: Stakeholder Round Table (perspectives -> synthesis -> alignment)"),
    ("59_Pre_mortem", "59: Pre-mortem Analysis (failure scenario -> causes -> prevention)"),
    ("21_Red_Team_vs_Blue_Team", "21: Red Team vs Blue Team (defense -> attack -> hardening)"),
    ("22_Shark_Tank_Pitch", "22: Shark Tank Pitch (pitch -> challenges -> refinement)"),
]

elicitation_schema = {
    "type": "object",
    "properties": {
        "method": {"type": "string"},
        "findings_markdown": {"type": "string"},
        "hardening_actions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["method", "findings_markdown", "hardening_actions"],
}

resultats_elicitation = await parallel(
    methodes,
    lambda m: agent(
        prompt=(
            "Lis obligatoirement le skill bmad-advanced-elicitation (SKILL.md). "
            f"Lis ensuite {prfaq_path}, {prd_path} et {arch_path}. "
            f"Applique rigoureusement la methode {m[1]} a cette proposition. "
            "Produis une critique concrete, chiffree et exploitable en entretien de direction "
            "(objections reelles, pivots Plan A vers Plan B activables en 24-48h, "
            "accelerateurs d'execution terrain ou durcissements des invariants AD-01..07). "
            "Redige en francais direct, sans remplissage ni emoji."
        ),
        schema=elicitation_schema,
        role=f"Elicitation {m[0]}",
        model="pro",
    ),
)

stress_res = await agent(
    prompt=(
        f"Consolide les 5 ateliers d'Advanced Elicitation ({resultats_elicitation}) dans {stress_path}. "
        "Structure la synthese en 4 blocs directement exploitables pour le deck final: "
        "1) Les 4 objections majeures des parties prenantes et les reponses du framework, "
        "2) Les 3 pivots de contingence (Plan A -> Plan B en 24 a 48h), "
        "3) Les 4 accelerateurs d'execution terrain contre les lenteurs grands groupes, "
        "4) Les ajustements a repercuter sur les invariants AD-01..07 et la feuille de route. "
        f"Passe obligatoirement {stress_path} dans le serveur MCP `ai-remover` "
        "(`clean_invisible_unicode`, `analyze_ai_density`, `humanize_text`) avant de terminer."
    ),
    schema=file_schema,
    role="Consolidation Stress-Test",
    model="pro",
)
log(f"Stress-test ecrit: {stress_res['file_written']}")

# ---------------------------------------------------------------------------
# Phase 4: Epics, Stories (mode macro) et Sprint Planning (T1-T4 + RACI)
# ---------------------------------------------------------------------------
phase("Phase 4: Epics macro, Roadmap T1-T4 et RACI")

roadmap_res = await agent(
    prompt=(
        "Lis obligatoirement les skills bmad-create-epics-and-stories et bmad-sprint-planning (SKILL.md). "
        f"Lis ensuite {prd_path}, {arch_path} et {stress_path}. "
        "Execute les etapes step-01-validate-prerequisites, step-02-design-epics, "
        "step-03-create-stories et step-04-final-validation en mode macro (niveau direction, "
        "pas de tickets granulaires de developpement), puis traduis le sprint planning en "
        "trajectoire sur 12 mois. "
        f"Ecris le resultat complet dans {roadmap_path} avec: "
        "1) Les Epics structurants alignes sur AD-01..07 et les parades du stress-test, "
        "2) Une feuille de route en 4 trimestres (T1 Fondations, T2 Quick-Wins, T3 Pilote avance/ROI, "
        "T4 Industrialisation) avec un livrable tangible par trimestre, "
        "3) Une matrice de gouvernance RACI claire entre ce role, Metier, Tech/Data et Juridique/DPO. "
        f"Passe obligatoirement {roadmap_path} dans le serveur MCP `ai-remover` "
        "(`clean_invisible_unicode`, `analyze_ai_density`, `humanize_text`) avant de terminer."
    ),
    schema=file_schema,
    role="Epics et Roadmap",
    model="inherit",
)
log(f"Roadmap ecrite: {roadmap_res['file_written']}")

# ---------------------------------------------------------------------------
# Phase 5: Generation de index.html, README.md et mise a jour docs/methodo.md
# ---------------------------------------------------------------------------
phase("Phase 5: Generation de index.html, README.md et trace")

run_date = datetime.now().strftime("%Y-%m-%d %H:%M")

deck_res = await agent(
    prompt=(
        "Lis obligatoirement le skill frontend-slides (SKILL.md). "
        f"Lis les entrees suivantes: {inputs_dir}/mon_profil.md, {inputs_dir}/cadrage_livrable.md, "
        f"{recon_path}, {brief_path}, {prfaq_path}, {prd_path}, {arch_path}, {stress_path}, "
        f"{roadmap_path}. "
        f"Inspire-toi de la qualite visuelle, de la navigation clavier/molette, du selecteur de "
        f"themes (theme par defaut specifie dans cadrage_livrable.md) et de la lightbox schema "
        f"(pointant vers `architecture.png`) de {reference_deck}. "
        f"IMPORTANT: {deck_path} a la racine est la version integrale NON anonymisee destinee a "
        "l'entretien: tout son contenu doit s'afficher 100% en clair des l'ouverture (aucun flou "
        "actif par defaut; l'anonymisation et le verrouillage SHA-256 seront appliques separement "
        "dans `github/index.html` par `workflow_03_publish.py`). "
        f"Genere le deck autonome de 15 slides dans {deck_path} "
        "en suivant exactement le plan des 15 slides du playbook (Slide 01 Couverture jusqu'a "
        "Slide 15 Alignement profil). "
        "Verifie la coherence de tous les chiffres et references AD-01..07 entre les slides, "
        "respecte imperativement la respiration verticale en haut de chaque slide "
        "(justify-content: flex-start et padding-top: clamp(4.75rem, 7.8vh, 5.85rem) sur "
        ".slide-content sous la topbar fixe, margin-bottom: clamp(0.7rem, 1.35vh, 1.05rem) sur "
        ".eyebrow et h2.slide-title, --content-gap: clamp(1.15rem, 2.35vh, 1.8rem) avant les "
        "grilles/tableaux, avec repli proportionnel @media (max-height: 860px) pour eviter "
        "tout ecrasement haut et tout debordement en 1920x1080, 1536x864 et 1440x900), et passe les blocs "
        "redactionnels (titres, sous-titres, cartes) dans le serveur MCP `ai-remover` "
        "(`analyze_ai_density`, `humanize_text`, `clean_invisible_unicode`) sans alterer les "
        "balises HTML, le CSS ni le JS."
    ),
    schema=file_schema,
    role="Generation index.html",
    model="pro",
)

readme_res = await agent(
    prompt=(
        f"Lis {inputs_dir}/cadrage_livrable.md, {brief_path}, {arch_path} et {roadmap_path}. "
        f"Redige un fichier {readme_path} concis, professionnel et pret pour GitHub. "
        "Structure attendue: "
        "1) Titre de la proposition et resume executif en 3 a 5 lignes, "
        "2) Lien vers la presentation interactive (`index.html` / GitHub Pages), "
        "3) Section Architecture affichant le schema `![Architecture cible](./architecture.png)` "
        "uniquement si `cadrage_livrable.md` indique qu'un schema d'architecture est requis "
        "(avec resume des invariants AD-01..07), "
        "4) Synthese de la feuille de route en 4 trimestres (T1 a T4), "
        "5) Liens vers la trace methodologique (`docs/methodo.md`) et les artefacts BMad "
        "(`_bmad-output/planning-artifacts/`). "
        f"Passe obligatoirement {readme_path} dans le serveur MCP `ai-remover` "
        "(`clean_invisible_unicode`, `analyze_ai_density`, `humanize_text`) avant de terminer. "
        f"Mets ensuite a jour {methodo_log_path}: passe les lignes Temps 3 (Phase 3A, 3B, 4, 5B, 5C) "
        f"au statut 'Fait' avec la date '{run_date}', renseigne la colonne MCP `ai-remover`, "
        "et ajoute une entree horodatee dans le 'Journal d'execution detaille' recapitulant "
        f"tous les skills et MCP executes ({arch_res['skills_used']}, bmad-advanced-elicitation "
        f"24/9/59/21/22, {roadmap_res['skills_used']}, frontend-slides, generation README.md, "
        "MCP ai-remover). "
        "Respecte strictement la typographie francaise: accents complets, zero espace avant les "
        "signes doubles, guillemets droits, zero tiret cadratin, zero emoji, pas de listes "
        "artificielles titre-gras-deux-points."
    ),
    schema=file_schema,
    role="Generation README.md et trace",
    model="inherit",
)

log(f"Deck final genere: {deck_res['file_written']}")
log(f"README genere: {readme_res['file_written']}")
log(f"Trace complete enregistree dans: {methodo_log_path}")
print(f"WORKFLOW_02_DONE: {deck_res['file_written']} | {readme_res['file_written']}")
