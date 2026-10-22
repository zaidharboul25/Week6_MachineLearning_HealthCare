# HealthConnect Rwanda — Plan Détaillé de la Présentation (15 Slides)
## Soutenance Finale d'Ingénierie Machine Learning — Semaine 6
**Développeur :** Zaid Harboul (Senior Machine Learning Engineer)  
**Programme :** AnalystLab Africa — Experience Lab  
**Date :** 22 Octobre 2026  
**Fichier PowerPoint :** `deliverables/HealthConnect_Rwanda_Week6_Presentation.pptx`  

---

### Slide 1 : HealthConnect Rwanda — Healthcare Analytics & AI Transformation
**Points Clés Abordés :**
- Titre du projet et soutenance Semaine 6
- AnalystLab Africa Experience Lab
- Zaid Harboul, Senior Machine Learning Engineer

**Notes de Présentation (Speaker Notes) :**
> *"Bienvenue à tous. Je suis Zaid Harboul et j'ai l'honneur de vous présenter aujourd'hui le projet HealthConnect Rwanda, réalisé dans le cadre de l'Experience Lab Semaine 6 chez AnalystLab Africa. Ce travail allie rigueur d'ingénierie ML, intégrité scientifique absolue et conformité éthique stricte."*

---

### Slide 2 : Vue d'Ensemble Exécutive & Problématique Métier
**Points Clés Abordés :**
- Enjeux cliniques : triage et multimorbidité
- Enjeux financiers : trésorerie d'assurance RSSB/MMI
- Enjeux opérationnels : désilotage OpenMRS et gouvernance

**Notes de Présentation (Speaker Notes) :**
> *"Le système de santé rwandais bénéficie d'une couverture universelle remarquable via les mutuelles de santé (CBHI) et la RSSB. Cependant, les hôpitaux de district font face à des goulots d'étranglement de trésorerie dus aux délais de remboursement d'assurance et à une tension chronique sur les capacités d'urgence."*

---

### Slide 3 : Objectifs du Projet & Workflow Machine Learning Engineering
**Points Clés Abordés :**
- 5 étapes clés : Audit, Features, Modélisation, XAI, Déploiement
- Approche disciplinée et reproductible

**Notes de Présentation (Speaker Notes) :**
> *"Notre démarche d'ingénierie suit 5 étapes séquentielles rigoureuses. Dès l'ingestion, nous appliquons un audit automatisé de qualité et d'intégrité référentielle avant toute ingénierie de variables, garantissant l'absence de fuite d'information."*

---

### Slide 4 : Inventaire des Données : 27 Tables & Architecture Relationnelle
**Points Clés Abordés :**
- Cartographie des 27 tables en 6 domaines
- Intégrité référentielle 100% vérifiée
- Résolution du fichier département dupliqué

**Notes de Présentation (Speaker Notes) :**
> *"L'infrastructure repose sur 27 fichiers CSV organisés en 6 pôles. L'audit confirme une intégrité référentielle parfaite. Nous avons détecté un doublon exact d'export entre deux tables de départements, et géré l'asymétrie entre les 5 000 rendez-vous détaillés et les 60 000 lignes de facturation globale."*

---

### Slide 5 : Qualité des Données & Protection Absolue de la Vie Privée
**Points Clés Abordés :**
- 26/27 tables avec 0% de nuls
- Imputation sémantique de ChronicCondition
- Bannissement strict des PII

**Notes de Présentation (Speaker Notes) :**
> *"Sur les 27 fichiers, 26 sont exempts de valeurs manquantes. L'unique colonne avec des nuls est ChronicCondition (25%), que nous avons sémantiquement imputée par 'None'. Côté vie privée, les noms, téléphones et dates exactes ont été strictement bannis des features et de Git."*

---

### Slide 6 : Ingénierie des Caractéristiques & Prévention des Fuites
**Points Clés Abordés :**
- 6 tables analytiques créées
- Barrières temporelles contre les fuites
- Identification du risque de split overlap sur 510 patients

**Notes de Présentation (Speaker Notes) :**
> *"Pour prévenir toute fuite de données, nous avons exclu les paiements ultérieurs et les commentaires textuels d'enquêtes. Notre audit d'étanchéité a révélé que 510 patients ont des visites répétées ; nous documentons donc un risque moyen de recoupement patient et prescrivons l'usage d'un GroupShuffleSplit pour le déploiement."*

---

### Slide 7 : Résultats de Classification : Modèles 1 à 4 & Baselines
**Points Clés Abordés :**
- Tableau complet des 4 modèles
- Prise en compte des baselines majoritaires
- Transparence sur les modèles sous baseline

**Notes de Présentation (Speaker Notes) :**
> *"Voici le tableau comparatif de nos 4 modèles de classification. Nous observons en toute transparence que le Modèle 2 se situe légèrement sous la baseline majoritaire en raison du bruit uniforme dans les enquêtes, et que le Modèle 3 avoisine 51% car le label est généré comme un pile ou face indépendant."*

---

### Slide 8 : Constat Critique : Le Modèle 4 Reconstruit une Règle Déterministe
**Points Clés Abordés :**
- Démonstration de la circularité mathématique
- ROC-AUC 0.994 est un artefact de règle
- Absence d'issues cliniques réelles dans le jeu brut

