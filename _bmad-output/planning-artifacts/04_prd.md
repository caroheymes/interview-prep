# PRD exécutif: plateforme interne de tarification dynamique d'Opérateur HPA Européen (Client Cible)

Date: 2026-11-23
Statut: Finalisé pour transmission vers l'architecture (`05_architecture.md`), le stress-test (`06_stress_test.md`) et les epics (`07_epics_roadmap.md`)
Sources: [02_product_brief.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/_bmad-output/planning-artifacts/02_product_brief.md) et [03_prfaq.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/_bmad-output/planning-artifacts/03_prfaq.md)

---

## 1. Objet, périmètre et trajectoire de déploiement

Ce document spécifie les exigences produit de la plateforme interne de tarification dynamique d'Opérateur HPA Européen (Client Cible). L'objectif est de remplacer progressivement le moteur externe en boîte noire par un actif décisionnel interne co-construit avec les équipes Revenue Management, opéré sur GCP et BigQuery, tout en conservant intégralement le socle transactionnel PMS central.

Le périmètre couvre les 450+ destinations européennes (117 campings en propre et près de 350 sites partenaires en tour-opérateur), déployées en quatre temps sur 12 mois: audit contrefactuel du prestataire (M1-M3), socle data et Challenger explicable en shadow mode (M3-M6), basculement progressif par segments à risque maîtrisé en protocole Champion/Challenger (M6-M9), puis décommissionnement du prestataire et extension complète incluant les acquisitions annuelles et la veille tarifaire (M9-M12+).

Sont explicitement exclus du périmètre: toute réécriture du PMS PMS central, toute gestion d'inventaire physique ou de plan de parcelles, toute infrastructure d'inférence temps réel permanente non justifiée par le cycle batch HPA, et tout profilage tarifaire individuel sur données personnelles.

---

## 2. Grille de scoring de priorisation sur 100 points

Cette grille sert à arbitrer objectivement l'ordre de bascule des périmètres (marques, zones géographiques, segments propre vs TO, chantiers fonctionnels) et les décisions trimestrielles de passage en production.

