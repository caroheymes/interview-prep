# Extraction structurée de l'entretien avec Hugo Rannou (ECG)

Date: 2026-11-23
Participants: Hugo Rannou (Responsable de l'équipe Data, ECG), Noélie (Easy Partner), Caroline Heymes
Sources: [entretien.mp4](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/00_inputs/entretien.mp4) et transcription Whisper complète [whisper_raw.txt](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/00_inputs/whisper_raw.txt) (33 min 36 s, 200 segments)

---

## 1. Profil de l'interlocuteur et suite du processus

Hugo Rannou est Responsable de l'équipe Data chez ECG (diplômé de Centrale Lyon, lien naturel établi avec EM Lyon). Son équipe est transverse (Data Engineers, Data Analysts, Data Scientists) et couvre toute la chaîne, de l'ingestion jusqu'à l'exposition BI et ML pour le marketing stratégique, le board, le commerce, les opérations terrain et la gestion de la flotte de mobil-homes.

Prochaine étape annoncée par Noélie en début d'appel: envoi d'un test technique à réaliser chez soi (planifié en début de semaine prochaine), suivi d'un débriefing avec l'équipe technique.

---

## 2. Faits techniques et métier confirmés en séance

### Stack et maturité Data
1. Système central de réservation: Resalys (progiciel tiers non possédé par ECG).
2. Data Warehouse: BigQuery structuré en architecture médaillon (mise en place récente; niveau jugé solide pour le secteur, sans avance particulière sur tous les design patterns).
3. Usage dominant actuel: BI (rapports industrialisés et analyses ad hoc). Les briques ML "classiques" (pricing, recommandation web) manquent encore et représentent la priorité d'Hugo au-delà de l'effet de mode IA générative.
4. Service client / Call center: ECG a répondu aux pics saisonniers par un voicebot IA plutôt que par une prévision de volume pour ajuster le staffing.

### Prestataire externe et réalité du mandat (nuance clé)
1. Le prestataire externe est confirmé: il s'agit bien d'ORTEC (cabinet de conseil néerlandais en mathématiques et logistique), qui a co-construit le moteur de recommandation de prix lorsque ECG manquait de maturité interne.
2. Nuance stratégique majeure: Hugo ne vise pas un remplacement brutal d'ORTEC dès le premier jour. Il reconnaît que l'outil "fait une bonne partie du boulot", mais juge ECG insatisfait sur l'automatisation fiable d'une partie raisonnable du périmètre.
3. Le poste (environ 80 % sur le pricing, 20 % sur les routines et pipelines d'équipe) suit deux étapes: d'abord l'analyse rétrospective approfondie des décisions passées et le challenge de l'élasticité-prix; ensuite la construction d'un contrepoids interne capable de challenger les recommandations d'ORTEC et, le cas échéant, d'aider à les améliorer.

### Données disponibles et granularité du pricing
1. Traçabilité confirmée: ECG a journalisé quotidiennement l'historique des prix recommandés par ORTEC ET les prix réellement appliqués sur le site. Il est donc possible de mesurer exactement si une recommandation a été suivie, suivie en direction ou inversée.
2. Granularité: un prix est défini par Produit (typologie de mobil-home, ex. 3 chambres climatisé) x Camping x Semaine de séjour (avril à fin octobre), révisable chaque jour (environ 218 jours ouvrés d'activité des priceurs).
3. Périmètre géographique et parc: quatre grilles de prix par marché (FR/IT/ES regroupés, Pays-Bas, UK et Allemagne), couvrant à la fois les sites en propre et les sites partenaires (où ECG loue des parcelles, par exemple 50 emplacements, et y déploie ses propres mobil-homes sans contrôle sur les équipements du camping).
4. Périmètre revenus: le yield porte aujourd'hui uniquement sur l'hébergement locatif (pas de yield F&B), avec un début de tarification dynamique sur les ancillaries (suppléments autour du séjour, comme les animaux). Les questionnaires de satisfaction clients sur sites propres constituent déjà un flux important.

### Angles morts reconnus par Hugo
1. Données exogènes quasi absentes: ni la météo, ni Google Trends / volumes de recherche, ni les prix concurrents de proximité, ni le prix du carburant ne sont intégrés aujourd'hui dans le modèle. Hugo qualifie cette absence d'"un des défauts majeurs du modèle".
2. Sous-exploitation des séries temporelles: l'approche actuelle reste centrée sur la vitesse de pick-up récent et n'exploite pas assez la saisonnalité en time series. Or Hugo observe un fort drift comportemental sur les trois dernières années (glissement d'achats très anticipés vers du last minute qui stresse le business), un report géographique "coolcation" (la Côte d'Azur en plein été performe moins bien que prévu) et un étalement vers les ailes de saison.
3. Arbitrage inter-grilles non mesuré: ECG n'a jamais mesuré le volume de clients contournant leur grille nationale (ex. clients britanniques réservant sur `homair.fr` ou `homair.pl`).
4. Expérimentation A/B jamais réalisée en production: la contrainte légale interdisant d'afficher deux prix différents pour le même produit au même moment bloque l'A/B test web classique. L'idée de clusteriser des campings jumeaux (localisation, prestations, prix) pour tester un modèle A contre un modèle B a été validée par Hugo ("on y a pensé, on n'a pas encore fait ça, c'est une bonne idée").
5. Règles légales citées par Hugo: directive Omnibus (prix barré constaté sur les 30 derniers jours) et unicité du prix affiché pour un même produit.

---

## 3. Points d'attention pour le test technique et le débriefing

1. Modélisation à maîtriser pour le test technique: prévision de demande / élasticité sur données tabulaires (XGBoost, Random Forest) ET approche séries temporelles (Prophet avec régresseurs exogènes comme jours fériés et tendances de recherche), puisque Hugo a explicitement réagi positivement à la comparaison d'erreurs entre XGBoost et Prophet.
2. Analyse rétrospective des prix: préparer une méthode propre pour comparer prix recommandé vs prix appliqué (taux de suivi, taux d'inversion, écart directionnel, impact sur le pick-up et le revenu).
3. Protocole d'expérimentation sans A/B test individuel: savoir expliquer en deux minutes le clustering de campings comparables (appariement sur caractéristiques et historique) pour comparer une V1 (ORTEC) et une V2 (interne) sans enfreindre l'unicité du prix.
4. Posture attendue avec l'équipe technique: rester pragmatique et constructif vis-à-vis d'ORTEC (contrepoids chiffré et montée en maturité interne, plutôt que discours dogmatique de rupture brutale) et ancrer chaque choix dans la mesure de l'erreur et l'explicabilité pour les priceurs.
