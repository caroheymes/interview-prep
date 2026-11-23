"""
Workflow 01: Identification entreprise, BMad Deep Recon multi-pistes et trace dans docs/methodo.md.

Usage via Antigravity (`run_workflow`):
    Args:
        dossier (str): Chemin absolu du dossier mission contenant `00_inputs/offre.md`.
                       Par defaut, utilise le premier workspace actif.
"""

from datetime import datetime

dossier = (args.get("dossier") or (WORKSPACES[0] if WORKSPACES else ".")).replace("\\", "/").rstrip("/")
inputs_dir = f"{dossier}/00_inputs"
artifacts_dir = f"{dossier}/_bmad-output/planning-artifacts"
offre_path = f"{inputs_dir}/offre.md"
deep_recon_out = f"{artifacts_dir}/01_deep_recon.md"
methodo_log_path = f"{dossier}/docs/methodo.md"

log(f"Demarrage Workflow 01 (Recon) sur: {dossier}")

# ---------------------------------------------------------------------------
# Phase 1A: Identification de l'entreprise cible et cadrage sectoriel
# ---------------------------------------------------------------------------
phase("Phase 1A: Identification entreprise et enjeux")

id_schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "confidence": {"type": "string"},
        "industry": {"type": "string"},
        "probable_stack": {"type": "array", "items": {"type": "string"}},
        "key_challenges": {"type": "array", "items": {"type": "string"}},
        "evidence_summary": {"type": "string"},
    },
    "required": ["company_name", "confidence", "industry", "key_challenges", "evidence_summary"],
}

identification = await agent(
    prompt=(
        f"Lis integralement le fichier {offre_path}. "
        "Identifie la societe la plus probable derriere cette offre (si elle est anonyme, "
        "cite les indices factuels precis et ton niveau de confiance), son industrie exacte, "
        "sa stack technologique ou data probable et ses 3 a 5 problematiques metier critiques. "
        "Reponds en francais direct, sans remplissage."
    ),
    schema=id_schema,
    role="Identification cible",
    model="pro",
)

log(f"Cible identifiee: {identification['company_name']} ({identification['confidence']})")

# ---------------------------------------------------------------------------
# Phase 1B: BMad Deep Recon en parallele sur les 5 pistes (MR, DR, CR, TS, UV)
# ---------------------------------------------------------------------------
phase("Phase 1B: BMad Deep Recon (5 pistes paralleles)")

pistes = [
    ("MR", "Market Research: taille de marche, tendances 2025-2026, leviers de croissance et marges."),
    ("DR", "Domain Research: contraintes metier specifiques, reglementation, maturite operationnelle."),
    ("CR", "Competitive Research: 3 a 4 acteurs internationaux benchmarkes et avantage asymetrique possible."),
    ("TS", "Technical and Stack Research: ecosysteme outils, data, architecture probable et points de friction."),
    ("UV", "User and Value Research: parties prenantes internes/externes, valeur attendue et obstacles d'adoption."),
]

piste_schema = {
    "type": "object",
    "properties": {
        "track": {"type": "string"},
        "key_facts": {"type": "array", "items": {"type": "string"}},
        "hypotheses": {"type": "array", "items": {"type": "string"}},
        "markdown_section": {"type": "string"},
    },
    "required": ["track", "key_facts", "markdown_section"],
}

resultats_pistes = await parallel(
    pistes,
    lambda item: agent(
        prompt=(
            f"Lis obligatoirement le skill bmad-deep-recon (SKILL.md) avant de commencer. "
            f"Lis aussi {offre_path}. "
            f"Contexte cible deja identifie: {identification}. "
            f"Execute uniquement la piste {item[0]} ({item[1]}). "
            "Appuie-toi sur des faits publics recents et verifiables. "
            "Distingue explicitement les faits sources des hypotheses de travail. "
            "Redige en francais naturel, voix active, sans tic d'IA ni emoji."
        ),
        schema=piste_schema,
        role=f"Deep Recon {item[0]}",
        model="pro",
    ),
)

# ---------------------------------------------------------------------------
# Phase 1C: Consolidation dans 01_deep_recon.md + mise a jour docs/methodo.md
# ---------------------------------------------------------------------------
phase("Phase 1C: Consolidation et trace methodologique")

consolidation_schema = {
    "type": "object",
    "properties": {
        "file_written": {"type": "string"},
        "methodo_updated": {"type": "boolean"},
        "brainstorming_angles": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["file_written", "methodo_updated", "brainstorming_angles"],
}

run_date = datetime.now().strftime("%Y-%m-%d %H:%M")

synthese = await agent(
    prompt=(
        f"1) Consolide l'identification cible ({identification}) et les 5 pistes Deep Recon "
        f"({resultats_pistes}) dans le fichier {deep_recon_out}. "
        "Structure le document avec: "
        "a) Fiche d'identite de l'entreprise cible et niveau de confiance, "
        "b) Synthese des 5 pistes (MR, DR, CR, TS, UV), "
        "c) Tableau comparatif de 3 a 4 acteurs benchmarkes avec l'enseignement strategique precis, "
        "d) Section finale proposant 5 a 8 angles d'attaque ou sujets a trancher lors du sas "
        "interactif bmad-brainstorming. "
        f"2) Passe obligatoirement le contenu de {deep_recon_out} dans le serveur MCP `ai-remover` "
        "(outils `clean_invisible_unicode`, `analyze_ai_density`, puis `humanize_text` si des "
        "marqueurs IA sont detectes) et reecris le fichier nettoye. "
        f"3) Mets a jour {methodo_log_path}: passe les lignes Temps 1 (Phase 1A et Phase 1B-1C) "
        f"au statut 'Fait' avec la date '{run_date}', renseigne la colonne MCP `ai-remover`, "
        "et ajoute une entree horodatee dans le 'Journal d'execution detaille' listant les skills "
        "et MCP utilises (agent natif, bmad-deep-recon MR/DR/CR/TS/UV, MCP ai-remover) et la "
        "cible identifiee. "
        "Respecte strictement la typographie francaise: accents complets, zero espace avant les "
        "signes doubles, guillemets droits, zero tiret cadratin, zero emoji, pas de listes "
        "artificielles titre-gras-deux-points."
    ),
    schema=consolidation_schema,
    role="Consolidation Deep Recon",
    model="pro",
)

log(f"Livrable pret: {synthese['file_written']}")
log(f"Trace mise a jour dans {methodo_log_path}: {synthese['methodo_updated']}")
log("Angles proposes pour le sas interactif bmad-brainstorming:")
for angle in synthese["brainstorming_angles"]:
    log(f"- {angle}")

print(f"WORKFLOW_01_DONE: {synthese['file_written']}")
