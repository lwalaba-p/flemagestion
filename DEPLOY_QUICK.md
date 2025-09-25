# 🚀 Déploiement Rapide - Centre FLEM

## ⚡ Déploiement en 5 minutes sur Render.com

### 1. 📤 Préparer le projet (Déjà fait!)
```bash
# Votre projet est déjà prêt avec Git initialisé
git status  # Vérifier que tout est commité
```

### 2. 🌐 Créer un repository GitHub
1. Aller sur https://github.com
2. Cliquer sur "New repository"
3. Nom: `flem-hospital`
4. Description: `Système de gestion hospitalière Centre FLEM`
5. Cliquer "Create repository"

### 3. 📤 Pousser le code sur GitHub
```bash
# Ajouter le remote GitHub
git remote add origin https://github.com/VOTRE-USERNAME/flem-hospital.git

# Pousser le code
git branch -M main
git push -u origin main
```

### 4. 🚀 Déployer sur Render.com
1. Aller sur https://render.com
2. Se connecter avec GitHub
3. Cliquer "New +" → "Web Service"
4. Connecter le repository `flem-hospital`
5. Configurer:
   - **Name**: `flem-hospital`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### 5. 🗄️ Créer la base de données
1. Sur Render, cliquer "New +" → "PostgreSQL"
2. Nom: `flem-database`
3. Copier l'URL de connexion

### 6. 🔧 Configurer les variables d'environnement
Dans votre Web Service sur Render, ajouter:
- `SECRET_KEY`: `votre_cle_secrete_tres_longue_et_complexe`
- `DATABASE_URL`: `postgresql://user:pass@host:port/dbname` (copié de la DB)
- `FLASK_ENV`: `production`

### 7. ✅ Déployer!
1. Cliquer "Create Web Service"
2. Attendre le déploiement (2-3 minutes)
3. Votre app sera sur: `https://flem-hospital.onrender.com`

## 🎯 Alternative: Railway.app

### Déploiement sur Railway (plus simple)
1. Aller sur https://railway.app
2. Se connecter avec GitHub
3. Cliquer "Deploy from GitHub repo"
4. Sélectionner `flem-hospital`
5. Railway détecte automatiquement Python
6. Ajouter une base PostgreSQL
7. Configurer les variables d'environnement
8. Déployer automatiquement!

## 🔍 Vérification du déploiement

### Tester l'application
1. Aller sur votre URL (ex: `https://flem-hospital.onrender.com`)
2. Créer un compte utilisateur
3. Tester les fonctionnalités principales

### Comptes de test
- **Admin**: `admin` / `admin123`
- **Médecin**: `medecin1` / `medecin123`
- **Pharmacien**: `pharmacien1` / `pharmacien123`

## 🛠️ Maintenance

### Mises à jour
```bash
# Modifier le code localement
git add .
git commit -m "Mise à jour"
git push origin main
# Le déploiement se fait automatiquement!
```

### Logs et monitoring
- Render: Dashboard → Logs
- Railway: Dashboard → Deployments → Logs

## 🆘 Dépannage

### Problèmes courants
1. **Erreur 500**: Vérifier les logs et les variables d'environnement
2. **Base de données**: S'assurer que DATABASE_URL est correcte
3. **Timeout**: Optimiser les requêtes lentes

### Support
- Documentation Render: https://render.com/docs
- Documentation Railway: https://docs.railway.app
- Issues GitHub: Créer une issue sur votre repository

## 💰 Coûts

### Render.com
- **Gratuit**: 750 heures/mois
- **Base de données**: PostgreSQL gratuit
- **Limite**: App se met en veille après 15 min d'inactivité

### Railway
- **Gratuit**: $5 de crédit/mois
- **Base de données**: Incluse
- **Limite**: App reste active

## 🎉 Félicitations!

Votre système Centre FLEM est maintenant en ligne et accessible partout dans le monde!

**URL de votre application**: `https://flem-hospital.onrender.com`

**Fonctionnalités disponibles**:
- ✅ Authentification et gestion des utilisateurs
- ✅ Gestion des patients et du personnel
- ✅ Système de rendez-vous
- ✅ Gestion de la pharmacie
- ✅ Facturation et hospitalisation
- ✅ Interface responsive et moderne
