# Product brief: actif tarifaire interne, explicable et résilient pour Opérateur HPA Européen (Client Cible)

Date: 2026-11-23
Statut: Validé pour enchaînement vers PRFAQ (`03_prfaq.md`) et PRD (`04_prd.md`)
Rôle analyste: Mary (`bmad-agent-analyst` / `bmad-product-brief`)
Sources: [offre.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/00_inputs/offre.md), [01_deep_recon.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/_bmad-output/planning-artifacts/01_deep_recon.md), [mon_profil.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/00_inputs/mon_profil.md) et arbitrages validés en Étape 2.1 dans [methodo.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/docs/methodo.md)

---

## 1. Résumé exécutif et thèse produit

Opérateur HPA Européen (Client Cible) exploite plus de 450 destinations en Europe (117 campings en propre et près de 350 sites partenaires en tour-opérateur, 48 000 mobil-homes, 813 M€ de chiffre d'affaires 2025, 91 % de ventes directes). Le groupe confie aujourd'hui ses recommandations tarifaires quotidiennes à un algorithme externe. Cette dépendance freine sa capacité à piloter sa marge sur un parc en consolidation rapide (5 à 10 acquisitions par an) et nourrit des débrayages manuels massifs par les équipes Revenue Management.

Ce product brief cadre le passage d'une boîte noire externe subie à un actif tarifaire interne co-construit, explicable et résilient, opéré sur le socle GCP et BigQuery d'Aix-en-Provence sans remettre en cause le cœur transactionnel PMS central. La démarche écarte tout remplacement brutal du jour au lendemain. Elle impose d'abord un audit terrain et contrefactuel du prestataire existant, puis une trajectoire assumée d'internalisation complète en quatre temps sur 12 mois, sécurisée par une gouvernance Champion/Challenger.

---

## 2. Problème métier et constats vérifiés

L'analyse croisée de l'offre et des données publiques 2025-2026 fait ressortir quatre limites structurelles du fonctionnement actuel.

### Opacité algorithmique et boucle de débrayage
Les Revenue Managers d'Aix-en-Provence, de Montpellier et de Breda portent le risque financier de juillet et août, qui concentrent 74 % du chiffre d'affaires hébergement brut sur une structure à 67 % de coûts fixes. Faute de comprendre pourquoi l'outil tiers recommande une hausse ou une baisse, ils surchargent fréquemment les tarifs à la main (parfois via des fichiers Excel ou VBA parallèles). La littérature sectorielle confirme que ces débrayages non expliqués dégradent la performance financière et polluent l'apprentissage ultérieur dès que les tarifs forcés réintègrent l'historique d'entraînement.

### Dualité économique mal arbitrée par un moteur générique
Le portefeuille d'Client Cible combine deux équations économiques incompatibles avec une fonction objectif unique. Sur les 117 campings en propre (dont les resorts Resorts Annuels A ouverts à l'année), une famille génère environ 12 % de revenus annexes sur place (restauration, bars, activités): stimuler le taux d'occupation en ailes de saison reste rentable si le revenu global par emplacement progresse. Sur les quelque 350 campings partenaires en tour-opérateur, ces dépenses annexes reviennent au propriétaire indépendant; Client Cible ne gagne que sur la marge nette d'hébergement après loyer garanti, ménage et commission. Un moteur optimisant uniformément le chiffre d'affaires hébergement brut sous-optimise mécaniquement l'un des deux segments.

