# Centre FLEM - Système de Gestion Hospitalière

## Description
Application web de gestion hospitalière pour le centre FLEM développée avec Flask et SQLite.

**Design :** Interface moderne avec couleurs bleu, blanc et touches de jaune
**Devise :** Prix affichés en CDF (Francs Congolais) avec équivalence en USD

## Fonctionnalités
- **Gestion des Patients** : Ajout, consultation et suivi des patients
- **Gestion du Personnel** : Gestion du personnel médical et administratif
- **Gestion des Rendez-vous** : Planification et suivi des rendez-vous
- **Gestion des Chambres** : Gestion des chambres et lits d'hospitalisation
- **Tableau de bord** : Statistiques et vue d'ensemble du centre

## Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   cd flemfinal
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python run.py
   ```
   
   Ou directement :
   ```bash
   python app.py
   ```

4. **Accéder à l'application**
   Ouvrez votre navigateur et allez à : `http://127.0.0.1:8080`

## Structure du projet
```
flemfinal/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── patients.html
│   ├── ajouter_patient.html
│   ├── detail_patient.html
│   ├── personnel.html
│   ├── ajouter_personnel.html
│   ├── rendez_vous.html
│   ├── ajouter_rendez_vous.html
│   ├── chambres.html
│   └── ajouter_chambre.html
└── flem_hospital.db      # Base de données SQLite (créée automatiquement)
```

## Base de données
L'application utilise SQLite avec les tables suivantes :
- **Patient** : Informations des patients
- **Personnel** : Informations du personnel médical
- **RendezVous** : Rendez-vous médicaux
- **Consultation** : Consultations et diagnostics
- **Chambre** : Chambres d'hospitalisation

## Utilisation

### Tableau de bord
- Vue d'ensemble des statistiques du centre
- Accès rapide aux fonctionnalités principales

### Gestion des Patients
- Ajouter de nouveaux patients
- Consulter la liste des patients
- Voir les détails d'un patient
- Suivre les rendez-vous et consultations

### Gestion du Personnel
- Ajouter du personnel médical
- Gérer les spécialités
- Suivre les informations de contact

### Gestion des Rendez-vous
- Planifier des rendez-vous
- Associer patients et médecins
- Gérer les types de consultations

### Gestion des Chambres
- Ajouter des chambres
- Gérer les types et prix
- Suivre le statut d'occupation

## Données de test
L'application inclut des données de test qui sont automatiquement créées au premier lancement :
- 1 patient de test
- 1 médecin de test
- 3 chambres de test

## Support
Pour toute question ou problème, contactez l'équipe de développement du centre FLEM.

## Licence
Propriétaire - Centre FLEM
