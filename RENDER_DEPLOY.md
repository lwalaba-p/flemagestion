# 🚀 Déploiement sur Render.com - Guide Étape par Étape

## 📦 Votre Dépôt
**Repository** : `https://github.com/lwalaba-p/flemagestion`

## ⚡ Déploiement en 10 Minutes

### 1. 🌐 Créer un Compte Render
1. Aller sur **https://render.com**
2. Cliquer **"Get Started for Free"**
3. Se connecter avec votre compte **GitHub**
4. Autoriser Render à accéder à vos repositories

### 2. ➕ Créer un Web Service
1. Cliquer **"New +"** en haut à droite
2. Sélectionner **"Web Service"**
3. Dans la liste, trouver **"lwalaba-p/flemagestion"**
4. Cliquer **"Connect"**

### 3. ⚙️ Configuration du Service

**Basic Settings :**
- **Name** : `flem-hospital`
- **Environment** : `Python 3`
- **Region** : `Oregon (US West)` (recommandé)
- **Branch** : `master`

**Build & Deploy :**
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn app:app`

**Advanced Settings :**
- **Auto-Deploy** : `Yes` (recommandé)
- **Pull Request Previews** : `No`

### 4. 🗄️ Créer une Base de Données PostgreSQL

**Pendant que votre service se configure :**

1. Cliquer **"New +"** → **"PostgreSQL"**
2. **Name** : `flem-database`
3. **Database** : `flem_hospital`
4. **User** : `flem_user`
5. **Region** : `Oregon (US West)` (même région que votre service)
6. Cliquer **"Create Database"**

### 5. 🔧 Configurer les Variables d'Environnement

**Dans votre Web Service :**

1. Aller dans l'onglet **"Environment"**
2. Ajouter ces variables :

```
SECRET_KEY = flem_hospital_secret_key_2024_production_changez_la
FLASK_ENV = production
DATABASE_URL = postgresql://flem_user:motdepasse@host:port/flem_hospital
```

**Important** : 
- Remplacer `SECRET_KEY` par une clé secrète longue et complexe
- Remplacer `DATABASE_URL` par l'URL réelle de votre base PostgreSQL

**Pour obtenir l'URL de la base de données :**
1. Aller dans votre base PostgreSQL
2. Onglet **"Info"**
3. Copier **"External Database URL"**
4. Coller dans la variable `DATABASE_URL`

### 6. 🚀 Déployer
1. Cliquer **"Create Web Service"**
2. Attendre le déploiement (2-3 minutes)
3. Votre app sera accessible sur : `https://flem-hospital.onrender.com`

## ✅ Vérification

### Tester votre Application
1. Aller sur `https://flem-hospital.onrender.com`
2. Créer un compte utilisateur
3. Tester les fonctionnalités principales

### Comptes de Test
- **Admin** : `admin` / `admin123`
- **Médecin** : `medecin1` / `medecin123`
- **Pharmacien** : `pharmacien1` / `pharmacien123`

## 🔍 Dépannage

### Problèmes Courants

**1. Erreur 500 - Internal Server Error**
- Vérifier les logs dans l'onglet "Logs"
- Vérifier que `DATABASE_URL` est correcte
- Vérifier que `SECRET_KEY` est définie

**2. App se met en veille**
- Normal sur le plan gratuit
- L'app se réveille automatiquement au premier accès
- Peut prendre 30 secondes à 1 minute

**3. Erreur de base de données**
- Vérifier que la base PostgreSQL est créée
- Vérifier que `DATABASE_URL` est correcte
- Vérifier que la base est dans la même région

### Voir les Logs
1. Aller dans votre Web Service
2. Onglet **"Logs"**
3. Voir les erreurs en temps réel

## 🎉 Félicitations !

Votre système Centre FLEM est maintenant en ligne à :
```
https://flem-hospital.onrender.com
```

## 📱 Partage

Vous pouvez maintenant :
- Partager l'URL avec vos utilisateurs
- Créer des comptes pour votre équipe
- Utiliser l'application depuis n'importe où
- Gérer votre centre hospitalier en ligne

## 🔄 Mises à Jour

Pour mettre à jour votre application :
1. Modifier le code localement
2. Commiter et pousser vers GitHub :
   ```bash
   git add .
   git commit -m "Mise à jour"
   git push origin master
   ```
3. Render déploie automatiquement !

## 💰 Coûts

- **Plan gratuit** : 750 heures/mois
- **Base de données** : PostgreSQL gratuit
- **Limite** : App se met en veille après 15 min d'inactivité
- **HTTPS** : Inclus gratuitement

**Votre système Centre FLEM est maintenant en ligne ! 🏥✨**