### Chocs fiscaux, commerciaux et structurels de 2026
L'environnement européen subit plusieurs ruptures simultanées que le moteur tiers absorbe trop lentement. La TVA sur les hébergements locatifs a bondi de 9 % à 21 % aux Pays-Bas au 1er janvier 2026 et de 6 % à 12 % en Belgique au 1er mars 2026, obligeant à séparer strictement le prix TTC perçu par le client (élasticité de la demande) du revenu net HT encaissé par Client Cible (marge). En parallèle, les courts séjours hors samedi-samedi progressent fortement en ailes de saison, les comportements d'anticipation divergent entre clientèles nord-européennes précoces et clientèles françaises tardives, les remises CSE (jusqu'à -40 % en Coup par Coup et -60 % en Linéaire avec rétrocession à J-15) créent des chocs d'offre, et la suppression des clauses de parité sur OTA majeure (DMA, septembre 2026) ouvre un nouvel espace d'arbitrage multicanal.

### Coût de dépendance, risque prestataire et souveraineté
Chaque adaptation métier (nouveau format de séjour, canal OTA, intégration d'un site acquis) dépend du calendrier et des avenants du prestataire externe (vraisemblablement Prestataire externe `#rm-externe` ou l'héritage Moteur historique de Marque B, avec le départ fin 2025 de deux responsables clés côté Prestataire externe). Internaliser la couche décisionnelle rend à Client Cible la propriété intellectuelle de son cœur de marge tout en réduisant l'exposition réglementaire liée aux outils tarifaires partagés entre concurrents (risque *hub-and-spoke* surveillé par les autorités de concurrence européennes en 2026).

---

## 3. Utilisateurs cibles et parties prenantes

Le produit vise d'abord les utilisateurs opérationnels qui valident les prix chaque matin, tout en répondant aux exigences de gouvernance financière et technique du groupe.

| Groupe de parties prenantes | Ancrage et rôle dans la décision | Attente centrale vis-à-vis de l'actif interne | Risque principal à neutraliser |
| :--- | :--- | :--- | :--- |
| Revenue Managers et Pricing Analysts | Aix-en-Provence, Montpellier, Breda; pilotage quotidien des tarifs et restrictions | Comprendre les moteurs de chaque recommandation (SHAP, booking pace, élasticité) et simuler des scénarios | Rejet d'une nouvelle boîte noire ou surcharge administrative lors des validations |
| Branche Digital, Data & IT | Aix-en-Provence (12 à 15 experts); Data Science, Data Engineering, BI | Posséder un code Python/SQL versionné, industrialisé sous GCP/BigQuery et maintenable à effectif constant | Sur-ingénierie cloud (cluster temps réel permanent) saturant la capacité de l'équipe |
| Direction générale et financière | Siège (Fonds majoritaire, Investisseur minoritaire); objectif >1 Md€ CA et basculement FOCF positif en 2027 | Sécuriser le pic juillet-août, prouver le gain de marge nette et absorber 5 à 10 acquisitions par an | Perte de revenu en haute saison lors d'une bascule précipitée |
| Marketing et directions de marques | Marque A, Marque C, Marque D, Resorts Annuels A, Place de marché interne (91 % direct) | Protéger le positionnement 4-5 étoiles, lisser les écarts inter-pays (30 % à 40 %) et éviter le *drip pricing* | Volatilité faciale incomprise par les clients (effet Concurrent B-Parcs ou Concurrent A) |
| Exploitations locales et partenaires TO | 117 sites en propre et ~350 campings indépendants partenaires | Stabiliser les rotations ménage sur les courts séjours et respecter l'image tarifaire sur sites partagés | Tension contractuelle avec les partenaires indépendants ou surréservation inter-systèmes |

---

## 4. Proposition de valeur et avantage asymétrique

Aucun concurrent européen de taille comparable ne réunit aujourd'hui le modèle hybride d'Client Cible (propre + TO + place de marché), 91 % de distribution directe et une couche de tarification dynamique internalisée et explicable. Concurrent A subit la friction de sa fusion et de la TVA néerlandaise; Concurrent B s'appuie sur le SaaS hôtelier SaaS RMS hôtelier dont la volatilité dégrade la perception client; Concurrent C (4-5* propre) opère un parc 100 % en propre récemment migré sur PMS cloud concurrent.

La proposition de valeur de l'actif interne tient en quatre piliers complémentaires.

### Un moteur bicéphale orienté marge nette
La modélisation sépare explicitement la prévision de demande non contrainte (intégrant la décontraction des semaines saturées à 100 % en été et les élasticités par nationalité) de l'optimisation sous contrainte. Deux fonctions objectif coexistent selon le statut du site: contribution totale (hébergement plus 12 % d'annexes) sur les 117 campings en propre, et marge nette d'hébergement après loyer garanti et commission sur les ~350 partenaires TO, toujours optimisée en net HT à partir d'une élasticité estimée en TTC.

