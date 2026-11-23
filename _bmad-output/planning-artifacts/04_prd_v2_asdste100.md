# PRD exécutif (version 2, style contrôlé ASD-STE100): plateforme interne de tarification dynamique d'European Camping Group

Date: 2026-11-23
Version: 2.0 (réécriture selon les principes ASD-STE100 appliqués au français technique)
Statut: Prêt pour revue, architecture (`05_architecture.md`) et tests d'acceptation
Sources: [04_prd.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/_bmad-output/planning-artifacts/04_prd.md), [02_product_brief.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/_bmad-output/planning-artifacts/02_product_brief.md) et [03_prfaq.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/_bmad-output/planning-artifacts/03_prfaq.md)

---

## 1. Règles rédactionnelles et vocabulaire contrôlé

Ce document applique les principes ASD-STE100 pour supprimer toute ambiguïté dans les exigences. Chaque phrase descriptive compte au maximum 25 mots. Chaque exigence fonctionnelle ou non fonctionnelle compte au maximum 20 mots et utilise la voix active. Chaque terme ci-dessous garde un sens unique dans tout le document.

| Terme contrôlé | Définition unique |
| :--- | :--- |
| Le Système | La plateforme interne de tarification dynamique construite sur GCP et BigQuery. |
| Le Modèle interne | L'ensemble formé par le module de prévision et le module d'optimisation d'ECG. |
| Le Modèle externe | L'algorithme tarifaire du prestataire tiers actuellement utilisé par ECG. |
| Le Cockpit | L'interface de consultation et de validation déployée dans Tableau ou Dash. |
| Resalys | Le logiciel transactionnel (CRS-PMS) qui gère l'inventaire, les caches et les ventes. |
| Le Revenue Manager | L'utilisateur métier d'Aix-en-Provence, de Montpellier ou de Breda qui valide les tarifs. |
| Un Débrayage | Toute modification manuelle d'un tarif recommandé par un Revenue Manager. |
| Un Site propre | L'un des 117 campings exploités en propre par ECG (incluant Alannia). |
| Un Site partenaire | L'un des quelque 350 campings tiers hébergeant des mobil-homes ECG en tour-opérateur. |

---

## 2. Objet, périmètre et phases de déploiement

Le Système remplace progressivement le Modèle externe sur plus de 450 destinations européennes. Le Système fonctionne sur GCP et BigQuery. Resalys conserve la gestion des stocks, des caches tarifaires et des passerelles de vente.

Le déploiement suit quatre phases sur 12 mois:
1. Phase 1 (M1 à M3): l'équipe Data réalise l'audit contrefactuel du Modèle externe dans BigQuery.
2. Phase 2 (M3 à M6): le Système exécute le Modèle interne en mode ombre (shadow mode) sans publication.
3. Phase 3 (M6 à M9): le Système bascule des segments pilotes en production selon un protocole Champion/Challenger.
4. Phase 4 (M9 à M12+): ECG retire le Modèle externe, couvre tout le parc et ajoute la veille tarifaire.

Le périmètre exclut quatre éléments:
1. Toute réécriture du PMS Resalys.
2. Toute gestion des plans de parcelles ou de l'inventaire physique.
3. Tout serveur d'inférence temps réel permanent hors cycle batch.
4. Tout calcul de prix personnalisé à partir de données personnelles.

---

## 3. Grille de scoring sur 100 points

L'équipe utilise cette grille pour classer chaque segment ou lot fonctionnel avant sa mise en production.

| Axe | Points maximum | Critères mesurés |
| :--- | :--- | :--- |
| Impact marge nette et RevPAC | 35 | Gain estimé en Net RevPAC HT et correction d'un biais prouvé du Modèle externe. |
| Adoptabilité Revenue Management | 25 | Baisse attendue du Débrayage, clarté SHAP et simplicité d'usage à Aix, Montpellier et Breda. |
| Faisabilité data et sobriété MLOps | 25 | Disponibilité des données dans BigQuery et maintien en batch par l'équipe de 12 à 15 experts. |
| Maîtrise des risques et conformité | 15 | Repli rapide vers Resalys, conformité juridique (Omnibus, art. L. 221-5, DMA, AI Act). |

