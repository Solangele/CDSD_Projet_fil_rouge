# Routage automatique Intel-Safe : Ce que nous avons appris

*Automatisation du routage audio pour le groupe MusiQualité.* 
Document préparé par Angèle Despretz (Chef de Projet Data et IA), avec l'appui de l'équipe DataScience -- 10 juin 2026
_________________________________________________________________________________________________________________________

## Pourquoi nous avons lancé ce projet
Avec 45 campus, France et un chiffre d'affaires de 25 M€, Musiqualité fait face à un défi logistique majeur : la gestion d'un flux massif de 10 000 extraits audio envoyés chaque semaine par nos élèves sur notre plateforme en ligne. 

Actuellement, le tri, la qualification et l'aiguillage de ces fichiers vers les différents départements pédagogiques (Cordes; Vents, Claviers...) sont effectués entièrement à la main par l'équipe administrative. Ce goulot d'étranglement génère des retards importants dans la correction des élèves et représente un coût de gestion annuel estimé à 1,8 M€ en pure perte de productivité. 

L'objectif du projet : Déployer l'outil Intel-Safe (Propulsé par notre plateforme DataPulse) pour automatiser ce routage dès le téléversement des fichiers, afin de libérer du temps administratif et d'accélérer le rythme des corrections pédagogiques. 



## Ce que nous avons livré (Phase 1 -- Démo COMEX du 04 juin 2026)
Une première version fonctionnelle (l'interface Web et l'API Flask de la plateforme DataPulse) capable de pré-classifier les flux. Pour chaque extrait audio envoyé par un élève, l'outil analyse instantanément ses caractéristiques physiques et sa signature accoustique (durée, taille en Mo, et le Centroïde Spectral qui calcul le centre de gravité des fréquences pour identifier le timbre de l'instrument).

L'outil produit ensuite une suggestion de routage automatique vers l'une des 7 familles cibles (Cordes frottées, Vents et Cuivres...).

L'humain reste dans la boucle : le système propose, l'équipe administrative ou pédagogique valide en un clic en fonction des % de propabilité d'exactitude. L'outil a été entraîné sur un échantillon historique de 8 mois, extrait de notre base PostgreSQL Gold (datapulse_db) et validé par un test à l'aveugle. 



## Une piste type -- Pour rendre cela concret
<p style = "background-color : #3080c5; border : 2px solid #061d76;">
    Fichier élève reçu sur la plateforme : (02)don't kill the whale-2.wav
    - Le problème actuel : Noyé au milieu des 1 000 envois de la semaine, ce fichier doit être écouté manuellement par un agent pour savoir s'il doit aller au département Cordes ou au département Vents par exemple.  
    - L'action d'Intel-Safe : Dès sont téléversement, l'algorithme a analysé le signal. Même si l'élève n'a pas renseigné ses métadonnées, le modèle calcule son Centroïde Spectral. Par exemple : constatant une signature riche en hautes fréquences (harmoniques au-delà de 4000 Hz), il l'attribue immédiatement à la famille des cordes frottées. 
    - Impact : Le fichier est poussé instantanément dans le bon tableau de bord du professeur concerné. Sur l'ensemble du flux de l'école, l'outil détecte et route correctement environ 7 cas sur 10 (taux de bonne détection / Rappel de 70%).
</p>


## Le retour sur investissement
La phase 1 de cadrage, d'analyse exploratoire des données (EDA) et de modélisation de l'API nous a coûté 36 000€ HT (parfaitement dans l'enveloppe de 35 000€ à 1 000€ près). La phase 2 de déploiement global requiert un investissement complémentaire de 100 000€ sur 6 mois. 


## Gain estimé (Phase 1+2)
<p style = "background-color : #58d58d; border : 2px solid #0c9946;">
    600 k€ à 1 M€ sur 12 mois 
    Soit un retour sur investissement entre 4 et 7 fois la mise — payback en 5-6 mois. 
</p>

Hypothèse opérationnelle : Si l'outil permet aux équipes des 5 campus pilotes de traiter automatiquement et sans friction seulement 1 dossier sur 4 (taux de rétention / routage automatique de 25%), l'impact dépasse les 600 000€. Si le taux de validation fluide monte à 1 dossier sur 2.5, le gain d'efficacité atteint le million d'euros. 


## Conformité et éthique
Une Analyse d'Impact sur la Protection des Données (AIPD) a été réalisée par Anne Violon (DPO du groupe) et validée le 01/06/2026. Le traitement massif des données audios de nos élèves repose sur l'intérêt légitime de l'école MusiQualité (article 6.1.f du RGPD) afin d'améliorer la qualité de ses services. 
Les élèves sont informés de cette indexation par un encart transparent dans la newsletter d'avril et disposent d'un droit d'opposition technique (champ Salesforce "opt_out_scoring" activé le 27 mars). Aucune donnée sensible (comme les données privées ou d'identification) n'est lue par l'IA. De plus, l'équipe administrative gardant la main sur plus de 15% des choix finaux, le projet reste totalement exclu du champ des décisions 100% automatisées (article 22 du RGPD).


## Phase 2 : Ce que nous proposons
Déploiement industriel de la solution sur les 5 campus pilotes du groupe MusiQualité (Paris-Marais, Lyon-Presqu'île, Bordeaux, Lille, Marseille). Connexion de notre API Flask à notre CRM Salesforce et à l'architecture Snowflake pour centraliser le flux des 1 000 fichiers hebdomadaires. 

Formation des équipes administratives des 5 campus pilotes (1/2 journée par centre, animée par Camille Bariton) et mise à disposition d'un tableau de bord de suivi pour Sophie et Caroline. 

- Calendrier : Démarrage le 1er mai, plein régime au 1er juillet, premier bilan à 6 mois. 
- Décision sollicitée du Board : Validation du budget de la phase 2 de 100 k€ HT et du périmètre des 5 campus pilotes. 


*Contacts projet : Angèle Despretz (Direction de Projet Date & IA -- MusiQualité), Anthony Piano (Direction Marketing -- MusiQualité), Mohamed Kassemi (Cabien Conseil DataPulse), Anne Violon (DPO), Medhi Banjo (Responsable CRM Salesforce).*


