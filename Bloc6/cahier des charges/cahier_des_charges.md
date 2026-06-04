## Table des matières
1. [Contexte et enjeux](#1-contexte-et-enjeux)
2. [Objectifs](#2-objectifs)
    - 2.1 [Objectif principal](#21-objectif-principal)
    - 2.2 [Objectifs mesurables](#22-objectifs-mesurables)
3. [Périmètre)](#3-périmètre)
    - 3.1 [Périmètre fonctionnel - phase 1](#31-périmètre-fonctionnel---phase-1-démo--confinement)
    - 3.2 [Périmètre fonctionnel - phase 2](#32-périmètre-fonctionnel---phase-2-pilote)
    - 3.3 [Hors périmètre](#33-hors-périmètre-a-ce-stade)
4. [Livrables](#4-livrables)
5. [Contraintes](#5-contraintes)
    - 5.1 [Contraintes techniques](#51-contraintes-techniques)
    - 5.2 [Contraintes RGPD](#52-contraintes-rgpd)
    - 5.3 [Contraintes métier](#53-contraintes-métier)
6. [Critères de succès et Définition of Done (DOD)](#6-critères-de-succès-et-definition-of-done-dod)
7. [Annexes](#7-annexes)
8. [Validation](#8-validation)


# Cahier des charges -- Système "Intel-Safe"
*Projet de routage automatisé des flux audio -- Ecoles MusiQualité · v1 · 14 mai 2026*

<table border="1" style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Projet</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Routage intelligent "Intel-Safe -- Phase 1 (Démo/Docker) + phase 2 (Pilote 5 campus)</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Sponsor</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Anthony Piano, Directeur Marketing & Innovation pédagogique</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Validation</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">DG : Caroline Clarinette (au Comex du 04/06/2026) · Président : Guillaume Guitare (zrbitrage phase 2)</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Auteur</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Angèle Despretz, Chef de Projet Data & MLOPS</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Version</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">v1 du 14/05/2026 -- A valider par Anthony Piano le 16/05/2026</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Statut</td>
      <td style="padding: 10px; border: 1px solid #cccccc; color : red">EN VALIDATION SPONSOR</td>
    </tr>
  </tbody>
</table>



## 1. Contexte et enjeux
L'école de musique privée MusiQualité (45 campus en France, 25 M€ de CA), fait face à un flux massif de 10 000 extraits audio envoyés chaque semaine par les élèves sur sa plateforme en ligne. 
Actuellement, le tri et l'aiguillage de ces fichiers vers différents départements (Cordes, Vents, Claviers...) se font manuellement par l'équipe administrative, ce qui génère des retards de correction et un coût de gestion estimé à 1,8 M€/an en perte de productivité.  

La direction souhaite implémenter l'outil Intel-Safe pour automatiser ce routage. Le projet est soutenu politiquement par la nouvelle DG (Caroline Clarinetten ex-Opéra de Paris) qui veut démontrer la modernisation des infrastructures du groupe lors du COMEX du 04/06/2026.



## 2. Objectifs
### 2.1 Objectif principal
Construire un modèle de Deep Learning capable de classifier automatiquement les enregistrements des élèves pour les router en temps réel vers les 5 campus pilotes (Paris-Marais, Lyon-Presqu'île, Bordeaux, Lille, Marseille), réduisant le délai de traitement de l'audio à moins de 2 secondes. 


### 2.2 Objectifs mesurables
- **Exactitude globale (Accuracy)** : >= 75% sur les 7 familles d'instruments cibles.
- **Vitesse de traitement** : Temps de réponse de l'API <= 2 secondes par fichier audio.
- **Taux d'automatisation** : >= 70% des fichiers entrants routés directement sans aucune correction humaine requise par les secrétariats.
- **Taux d'erreur RGPD** : Strictement 0 fichier élève stocké sur le conteneur d'analyse après traitement. 


## 3. Périmètre
### 3.1 Périmètre fonctionnel - phase 1 (Démo & Confinement)
- **Classification** des fichiers audio de 3 secondes (.wav et .mp3) sur 7 catégories (Cordes frottées, Cordes pincées, Orgues/Clavier, Percussions, Piano, Vents/Cuivres, Chant).
- **Architecture technique isolée** : API Flask (app.py) intégrée dans une image Docker pour garantir la portabilité. 
- **Démonstrateur** avec interface Web HTML simplifiée pour le COMEX du 04/06/2026.
- **Données d'entraînement** : Echantillon extrait des Datasets IRMAS et Philarmonia (23 262 fichiers éligibles).


### 3.2 Périmètre fonctionnel - phase 2 (Pilote)
- Déploiement de l'infrastructure Docker sur les serveurs locaus des 5 campus pilotes. 
- Mise en production d'un tableau de bord de suivi de l'adoption de l'IA par le secrétariat. 
- Formation des équipes administratives des 5 campus (1/2 journée par équipe).


### 3.3 Hors périmètre (A ce stade)
- L'extension du système aux 40 autres campus nationaux (phase 2).
- L'analyse des fichiers audio corrompus ou d'une durée inférieure à 1 seconde. 
- Le traitement des commentaires textuels des professeurs (données non structurées, exclues de la V1).
- L'intégration de l'IA directement à l'intérieur de l'application mobile native des élèves (Phase 3).


## 4. Livrables

<table border="1" style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 10px; border: 1px solid #cccccc; text-align: left;">Livrable</th>
      <th style="padding: 10px; border: 1px solid #cccccc; text-align: left;">Description</th>
      <th style="padding: 10px; border: 1px solid #cccccc; text-align: center;">Phase</th>
      <th style="padding: 10px; border: 1px solid #cccccc; text-align: left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Note de cadrage</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Document stratégique de validation validé par le sponsor (MQ-T01).</td>
      <td style="padding: 10px; border: 1px solid #cccccc; text-align: center;">Phase 1</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">.md / .docx</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Modèle de Deep Learning</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Réseau de neurones CNN entraîné et optimisé (26 classes réduites à 7 familles).</td>
      <td style="padding: 10px; border: 1px solid #cccccc; text-align: center;">Phase 1</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Python + .h5 (Keras)</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">API & Conteneurisation</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Script Flask (app.py) et environnement virtualisé Dockerfile.</td>
      <td style="padding: 10px; border: 1px solid #cccccc; text-align: center;">Phase 1</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Code + Image Docker</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Analyse RGPD (AIPD)</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Dossier de conformité et de sécurité validé par Anne Violon (DPO).</td>
      <td style="padding: 10px; border: 1px solid #cccccc; text-align: center;">Phase 1</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">.docx</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Dashboard de suivi</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Indicateurs clés (KPI) de suivi de l'adoption et de la disponibilité de l'API.</td>
      <td style="padding: 10px; border: 1px solid #cccccc; text-align: center;">Phase 2</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">HTML / Tableau de bord</td>
    </tr>
  </tbody>
</table>



## 5. Contraintes
### 5.1 Contraintes techniques
- **Prétraitement obligatoire** : Conversion obligatoire du signal audio temporel en spectrogrammes de Mel (taille 128 x 128) avant injection dans le CNN
- **Mémoire et Isolation** : L'application doit tourner de façon autonome dans son conteneur Docker sans dépendances logicielles extérieures à installer sur les PC du secrétariat. 
- **Gestion des ressources** : Utilisation d'un modèle optimisé (TensorFlow-CPU) pour ne pas nécessiter de carte graphique (GPU) onéreuse sur les serveurs des campus pilotes. 


### 5.2 Contraintes RGPD
- **AIPD obligatoire** : Validation impérative par Anne Violon (DPO) avant le passage en phase pilote.
- **Rétention de données** : Interdiction stricte de stocker ou d'archiver les fichiers audio soumis. Le code de l'API Flask doit intégrer une routine de nettoyage automatique (os.remove()) immédiatement après l'envoi de la réponse JSON.
- **Article 22 du RGPD** : L'IA ne peut pas prendre de décision unilatérale. Le choix de routage de l'IA reste modifiable par l'opérateur humain.

### 5.3 Contraintes métier
- **Date butoir** : Présentation du démonstrateur fonctionnel au COMEX le 04/06/2026 de manière impérative.
- **Vulgarisation nécessaire** : L'explicabilité du modèle doit être simplifiée (notion de signature visuelle du son) pour rassurer le personnel administratif de MusiQualité.


## 6. Critères de succès et Definition of Done (DoD)
<table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 11pt; margin-bottom: 30px;">
  <thead>
    <tr style="background-color: #34495e; color: #ffffff;">
      <th style="padding: 12px; border: 1px solid #2c3e50; text-align: left; width: 25%;">Critère</th>
      <th style="padding: 12px; border: 1px solid #2c3e50; text-align: left; width: 55%;">Definition of Done (DoD)</th>
      <th style="padding: 12px; border: 1px solid #2c3e50; text-align: center; width: 20%;">Cible</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #ffffff;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Fiabilité IA</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Métriques de précision validées sur l'échantillon de test temporel.</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold;">Accuracy &ge; 75%</td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Isolation Docker</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">L'image build sans erreur et l'API Flask répond correctement aux requêtes Postman.</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center;">Image validée localement</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Conformité CNIL</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">AIPD signée par la DPO, conforme à la méthodologie officielle de la CNIL.</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center;">Signée avant J+20</td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Validation Métier</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Démonstration en direct réussie devant Caroline Clarinette au COMEX (durée 7 min).</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center;">GO / NO-GO obtenu</td>
    </tr>
  </tbody>
</table>



## 7. Annexes
- **Annexe A** — Cartographie des parties prenantes (Anthony Piano, Caroline Clarinette, Anne Violon, Guillaume Guitard).
- **Annexe B** — Matrice d'analyse des besoins métiers du secrétariat.
- **Annexe C** — Architecture du réseau de neurones convolutif (CNN).
- **Annexe D** — Analyse d'impact relative à la protection des données (AIPD).


## 8. Validation
<table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 11pt; margin-bottom: 30px;">
  <thead>
    <tr style="background-color: #34495e; color: #ffffff;">
      <th style="padding: 12px; border: 1px solid #2c3e50; text-align: left; width: 30%;">Indicateur de suivi</th>
      <th style="padding: 12px; border: 1px solid #2c3e50; text-align: center; width: 20%;">Cible Horizon M+1</th>
      <th style="padding: 12px; border: 1px solid #2c3e50; text-align: left; width: 50%;">Mode de mesure</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #ffffff;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Précision du routage (Recall)</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold;">&ge; 75%</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Évalué rétroactivement sur le dataset de test (23 262 fichiers).</td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Disponibilité de l'API</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold;">99,9%</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Logs du conteneur Docker en environnement de pré-production.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Adoption secrétariat</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold;">&ge; 80%</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">% de dossiers triés automatiquement par l'IA et validés sans modification.</td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Respect RGPD</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold;">0 fichier stocké</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Audit automatique et continu du dossier temporaire <span style="font-family: monospace;">/app</span>.</td>
    </tr>
  </tbody>
</table>