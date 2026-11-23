import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent

# Ordered longest-match-first to avoid partial replacements
REPLACEMENTS = [
    # Target company, legal entities, domains, GitHub orgs, brands
    ("European Camping Group (ECG)", "Opérateur HPA Européen (Client Cible)"),
    ("European Camping Group", "Opérateur HPA Européen"),
    ("European-Camping-Group-Data-Team", "client-cible-data-team"),
    ("ECG TopCo SAS", "Holding Client Cible"),
    ("Homair Vacances SAS", "Filiale France Client Cible"),
    ("VacanceSelect Travel", "Place de marché interne"),
    ("VacanceSelect Connect", "Portail XML partenaires"),
    ("Vacanceselect", "Enseigne acquise V"),
    ("VacanceSelect", "Enseigne acquise V"),
    ("Marvilla Parks", "Marque M"),
    ("Camping Vision", "Place de marché interne"),
    ("Dansk Bilferie", "Portail Nordique A"),
    ("homair.fr", "portail-fr.example"),
    ("homair.pl", "portail-pl.example"),
    ("homair.uk", "portail-uk.example"),
    ("ecg.camp", "client-cible.example"),
    ("Homair", "Marque A"),
    ("Tohapi", "Marque B"),
    ("Eurocamp", "Marque C"),
    ("Alannia", "Resorts Annuels A"),
    ("Roan", "Marque D"),
    ("Allcamps", "Portail E"),
    ("LuxCamp", "Portail F"),
    ("Friferie", "Portail Nordique B"),
    ("ECG", "Client Cible"),

    # People (interviewer, recruiter, executives, vendor staff)
    ("Hugo Rannou", "le Responsable Data"),
    ("HUGO RANNOU", "LE RESPONSABLE DATA"),
    ("HUGO (HEAD OF DATA)", "RESPONSABLE DATA"),
    ("Hugo", "le Responsable Data"),
    ("Noélie", "la Consultante Recrutement"),
    ("Easy Partner", "le cabinet de recrutement"),
    ("Sébastien Manceau", "le Président"),
    ("Philippe de Trémiolles", "le Directeur Financier"),
    ("Amadou Diouldé Baldé", "le VP Digital, Data & IT"),
    ("Aurélien Pioger", "le VP Commercial"),
    ("Quentin Schaepelynck", "le Directeur RM"),
    ("Darren Marsh", "le Responsable Pricing UK"),
    ("Béatrice Tourvieille", "la Directrice Marketing"),
    ("Ross Matthews", "le Directeur Marque UK"),
    ("Ralf de Bruijn", "le Directeur Place de marché"),
    ("Romain Lucas", "le Directeur Exploitation Propre"),
    ("Fernando Garijo", "le Directeur Exploitation Espagne"),
    ("Mathilde Lucas", "la Directrice Partenaires"),
    ("Guillaume Boyer", "la Direction Générale"),
    ("Aude Hiltbrand", "la Direction Financière"),
    ("Marije Zomerdijk", "une responsable programme externe"),
    ("Niels Tailleur", "un responsable programme externe"),
    ("Nicolas Dayot", "la présidence FNHPA"),

    # Shareholders & Investors
    ("PAI Partners", "Fonds majoritaire"),
    ("InfraVia Capital Partners", "Fonds d'infrastructure C"),
    ("InfraVia Capital", "Fonds d'infrastructure C"),
    ("InfraVia", "Fonds d'infrastructure C"),
    ("Corpfin Capital", "Fonds minoritaire espagnol"),
    ("Grupo Marjal", "Groupe hôtelier espagnol"),
    ("Crédit Agricole", "Partenaire bancaire"),
    ("ADIA", "Investisseur minoritaire"),
    ("KKR", "Fonds LBO A"),

    # External pricing vendors & PMS
    ("ORTEC Lumina", "Prestataire algorithmique externe"),
    ("ORTEC", "Prestataire externe"),
    ("#revcamp", "#rm-externe"),
    ("EURODECISION", "Éditeur historique"),
    ("QRUSH", "Moteur historique"),
    ("RevenuePilot", "Module yield PMS"),
    ("Septeo Hospitality", "Éditeur PMS"),
    ("Septeo", "Éditeur PMS"),
    ("Resalys", "PMS central"),
    ("RESALYS", "PMS CENTRAL"),
    ("resalys", "pms_central"),

    # Competitors & OTAs
    ("Landal GreenParks", "Concurrent A (Nord Europe)"),
    ("Roompot", "Concurrent A-bis"),
    ("Landal", "Concurrent A"),
    ("Pierre & Vacances - Center Parcs", "Concurrent B (Résidences & Parcs)"),
    ("Pierre & Vacances", "Concurrent B"),
    ("Center Parcs", "Concurrent B-Parcs"),
    ("PVCP", "Concurrent B"),
    ("maeva&co", "Branche franchise B"),
    ("maeva.com", "portail-b.example"),
    ("Maeva", "Branche B"),
    ("Duetto", "SaaS RMS hôtelier"),
    ("Maxxton", "PMS cloud concurrent"),
    ("Sandaya", "Concurrent C (4-5* propre)"),
    ("Huttopia", "Concurrent D (Nature)"),
    ("Hékipia", "Filiale industrielle D"),
    ("Huttosoft", "Logiciel interne D"),
    ("OnlyCamp", "Enseigne économique D"),
    ("Capfun", "Concurrent E (100 % direct)"),
    ("Groupe PHA", "Groupe E"),
    ("Camping Paradis", "Franchise F"),
    ("Ushuaïa Villages", "Franchise G"),
    ("Mistercamp", "Agrégateur H"),
    ("Booking.com", "OTA majeure"),
    ("Booking Sponsored Benefit", "programme sponsorisé OTA"),
    ("Campings.com", "Comparateur HPA"),
    ("ZEcamping", "Opérateur en ligne"),
    ("ZE-Camping", "Opérateur en ligne"),
    ("HippoCamp", "Baromètre secteur"),
    ("AimerCamper", "Observatoire secteur"),
    ("Camp Boost", "Cabinet RM secteur"),
    ("Revbell", "Éditeur RM secteur"),
    ("PiNCAMP", "Portail européen HPA"),
    ("ACSI", "Guide européen HPA"),
    ("Hilton, IHG, Marriott", "trois chaînes hôtelières"),
    ("STR/CoStar", "un fournisseur de benchmark partagé"),
    ("CMA/STR", "autorité de concurrence"),
    ("Aldi Süd", "jurisprudence CJUE C-330/23"),

    # Candidate past employers (for public GitHub safety)
    ("Interflora", "Acteur européen du e-commerce périssable"),
    ("GL events", "Groupe international événementiel"),
    ("Tyredating Michelin", "Acteur e-commerce automobile"),
    ("Spotify Data Governance", "Cas d'étude Data Governance"),
]

