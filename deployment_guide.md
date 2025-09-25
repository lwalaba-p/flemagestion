# Guide de Déploiement - Centre FLEM

## 🚀 Options d'Hébergement Gratuit

### 1. **Render.com** (Recommandé)
- **Gratuit** : 750 heures/mois
- **Base de données** : PostgreSQL gratuit
- **Déploiement** : Automatique depuis GitHub
- **URL** : https://render.com

### 2. **Railway**
- **Gratuit** : $5 de crédit/mois
- **Base de données** : PostgreSQL inclus
- **Déploiement** : Depuis GitHub
- **URL** : https://railway.app

### 3. **Heroku** (Limité)
- **Gratuit** : Plus disponible pour les nouveaux comptes
- **Alternative** : Heroku Postgres payant

### 4. **PythonAnywhere**
- **Gratuit** : Compte gratuit limité
- **Base de données** : MySQL/PostgreSQL
- **URL** : https://pythonanywhere.com

## 📋 Préparation pour le Déploiement

### 1. Créer un fichier Procfile
```bash
# Créer un fichier Procfile (sans extension)
echo "web: gunicorn app:app" > Procfile
```

### 2. Mettre à jour requirements.txt
```bash
# Ajouter les dépendances de production
echo "gunicorn==20.1.0" >> requirements.txt
echo "psycopg2-binary==2.9.5" >> requirements.txt
```

### 3. Modifier app.py pour la production
```python
# Remplacer la dernière ligne
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 4. Créer un fichier .env pour les variables d'environnement
```bash
# Créer un fichier .env
echo "SECRET_KEY=votre_cle_secrete_ici" > .env
echo "DATABASE_URL=postgresql://user:pass@host:port/dbname" >> .env
```

## 🔧 Configuration pour Render.com

### 1. Créer un compte sur GitHub
1. Aller sur https://github.com
2. Créer un nouveau repository
3. Uploader tous les fichiers du projet

### 2. Déployer sur Render
1. Aller sur https://render.com
2. Se connecter avec GitHub
3. Cliquer sur "New +" → "Web Service"
4. Connecter votre repository GitHub
5. Configurer :
   - **Name** : flem-hospital
   - **Environment** : Python 3
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`

### 3. Configurer la base de données
1. Créer une base PostgreSQL sur Render
2. Copier l'URL de connexion
3. L'ajouter dans les variables d'environnement

## 🗄️ Migration vers PostgreSQL

### 1. Modifier app.py
```python
import os
from urllib.parse import urlparse

# Configuration de la base de données
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Parse l'URL pour PostgreSQL
    result = urlparse(DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{hostname}:{port}/{database}'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flem_hospital.db'
```

### 2. Mettre à jour requirements.txt
```bash
echo "psycopg2-binary==2.9.5" >> requirements.txt
```

## 🔒 Sécurité en Production

### 1. Variables d'environnement
```bash
SECRET_KEY=votre_cle_secrete_tres_longue_et_complexe
FLASK_ENV=production
```

### 2. Désactiver le mode debug
```python
app.run(debug=False)  # En production
```

## 📱 Configuration du Domaine

### 1. Domaine personnalisé (optionnel)
- Acheter un domaine (ex: flem-hospital.com)
- Configurer les DNS vers Render
- Activer HTTPS automatique

### 2. Sous-domaine Render
- Votre app sera accessible sur : https://flem-hospital.onrender.com

## 🚀 Étapes de Déploiement Rapide

### 1. Préparer le projet
```bash
# Dans le dossier du projet
git init
git add .
git commit -m "Initial commit"
```

### 2. Pousser sur GitHub
```bash
git remote add origin https://github.com/votre-username/flem-hospital.git
git push -u origin main
```

### 3. Déployer sur Render
1. Connecter le repository
2. Configurer les variables d'environnement
3. Déployer automatiquement

## 📊 Monitoring et Maintenance

### 1. Logs
- Accéder aux logs sur Render Dashboard
- Surveiller les erreurs et performances

### 2. Sauvegarde
- Base de données sauvegardée automatiquement
- Exporter les données régulièrement

### 3. Mises à jour
- Push sur GitHub = déploiement automatique
- Tester en local avant déploiement

## 💡 Conseils d'Optimisation

### 1. Performance
- Utiliser un CDN pour les assets statiques
- Optimiser les requêtes de base de données
- Mettre en cache les données fréquentes

### 2. Sécurité
- Changer la SECRET_KEY en production
- Utiliser HTTPS uniquement
- Limiter les tentatives de connexion

### 3. Coûts
- Surveiller l'utilisation des ressources
- Optimiser les requêtes pour éviter les timeouts
- Utiliser les limites gratuites efficacement

## 🆘 Support et Dépannage

### Problèmes courants :
1. **Erreur de base de données** : Vérifier l'URL de connexion
2. **Timeout** : Optimiser les requêtes lentes
3. **Erreur 500** : Vérifier les logs sur Render
4. **Variables d'environnement** : S'assurer qu'elles sont définies

### Ressources utiles :
- Documentation Render : https://render.com/docs
- Documentation Flask : https://flask.palletsprojects.com/
- Support communautaire : Stack Overflow
