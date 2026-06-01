## Table des matières
1. [Entreprise concernée](#1-entreprise-concernée)
2. [Contexte business](#2-contexte-business)
3. [La problématique data (SMART)](#3-la-problématique-data-smart)
4. [Périmètre proposé](#4-périmètre-proposé)
5. [Bénéfices attendus chiffrés](#5-bénéfices-attendus-chiffrés)
6. [Hypothèses de faisabilité & Risques](#6-hypothèses-de-faisabilité--risques)
7. [Calendrier macro du projet](#7-calendrier-macro-du-projet-3-semaines)
8. [Tableau de suivi et KPIs du Projet](#8-tableau-de-suivi-et-kpis-du-projet)


# Note de cadrage - MusiQualité 
*Pour décision GO/NO-GO en COMEX du 04/06/2026 · Sponsor : Anthony Piano (Direction Marketing) · Date : 04/05/2026 · Référence : T01*
______________________________________________________________________________________
## 1. Entreprise concernée
MusiQualité est une école de musique privée prestigieuse qui compte 45 campus en France (cours d'instruments, de chant, et ateliers de groupe). Pour moderniser son approche pédagogique, l'école a lancé une plateforme en ligne permettant aux élèves d'enregistrer leurs exercices hebdomadaires à la maison et de les soumettre à leurs professeurs via une application dédiée. 



## 2. Contexte business
L'école de musique privée MusiQualité (45 campus en France, 25 M€ de CA), fait face à un flux massif de 1000 extraits audio envoyés chaque semaine par les élèves sur sa plateforme en ligne. 
Actuellement, le tri et l'aiguillage de ces fichiers vers différents départements (Cordes, Vents, Claviers...) se font manuellement par l'équipe administrative, ce qui génère des retards de correction et un coût de gestion estimé à 1,8 M€/an en perte de productivité. 

Caroline Clarinette, nouvelle Directrice Générale (ancienne directrice de l'Opéra de Paris), souhaite moderniser l'école en déployant un système automatisé de routage intelligent. L'enjeu est de capitaliser sur la donnée audio brute, pour produire un outil de tri actionnable à l'échelle, d'abord testé sur 5 campus pilotes (Paris-Marais, Lyon-Presqu'île, Bordeaux, Lille, Marseille), sous la pression du président Guillaume Guitare qui exige une modernisation rapide de l'infrastructure. 



## 3. La problématique data (SMART)
Pour chaque fichier audio déposé sur la plateforme des 5 campus pilotes (extraits de 3 secondes, format .wav ou .mp3), prédire la famille d'instruments parmi 7 catégories (Cordes frottées, Cordes pincées, Orgues/Claviers, Percussions, Pianos, Vents/Cuivre, Chant), grâce à un traitement par Réseau de Neurones Convolutif (CNN/TensorFlow) alimenté par des spectrogrammes de Mel (Librosa), avec une intégration dans le système de routage via une API Flask conteneurisée sous Docker, testable avant le 04/06/2026.



## 4. Périmètre proposé
- **✓ Inclus dans le périmètre** :
    - Les 5 campus pilotes cités (23262 fichiers de test éligibles).
    - Traitement audio via spectrogrammes de Mel (128 bandes de fréquences) + modèle CNN optimisé
    - Architecture MLOps : API Flask (Bloc5/app.py), environnement isolé et portable via Dockerfile.
    - Interface Web simplifiée en HTML pour le démonstrateur métier. 
    - Validation réglementaire (AIPD) signée par Anne Violon (DPO) pour valider la suppression des flux temporaires. 
- **✗ Exclus dans le périmètre** :
    - Le déploiement national sur les 40 autres campus (Phase 2).
    - Les fichiers corrompus ou de moins de 1 seconde. 
    - Les données textuelles d'évaluation des professeurs, jugées trop complexes pour la V1.
    - L'intégration directe dans l'application mobile des élèves (prévue en Phase 3).
    - Toute décision finale de suppression de fichier : l'IA propose un dossier de routage, l'humain reste superviseur (Respect de l'Article 22 du RGPD).



## 5. Bénéfices attendus chiffrés
- **ROI estimé** : Réduction du temps de traitement administratif de 2 minutes à 1,5 seconde par fichier. Economie d'échelle projetée entre 600 k€ et 1M€ par an à l'échelle nationale.
- **Investissement Phase 1 (R&D + Prototype Docker)** : 35 k€ HT (déjà validé sur l'enveloppe innovation).
- **Bénéfices secondaires** : Fluidification de la correction pour les professeurs, revalorisation du temps de travail du personnel administratif, image de marque moderne de l'école. 



## 6. Hypothèses de faisabilité & Risques
- **Faisabilité** : Le modèle hybride tolérant aux pannes (capable de basculer de 26 classes à 7 familles) garantit une exactitude de 75%, ce qui est supérieur au seuil métier exigé (70%).
- **Risques majeurs & Atténuation** :
    - *Risque* : Rejet de l'outil par le secrétariat -> *Atténuation* : Intégration d'une clé JSON claire action_industrialisation pour faciliter la compréhension. 
    - *Risque (RGPD)* : Capture accidentelle de voix d'élèves mineurs -> *Atténuation* : Intégration du code de sécurité os.remove() qui détruit instantanément l'audio après la prédiction (Zéro stockage de données personnelles).



## 7. Calendrier macro du projet (3 semaines)
- **J0** : Kick-off et validation des spécifications avec Anthony Piano.
- **J+10** : Prétraitement de la donnée audio (Librosa) et entraînement du CNN (Bloc4).
- **J+15** : Développement de l'API Flask et création de l'image Docker (Bloc5).
- **J+20 (04/06/2026)** : Restitution COMEX, démonstration de l'interface et validation pour le déploiement national. 



## 8. Tableau de suivi et KPIs du Projet

<table border="1" style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 10px; border: 1px solid #cccccc; text-align: left;">Indicateur de suivi</th>
      <th style="padding: 10px; border: 1px solid #cccccc; text-align: center;">Cible Horizon M+1</th>
      <th style="padding: 10px; border: 1px solid #cccccc; text-align: left;">Mode de mesure</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Précision du routage (Recall)</td>
      <td style="padding: 10px; border: 1px solid #cccccc; text-align: center;">>= 75%</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Évalué sur le dataset de test (23 262 fichiers)</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Disponibilité de l'API</td>
      <td style="padding: 10px; border: 1px solid #cccccc; text-align: center;">99,9%</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Logs du conteneur Docker en production</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Adoption secrétariat</td>
      <td style="padding: 10px; border: 1px solid #cccccc; text-align: center;">>= 80%</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">% de dossiers triés par l'IA uniquement</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Respect RGPD</td>
      <td style="padding: 10px; border: 1px solid #cccccc; text-align: center;">0 fichier stocké</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Audit automatique du dossier temporaire /app</td>
    </tr>
  </tbody>
</table>

