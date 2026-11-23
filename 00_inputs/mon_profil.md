# Career-Ops Profile Configuration
# This is the single source of truth for your personal data across all modes.

candidate:
  full_name: "Caroline Heymes"
  email: "caroline.heymes@gmail.com"
  phone: "0660869466"
  location: "France"
  linkedin: "linkedin.com/in/caroline-heymes/"
  github: "https://github.com/caroheymes"

target_roles:
  # Your North Star roles — what you're optimizing for
  primary:
    - "Data Scientist"
    - "Lead Data Scientist"
    - "Expert IA / Lead IA"
    - "ML Engineer / LLMOps"
    - "Ingénieure Python Scraping & Extraction de données"
    - "Web Scraping / Crawling Engineer"
  # Archetypes help the evaluation system score fit
  archetypes:
    - name: "Web Scraping / Data Extraction Engineer"
      level: "Senior/Staff"
      fit: "primary"
    - name: "Data scientist"
      level: "Senior/Staff"
      fit: "primary"        # primary = dream role, secondary = good fit, adjacent = stretch
    - name: "Lead IA"
      level: "Staff"
      fit: "primary"
    - name: "AI Engineer"
      level: "Staff"
      fit: "secondary"
    - name: "ML Engineer / LLMOps"
      level: "Staff"
      fit: "secondary"
    - name: "Ingénieur en Intelligence Artificielle"
      level: "Staff"
      fit: "adjacent"

narrative:
  # Your professional headline (1 line)
  headline: "Senior Data Scientist & Lead IA | Web Scraping & Extraction à grande échelle (Scrapy, Playwright) | Machine Learning | Gen AI | MLOps (Docker, Kubernetes, Airflow, Ray)"
  # Your exit story — what makes you unique
  exit_story: "Je ne suis pas une data scientist qui découvre le métier en atelier de cadrage. J'ai passé 15 ans côté business avant de coder mes propres modèles. Ça change la manière de poser un problème."
  # Your top 3-5 superpowers
  superpowers:
    - "Web Scraping, Crawling & Extraction documentaire à grande échelle : plateforme de veille 4 pays quasi temps réel (Scrapy, Zyte, Mozenda, Playwright, GraphQL chez Interflora), moteur d'ingestion de 10M+ pages/an (GL events), parsing de PDF et tableaux complexes (MinerU, OCR)"
    - "NLP en production : classification multi-label, SetFit, zero-shot (F1 > 0.85)"
    - "Orchestration, CI/CD, MLOps & Data : standardisation (Docker, GKE, EKS), modélisation & transformation (dbt), automatisation (Airflow, ETL/ELT, Redshift, Glue, Lambda), CI/CD, tests (unitaires & intégration), monitoring & drift (Evidently), gouvernance (DMBOK, MLflow Model Registry)"
    - "Entraînement distribué & Deep Learning : systèmes distribués à grande échelle (Ray, Reinforcement Learning)"
    - "IA générative & Méthodologie BMAD : Très adepte de la méthodologie BMAD (Breakthrough Method of Agile AI-Driven Development) pour orchestrer des agents autonomes (CrewAI, Google ADK) et concevoir des architectures robustes du parsing (MinerU) au RAG."
    - "Modèles à impact mesurable : 500k€ d'économies (géospatial), MAPE 15 % (prévision ventes)"
  # pitch 
  Diplômée d'EM Lyon et titulaire du titre d'Architecte en Intelligence Artificielle (RNCP niveau 7), j'ai passé plus de dix ans en direction d'études chez GL events à analyser les dynamiques d'activité pour le comité de direction, avant de me consacrer pleinement à la data science en production. Chez Interflora, j'ai notamment piloté la prévision des ventes par séries temporelles (Prophet, 15 % de MAPE) sur des pics d'activité extrêmes très proches de la saisonnalité des vacances d'été. J'y ai aussi développé une plateforme d'observation automatisée des prix et promotions de la concurrence sur quatre pays européens, ainsi qu'une solution d'optimisation sous BigQuery et Streamlit dégageant 500 kEUR d'économies annuelles.

Ce projet d'internalisation chez European Camping Group m'intéresse beaucoup parce qu'il ne s'agit pas de faire de la recherche théorique, mais de challenger un algorithme externe en boîte noire, de redonner la maîtrise de la marge aux Revenue Managers et de poser un socle BigQuery et Python industrialisé.

### Pitch 
Mon parcours repose sur un principe simple : un algorithme de tarification n'a de valeur que si les équipes commerciales le comprennent, lui font confiance et constatent une progression réelle de leur chiffre d'affaires.

