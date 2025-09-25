# Script PowerShell pour déployer automatiquement le Centre FLEM
# Exécuter avec: .\deploy_automatique.ps1

Write-Host "🏥 CENTRE FLEM - DÉPLOIEMENT AUTOMATIQUE" -ForegroundColor Blue
Write-Host "=" * 50 -ForegroundColor Blue

# Vérifier que le dépôt est connecté
Write-Host "`n🔍 Vérification du dépôt GitHub..." -ForegroundColor Yellow
$remoteUrl = git remote get-url origin 2>$null
if ($remoteUrl) {
    Write-Host "✅ Dépôt connecté: $remoteUrl" -ForegroundColor Green
} else {
    Write-Host "❌ Aucun dépôt GitHub connecté" -ForegroundColor Red
    Write-Host "Veuillez d'abord créer un dépôt GitHub avec: .\creer_depot.ps1" -ForegroundColor Yellow
    exit 1
}

# Vérifier que tout est commité
Write-Host "`n🔍 Vérification des changements..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  Il y a des changements non commités:" -ForegroundColor Yellow
    Write-Host $gitStatus -ForegroundColor Yellow
    Write-Host "`nVoulez-vous les commiter maintenant? (o/n)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "o" -or $response -eq "O") {
        git add .
        $commitMessage = Read-Host "Message de commit (ou Entrée pour 'Mise à jour')"
        if (-not $commitMessage) {
            $commitMessage = "Mise à jour"
        }
        git commit -m $commitMessage
        Write-Host "✅ Changements commités" -ForegroundColor Green
    } else {
        Write-Host "❌ Veuillez commiter vos changements d'abord" -ForegroundColor Red
        exit 1
    }
}

# Pousser vers GitHub
Write-Host "`n📤 Poussée vers GitHub..." -ForegroundColor Yellow
try {
    git push origin master
    Write-Host "✅ Code poussé vers GitHub" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur lors de la poussée vers GitHub" -ForegroundColor Red
    exit 1
}

# Afficher les options de déploiement
Write-Host "`n🌐 OPTIONS DE DÉPLOIEMENT" -ForegroundColor Yellow
Write-Host "=" * 40 -ForegroundColor Yellow

Write-Host "`n1. 🚀 Render.com (Recommandé)" -ForegroundColor Cyan
Write-Host "   - Gratuit: 750h/mois" -ForegroundColor White
Write-Host "   - Base PostgreSQL incluse" -ForegroundColor White
Write-Host "   - Déploiement automatique" -ForegroundColor White

Write-Host "`n2. ⚡ Railway.app (Plus simple)" -ForegroundColor Cyan
Write-Host "   - Gratuit: $5 crédit/mois" -ForegroundColor White
Write-Host "   - Déploiement en 1 clic" -ForegroundColor White
Write-Host "   - Base PostgreSQL incluse" -ForegroundColor White

Write-Host "`n3. 📚 Guide Manuel" -ForegroundColor Cyan
Write-Host "   - Suivre DEPLOY_VOTRE_PROJET.md" -ForegroundColor White

# Demander le choix
Write-Host "`n🎯 Choisissez votre option (1, 2, ou 3):" -ForegroundColor Yellow
$choice = Read-Host