| Axe d'évaluation | Poids | Critères de notation détaillés |
| :--- | :--- | :--- |
| Impact marge nette et RevPAC | 35 pts | Potentiel de gain en marge nette HT (propre avec 12 % d'annexes ou partenaire TO après loyer), correction d'un biais avéré du prestataire (TVA 2026, courts séjours, sous-pricing estival) |
| Adoptabilité Revenue Management | 25 pts | Réduction attendue du débrayage manuel, clarté des explications locales SHAP, alignement opérationnel entre Aix-en-Provence, Montpellier et Breda, absence de friction de saisie |
| Faisabilité data et sobriété MLOps | 25 pts | Qualité et disponibilité de l'historique dans BigQuery/PMS central, compatibilité avec une exécution batch Cloud Run Jobs et Dataform, maintenabilité par l'équipe de 12 à 15 experts |
| Maîtrise des risques et conformité | 15 pts | Réversibilité immédiate vers PMS central, conformité juridique (Omnibus 30 jours, art. L. 221-5, DMA, AI Act), protection de l'image marque et des relations partenaires TO |

### Seuils de décision
Un périmètre ou lot fonctionnel obtenant un score supérieur ou égal à 75/100 passe en statut Go (priorité immédiate sur le trimestre en cours). Un score compris entre 55 et 74/100 passe en statut Backlog (à requalifier après levée d'une dépendance data ou métier). Un score strictement inférieur à 55/100 passe en statut No-Go (écarté du plan à 12 mois).

### Critères éliminatoires (veto immédiat quel que soit le score)
1. Toute mise en production initiale ou bascule de prestataire programmée durant le pic estival de juin, juillet ou août.
2. Toute utilisation d'une donnée personnelle ou d'un identifiant client individuel dans les variables d'entrée du modèle tarifaire (violation potentielle de l'art. L. 221-5).
3. Absence d'historique vérifiable permettant une comparaison contrefactuelle ou un protocole Champion/Challenger avant généralisation.
4. Impossibilité de revenir aux grilles de sécurité PMS central en moins de deux heures en cas d'anomalie.
5. Déploiement d'un agent d'analytique conversationnelle sur des tables BigQuery brutes sans couche sémantique gouvernée préalable.

---

## 3. Exigences fonctionnelles (FR)

Les exigences sont regroupées par capacité métier avec identifiants stables pour la traçabilité vers l'architecture et les epics.

### Capacité A: audit contrefactuel et socle de données BigQuery (M1-M3)
FR-01: Le système ingère quotidiennement dans BigQuery les réservations, stocks, tarifs publiés, restrictions (MinLOS, CTA, CTD) et annulations issus de PMS central/Snowflake, ainsi que l'historique des recommandations du prestataire externe.
FR-02: Le système calcule et expose un rapport d'audit contrefactuel comparant, par segment (propre vs TO, haute saison vs ailes, marque, pays), les tarifs recommandés par le prestataire, les tarifs effectivement publiés après débrayage RM et le RevPAC réalisé.
FR-03: Le socle Dataform construit des tables de features versionnées intégrant le booking pace comparé à N-1 et N-2 par horizon (J-x), le lead time par marché émetteur (NL, DE, UK, FR, ES), les calendriers scolaires européens et les règles fiscales par pays et typologie (TVA 2026 NL 21 %, BE 12 %).
FR-04: Un contrôle automatisé de schéma Dataform rejette toute ingestion contenant des colonnes d'identifiants personnels (email, nom, cookie individuel, ID client nominatif) dans les tables d'entraînement et d'inférence du moteur de pricing.

### Capacité B: prévision de demande non contrainte et élasticité (M3-M6)
FR-05: Le moteur de prévision estime la demande non contrainte par destination, gamme d'hébergement, date de séjour et durée (séjour semaine et court séjour hors samedi-samedi) en corrigeant la censure à 100 % d'occupation (module d'unconstraining alimenté par les dates de fermeture à la vente et les recherches sans disponibilité Tealium/GA4).
FR-06: Le moteur d'élasticité estime la sensibilité de la demande sur le prix TTC réellement affiché au client (frais obligatoires inclus) tout en transmettant à l'optimiseur la conversion exacte en revenu net HT après TVA locale, taxe de séjour et commission canal.
FR-07: Le pipeline d'entraînement isole systématiquement les observations issues de débrayages manuels afin d'éviter la boucle de rétroaction toxique sur les courbes d'élasticité, tout en réintégrant les motifs structurés validés comme variables contextuelles.
FR-08: Pour toute nouvelle acquisition sans historique Client Cible (5 à 10 sites par an), le moteur initialise les prévisions en moins de deux semaines par transfert d'apprentissage à partir de campings jumeaux (bassin géographique, classement 4-5 étoiles, mix nationalités).

### Capacité C: optimisation sous contrainte à double fonction objectif (M3-M9)
FR-09: L'optimiseur applique une fonction objectif différenciée selon le statut contractuel du site: maximisation de la contribution totale (hébergement plus 12 % de dépenses annexes estimées) sur les 117 campings en propre (incluant les resorts Resorts Annuels A ouverts à l'année), et maximisation de la marge nette HT d'hébergement après loyer garanti, ménage et commission sur les quelque 350 sites partenaires TO.
FR-10: L'optimiseur respecte des contraintes dures paramétrables par marque et par site: prix planchers partenaires, bornes de variation quotidienne anti-volatilité, plafonds d'écart inter-pays entre portails (Marque A, Marque C, Marque D), grilles CSE (Coup par Coup -40 %, Bouquet, Linéaire avec rétrocession J-15) et règles de comblement d'interstices calendrier (MinLOS, CTA, CTD).
FR-11: Le module d'arbitrage multicanal calcule les prix nets de commission entre vente directe (91 %), OTA (OTA majeure post-DMA, Comparateur HPA, Branche B) et Chèques-Vacances ANCV (2,5 %), tout en maintenant une table glissante sur 30 jours du prix le plus bas pratiqué pour la conformité Omnibus sur les prix barrés.

### Capacité D: cockpit explicable, gouvernance RM et publication PMS central (M3-M12)
FR-12: Le cockpit Tableau ou Dash affiche pour chaque recommandation quotidienne sa décomposition explicable locale (contributions SHAP: booking pace, stock résiduel, calendrier, élasticité nationalité, fiscalité, canal), son intervalle de confiance et un simulateur d'impact ("what-if") sur le taux d'occupation et la marge nette.
FR-13: Le workflow de publication applique deux régimes distincts: automatisation bornée dans une fourchette de tolérance sur les ailes de saison et ajustements mineurs, et validation humaine souveraine sur juillet-août. Tout débrayage manuel exige la sélection d'un motif structuré en une ligne (événement local, météo/incendie, action concurrente, contrainte partenaire, CSE ou autre).
FR-14: Les tarifs et restrictions validés sont discrétisés et poussés vers PMS central via son connecteur bidirectionnel 2-ways, couplé à un pré-chauffage planifié des caches `semainier` et `journalier` pour garantir la parité entre prix catalogue et prix checkout.
FR-15: Un module d'expérimentation Champion/Challenger gère le shadow mode puis l'allocation contrôlée par segments appariés, avec suivi mensuel automatisé des écarts de RevPAC, de marge nette HT et de taux de débrayage entre modèle externe et modèle interne.
FR-16: Une fois la couche décisionnelle stabilisée (Temps 4), le système intègre une veille tarifaire concurrentielle multi-pays basée uniquement sur des prix publics affichés et expose une couche sémantique gouvernée dans BigQuery préalable à tout assistant d'analytique conversationnelle (avec mention AI Act article 50).

---

## 4. Exigences non fonctionnelles (NFR)

### Performance et cadence d'exécution
NFR-01: Le pipeline complet quotidien (ingestion, Dataform, prévision, optimisation, calcul SHAP et export PMS central) s'exécute en batch serverless en moins de 90 minutes, afin que les recommandations soient disponibles avant 07h30 CET pour les équipes d'Aix-en-Provence, de Montpellier et de Breda.
NFR-02: Le temps de chargement des vues principales du cockpit Tableau ou Dash reste inférieur à 5 secondes par périmètre régional, sans dépendre de BigQuery BI Engine en présence de sécurité au niveau des lignes (usage d'extraits optimisés ou de tables agrégées dédiées).
NFR-03: Les écritures vers PMS central respectent les limites de débit de l'API et la contrainte de latence hors cache (environ 4 secondes par appel GraphQL) grâce à la discrétisation par lots et au pré-chauffage planifié.

### Fiabilité, MLOps et sobriété opérationnelle
NFR-04: L'architecture repose exclusivement sur des composants managés GCP cohérents avec une équipe de 12 à 15 experts (BigQuery, Dataform, Cloud Workflows, Cloud Run Jobs conteneurisés Docker, GitHub Actions CI/CD, Terraform), sans cluster temps réel permanent ni Feature Store toujours actif.
NFR-05: Chaque exécution est versionnée et reproductible (code Git, jeu de features daté, modèle enregistré et paramètres d'optimisation archivés), permettant un audit complet d'un tarif publié jusqu'à 24 mois en arrière.
NFR-06: Une sonde automatisée surveille chaque semaine la dérive des données d'entrée (data drift), la dérive des prédictions et l'erreur de prévision (MAPE/WAPE par segment), avec alerte vers l'équipe Data Science en cas de dépassement de seuil.
NFR-07: Le plan de repli garantit le retour aux grilles de sécurité PMS central (ou au modèle externe durant la phase de transition M6-M12) en moins de 2 heures, sans perte de données ni coupure de vente.

### Sécurité, conformité et gouvernance
NFR-08: Zéro donnée personnelle identifiable dans le périmètre de tarification (conformité RGPD et exclusion du champ de l'art. L. 221-5 sur le prix personnalisé automatisé).
NFR-09: Respect vérifiable de la directive Omnibus (historique 30 jours du prix le plus bas), affichage TTC intégrant les frais obligatoires (anticipation *Digital Fairness Act*), respect des règles de concurrence (aucune donnée concurrentielle non publique) et mention transparente AI Act article 50 sur tout futur agent conversationnel.
NFR-10: Gestion des droits d'accès par rôle (RBAC) entre Data Scientists, Data Engineers, Revenue Managers par zone géographique (Aix, Montpellier, Breda) et Direction financière, avec journalisation immuable de chaque validation et de chaque débrayage.

---

## 5. North-Star Metric, contre-métriques et kill-switches

### North-Star Metric (NSM)
La métrique directrice unique du programme est la **marge nette contributive HT par emplacement disponible (Net RevPAC contributif)**, calculée sur les segments pilotés en protocole Champion/Challenger. Sur les 117 campings en propre, elle intègre l'hébergement net HT plus la contribution estimée des dépenses annexes (12 %). Sur les quelque 350 sites partenaires TO, elle mesure strictement le revenu hébergement net HT diminué du loyer garanti, des coûts de rotation et des commissions de distribution.

Objectif cible réaliste à M+12: progression mesurée de +3 % à +5 % sur les segments basculés, validée à périmètre comparable.

### Contre-métriques obligatoires (garde-fous anti-effets pervers)
Une hausse du Net RevPAC n'est validée que si les cinq contre-métriques suivantes restent dans leur zone de contrôle.

| Contre-métrique | Définition opérationnelle | Seuil d'alerte |
| :--- | :--- | :--- |
| Taux de débrayage manuel RM | Part des recommandations modifiées manuellement par les Revenue Managers | Supérieur à 25 % en régime de croisière (ou absence de motif sur >5 % des débrayages) |
| Taux d'occupation en ailes de saison | Remplissage sur mai, juin et septembre par bassin | Recul supérieur à 3 points par rapport au groupe témoin apparié |
| Parité prix catalogue vs checkout | Écart constaté entre prix affiché en recherche et prix final au paiement | Tout écart supérieur à 0,5 % des sessions ou tout écart systématique lié au cache |
| Volatilité faciale et dispersion inter-pays | Variation journalière faciale et écart entre portails pays pour un même séjour | Variation faciale hors borne convenue ou écart inter-pays supérieur aux plafonds marque |
| Signal réputationnel prix et partenaires | Part des avis clients 1-2 étoiles citant le prix et nombre de litiges partenaires TO | Hausse statistiquement significative sur deux semaines consécutives |

### Kill-switches (arrêt automatique et bascule de repli)
Quatre déclencheurs provoquent l'arrêt immédiat de la publication automatique vers PMS central et le basculement sur les grilles de sécurité validées (ou sur le modèle externe en phase de transition), avec alerte prioritaire vers le Data Team Lead RM et le responsable Revenue Management.

1. Kill-switch financier: dégradation du Net RevPAC ou du rythme de réservation (booking pace) supérieure à 5 % sur 14 jours glissants par rapport au groupe témoin Champion, sans événement exogène documenté (météo extrême ou incendie).
2. Kill-switch intégrité tarifaire: détection d'un tarif recommandé hors bornes plancher/plafond, d'une erreur de taux de TVA pays, ou d'une désynchronisation de parité entre cache PMS central et checkout dépassant 1 % des devis testés.
3. Kill-switch adoption terrain: taux de débrayage manuel dépassant 40 % pendant sept jours consécutifs sur un segment basculé en production, traduisant une perte de confiance ou un angle mort critique du modèle.
4. Kill-switch conformité et fraîcheur data: détection d'une colonne contenant une donnée personnelle dans le flux d'entrée, rupture du rafraîchissement PMS central/Snowflake depuis plus de 24 heures, ou anomalie bloquante sur la table Omnibus 30 jours.
