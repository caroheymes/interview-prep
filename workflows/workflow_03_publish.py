"""
Workflow 03: Publication GitHub publique (dossier `github/`).

Dissociation stricte entre la racine et `github/`:
    - `./index.html` (a la racine): reste 100% NON ANONYMISE et 100% DEVERROUILLE en clair
      des l'ouverture (usage interne / soutenance en entretien).
    - `./github/index.html`: version publique ANONYMISEE de la slide 1 a 15 (aucun nom de
      l'entreprise cible, de ses marques, dirigeants, partenaires ou reseaux membres) ET
      IRREVERSIBLEMENT VERROUILLEE des la slide 5 via `workflows/caviarder-presentation.mjs`
      (SHA-256 dans le DOM sur paragraphes, listes, KPIs, badges, bannieres et colonnes 2..N
      des tableaux; suppression du bouton [U], du raccourci clavier U et de la lightbox HD;
      floutage verrouille du schema sur la slide d'architecture; blocage print PDF).
    - `./github/architecture.png`: copie du schema (si present et anonymise visuellement).
    - `./github/README.md`: vitrine publique 100% anonymisee avec appel a prise de contact.
    - Mise a jour de `docs/methodo.md` (Temps 4 / Phase 6).

Usage via Antigravity (`run_workflow`):
    Args:
        dossier (str): Chemin absolu du dossier mission. Par defaut, premier workspace actif.
        start_slide (int): Numero de la premiere slide a verrouiller/caviarder (defaut: 5).
        keep_cols (int): Nombre de colonnes de tableau laissees en clair comme ossature (defaut: 1).
"""

import json
import os
import re
import shutil
import subprocess
from datetime import datetime

dossier = (args.get("dossier") or (WORKSPACES[0] if WORKSPACES else ".")).replace("\\", "/").rstrip("/")
start_slide = int(args.get("start_slide", 5))
keep_cols = int(args.get("keep_cols", 1))

inputs_dir = f"{dossier}/00_inputs"
artifacts_dir = f"{dossier}/_bmad-output/planning-artifacts"
github_dir = f"{dossier}/github"

script_caviardage = f"{dossier}/workflows/caviarder-presentation.mjs"
source_html = f"{dossier}/index.html"
public_html = f"{github_dir}/index.html"
source_arch = f"{dossier}/architecture.png"
public_arch = f"{github_dir}/architecture.png"
public_readme = f"{github_dir}/README.md"
anon_map_path = f"{artifacts_dir}/08_anonymize_map.json"
methodo_log_path = f"{dossier}/docs/methodo.md"

os.makedirs(github_dir, exist_ok=True)
os.makedirs(artifacts_dir, exist_ok=True)
log(f"Demarrage Workflow 03 (Publication GitHub anonymisee et verrouillee) sur: {dossier}")

# ---------------------------------------------------------------------------
# Phase 6A: Verification index.html racine en clair + dictionnaire d'anonymisation
# ---------------------------------------------------------------------------
phase("Phase 6A: Preparation index.html racine en clair et table d'anonymisation")

# S'assurer que ./index.html a la racine est 100% en clair et NON BLURRE (aucun flou actif)
if os.path.exists(source_html):
    with open(source_html, "r", encoding="utf-8") as f:
        root_html_content = f.read()

    # 1. Neutraliser le CSS de flou
    clean_html = re.sub(
        r"/\*\s*Teaser Blur System[\s\S]*?body\.unlock-all-teasers\s+\.teaser-blur\s+\.teaser-badge\s*\{[\s\S]*?\}",
        """/* Mode entretien: contenu integralement en clair sans aucun flou */
.teaser-blur .blur-target,
.blur-target {
    filter: none !important;
    opacity: 1 !important;
    user-select: auto !important;
}
.teaser-badge,
#teaserToggleBtn {
    display: none !important;
}""",
        root_html_content,
    )
    # 2. Supprimer les classes de flou
    clean_html = re.sub(r"\bteaser-blur\b", "", clean_html)
    clean_html = re.sub(r"\bblur-target\b", "", clean_html)
    # 3. Supprimer les badges teaser et les infobulles de deverrouillage
    clean_html = re.sub(r'<span class="teaser-badge">[\s\S]*?</span>', "", clean_html)
    clean_html = re.sub(r'\s*title="Cliquer pour dévoiler[^"]*"', "", clean_html)
    # 4. Supprimer le bouton [U] Mode seance
    clean_html = re.sub(r'<button\b[^>]*\bid="teaserToggleBtn"[^>]*>[\s\S]*?</button>', "", clean_html)
    # 5. Nettoyer les attributs de classes et body
    clean_html = re.sub(r'\bunlock-all-teasers\b', "", clean_html)
    clean_html = re.sub(r'class="\s+', 'class="', clean_html)
    clean_html = re.sub(r'\s+"', '"', clean_html)
    clean_html = re.sub(r'class=""\s*', '', clean_html)

    if clean_html != root_html_content:
        with open(source_html, "w", encoding="utf-8") as f:
            f.write(clean_html)
        log("index.html racine configure en lecture 100% claire et NON BLURRE (flou neutralise).")

