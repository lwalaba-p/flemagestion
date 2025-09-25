# 🔧 Dépannage Render - Centre FLEM

## 🚨 Problème : Serveur tombe après login

### ✅ Solutions appliquées :

#### 1. **Correction du code principal**
- ✅ Séparé `app.run()` du code principal
- ✅ Ajouté `if __name__ == '__main__':`
- ✅ Configuration Gunicorn optimisée

#### 2. **Gestion d'erreurs robuste**
- ✅ Logging configuré pour Render
- ✅ Gestionnaire d'erreurs global
- ✅ Template d'erreur personnalisé
- ✅ Validation des données de login

#### 3. **Configuration de production**
- ✅ `render.yaml` pour configuration automatique
- ✅ `gunicorn.conf.py` optimisé
- ✅ Variables d'environnement sécurisées

## 🚀 Redéploiement sur Render

### Étapes à suivre :

1. **Pousser les corrections vers GitHub :**
```bash
git add .
git commit -m "Corrections pour Render - gestion d'erreurs et configuration"
git push origin main
```

2. **Sur Render Dashboard :**
   - Aller dans votre service
   - Cliquer **"Manual Deploy"** → **"Deploy latest commit"**
   - Ou attendre le déploiement automatique

3. **Vérifier les logs :**
   - Aller dans **"Logs"** sur Render
   - Chercher les erreurs en temps réel

## 🔍 Diagnostic des problèmes courants

### Problème 1 : "Application failed to start"
**Solution :**
- Vérifier que `requirements.txt` contient `gunicorn`
- Vérifier que `Procfile` est correct
- Vérifier les variables d'environnement

### Problème 2 : "Database connection failed"
**Solution :**
- Créer une base PostgreSQL sur Render
- Copier l'URL de connexion
- L'ajouter comme variable `DATABASE_URL`

### Problème 3 : "Session expired"
**Solution :**
- Vérifier que `SECRET_KEY` est définie
- Redémarrer l'application
- Vider le cache du navigateur

## 📊 Variables d'environnement requises

```
SECRET_KEY = flem_hospital_secret_key_2024_production
FLASK_ENV = production
DATABASE_URL = [URL de votre base PostgreSQL]
PYTHON_VERSION = 3.11.0
```

## 🧪 Test de l'application

### Comptes de test :
- **Admin** : `admin` / `admin123`
- **Médecin** : `medecin1` / `medecin123`
- **Pharmacien** : `pharmacien1` / `pharmacien123`

### URLs de test :
- Login : `https://votre-app.onrender.com/login`
- Dashboard : `https://votre-app.onrender.com/`
- Pharmacie : `https://votre-app.onrender.com/pharmacie`

## 📞 Support

Si le problème persiste :
1. Vérifier les logs Render
2. Tester en local avec `python run.py`
3. Vérifier la configuration de la base de données
4. Redémarrer le service sur Render

## ✅ Vérifications finales

- [ ] Code poussé vers GitHub
- [ ] Service redéployé sur Render
- [ ] Base de données connectée
- [ ] Variables d'environnement définies
- [ ] Application accessible
- [ ] Login fonctionne
- [ ] Dashboard s'affiche
- [ ] Pas d'erreurs dans les logs