TARGET_FILES = [
    WORKSPACE / "README.md",
    WORKSPACE / "index.html",
    WORKSPACE / "docs" / "methodo.md",
    WORKSPACE / "utils" / "cartoon_explainer.html",
    WORKSPACE / "utils" / "demarche_explainer.html",
    WORKSPACE / "utils" / "transcribe_whisper.py",
    WORKSPACE / "_bmad-output" / "planning-artifacts" / "01_deep_recon.md",
    WORKSPACE / "_bmad-output" / "planning-artifacts" / "02_product_brief.md",
    WORKSPACE / "_bmad-output" / "planning-artifacts" / "03_prfaq.md",
    WORKSPACE / "_bmad-output" / "planning-artifacts" / "04_prd.md",
    WORKSPACE / "_bmad-output" / "planning-artifacts" / "04_prd_v2_asdste100.md",
    WORKSPACE / "_bmad-output" / "planning-artifacts" / "05_architecture.md",
    WORKSPACE / "_bmad-output" / "planning-artifacts" / "06_stress_test.md",
    WORKSPACE / "_bmad-output" / "planning-artifacts" / "07_epics_roadmap.md",
]

AUDIT_TERMS = [
    "European Camping Group", "ECG", "Homair", "Tohapi", "Eurocamp", "Alannia",
    "Vacanceselect", "VacanceSelect", "Marvilla", "Hugo Rannou", "Rannou",
    "Noélie", "Easy Partner", "ORTEC", "QRUSH", "EURODECISION", "Resalys",
    "Septeo", "PAI Partners", "ADIA", "Landal", "Roompot", "PVCP", "Center Parcs",
    "Sandaya", "Huttopia", "Capfun", "Duetto", "Maxxton", "Interflora", "GL events",
    "Manceau", "Trémiolles", "Baldé", "Pioger",
]