### Une explicabilité native qui transforme le débrayage en signal
Chaque recommandation exposée dans Tableau ou Dash affiche ses facteurs explicatifs locaux (booking pace vs N-1/N-2, niveau de stock, pression calendaire, effet canal ou fiscalité) et un simulateur d'impact. Le débrayage humain reste autorisé, mais requiert un motif structuré en une ligne. Ces motifs alimentent une revue mensuelle entre Data Science et Revenue Management afin d'enrichir les features au lieu de fausser l'entraînement.

### Une architecture modulaire sans refonte du PMS
PMS central conserve la gestion d'inventaire, les caches `semainier`/`journalier` et la diffusion multicanale via son connecteur bidirectionnel 2-ways. La valeur analytique vit dans GCP (BigQuery, Dataform, Cloud Workflows, Cloud Run Jobs et Python/XGBoost/OR-Tools), ce qui permet d'intégrer de nouvelles acquisitions par unification analytique rapide sans attendre une migration PMS.

### Un portage incarné par un profil hybride métier et MLOps
L'exécution de cette trajectoire repose sur une posture praticienne alliant 15 ans de direction d'études côté métier (dialogue direct avec les équipes commerciales et direction générale), une expérience éprouvée en production sur un stock périssable à saisonnalité extrême (prévision de ventes à 15 % de MAPE, explicabilité SHAP, optimisation BigQuery à 500 k€ d'économies et veille tarifaire automatisée sur 4 pays européens) et la maîtrise des standards MLOps (gouvernance Champion/Challenger, détection de drift, Docker, CI/CD).

---

## 5. Feuille de route globale d'internalisation en quatre temps

Plutôt que de disperser l'équipe sur des POCs isolés sans chemin vers la production, la feuille de route séquence une reprise de souveraineté complète sur 12 mois, avec un jalon go/no-go mesurable à chaque étape.

| Phase et horizon | Objectif stratégique | Livrables principaux | Critère de passage (jalon) |
| :--- | :--- | :--- | :--- |
| Temps 1: Compréhension terrain et audit contrefactuel (M1 à M3) | Mesurer objectivement la performance réelle du prestataire externe face aux décisions RM et cartographier les biais | Immersion Aix/Montpellier/Breda; extraction historique recommandations vs prix publiés dans BigQuery; rapport d'audit contrefactuel (propre vs TO, haute saison vs ailes) | Cartographie chiffrée des zones de perte de valeur du prestataire et choix validé du périmètre Challenger |
| Temps 2: Fondations data et socle Challenger explicable (M3 à M6) | Bâtir le socle de features versionnées dans BigQuery et lancer le premier moteur interne en shadow mode | Pipeline Dataform (booking pace, décontraction estivale, séparation TTC/HT); modèle XGBoost + optimisation sous contrainte en mode Challenger; cockpit Tableau/Dash avec SHAP | Précision de prévision et cohérence économique validées en shadow mode par les RM sur données historiques et flux courant |
| Temps 3: Basculement progressif et gouvernance Champion/Challenger (M6 à M9) | Prendre la main en production sur un périmètre à fort levier et risque maîtrisé en encadrant l'adoption | Mise en production sur ailes de saison, courts séjours hors samedi-samedi ou marque/zone pilote via connecteur 2-ways PMS central; capture du motif de débrayage en une ligne; monitoring de drift | Gain de RevPAC / marge nette prouvé en test contrôlé et taux de débrayage en baisse vers le seuil cible de 20 % à 25 % |
| Temps 4: Décommissionnement et extension de la valeur (M9 à M12+) | Retirer progressivement le prestataire externe et étendre la couverture au portefeuille complet | Généralisation aux 450+ destinations et protocole d'onboarding rapide des acquisitions; intégration d'une veille tarifaire concurrentielle multi-pays conforme; couche sémantique BigQuery pour analytique conversationnelle | Extinction contractuelle du moteur externe validée par la direction financière et autonomie complète de l'équipe Data/RM |

---

## 6. Garde-fous politiques, techniques et périmètre exclu

Quatre lignes rouges non négociables protègent la crédibilité opérationnelle et financière du programme.

### Conservation du cœur transactionnel PMS central
Le projet ne réécrit pas un PMS, ne remplace pas la gestion de parcelles ni les passerelles OTA natives de PMS central. L'internalisation cible exclusivement la couche de prévision, d'optimisation et d'explicabilité.

### Interdiction de tout basculement en plein pic juillet-août
La haute saison concentre l'essentiel de l'EBITDA annuel. Aucune mise en production initiale ni aucun décommissionnement brutal n'intervient entre juin et août; chaque version du modèle interne doit d'abord prouver sa stabilité en shadow mode puis sur des ailes de saison ou un segment borné.

### Rejet de l'automatisation aveugle entre Aix, Montpellier et Breda
L'outil ne force jamais des prix opaques contre les équipes commerciales. L'automatisation reste bornée dans une fourchette de tolérance sur les périodes calmes, tandis que le pic estival fonctionne en mode recommandation expliquée avec validation humaine et motif structuré obligatoire en une ligne.

### Sobriété d'architecture cloud et discipline sur l'IA agentique
Pour une équipe de 12 à 15 experts couvrant aussi le CRM et la BI, tout Feature Store temps réel permanent ou cluster surdimensionné est écarté au profit d'exécutions batch quotidiennes ou infra-journalières (Cloud Run Jobs, Cloud Workflows, Dataform) alignées sur les caches PMS central. Le déploiement d'un agent d'analytique conversationnelle (atout mentionné dans l'offre) reste explicitement conditionné à la livraison préalable d'une couche sémantique gouvernée dans BigQuery et au respect de l'article 50 de l'AI Act.