**Notes de Présentation (Speaker Notes) :**
> *"Ce slide est capital pour notre crédibilité scientifique. Le Modèle 4 affiche un ROC-AUC spectaculaire de 0,9936. Mais notre audit a mis en évidence que la cible a été générée par une règle booléenne sur l'âge et l'IMC, qui sont précisément les entrées du modèle. Nous le qualifions donc honnêtement de reconstructeur de règle et non de prédicteur clinique."*

---

### Slide 9 : Résultats de Régression : Facturation Clinique & Limite LOS
**Points Clés Abordés :**
- Comparaison factuelle avec la baseline moyenne
- Explication du R2 négatif (bruit uniforme)
- Confirmation du statut UNSUPPORTED pour le Modèle 6

**Notes de Présentation (Speaker Notes) :**
> *"En régression financière, notre Random Forest obtient un R² négatif de -0,0297 et une MAE de 70 960 RWF, soit 752 RWF de plus que la moyenne simple. Cela s'explique par la distribution uniforme des montants dans les données. Quant au Modèle 6 de durée de séjour, il est honnêtement documenté comme non supporté car aucun horodatage n'existe."*

---

### Slide 10 : Segmentation Non Supervisée : Patients & Structures Hospitalières
**Points Clés Abordés :**
- 3 personas de patients (Silhouette 0.343)
- Typologie en 3 tiers hospitaliers via PCA (Silhouette 0.378)

**Notes de Présentation (Speaker Notes) :**
> *"L'analyse non supervisée apporte une valeur descriptive immédiate. Pour les patients, nous isolons 3 profils nets : les jeunes en ambulatoire préventif, les seniors multimorbides à haut coût, et les adultes à risque métabolique. Côté structures, la PCA valide la séparation entre centres de santé, hôpitaux de district et centres de référence."*

---

### Slide 11 : Détection des Anomalies & Circuit de Révision Humaine
**Points Clés Abordés :**
- 49 factures extrêmes
- 211 discordances réclamation > facture
- Principe de tri humain prioritaire (non requalifiable en fraude brute)

**Notes de Présentation (Speaker Notes) :**
> *"En matière de détection d'anomalies, nous isolons 49 factures extrêmes, 211 réclamations où le montant réclamé dépasse le montant facturé, et 10 collisions d'identités. Sur le plan déontologique, nous rappelons qu'une anomalie détectée est une invitation à l'audit humain et non une preuve irréfutable de fraude."*

---

### Slide 12 : Intelligence Artificielle Explicable : Attributions SHAP
**Points Clés Abordés :**
- Attribution SHAP sur réclamations et facturation
- Distinction formelle entre attribution statistique et causalité clinique

**Notes de Présentation (Speaker Notes) :**
> *"Pour ouvrir la boîte noire, nous utilisons SHAP TreeExplainer. Les drivers majeurs sont l'affiliation d'assurance pour les réclamations et l'âge pour la facturation. Cependant, nous insistons sur le fait qu'une valeur SHAP mesure une attribution statistique au sein du modèle et ne prouve pas une causalité biologique ou médicale."*

---

### Slide 13 : Architecture de Déploiement MLOps & Service API FastAPI
**Points Clés Abordés :**
- Schéma d'architecture MLOps 10 couches
- Microservice FastAPI opérationnel avec Pydantic
- Latence d'inférence < 15 ms

**Notes de Présentation (Speaker Notes) :**
> *"Pour la production, nous concevons une architecture cible en 10 couches allant de l'ingestion Kafka à la surveillance de dérive Evidently. Sur le plan pratique, nous avons concrètement développé et testé l'API FastAPI dans deployment/app.py, qui répond en moins de 15 ms avec une validation Pydantic stricte."*

---

### Slide 14 : Tests, Reproductibilité, Sécurité Git & Gouvernance Légale
**Points Clés Abordés :**
- 14/14 tests Pytest validés
- Pipeline reproductible de bout en bout
- Analyse légale Loi 058/2021 et obligation Human-in-the-Loop

**Notes de Présentation (Speaker Notes) :**
> *"Notre code est couvert par 14 tests Pytest exécutés avec succès. Côté éthique et conformité légale à la loi rwandaise n° 058/2021, nous soulignons qu'implémenter des filtres d'anonymisation ne dispense pas des formalités juridiques auprès de la NCSA, et que le principe Human-in-the-Loop reste obligatoire en santé."*

---

### Slide 15 : Conclusion Générale, Feuille de Route & Échanges (Q&A)
**Points Clés Abordés :**
- Roadmap à 3, 6 et 12 mois
- Synthèse de la rigueur déontologique
- Session de questions-réponses

**Notes de Présentation (Speaker Notes) :**
> *"Pour conclure, la véritable valeur ajoutée de ce projet réside dans sa totale transparence scientifique et son architecture logicielle robuste. Nous recommandons en priorité d'intégrer un module ADT dans OpenMRS pour débloquer la durée de séjour et d'activer le filtre pré-soumission des réclamations. Je suis maintenant disponible pour vos questions."*

---

