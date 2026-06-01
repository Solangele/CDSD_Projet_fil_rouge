## Table des matières
1. [Présentation et finalité](#1-présentation-et-finalité)
2. [Evaluation détaillée](#2-evaluation-détaillée)
3. [Alternatives évaluées](#3-alternatives-évaluées)
4. [Recommandation](#4-recommandation)
5. [Plan d'action](#5-plan-daction)
6. [Sources documentaires](#6-sources-documentaires)


# Fiche de Veille Technologique
*Cas MusiQualité · Compétence 6.2 · Auteur : Angèle Despretz · Date d'évaluation : 04/06/2026*


<table border="1" style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Techno évaluée</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Grad-CAM (Gradient-weighted Class Activation Mapping)</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Catégorie</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Deep Learning Explainability & Computer Vision — Bibliothèque d'explicabilité pour réseaux de neurones (TensorFlow / Keras)</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Source primaire</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Repository officiel Keras-io (keras.io/examples/vision/grad_cam/) · Documentation TensorFlow Core · Note technique interne d'Anthony Piano (Réf: MQ-S07)</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cccccc; font-weight: bold;">Projet concerné</td>
      <td style="padding: 10px; border: 1px solid #cccccc;">Routage automatisé "Intel-Safe" — phase 1 (Démo) + phase 2 (Pilote 5 campus)</td>
    </tr>
  </tbody>
</table>


## 1. Présentation et finalité
Grad-CAM est une technique d'explicabilité visuelle pour les Réseaux de neurones Convolutifs (CNN). Elle utilise les gradients de la dernière couche convolutive pour générer une carte de chaleur (Heatmap) sur l'image d'entrée, mettant en évidence les régions exactes qui ont poussé le modèle à prendre sa décision. 

Pour le projet MusiQualité, notre modèle n'écoute pas directement l'audio brut, il analyse une image : le spectrogramme de Mel généré par Librosa. 
L'enjeu de cette veille est de pouvoir afficher visuellement aux secrétariats et à la DG (Caroline Clarinette) quelles plages de fréquences et quels motifs harmoniques l'IA a détéctés pour classifier un instrument (ex : mettre en surbrillance rouge les fréquences aiguës caractéristiques du chant ou de la clarinette). C'est une exigence forte pour lever la résistance au changement des équipes et respecter l'esprit de l'Article 22 du RGPD. 


## 2. Evaluation détaillée
<table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 11pt; margin-bottom: 30px;">
  <thead>
    <tr style="background-color: #34495e; color: #ffffff;">
      <th style="padding: 12px; border: 1px solid #2c3e50; text-align: left; width: 25%;">Critère</th>
      <th style="padding: 12px; border: 1px solid #2c3e50; text-align: center; width: 15%;">Note (sur 5)</th>
      <th style="padding: 12px; border: 1px solid #2c3e50; text-align: left; width: 60%;">Justification</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #ffffff;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Maturité techno</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold; color: #27ae60;">5 / 5</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Technique publiée en 2017 par l'IEEE, devenue le standard académique et industriel incontournable pour l'explicabilité des réseaux de neurones (CNN).</td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Communauté</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold; color: #27ae60;">5 / 5</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Des milliers de dépôts d'implémentation sur GitHub et d'échanges Stack Overflow. Intégrée nativement dans la plupart des frameworks de XAI (e.g., Lucent, tf-explain).</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Courbe d'apprentissage</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold; color: #f39c12;">3.5 / 5</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">L'extraction mathématique des cartes de gradients demande une bonne maîtrise de l'API de calcul de TensorFlow (GradientTape), mais l'implémentation standard reste rapide.</td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Coût d'usage</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold; color: #27ae60;">5 / 5</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Totalement open-source (aucune licence logicielle). Ne requiert aucune infrastructure cloud payante supplémentaire, s'exécute localement dans le conteneur Docker.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Compatibilité stack</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold; color: #27ae60;">5 / 5</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Parfaite synergie avec notre architecture logicielle : TensorFlow/Keras (modèle d'IA), Flask (API backend) et environnement conteneurisé Docker.</td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Performance / scaling</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold; color: #27ae60;">4 / 5</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Calcul ultra-rapide en tâche de fond (quelques millisecondes par inférence). Totalement transparent pour l'utilisateur final sur l'interface Web HTML.</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 12px; border: 1px solid #dddddd; font-weight: bold;">Conformité RGPD</td>
      <td style="padding: 12px; border: 1px solid #dddddd; text-align: center; font-weight: bold; color: #27ae60;">5 / 5</td>
      <td style="padding: 12px; border: 1px solid #dddddd;">Répond nativement à l'obligation de transparence algorithmique (Article 22). Validation par Anne Violon (DPO) intégrée dans l'AIPD.</td>
    </tr>
  </tbody>
</table>


## 3. Alternatives évaluées
Trois approches technologiques ont été mises en concurrence pour cette veille d'explicabilité :
- **Grad-CAM** -- Référence retenue ici : explicabilité locale visuelle parfaite pour notre pipeline qui traite le son sous forme d'image (spectrogramme).
- **LIME** (pour images) -- Segmentation de l'image en super-pixels. Moins précis sur des spectrogrammes de Mel continus et temps de calcul beaucoup trop lourd pour notre conteneur Docker léger. 
- **Feature Importance globale** -- Donne uniquement le poids global des variables sur l'ensemble de l'apprentissage du CNN. Ne permet par de comprendre l'erreur ou la décision sur un fichier audio spécifique envoyé en temps réel par un élève. 


## 4. Recommandation
<p style = "background-color : #58d58d; border : 2px solid #0c9946;">
    RECOMMANDE -- ADOPTER GRAND-CAM. Adoption immédiate pour la Phase 1 (Démonstrateur COMEX du 04/04/2026) et déploiement en Phase 2 (Pilote 5 campus). L'algorithme sera encapsulé dans le script Bloc5/app.py pour renvoyer la heatmap du spectrogramme en surimpression directement sur l'interface HTML de démonstration métier.
</p>


## 5. Plan d'action
- Angèle Despretz (Chef de Projet/Data Scientist) -- Ecriture de la fonction d'extraction des cartes d'activation de la dernière couche Conv2D dans le script d'inférence (Prévu à J+10)
- Angèle Despretz -- Intégration de la génération d'images composites (Spactrogramme + Heatmap) pour l'affichage dynamique sur l'interface Web HTML (Prévu à J+15).
- Anthony Piano (Sponsor Marketing) -- Conceptiopn d'un guide d'interprétation visuelle de 2 pages à destination du secrétariat des 5 campus pilotes pour vulgariser les fréquences. 
- Anne Violon (DPO) -- Mentionner l'utilisation de Grad-CAM dans l'AIPD pour documenter notre conformité à l'obligation d'explicabilité via-à-vis des usagers. 


## 6. Sources documentaires
- Selvaraju et al., 2017, "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization", IEEE International Conference on Computer Vision (ICCV).
- Documentation officielle Keras Vision Core : keras.io/examples/vision/grad_cam/
- CNIL, Guide pratique "Gérer les risques des systèmes d'Intelligence Artificielle", volet explicabilité et traçabilité.
- Note de cadrage de projet MusiQualité (MQ-T01).