Chez Interflora, j'ai été confrontée aux mêmes problématiques qu'un opérateur de campings : une activité rythmée par une saisonnalité violente, un stock périssable par nature (une date passée est une vente perdue), et des arbitrages permanents entre volume de commandes et taux de marge. Pour y répondre, j'ai combiné trois approches :
- L'analyse prédictive de la demande via des modèles de régression et de séries temporelles sous Python et scikit-learn.
- La veille tarifaire automatisée de la concurrence pour mesurer l'élasticité réelle face aux offres du marché.
- L'explicabilité des décisions avec des outils comme SHAP, afin que les responsables opérationnels sachent précisément pourquoi le système recommande d'augmenter ou de baisser un tarif.

Reprendre la main sur un prestataire externe exige de la méthode : on ne jette pas un modèle du jour au lendemain. Il faut d'abord poser un cadre d'évaluation contrefactuel pour comparer les gains théoriques du prestataire aux décisions réelles, identifier les biais ou les angles morts de leur solution, puis construire brique par brique des modèles internes sous BigQuery et Docker, validés par des tests A/B rigoureux.

  # Proof points — projects, articles, case studies with measurable impact
  proof_points:
    - name: "Plateforme de veille concurrentielle multi-pays (Interflora)"
      hero_metric: "Infrastructure de scraping résiliente couvrant 4 pays (FR, ES, IT, PT) sous Scrapy, Playwright et GraphQL : suivi quasi temps réel des catalogues, ruptures de stock et promotions par computer vision"
    - name: "Moteur de recherche et d'ingestion interne (GL events)"
      hero_metric: "Scraping et indexation de plus de 10 millions de pages par an pour les équipes M&A, études concurrentielles et ciblage commercial (200+ demandes traitées par an)"
    - name: "LyonFlow — Plateforme MLOps Spatio-Temporelle & Entraînement Distribué"
      url: "https://lyonflow-app.ngrok.io/"
      repo: "https://github.com/caroheymes/Architect-IA-final-project"
      hero_metric: "GNN Spatial Grid, Airflow ETL every 5 min, Distributed HPO via Ray & Optuna, automatic model retraining"
    - name: "Fraud Detection MLOps Pipeline & Drift Auto-Healing"
      url: "https://fraud-detection.ngrok.app/"
      repo: "https://github.com/caroheymes/fraud_detection_pipeline"
      hero_metric: "Inférence temps réel FastAPI & Redis, entraînement distribué Ray Train, détection de drift Evidently AI avec boucle de réentraînement Airflow et gouvernance Champion/Challenger MLflow"
    - name: "AI Remover for Legal, Dev & Copywriters"
      url: "https://ai-remover-for-legal-dev-copywriter.streamlit.app/"
      repo: "https://github.com/caroheymes/ai-remover"
      hero_metric: "Détection et nettoyage des marques et tics stylistiques IA dans les textes juridiques, rédactionnels et de développement (Playwright headless, 46 tests pytest)"
    - name: "Custom OCR Tool"
      url: "https://huggingface.co/spaces/caroms/ocr_tool"
      repo: "https://github.com/caroheymes/custom_ocr_tool"
      hero_metric: "Extraction OCR et parsing de documents complexes et non structurés (PDFs, tableaux, mise en page via MinerU)"
    - name: "Strategic Intelligence Crew — Systèmes Multi-Agents"
      url: "https://github.com/caroheymes/strategic-intelligence-crew"
      repo: "https://github.com/caroheymes/strategic-intelligence-crew"
      hero_metric: "Orchestration multi-agents sous méthodologie BMAD & CrewAI pour la veille et l'analyse stratégique d'aide à la décision"
    - name: "Spotify Data Governance"
      url: "https://github.com/caroheymes/bloc-1-certification-data-architect"
      hero_metric: "Cadre cible DAMA-DMBOK2, ISO 27001, RGPD, structuration des rôles data et sécurisation des flux (Talend, Spark, BigQuery)"
    - name: "Google SERP Ranking Factors (2021)"
      hero_metric: "Modélisation des facteurs de ranking dans le top 10 des SERPs Google (scikit-learn)"
    - name: "Tyredating Michelin SEO Benchmarks"
      hero_metric: "Benchmarks SEO/SEA et backlinks avancés (collecte et analyse de 5000+ mots-clés par pays sur 5 pays)"
  # Optional: dashboard/demo URL with credentials
  dashboard:
    url: "https://lyonflow-app.ngrok.io/"

language:
  primary: fr
  modes_dir: modes/fr

compensation:
  target_range: "$55-65K"     # Your target total comp
  currency: "EUR"
  minimum: "€55"               # Walk-away number (general)
  s

location:
  country: "France"
  city: "Lyon, Paris"
  timezone: "CET"
 