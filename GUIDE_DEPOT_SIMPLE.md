# 📦 Créer votre Dépôt GitHub - Guide Simple

## 🎯 Objectif
Créer un dépôt GitHub pour votre projet Centre FLEM et le rendre accessible en ligne.

## ⚡ Étapes Rapides

### 1. 🌐 Aller sur GitHub
- Ouvrir https://github.com
- Se connecter (ou créer un compte)

### 2. ➕ Créer un nouveau repository
1. Cliquer **"New"** (bouton vert)
2. **Repository name** : `flem-hospital`
3. **Description** : `Système de gestion hospitalière Centre FLEM`
4. **Public** ✅
5. **NE PAS cocher** : README, .gitignore, license
6. Cliquer **"Create repository"**

### 3. 📤 Connecter votre projet
Dans votre terminal, exécuter :

```bash
# Remplacer VOTRE-USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/VOTRE-USERNAME/flem-hospital.git
git branch -M main
git push -u origin main
```

## 🔍 Exemple Concret

Si votre nom d'utilisateur GitHub est `pascal123` :

```bash
git remote add origin https://github.com/pascal123/flem-hospital.git
git branch -M main
git push -u origin main
```

## ✅ Vérification

Après ces commandes, votre projet sera accessible à :
```
https://github.com/VOTRE-USERNAME/flem-hospital
```

## 🚀 Prochaine Étape

Une fois le dépôt créé, suivez le guide `DEPLOY_QUICK.md` pour déployer votre application en ligne !

## 🆘 Aide

Si vous avez des erreurs :
1. Vérifiez que le repository a été créé sur GitHub
2. Vérifiez votre nom d'utilisateur
3. Assurez-vous d'être connecté à GitHub

**Votre projet Centre FLEM sera bientôt en ligne ! 🏥✨**