anon_schema = {
    "type": "object",
    "properties": {
        "map_file": {"type": "string"},
        "rules_count": {"type": "integer"},
        "forbidden_terms": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["map_file", "rules_count", "forbidden_terms"],
}

anon_res = await agent(
    prompt=(
        f"Lis {source_html}, {inputs_dir}/offre.md, {artifacts_dir}/01_deep_recon.md et {inputs_dir}/mon_profil.md. "
        f"Construis et ecris dans {anon_map_path} un fichier JSON strict contenant deux cles: "
        "1) `replacements`: tableau d'objets `{\"from\": \"...\", \"to\": \"...\"}` couvrant TOUTES les "
        f"mentions identifiantes presentes dans {source_html} (balise <title>, topbar .deck-brand, "
        "slides 1 a 15, titres h1/h2/h3, sous-titres, cartes, tableaux, footers, attributs alt/title): "
        "nom de l'entreprise cible (toutes casses: majuscules, minuscules, domaine web, SIREN), "
        "noms de son partenaire technologique ou editeur affilie, codes d'agrement specifiques "
        "(ex. numero exact de Plateforme Agreee), assistants proprietaires du partenaire, noms de "
        "dirigeants, et noms des cabinets/filiales associes. Remplace chaque terme par un equivalent "
        "sectoriel generique fluide et grammaticalement naturel en francais (ex. 'Consortium Data Comptable', "
        "'CONSORTIUM DATA COMPTABLE', 'l\\'operateur cloud partenaire', 'la Plateforme Agreee partenaire', "
        "'l\\'assistant interne partenaire', 'un groupe europeen'). "
        "IMPORTANT: NE REMPLACE PAS le nom de la candidate ni ses coordonnees publiques issus de "
        f"{inputs_dir}/mon_profil.md, ni les references publiques purement reglementaires ou "
        "benchmark international (CNOEC, La Source, DATEV, Validis, Xero, Snowflake, AWS, Power BI) "
        "sauf lorsqu'un acteur international est cite nommement comme actionnaire identifiant le partenaire. "
        "2) `forbidden_terms`: tableau de chaines listant tous les noms propres interdits (entreprise cible, "
        "domaine, SIREN, partenaire technologique, numero PA exact, assistant partenaire, dirigeants, "
        "cabinets membres) qui doivent avoir 0 occurrence dans github/index.html et github/README.md."
    ),
    schema=anon_schema,
    role="Table anonymisation HTML",
    model="pro",
)

log(f"Table d'anonymisation prete ({anon_res['rules_count']} regles): {anon_res['map_file']}")

# ---------------------------------------------------------------------------
# Phase 6B: Generation de github/index.html anonymise et verrouille + architecture.png
# ---------------------------------------------------------------------------
phase("Phase 6B: Anonymisation et verrouillage cryptographique de github/index.html")

if os.path.exists(public_html):
    try:
        os.remove(public_html)
    except OSError:
        pass

proc = subprocess.run(
    [
        "node",
        script_caviardage,
        "--input",
        source_html,
        "--output",
        public_html,
        "--start-slide",
        str(start_slide),
        "--keep-cols",
        str(keep_cols),
        "--anonymize-map",
        anon_map_path,
    ],
    capture_output=True,
    text=True,
    check=False,
)

if proc.returncode != 0:
    log(f"Alerte 1re passe caviardage: {proc.stderr or proc.stdout}. Correction auto de la table...")
    await agent(
        prompt=(
            f"L'execution de {script_caviardage} a signale une fuite residuelle: {proc.stderr or proc.stdout}. "
            f"Inspecte {source_html} et enrichis {anon_map_path} (`replacements`) pour eliminer "
            "integralement les termes signales sans casser le HTML ni le JS."
        ),
        role="Correction fuite anonymisation",
        model="pro",
    )
    if os.path.exists(public_html):
        try:
            os.remove(public_html)
        except OSError:
            pass
    proc = subprocess.run(
        [
            "node",
            script_caviardage,
            "--input",
            source_html,
            "--output",
            public_html,
            "--start-slide",
            str(start_slide),
            "--keep-cols",
            str(keep_cols),
            "--anonymize-map",
            anon_map_path,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Echec verrouillage/anonymisation ({proc.returncode}): {proc.stderr or proc.stdout}")

log(f"github/index.html anonymise et verrouille: {proc.stdout.strip()}")

has_arch_png = os.path.exists(source_arch) and os.path.getsize(source_arch) > 0
if has_arch_png:
    shutil.copy2(source_arch, public_arch)
    log(f"Schema copie vers: {public_arch}")
else:
    log("Aucun architecture.png non vide trouve a la racine (etape copie ignoree).")

# ---------------------------------------------------------------------------
# Phase 6C: Generation de github/README.md 100% anonymise + trace methodo.md
# ---------------------------------------------------------------------------
phase("Phase 6C: Redaction github/README.md anonymise et trace")

readme_schema = {
    "type": "object",
    "properties": {
        "file_written": {"type": "string"},
        "anonymized_terms": {"type": "array", "items": {"type": "string"}},
        "company_leak_check": {"type": "string"},
    },
    "required": ["file_written", "anonymized_terms", "company_leak_check"],
}

run_date = datetime.now().strftime("%Y-%m-%d %H:%M")

readme_res = await agent(
    prompt=(
        f"Lis {dossier}/README.md (s'il existe), {anon_map_path}, {artifacts_dir}/01_deep_recon.md, "
        f"{artifacts_dir}/02_product_brief.md, {artifacts_dir}/05_architecture.md, "
        f"{artifacts_dir}/07_epics_roadmap.md et {inputs_dir}/mon_profil.md. "
        f"Redige une version publique 100% ANONYMISEE dans {public_readme}. "
        "Regles strictes d'anonymisation: "
        f"1) Aucun des termes listes dans `forbidden_terms` de {anon_map_path} ne doit apparaitre "
        "(entreprise cible, marques, partenaire technologique, numero PA, dirigeants, reseaux membres). "
        "Utilise un descripteur sectoriel generique coherent avec `github/index.html`. "
        "2) Explique l'approche methodologique (BMad, cadrage executif, architecture cible, "
        "gestion des risques, feuille de route 12 mois) sans livrer les secrets d'execution "
        "verrouilles dans le deck. "
        f"3) Indique clairement que les slides 1 a {start_slide - 1} de `index.html` sont "
        f"consultables en version anonymisee et que les slides {start_slide} a 15 sont "
        "irreversiblement verrouillees et caviardees en SHA-256 (version complete non anonymisee "
        "presentee uniquement en entretien). "
        f"4) Presence du schema architecture.png dans github/: {has_arch_png}. "
        "Si True, affiche `![Architecture cible](./architecture.png)` avec une legende "
        "generique anonymisee. Si False, n'insere pas d'image cassee. "
        "5) Termine par une section 'Prendre contact' avec les coordonnees publiques issues de "
        f"{inputs_dir}/mon_profil.md (LinkedIn, GitHub, email) pour demander la presentation complete. "
        "6) Verifie ZERO occurrence de `forbidden_terms` dans `github/README.md` ET dans "
        "`github/index.html`, puis passe obligatoirement "
        f"{public_readme} dans le serveur MCP `ai-remover` (`clean_invisible_unicode`, "
        "`analyze_ai_density`, `humanize_text` si marqueurs detectes) et reecris le fichier nettoye. "
        f"7) Mets a jour {methodo_log_path}: passe la ligne Temps 4 (Phase 6 Publication GitHub) "
        f"au statut 'Fait' avec la date '{run_date}', renseigne la colonne MCP `ai-remover`, "
        "et ajoute une entree horodatee dans le 'Journal d'execution detaille' "
        "(dissociation index.html racine en clair non anonymise vs github/index.html anonymise "
        "1-15 et verrouille SHA-256 des slide 5 + github/README.md anonymise + MCP ai-remover). "
        "Respecte strictement la typographie francaise: accents complets, zero espace avant les "
        "signes doubles, guillemets droits, zero tiret cadratin, zero emoji, pas de listes "
        "artificielles titre-gras-deux-points."
    ),
    schema=readme_schema,
    role="Publication README anonymise",
    model="pro",
)

log(f"README public anonymise ecrit: {readme_res['file_written']}")
log(f"Verification fuite entreprise: {readme_res['company_leak_check']}")
print(f"WORKFLOW_03_DONE: {public_html} | {public_readme}")
