# Script PowerShell pour héberger le Centre FLEM
# Exécuter avec: .\heberger_maintenant.ps1

Write-Host "🏥 CENTRE FLEM - HÉBERGEMENT AUTOMATIQUE" -ForegroundColor Blue
Write-Host "=" * 50 -ForegroundColor Blue

# Vérifier le dépôt
Write-Host "`n🔍 Vérification du dépôt GitHub..." -ForegroundColor Yellow
$remoteUrl = git remote get-url origin 2>$null
if ($remoteUrl) {
    Write-Host "✅ Dépôt connecté: $remoteUrl" -ForegroundColor Green
} else {
    Write-Host "❌ Aucun dépôt GitHub connecté" -ForegroundColor Red
    exit 1
}

# Vérifier que tout est à jour
Write-Host "`n🔍 Vérification des changements..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  Il y a des changements non commités:" -ForegroundColor Yellow
    Write-Host $gitStatus -ForegroundColor Yellow
    Write-Host "`nVoulez-vous les commiter et pousser maintenant? (o/n)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "o" -or $response -eq "O") {
        git add .
        git commit -m "Mise à jour avant déploiement"
        git push origin main
        Write-Host "✅ Changements poussés vers GitHub" -ForegroundColor Green
    }
}

Write-Host "`n🌐 OPTIONS D'HÉBERGEMENT" -ForegroundColor Yellow
Write-Host "=" * 40 -ForegroundColor Yellow

Write-Host "`n1. 🚀 Render.com (Recommandé)" -ForegroundColor Cyan
Write-Host "   ✅ Gratuit: 750h/mois" -ForegroundColor Green
Write-Host "   ✅ Base PostgreSQL incluse" -ForegroundColor Green
Write-Host "   ✅ Déploiement automatique" -ForegroundColor Green
Write-Host "   ✅ HTTPS automatique" -ForegroundColor Green

Write-Host "`n2. ⚡ Railway.app (Plus simple)" -ForegroundColor Cyan
Write-Host "   ✅ Gratuit: $5 crédit/mois" -ForegroundColor Green
Write-Host "   ✅ Déploiement en 1 clic" -ForegroundColor Green
Write-Host "   ✅ Base PostgreSQL incluse" -ForegroundColor Green
Write-Host "   ✅ Configuration automatique" -ForegroundColor Green

# Demander le choix
Write-Host "`n🎯 Choisissez votre option (1 ou 2):" -ForegroundColor Yellow
$choice = Read-Host

switch ($choice) {
    "1" {
        Write-Host "`n🚀 DÉPLOIEMENT SUR RENDER.COM" -ForegroundColor Green
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
        
        Write-Host "`n🔧 Variables d'environnement à ajouter:" -ForegroundColor Yellow
        Write-Host "SECRET_KEY = flem_hospital_secret_key_2024_production" -ForegroundColor White
        Write-Host "FLASK_ENV = production" -ForegroundColor White
        Write-Host "DATABASE_URL = [URL de votre base PostgreSQL]" -ForegroundColor White
        
        # Ouvrir Render
        try {
            Start-Process "https://render.com"
            Write-Host "`n🌐 Render.com ouvert dans votre navigateur" -ForegroundColor Green
        } catch {
            Write-Host "`n⚠️  Ouvrez manuellement https://render.com" -ForegroundColor Yellow
        }
    }
    
    "2" {
        Write-Host "`n⚡ DÉPLOIEMENT SUR RAILWAY.APP" -ForegroundColor Green
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
    
    default {
        Write-Host "`n❌ Choix invalide" -ForegroundColor Red
        Write-Host "Veuillez choisir 1 ou 2" -ForegroundColor Yellow
    }
}

# Informations finales
Write-Host "`n" + "=" * 60 -ForegroundColor Green
Write-Host "🎉 VOTRE CODE EST PRÊT POUR L'HÉBERGEMENT!" -ForegroundColor Green
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
Write-Host "   - HEBERGER_MAINTENANT.md: Guide rapide" -ForegroundColor Cyan
Write-Host "   - RENDER_DEPLOY.md: Guide Render détaillé" -ForegroundColor Cyan
Write-Host "   - README.md: Documentation du projet" -ForegroundColor Cyan

Write-Host "`n🎉 Bon hébergement! Votre Centre FLEM sera bientôt en ligne!" -ForegroundColor Green
Write-Host "`n⏰ Temps estimé: 5-10 minutes" -ForegroundColor Yellow