switch ($choice) {
    "1" {
        Write-Host "`n🚀 Déploiement sur Render.com" -ForegroundColor Green
        Write-Host "=" * 40 -ForegroundColor Green
        
        Write-Host "`n📋 Étapes à suivre:" -ForegroundColor Yellow
        Write-Host "1. Aller sur: https://render.com" -ForegroundColor Cyan
        Write-Host "2. Se connecter avec GitHub" -ForegroundColor Cyan
        Write-Host "3. Cliquer 'New +' → 'Web Service'" -ForegroundColor Cyan
        Write-Host "4. Connecter: lwalaba-p/flemagestion" -ForegroundColor Cyan
        Write-Host "5. Configurer:" -ForegroundColor Cyan
        Write-Host "   - Name: flem-hospital" -ForegroundColor White
        Write-Host "   - Environment: Python 3" -ForegroundColor White
        Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor White
        Write-Host "   - Start Command: gunicorn app:app" -ForegroundColor White
        Write-Host "6. Créer une base PostgreSQL" -ForegroundColor Cyan
        Write-Host "7. Ajouter les variables d'environnement" -ForegroundColor Cyan
        Write-Host "8. Déployer!" -ForegroundColor Cyan
        
        # Ouvrir Render
        try {
            Start-Process "https://render.com"
            Write-Host "`n🌐 Render.com ouvert dans votre navigateur" -ForegroundColor Green
        } catch {
            Write-Host "`n⚠️  Ouvrez manuellement https://render.com" -ForegroundColor Yellow
        }
    }
    
    "2" {
        Write-Host "`n⚡ Déploiement sur Railway.app" -ForegroundColor Green
        Write-Host "=" * 40 -ForegroundColor Green
        
        Write-Host "`n📋 Étapes à suivre:" -ForegroundColor Yellow
        Write-Host "1. Aller sur: https://railway.app" -ForegroundColor Cyan
        Write-Host "2. Se connecter avec GitHub" -ForegroundColor Cyan
        Write-Host "3. Cliquer 'Deploy from GitHub repo'" -ForegroundColor Cyan
        Write-Host "4. Sélectionner: lwalaba-p/flemagestion" -ForegroundColor Cyan
        Write-Host "5. Cliquer 'Deploy Now'" -ForegroundColor Cyan
        Write-Host "6. Ajouter une base PostgreSQL" -ForegroundColor Cyan
        Write-Host "7. C'est tout! Railway fait le reste" -ForegroundColor Cyan
        
        # Ouvrir Railway
        try {
            Start-Process "https://railway.app"
            Write-Host "`n🌐 Railway.app ouvert dans votre navigateur" -ForegroundColor Green
        } catch {
            Write-Host "`n⚠️  Ouvrez manuellement https://railway.app" -ForegroundColor Yellow
        }
    }
    
    "3" {
        Write-Host "`n📚 Guide Manuel" -ForegroundColor Green
        Write-Host "=" * 40 -ForegroundColor Green
        
        Write-Host "`n📖 Consultez le fichier: DEPLOY_VOTRE_PROJET.md" -ForegroundColor Cyan
        Write-Host "Ce guide contient toutes les instructions détaillées." -ForegroundColor White
        
        # Ouvrir le guide
        try {
            Start-Process "DEPLOY_VOTRE_PROJET.md"
            Write-Host "`n📖 Guide ouvert" -ForegroundColor Green
        } catch {
            Write-Host "`n⚠️  Ouvrez manuellement DEPLOY_VOTRE_PROJET.md" -ForegroundColor Yellow
        }
    }
    
    default {
        Write-Host "`n❌ Choix invalide" -ForegroundColor Red
        Write-Host "Veuillez choisir 1, 2, ou 3" -ForegroundColor Yellow
    }
}

# Informations finales
Write-Host "`n" + "=" * 60 -ForegroundColor Green
Write-Host "🎉 VOTRE CODE EST PRÊT POUR LE DÉPLOIEMENT!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

Write-Host "`n📦 Repository GitHub:" -ForegroundColor Yellow
Write-Host "   $remoteUrl" -ForegroundColor Cyan

Write-Host "`n🚀 Après le déploiement, votre app sera accessible sur:" -ForegroundColor Yellow
Write-Host "   https://flem-hospital.onrender.com (Render)" -ForegroundColor Cyan
Write-Host "   https://flem-hospital.railway.app (Railway)" -ForegroundColor Cyan

Write-Host "`n🔐 Comptes de test disponibles:" -ForegroundColor Yellow
Write-Host "   - Admin: admin / admin123" -ForegroundColor Cyan
Write-Host "   - Médecin: medecin1 / medecin123" -ForegroundColor Cyan
Write-Host "   - Pharmacien: pharmacien1 / pharmacien123" -ForegroundColor Cyan

Write-Host "`n📚 Documentation:" -ForegroundColor Yellow
Write-Host "   - DEPLOY_VOTRE_PROJET.md: Guide complet" -ForegroundColor Cyan
Write-Host "   - README.md: Documentation du projet" -ForegroundColor Cyan

Write-Host "`n🎉 Bon déploiement! Votre Centre FLEM sera bientôt en ligne!" -ForegroundColor Green
