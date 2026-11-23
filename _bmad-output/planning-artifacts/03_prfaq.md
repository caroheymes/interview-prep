# PRFAQ (Working Backwards à horizon 12 mois): actif tarifaire interne d'European Camping Group

Date de rédaction: 2026-11-23
Horizon projeté du communiqué: novembre 2027 (M+12)
Méthode: Working Backwards (`bmad-prfaq`), communiqué de presse interne projeté suivi d'une FAQ externe et d'une FAQ interne exigeante (Direction, DPO/Juridique, Tech/Data, Revenue Management)
Sources: [01_deep_recon.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/_bmad-output/planning-artifacts/01_deep_recon.md) et [02_product_brief.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/_bmad-output/planning-artifacts/02_product_brief.md)

---

## 1. Communiqué de presse interne projeté (M+12)

### European Camping Group reprend la maîtrise complète de sa tarification dynamique sur ses 450 destinations sans toucher à son socle Resalys

Douze mois après le lancement de son programme d'internalisation, la branche Digital, Data & IT d'Aix-en-Provence et les équipes Revenue Management d'Aix, de Montpellier et de Breda décommissionnent le moteur tarifaire externe et opèrent désormais un actif interne explicable sous GCP et BigQuery, dégageant +3 % à +5 % de RevPAC sur les segments basculés tout en ramenant le débrayage manuel sous le seuil de 25 %.