---

## 7. Indicateurs de succès et hypothèses à lever dès M1

La réussite du programme se juge sur un équilibre entre performance financière, adoption humaine et vélocité technique.

| Dimension | Indicateur cible | Horizon de mesure |
| :--- | :--- | :--- |
| Performance économique | Progression mesurée du RevPAC et de la marge nette HT (cible réaliste +3 % à +5 % sur les segments basculés, validée en Champion/Challenger) | M6 à M12 |
| Adoption Revenue Management | Taux de débrayage manuel ramené vers une zone saine de 20 % à 25 % avec 100 % des débrayages estivaux motivés en une ligne | M6 à M12 |
| Agilité opérationnelle | Délai d'intégration tarifaire d'une nouvelle acquisition ou d'une nouvelle règle fiscale/canal ramené de plusieurs mois prestataire à moins de deux semaines en interne | M9 à M12 |
| Souveraineté et conformité | Extinction de la dépendance au moteur externe, zéro infraction Omnibus (historique 30 jours des prix barrés) ni dérive de parité cache-checkout | M12 |

### Hypothèses ouvertes à vérifier lors de l'audit de Phase 1
1. `[À VÉRIFIER EN AUDIT]` Identité exacte et périmètre contractuel du ou des prestataires en place (Prestataire externe `#rm-externe`, Moteur historique hérité de Marque B, ou module Éditeur PMS) ainsi que les clauses et échéances de sortie.
2. `[À VÉRIFIER EN AUDIT]` Disponibilité et granularité dans BigQuery de l'historique des prix recommandés par le prestataire face aux prix réellement publiés dans PMS central (et part des retraitements effectués sous SQL Server ou VBA).
3. `[À VÉRIFIER EN AUDIT]` Latence réelle du pont de données entre la couche BI Snowflake de PMS central et BigQuery, et capacité d'écriture API 2-ways sur les grilles MinLOS, CTA et CTD.
4. `[À VÉRIFIER EN AUDIT]` Niveau exact d'harmonisation des flux de pricing entre les marques convergées sur PMS central (Marque A, Marque C, Marque D, Resorts Annuels A) et Place de marché interne (PHP/MariaDB).