def anonymize_text(text: str) -> str:
    # Protect workspace folder name in file:/// links if present
    text = text.replace("TEMPLATE_GENERATE_ROADMAP%20-%20ECG", "__WS_ENC__")
    text = text.replace("TEMPLATE_GENERATE_ROADMAP - ECG", "__WS_RAW__")

    # Specific prefixes/identifiers before word-boundary replacements
    text = re.sub(r"\becg_[a-zA-Z0-9_]+\b", "client_cible_repo", text, flags=re.IGNORECASE)
    text = text.replace("notes_entretien_hugo_rannou.md", "notes_entretien_responsable_data.md")
    text = text.replace("presentation_ecg_v2.pptx", "presentation_pricing_v2.pptx")
    text = text.replace("presentation_ecg.pptx", "presentation_pricing_v2.pptx")
    text = text.replace("demarche_ecg_cartoon.mp4", "demarche_cartoon.mp4")
    text = text.replace("demarche_ecg_cartoon_thumb.png", "demarche_cartoon_thumb.png")
    text = text.replace("demarche_ecg.mp4", "demarche_demo.mp4")
    text = text.replace("demarche_ecg_thumb.png", "demarche_demo_thumb.png")

    for src, dst in REPLACEMENTS:
        if len(src) <= 4 and src.isalpha():
            pattern = re.compile(rf"\b{re.escape(src)}\b", flags=re.IGNORECASE)
        else:
            pattern = re.compile(re.escape(src), flags=re.IGNORECASE)
        text = pattern.sub(dst, text)

    # Restore workspace folder name in local links (or replace with relative links)
    text = text.replace("__WS_ENC__", "TEMPLATE_GENERATE_ROADMAP%20-%20ECG")
    text = text.replace("__WS_RAW__", "TEMPLATE_GENERATE_ROADMAP - ECG")
    return text


def main():
    for path in TARGET_FILES:
        if not path.exists():
            print(f"SKIP (absent): {path.name}")
            continue
        raw = path.read_text(encoding="utf-8")
        cleaned = anonymize_text(raw)
        path.write_text(cleaned, encoding="utf-8")
        print(f"ANONYMIZED: {path.relative_to(WORKSPACE)}")

    # Audit for any remaining leaks (ignoring file:/// workspace folder path names)
    print("\n--- AUDIT ANTI-FUITE ---")
    leaks_total = 0
    for path in TARGET_FILES:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        # Strip workspace folder name from file:/// links during audit
        audit_view = content.replace("TEMPLATE_GENERATE_ROADMAP%20-%20ECG", "WORKSPACE").replace("TEMPLATE_GENERATE_ROADMAP - ECG", "WORKSPACE")
        found = []
        for term in AUDIT_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", audit_view, flags=re.IGNORECASE):
                found.append(term)
        if found:
            leaks_total += len(found)
            print(f"LEAK in {path.relative_to(WORKSPACE)}: {', '.join(found)}")
    if leaks_total == 0:
        print("ZERO_LEAKS_DETECTED")


if __name__ == "__main__":
    main()