Aix-en-Provence, novembre 2027. European Camping Group (ECG) achève aujourd'hui la bascule de son intelligence tarifaire vers un moteur interne co-construit par ses équipes Data Science et Revenue Management. Jusqu'à fin 2026, les recommandations quotidiennes de prix sur les 48 000 mobil-homes du groupe reposaient sur un algorithme externe en boîte noire. Ce fonctionnement exposait les équipes commerciales à des recommandations peu lisibles sur le pic estival (74 % du chiffre d'affaires hébergement brut), freinait l'intégration des 5 à 10 acquisitions annuelles et imposait des délais prestataires à chaque évolution fiscale ou commerciale.

La nouvelle plateforme interne ne remplace pas le PMS Resalys, qui continue de gérer l'inventaire, les caches tarifaires et la distribution multicanale. Elle internalise exclusivement la couche décisionnelle sur BigQuery, Dataform et Python (XGBoost et optimisation sous contrainte), reliée à Resalys par son connecteur bidirectionnel. Le moteur distingue pour la première fois la fonction objectif des 117 campings en propre (revenu global incluant les 12 % de dépenses annexes sur place et les resorts Alannia ouverts à l'année) de celle des quelque 350 sites partenaires en tour-opérateur (marge nette d'hébergement après loyer garanti et commission). Il sépare également le prix TTC perçu par le client du revenu net HT encaissé par ECG, absorbant sans distorsion les hausses de TVA néerlandaise (21 %) et belge (12 %).

Sur le terrain, chaque matin, les Revenue Managers et Pricing Analysts consultent dans Tableau et Dash les recommandations accompagnées de leurs facteurs explicatifs locaux (booking pace comparé à N-1 et N-2, stock résiduel décontracté, sensibilité par nationalité, pression calendaire). Hors haute saison, les ajustements restent automatisés dans une bande de tolérance convenue. Sur juillet et août, la validation humaine reste souveraine: tout débrayage s'accompagne d'un motif structuré en une ligne qui alimente la revue mensuelle d'amélioration du modèle.

Résultats mesurés à douze mois en protocole Champion/Challenger (objectifs cibles projetés): progression de +3 % à +5 % du RevPAC et de la marge nette HT sur les segments basculés, baisse du taux de débrayage manuel dans la zone cible de 20 % à 25 % avec 100 % des débrayages estivaux tracés, délai d'intégration tarifaire d'une nouvelle acquisition réduit à moins de deux semaines, et extinction contractuelle complète du moteur externe.

> `[Citation projetée, Working Backwards M+12, Direction Commerciale & Revenue Management]`
> "Nous sommes passés d'un outil tiers que nos équipes contournaient par prudence sur juillet-août à un copilote tarifaire interne que nous avons co-construit. Les analystes à Aix, Montpellier et Breda voient immédiatement pourquoi un tarif bouge et gardent la main quand un événement local l'exige."

> `[Citation projetée, Working Backwards M+12, Direction Digital, Data & IT]`
> "L'architecture retenue reste sobre et maintenable par notre équipe d'Aix-en-Provence. Nous avons évité la sur-ingénierie temps réel, conservé Resalys pour l'exécution transactionnelle et posé une couche sémantique gouvernée dans BigQuery qui prépare sereinement nos cas d'usage d'analytique conversationnelle."

---

## 2. FAQ externe (clients, partenaires indépendants, CSE et OTA)

### Les prix d'Homair, d'Eurocamp ou de Roan vont-ils osciller brutalement d'un jour à l'autre ou sauter au moment du paiement?
Non. L'analyse des avis clients de concurrents européens en 2026 (notamment Center Parcs et Landal) a montré que les variations faciales erratiques et les écarts entre catalogue et panier détruisent la confiance. Le moteur interne applique des bornes de variation quotidiennes par gamme et par saison, et impose une synchronisation stricte avec les caches `semainier` et `journalier` de Resalys afin de garantir la parité entre le prix affiché en recherche et le prix payé au checkout.

### Mes données personnelles de navigation servent-elles à fixer un tarif personnalisé plus élevé?
Non. Le moteur tarife exclusivement à partir de variables agrégées et anonymes: niveau de stock disponible par typologie, rythme de réservation collectif comparé aux saisons précédentes, calendrier scolaire par marché émetteur, canal de distribution et fiscalité locale. Aucun profilage individuel ni historique personnel de navigation n'entre dans le calcul d'un prix.

### Comment les quelque 350 campings indépendants partenaires sont-ils protégés contre un bradage tarifaire en basse saison?
La fonction objectif dédiée au parc partenaire maximise la marge nette d'hébergement après loyer garanti et intègre des prix planchers contractuels par site et par gamme. Le moteur ne déclenche jamais de baisse agressive qui dégraderait l'image du camping hôte ou créerait une concurrence frontale destructrice avec les propres locatifs du propriétaire indépendant. Les écarts inter-pays entre portails de marques (auparavant observés jusqu'à 30 % ou 40 %) sont également bornés par des règles de cohérence.

### Les accords CSE (plus de 3 000 clients) et les engagements de transparence OTA restent-ils respectés?
Oui. Les mécaniques contractuelles CSE (remises Coup par Coup plafonnées à -40 % en basse saison, Bouquet en haute saison, blocs Linéaires avec rétrocession à J-15) sont encodées comme contraintes dures dans l'optimiseur. Côté OTA (9 % du chiffre d'affaires), la diffusion via les passerelles Resalys respecte la charte de transparence FNHPA de mars 2026 et exploite légalement la suppression des clauses de parité sur Booking.com (DMA) pour préserver la compétitivité des 91 % de ventes directes.

---

## 3. FAQ interne difficile (Direction, DPO/Juridique, Tech/Data, Revenue Management)

### Direction générale et Finance

#### Les études sectorielles rappellent qu'un RMS sur mesure mobilise souvent 10 personnes sur 24 mois et échoue fréquemment. Pourquoi votre approche tiendrait-elle en 12 mois?
Parce que nous ne construisons pas un RMS complet ni un PMS. Les projets qui dérapent veulent réécrire la gestion d'inventaire, les connecteurs OTA et une interface frontale lourde. Nous conservons 100 % du socle transactionnel Resalys et nous construisons uniquement une couche décisionnelle modulaire dans BigQuery et Python, déployée en quatre temps avec un jalon go/no-go tous les trimestres.

#### Comment prouvez-vous à la direction financière et aux actionnaires (PAI Partners, ADIA) que le gain de +3 % à +5 % vient du modèle et non d'une météo favorable?
Par un protocole Champion/Challenger strict sur des segments appariés (même typologie de destination, même saisonnalité, même marché émetteur) complété par un audit contrefactuel préalable en Phase 1. Le modèle interne n'est généralisé que lorsqu'il bat statistiquement le modèle externe (ou le pilotage historique) sur le RevPAC et la marge nette HT, à périmètre comparable.

#### Que se passe-t-il si le modèle interne échoue avant ou pendant la saison estivale?
Le risque est borné par conception. La ligne rouge interdit tout basculement initial en juin, juillet ou août. Le moteur tourne d'abord en shadow mode (M3-M6), puis en production sur des ailes de saison ou un périmètre pilote limité (M6-M9). Le prestataire externe reste actif en repli jusqu'à validation complète de la bascule en M9-M12, et Resalys conserve en permanence un mécanisme de retour immédiat aux grilles de sécurité validées par les Revenue Managers.

### DPO et Juridique

#### L'ordonnance 2026-2 (art. L. 221-5 du Code de la consommation) impose d'informer le client en cas de prix personnalisé automatisé, sous peine de 75 000 € d'amende. Sommes-nous exposés?
Non, à condition de maintenir une discipline stricte sur les variables d'entrée. L'architecture exclut toute donnée personnelle (identifiant client, cookie individuel, historique d'achat nominatif) des features du modèle de pricing. Le tarif reste purement dynamique sur des agrégats de demande et de stock, ce qui le place hors champ de la personnalisation individuelle automatisée. Un contrôle de schéma Dataform bloque automatiquement toute colonne contenant un identifiant personnel.

#### Comment garantissons-nous la conformité Omnibus sur les prix barrés et l'absence de *drip pricing*?
Le pipeline BigQuery conserve un historique glissant sur 30 jours du prix le plus bas pratiqué par site, gamme et date de séjour (exigence de l'article L. 112-1-1 et de l'arrêt CJUE *Aldi Süd*). Toute promotion affichée sur les sites ECG s'appuie sur cette table de référence. De plus, les recommandations et les simulations d'élasticité intègrent les frais obligatoires (dossier, ménage) afin d'afficher un prix TTC complet dès la première étape du tunnel, en anticipation du *Digital Fairness Act*.

#### La veille tarifaire concurrentielle et l'analytique conversationnelle créent-elles des risques antitrust ou AI Act?
Côté concurrence, l'internalisation réduit précisément le risque *hub-and-spoke* surveillé en 2026 par les autorités européennes (affaire hôtelière CMA/STR) puisque l'algorithme n'est partagé avec aucun concurrent; la veille externe intégrée en Temps 4 collecte uniquement des prix publics affichés, sans aucun échange d'informations non publiques. Côté AI Act, tout assistant conversationnel interne ou externe déployé après la couche sémantique BigQuery affiche une mention explicite d'interaction avec une IA dès le premier message (article 50).

### Tech et Data (Aix-en-Provence)

#### Une équipe de 12 à 15 experts qui gère déjà le CRM et la BI peut-elle industrialiser et maintenir ce moteur sans exploser les coûts GCP?
Oui, à condition de refuser la sur-ingénierie. Le pricing en hôtellerie de plein air ne nécessite pas une inférence en millisecondes sur un Feature Store Vertex AI permanent ni un cluster GKE dédié 24h/24. Les grilles se recalculent en batch quotidien ou infra-journalier via des conteneurs Docker exécutés sur Cloud Run Jobs, orchestrés par Cloud Workflows et alimentés par Dataform dans BigQuery. Cette architecture serverless maintient un coût marginal bas et limite la dette opérationnelle.

#### Comment gérez-vous la coexistence entre Resalys/Snowflake, BigQuery, les fichiers SQL Server/VBA et VacanceSelect Travel (PHP/MariaDB)?
Le programme suit une convergence pragmatique en couches. En Temps 1 et 2, BigQuery devient le hub unique de modélisation en ingérant les exports quotidiens de Resalys/Snowflake et les tables de référence des sites propres et partenaires, tandis que les fichiers VBA servent d'indice d'audit pour identifier les règles métier manquantes avant leur rapatriement dans Dataform. Les flux de VacanceSelect Travel (PHP/MariaDB) sont traités dans un lot dédié après stabilisation du cœur Resalys (Homair, Eurocamp, Roan, Alannia). Côté API GraphQL Resalys (environ 4 secondes hors cache), les écritures 2-ways sont discrétisées et couplées à un pré-chauffage planifié des caches.

#### Comment évitez-vous les deux pièges statistiques classiques: la censure à 100 % d'occupation en été et la boucle toxique des débrayages?
Deux garde-fous mathématiques sont intégrés dès le Temps 2. Premièrement, un module de décontraction (unconstraining) estime la demande non servie lorsque la capacité atteint 100 % en juillet-août, en croisant les dates de fermeture à la vente et les recherches sans disponibilité issues du tracking web (Tealium/GA4). Deuxièmement, l'entraînement sépare strictement les observations issues des recommandations suivies des observations issues de débrayages manuels, afin d'éviter qu'un prix forcé ne biaise la courbe d'élasticité estimée.

### Revenue Managers (Aix-en-Provence, Montpellier, Breda)

#### Pourquoi cet outil interne ne deviendrait-il pas une nouvelle boîte noire que nous finirons aussi par débrayer?
Parce que les règles métier et l'explicabilité sont conçues avec vous avant la première ligne de code de production. Chaque recommandation dans Tableau ou Dash affiche la décomposition locale de son calcul (contributions SHAP et effets booking pace, stock, calendrier, concurrence, TVA) ainsi qu'un simulateur "et si" permettant de tester un autre prix avant publication. L'audit de Phase 1 commence d'ailleurs par analyser vos propres débrayages pour comprendre là où votre intuition locale bat aujourd'hui l'algorithme.

#### Allez-vous nous retirer la main sur juillet-août ou nous imposer une saisie administrative lourde chaque matin?
Ni l'un ni l'autre. Sur juillet et août, aucune baisse ou hausse ne passe sans votre validation; l'automatisation bornée ne s'applique qu'aux ailes de saison et aux ajustements mineurs dans une fourchette définie ensemble. Lorsqu'un Revenue Manager débraye une recommandation, la saisie se limite à un motif structuré en une ligne (menu rapide: événement local, météo/incendie, action concurrente, contrainte partenaire ou CSE), ce qui prend moins de dix secondes et remplace les commentaires dispersés dans Excel.

#### Comment le modèle gère-t-il concrètement les différences entre nos 117 campings en propre, nos 350 sites partenaires et les nouvelles acquisitions?
Le modèle applique deux fonctions objectif distinctes: maximisation du revenu global (hébergement plus 12 % d'annexes) sur les 117 sites en propre, et maximisation de la marge nette HT après loyer garanti sur les ~350 partenaires TO. Pour une nouvelle acquisition sans historique ECG, le moteur démarre par apprentissage par transfert à partir de campings jumeaux (même bassin géographique, standing 4-5 étoiles, mix nationalités), ce qui permet un pilotage tarifaire opérationnel en moins de deux semaines.

---

## 4. Verdict Working Backwards et exigences transmises au PRD (`04_prd.md`)

Le passage au crible Working Backwards valide la solidité du concept à condition de traduire cinq points non négociables en exigences fonctionnelles et non fonctionnelles dans [04_prd.md](file:///C:/Users/Admin/Documents/TEMPLATE_GENERATE_ROADMAP%20-%20ECG/_bmad-output/planning-artifacts/04_prd.md):

1. Traçabilité complète de l'audit contrefactuel en Phase 1 (recommandations prestataire vs prix publiés Resalys vs débrayages) avant toute écriture en production.
2. Séparation architecturale entre prévision de demande non contrainte (avec décontraction estivale et élasticité TTC par nationalité) et moteur d'optimisation sous contrainte à double fonction objectif (propre vs TO, net HT).
3. Cockpit Tableau/Dash intégrant explicabilité locale SHAP, simulateur d'impact et journalisation obligatoire en une ligne des débrayages, avec isolation des prix forcés dans le jeu d'entraînement.
4. Conformité intégrée par construction: historique glissant 30 jours Omnibus, blocage de toute donnée personnelle (art. L. 221-5), bornes de parité cache-checkout Resalys et contraintes contractuelles CSE/partenaires.
5. Sobriété MLOps sous GCP (batch Cloud Run Jobs, Cloud Workflows, Dataform, monitoring de drift et protocole Champion/Challenger), sans bascule estivale et avec couche sémantique BigQuery préalable à tout agent conversationnel.