### Seuils de décision
1. Score supérieur ou égal à 75/100: statut Go (exécution immédiate sur le trimestre).
2. Score entre 55 et 74/100: statut Backlog (attente d'une levée de dépendance).
3. Score inférieur à 55/100: statut No-Go (rejet du plan à 12 mois).

### Critères éliminatoires (veto immédiat)
1. Le lot prévoit une première mise en production en juin, juillet ou août.
2. Le lot utilise un identifiant client ou une donnée personnelle en entrée du modèle.
3. Le lot ne dispose d'aucun historique permettant un test Champion/Challenger.
4. Le lot ne permet pas un retour aux grilles Resalys en moins de 2 heures.
5. Le lot branche un agent conversationnel sur BigQuery sans couche sémantique gouvernée.

---

## 4. Exigences fonctionnelles (FR)

Chaque exigence décrit une action unique et vérifiable du Système.

### Capacité A: audit contrefactuel et socle BigQuery (M1 à M3)
FR-01: Le Système ingère chaque jour les réservations, stocks, prix publiés et restrictions depuis Resalys vers BigQuery.
FR-02: Le Système ingère chaque jour l'historique des prix recommandés par le Modèle externe dans BigQuery.
FR-03: Le Système compare les prix du Modèle externe, les prix publiés et le RevPAC réalisé par segment.
FR-04: Dataform construit des tables de features versionnées incluant le booking pace N-1 et N-2 par horizon.
FR-05: Dataform intègre le délai de réservation par pays, les calendriers scolaires et les taux de TVA locaux.
FR-06: Dataform rejette automatiquement toute table contenant une donnée personnelle identifiable (nom, email, cookie, ID client).

### Capacité B: prévision de demande et élasticité (M3 à M6)
FR-07: Le Modèle interne prévoit la demande par site, gamme, date et durée (semaine et court séjour).
FR-08: Le module de décontraction corrige la censure à 100 % d'occupation grâce aux recherches sans disponibilité (Tealium/GA4).
FR-09: Le Modèle interne estime l'élasticité sur le prix TTC client, frais obligatoires inclus.
FR-10: Le Système convertit chaque prix TTC en revenu net HT après TVA locale, taxe de séjour et commission.
FR-11: Le pipeline d'entraînement sépare les observations issues d'un Débrayage pour protéger la courbe d'élasticité.
FR-12: Pour chaque nouvelle acquisition, le Modèle interne initialise les prévisions en moins de 14 jours via des sites jumeaux.

### Capacité C: optimisation à double fonction objectif (M3 à M9)
FR-13: Sur un Site propre, l'optimiseur maximise le revenu total HT incluant les 12 % de dépenses annexes estimées.
FR-14: Sur un Site partenaire, l'optimiseur maximise la marge nette HT après loyer garanti, ménage et commission.
FR-15: L'optimiseur applique les prix planchers partenaires et les bornes quotidiennes de variation tarifaire.
FR-16: L'optimiseur borne les écarts de prix entre portails pays et applique les grilles CSE (Coup par Coup, Bouquet, Linéaire).
FR-17: L'optimiseur calcule les restrictions MinLOS, CTA et CTD pour combler les interstices du calendrier.
FR-18: Le Système archive sur 30 jours glissants le prix le plus bas pratiqué pour la conformité Omnibus.

### Capacité D: cockpit explicable, gouvernance et publication (M3 à M12)
FR-19: Le Cockpit affiche la décomposition SHAP de chaque prix recommandé et son intervalle de confiance.
FR-20: Le Cockpit fournit un simulateur permettant au Revenue Manager de tester un prix alternatif avant validation.
FR-21: Hors juillet et août, le Système publie automatiquement les variations situées dans la bande de tolérance convenue.
FR-22: En juillet et août, le Système exige une validation humaine avant toute publication de prix.
FR-23: Pour chaque Débrayage, le Cockpit impose la sélection d'un motif structuré en une ligne.
FR-24: Le Système pousse les tarifs validés vers Resalys par lots via le connecteur 2-ways.
FR-25: Le Système déclenche un pré-chauffage des caches `semainier` et `journalier` après chaque lot d'écriture Resalys.
FR-26: Le module Champion/Challenger suit chaque mois les écarts de Net RevPAC, de marge et de Débrayage entre modèles.
FR-27: En Phase 4, le Système collecte uniquement des prix concurrents publics affichés sur les marchés européens.
FR-28: En Phase 4, le Système expose une couche sémantique BigQuery avant tout assistant conversationnel (mention AI Act art. 50).

---

## 5. Exigences non fonctionnelles (NFR)

### Performance et cadence
NFR-01: Le batch quotidien complet s'exécute en moins de 90 minutes et termine avant 07h30 CET.
NFR-02: Chaque vue régionale du Cockpit charge en moins de 5 secondes sans dépendre de BigQuery BI Engine.
NFR-03: Le module d'écriture Resalys respecte la latence API (4 secondes hors cache) par discrétisation en lots.

### Fiabilité et sobriété MLOps
NFR-04: Le Système utilise uniquement BigQuery, Dataform, Cloud Workflows, Cloud Run Jobs, Docker, Terraform et GitHub Actions.
NFR-05: Le Système exclut tout Feature Store temps réel permanent et tout cluster GKE actif 24h/24.
NFR-06: Le Système archive le code, les features, le modèle et les paramètres de chaque prix pendant 24 mois.
NFR-07: Une sonde hebdomadaire mesure la dérive des données (data drift) et l'erreur MAPE/WAPE par segment.
NFR-08: L'équipe peut restaurer les grilles de sécurité Resalys en moins de 2 heures sans coupure de vente.

### Sécurité et conformité
NFR-09: Le Système traite zéro donnée personnelle identifiable dans le pipeline de tarification (conformité RGPD et art. L. 221-5).
NFR-10: Le Système applique un contrôle d'accès par rôle (RBAC) par zone (Aix, Montpellier, Breda) et journalise chaque action.

---

## 6. North-Star Metric, contre-métriques et kill-switches

### North-Star Metric
La métrique directrice est la **marge nette contributive HT par emplacement disponible (Net RevPAC contributif)**. Sur un Site propre, elle additionne l'hébergement net HT et les 12 % d'annexes estimées. Sur un Site partenaire, elle soustrait le loyer garanti, le ménage et les commissions du revenu hébergement net HT. L'objectif à M+12 est une hausse mesurée de +3 % à +5 % sur les segments basculés.

### Contre-métriques
La hausse de la North-Star Metric est validée uniquement si les cinq seuils ci-dessous restent respectés.

| Contre-métrique | Mesure | Seuil d'alerte |
| :--- | :--- | :--- |
| Taux de Débrayage | Part des recommandations modifiées par les Revenue Managers | Supérieur à 25 % en régime normal (ou >5 % sans motif) |
| Occupation ailes de saison | Taux d'occupation en mai, juin et septembre | Recul supérieur à 3 points face au groupe témoin |
| Parité catalogue vs checkout | Écart entre prix de recherche et prix au paiement | Supérieur à 0,5 % des sessions |
| Volatilité et écarts pays | Variation journalière et dispersion entre portails pays | Dépassement des bornes fixées par marque |
| Signal client et partenaire | Avis 1-2 étoiles citant le prix et litiges partenaires | Hausse significative sur 2 semaines consécutives |

### Kill-switches (arrêt automatique et repli)
Le Système suspend la publication automatique vers Resalys et bascule sur les grilles de sécurité dès qu'une condition ci-dessous survient:
1. Kill-switch financier: le Net RevPAC ou le booking pace chute de plus de 5 % sur 14 jours face au groupe témoin, hors événement météo ou incendie documenté.
2. Kill-switch intégrité: le Système détecte un prix hors bornes, un taux de TVA erroné ou un écart cache-checkout supérieur à 1 %.
3. Kill-switch adoption: le taux de Débrayage dépasse 40 % pendant 7 jours consécutifs sur un segment en production.
4. Kill-switch conformité et data: le Système détecte une donnée personnelle, un retard Resalys supérieur à 24 heures ou une erreur sur la table Omnibus 30 jours.

---

## 7. Annexe technique de modélisation, explicabilité SHAP et hyperparamètres

### 7.1 Explicabilité locale par valeurs SHAP
Une valeur SHAP mesure la contribution exacte d'une variable à une prédiction précise. Le calcul part d'une valeur de référence égale au prix moyen ou à la demande moyenne. Chaque variable ajoute ou retire un montant précis à cette référence. La somme de la référence et de toutes les valeurs SHAP égale exactement la prédiction du Modèle interne.

Le Cockpit affiche cette décomposition pour chaque camping, chaque gamme et chaque semaine. Le Revenue Manager vérifie la logique locale en dix secondes avant de valider ou de créer un Débrayage.

### 7.2 Familles de modèles et hyperparamètres principaux

#### Random Forest (RF, Forêts aléatoires)
Le modèle entraîne plusieurs centaines d'arbres en parallèle sur des sous-échantillons aléatoires. La prédiction finale calcule la moyenne des arbres. Cette famille réduit la variance et résiste au bruit.

| Hyperparamètre | Rôle exact | Pourquoi le régler |
| :--- | :--- | :--- |
| `n_estimators` | Fixe le nombre total d'arbres dans la forêt. | Stabilise la variance des prédictions sans provoquer de surapprentissage. |
| `max_depth` | Limite la profondeur maximale de chaque arbre. | Empêche les arbres de mémoriser les anomalies isolées d'une saison. |
| `min_samples_leaf` | Impose un nombre minimum d'observations par feuille finale. | Lisse les prédictions sur les petits campings à faible volume. |
| `max_features` | Fixe la part de variables testées à chaque coupure. | Décorrèle les arbres et réduit la variance globale du modèle. |
| `max_samples` | Fixe la taille de l'échantillon tiré pour chaque arbre. | Accélère le batch quotidien et limite la sensibilité aux valeurs extrêmes. |

#### XGBoost (Extreme Gradient Boosting)
Le modèle entraîne des arbres séquentiels où chaque arbre corrige les erreurs résiduelles des précédents. Cette famille offre une précision élevée sur données tabulaires et calcule les valeurs SHAP rapidement via TreeSHAP.

| Hyperparamètre | Rôle exact | Pourquoi le régler |
| :--- | :--- | :--- |
| `learning_rate` (`eta`) | Réduit le poids ajouté par chaque nouvel arbre. | Empêche le modèle d'apprendre trop vite sur le bruit estival. |
| `n_estimators` | Fixe le nombre maximal d'arbres séquentiels. | Contrôle la capacité d'apprentissage en lien direct avec `learning_rate`. |
| `max_depth` | Limite la profondeur maximale de chaque arbre. | Contrôle le degré d'interaction autorisé (ex. nationalité x délai x TVA). |
| `min_child_weight` | Fixe la somme minimale de poids dans une feuille. | Bloque la création de règles tarifaires sur trop peu de réservations. |
| `subsample` | Fixe la fraction des lignes utilisée par chaque arbre. | Réduit le surapprentissage et stabilise le modèle face aux chocs ponctuels. |
| `colsample_bytree` | Fixe la fraction des variables tirée pour chaque arbre. | Évite qu'une seule variable dominante (ex. prix N-1) n'écrase les autres signaux. |
| `reg_alpha` (L1) et `reg_lambda` (L2) | Appliquent une pénalité sur les poids des feuilles. | Élimine les variables inutiles (L1) et lisse les sauts brusques de prix (L2). |
| `gamma` | Impose un gain minimal de perte avant toute coupure. | Empêche les découpages inutiles qui complexifient l'arbre sans gain réel. |

#### Random Fourier Features (RFF, approximation de noyaux)
Cette méthode projette les variables dans un espace aléatoire de fonctions sinusoïdales pour transformer un modèle non linéaire en modèle linéaire rapide. En tarification tabulaire, le Système privilégie XGBoost, mais ce tableau couvre le réglage RFF si un modèle à noyau sert de référence.

| Hyperparamètre | Rôle exact | Pourquoi le régler |
| :--- | :--- | :--- |
| `n_components` | Fixe le nombre de projections aléatoires (dimension cible). | Arbitre directement entre qualité d'approximation du noyau et temps de calcul. |
| `gamma` | Règle la largeur du noyau gaussien (RBF). | Contrôle la sensibilité locale aux variations de prix et de calendrier. |
| `alpha` (régularisation Ridge) | Pénalise la norme des coefficients du modèle linéaire final. | Empêche le surapprentissage lorsque `n_components` devient élevé. |
| `random_state` | Fixe la graine du tirage aléatoire des fréquences. | Garantit la reproductibilité stricte du modèle pour l'audit sur 24 mois. |

### 7.3 Protocole d'optimisation des hyperparamètres
L'équipe Data exécute le réglage des hyperparamètres en cinq étapes strictes:
1. Découper l'historique par ordre chronologique avec une validation croisée temporelle (`TimeSeriesSplit`) pour interdire toute fuite du futur.
2. Mesurer l'erreur avec une métrique alignée sur la marge (WAPE ou RMSE pondérée par le chiffre d'affaires).
3. Explorer les combinaisons par optimisation bayésienne (`Optuna`) afin de converger en moins d'essais qu'une grille exhaustive.
4. Activer l'arrêt anticipé (`early_stopping_rounds`) pour stopper l'entraînement dès que l'erreur de validation cesse de baisser.
5. Vérifier le modèle retenu sur une saison ou une période de test jamais vue avant toute mise en mode ombre.
