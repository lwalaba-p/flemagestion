# 🚀 Déploiement de votre Centre FLEM

## 📦 Votre Dépôt GitHub
**Repository** : `https://github.com/lwalaba-p/flemagestion`

## ⚡ Déploiement Rapide sur Render.com

### 1. 🌐 Aller sur Render.com
- Ouvrir https://render.com
- Cliquer **"Get Started for Free"**
- Se connecter avec votre compte GitHub

### 2. ➕ Créer un Web Service
1. Cliquer **"New +"** → **"Web Service"**
2. Connecter votre repository : `lwalaba-p/flemagestion`
3. Cliquer **"Connect"**

### 3. ⚙️ Configuration du Service
Remplir les informations :

**Basic Settings :**
- **Name** : `flem-hospital` (ou le nom de votre choix)
- **Environment** : `Python 3`
- **Region** : `Oregon (US West)` (le plus proche)
- **Branch** : `master` (ou `main`)

**Build & Deploy :**
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn app:app`

### 4. 🗄️ Créer une Base de Données PostgreSQL
1. Sur Render, cliquer **"New +"** → **"PostgreSQL"**
2. **Name** : `flem-database`
3. **Database** : `flem_hospital`
4. **User** : `flem_user`
5. Cliquer **"Create Database"**

### 5. 🔧 Variables d'Environnement
Dans votre Web Service, aller dans **"Environment"** et ajouter :

```
SECRET_KEY = votre_cle_secrete_tres_longue_et_complexe_ici_changez_la
FLASK_ENV = production
DATABASE_URL = postgresql://flem_user:motdepasse@host:port/flem_hospital
```

**Important** : Remplacer `DATABASE_URL` par l'URL réelle de votre base PostgreSQL (visible dans les détails de votre base de données).

### 6. 🚀 Déployer
1. Cliquer **"Create Web Service"**
2. Attendre le déploiement (2-3 minutes)
3. Votre app sera accessible sur : `https://flem-hospital.onrender.com`

## 🎯 Alternative : Railway.app (Plus Simple)

### 1. 🌐 Aller sur Railway
- Ouvrir https://railway.app
- Se connecter avec GitHub

### 2. 🚀 Déployer en 1 Clic
1. Cliquer **"Deploy from GitHub repo"**
2. Sélectionner `lwalaba-p/flemagestion`
3. Railway détecte automatiquement Python
4. Cliquer **"Deploy Now"**

### 3. 🗄️ Ajouter une Base de Données
1. Cliquer **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway configure automatiquement

### 4. 🔧 Variables d'Environnement
Railway détecte automatiquement les variables nécessaires.

## ✅ Vérification du Déploiement

### Tester votre Application
1. Aller sur votre URL (ex: `https://flem-hospital.onrender.com`)
2. Créer un compte utilisateur
3. Tester les fonctionnalités principales

### Comptes de Test Disponibles
- **Admin** : `admin` / `admin123`
- **Médecin** : `medecin1` / `medecin123`
- **Pharmacien** : `pharmacien1` / `pharmacien123`

## 🔍 Dépannage

### Problèmes Courants
1. **Erreur 500** : Vérifier les logs et les variables d'environnement
2. **Base de données** : S'assurer que DATABASE_URL est correcte
3. **Timeout** : L'app se met en veille après 15 min d'inactivité (normal sur le plan gratuit)

### Voir les Logs
- **Render** : Dashboard → Logs
- **Railway** : Dashboard → Deployments → Logs

## 🎉 Félicitations !

Votre système Centre FLEM sera accessible à :
```
https://flem-hospital.onrender.com
```

**Avec toutes ces fonctionnalités :**
- 🏥 Gestion hospitalière complète
- 👥 Authentification et rôles
- 💊 Pharmacie intégrée
- 💰 Facturation automatique
- 📱 Interface moderne
- 🌐 Accessible partout dans le monde

## 📱 Partage

Une fois déployé, vous pouvez :
- Partager l'URL avec vos utilisateurs
- Créer des comptes pour votre équipe
- Utiliser l'application depuis n'importe où
- Gérer votre centre hospitalier en ligne

**Votre système Centre FLEM est maintenant en ligne ! 🏥✨**
