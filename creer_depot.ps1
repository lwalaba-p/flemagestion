# Script PowerShell pour créer un dépôt GitHub - Centre FLEM
# Exécuter avec: .\creer_depot.ps1

Write-Host "🏥 CENTRE FLEM - CRÉATION DU DÉPÔT GITHUB" -ForegroundColor Blue
Write-Host "=" * 50 -ForegroundColor Blue

# Vérifier Git
Write-Host "`n🔍 Vérification de Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ Git trouvé: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git n'est pas installé. Veuillez installer Git d'abord." -ForegroundColor Red
    exit 1
}

# Vérifier le statut Git
Write-Host "`n🔍 Vérification du statut Git..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  Il y a des changements non commités:" -ForegroundColor Yellow
    Write-Host $gitStatus -ForegroundColor Yellow
    Write-Host "`nVeuillez d'abord commiter vos changements:" -ForegroundColor Yellow
    Write-Host "git add ." -ForegroundColor Cyan
    Write-Host "git commit -m 'Votre message'" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ Repository Git prêt" -ForegroundColor Green

# Demander le nom d'utilisateur GitHub
Write-Host "`n📝 Configuration du repository GitHub" -ForegroundColor Yellow
$username = Read-Host "Entrez votre nom d'utilisateur GitHub"

if (-not $username) {
    Write-Host "❌ Nom d'utilisateur requis" -ForegroundColor Red
    exit 1
}

# Afficher les instructions
Write-Host "`n🌐 Instructions pour créer le repository GitHub" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Yellow
Write-Host "1. Aller sur: https://github.com/new" -ForegroundColor Cyan
Write-Host "2. Repository name: flem-hospital" -ForegroundColor Cyan
Write-Host "3. Description: Système de gestion hospitalière Centre FLEM" -ForegroundColor Cyan
Write-Host "4. Visibilité: Public (recommandé)" -ForegroundColor Cyan
Write-Host "5. NE PAS cocher: Add README, .gitignore, license" -ForegroundColor Cyan
Write-Host "6. Cliquer 'Create repository'" -ForegroundColor Cyan

$repoUrl = "https://github.com/$username/flem-hospital"
Write-Host "`n📋 Votre repository sera accessible à:" -ForegroundColor Yellow
Write-Host "   $repoUrl" -ForegroundColor Cyan

# Ouvrir GitHub
Write-Host "`n🌐 Ouverture de GitHub dans votre navigateur..." -ForegroundColor Yellow
try {
    Start-Process "https://github.com/new"
    Write-Host "✅ GitHub ouvert" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Ouvrez manuellement https://github.com/new" -ForegroundColor Yellow
}

# Attendre que l'utilisateur crée le repository
Write-Host "`n⏸️  Appuyez sur Entrée quand vous avez créé le repository..." -ForegroundColor Yellow
Read-Host

# Pousser vers GitHub
Write-Host "`n📤 Poussée du code vers GitHub..." -ForegroundColor Yellow

$commands = @(
    "git remote add origin https://github.com/$username/flem-hospital.git",
    "git branch -M main",
    "git push -u origin main"
)

foreach ($cmd in $commands) {
    Write-Host "🔄 Exécution: $cmd" -ForegroundColor Yellow
    try {
        Invoke-Expression $cmd
        Write-Host "✅ Succès" -ForegroundColor Green
    } catch {
        Write-Host "❌ Erreur lors de l'exécution: $cmd" -ForegroundColor Red
        Write-Host "Vérifiez que:" -ForegroundColor Yellow
        Write-Host "1. Le repository a été créé sur GitHub" -ForegroundColor Yellow
        Write-Host "2. Votre nom d'utilisateur est correct" -ForegroundColor Yellow
        Write-Host "3. Vous avez les permissions d'écriture" -ForegroundColor Yellow
        exit 1
    }
}

# Afficher le succès
Write-Host "`n" + "=" * 60 -ForegroundColor Green
Write-Host "🎉 DÉPÔT GITHUB CRÉÉ AVEC SUCCÈS!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

Write-Host "`n📦 Votre repository:" -ForegroundColor Yellow
Write-Host "   $repoUrl" -ForegroundColor Cyan

Write-Host "`n🚀 Prochaines étapes:" -ForegroundColor Yellow
Write-Host "   1. Vérifier votre repository sur GitHub" -ForegroundColor Cyan
Write-Host "   2. Suivre le guide DEPLOY_QUICK.md pour déployer" -ForegroundColor Cyan
Write-Host "   3. Votre app sera accessible en ligne!" -ForegroundColor Cyan

Write-Host "`n📚 Fichiers importants:" -ForegroundColor Yellow
Write-Host "   - README.md: Documentation du projet" -ForegroundColor Cyan
Write-Host "   - DEPLOY_QUICK.md: Guide de déploiement rapide" -ForegroundColor Cyan
Write-Host "   - deployment_guide.md: Guide complet" -ForegroundColor Cyan

Write-Host "`n🔗 Liens utiles:" -ForegroundColor Yellow
Write-Host "   - Repository: $repoUrl" -ForegroundColor Cyan
Write-Host "   - Déploiement Render: https://render.com" -ForegroundColor Cyan
Write-Host "   - Déploiement Railway: https://railway.app" -ForegroundColor Cyan

Write-Host "`n🎉 Félicitations! Votre projet Centre FLEM est maintenant sur GitHub!" -ForegroundColor Green
