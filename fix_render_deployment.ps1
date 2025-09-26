# Script PowerShell pour corriger le déploiement FLEM Hospital sur Render
# Ce script vous guide à travers la résolution des problèmes de connexion

Write-Host "🏥 CORRECTION DÉPLOIEMENT FLEM HOSPITAL" -ForegroundColor Blue
Write-Host "=" * 50 -ForegroundColor Blue

Write-Host "`n🔍 DIAGNOSTIC DU PROBLÈME" -ForegroundColor Yellow
Write-Host "Le problème principal est probablement :" -ForegroundColor White
Write-Host "1. Base de données PostgreSQL non configurée" -ForegroundColor Red
Write-Host "2. Variable DATABASE_URL manquante" -ForegroundColor Red
Write-Host "3. Application utilise SQLite au lieu de PostgreSQL" -ForegroundColor Red

Write-Host "`n📋 ÉTAPES DE RÉSOLUTION" -ForegroundColor Green
Write-Host "=" * 30 -ForegroundColor Green

Write-Host "`n1️⃣ CRÉER UNE BASE POSTGRESQL SUR RENDER" -ForegroundColor Cyan
Write-Host "   • Aller sur https://render.com" -ForegroundColor White
Write-Host "   • Cliquer 'New +' → 'PostgreSQL'" -ForegroundColor White
Write-Host "   • Nom: flem-database" -ForegroundColor White
Write-Host "   • Plan: Free" -ForegroundColor White
Write-Host "   • Région: Oregon (US West)" -ForegroundColor White
Write-Host "   • Cliquer 'Create Database'" -ForegroundColor White

Write-Host "`n2️⃣ CONFIGURER LES VARIABLES D'ENVIRONNEMENT" -ForegroundColor Cyan
Write-Host "   Dans votre service web Render :" -ForegroundColor White
Write-Host "   • Aller dans l'onglet 'Environment'" -ForegroundColor White
Write-Host "   • Ajouter ces variables :" -ForegroundColor White
Write-Host "     - SECRET_KEY = flem_hospital_secret_key_2024_production" -ForegroundColor Yellow
Write-Host "     - FLASK_ENV = production" -ForegroundColor Yellow
Write-Host "     - DATABASE_URL = [URL de votre base PostgreSQL]" -ForegroundColor Yellow

Write-Host "`n3️⃣ OBTENIR L'URL DE LA BASE DE DONNÉES" -ForegroundColor Cyan
Write-Host "   • Aller dans votre base PostgreSQL" -ForegroundColor White
Write-Host "   • Onglet 'Info'" -ForegroundColor White
Write-Host "   • Copier 'External Database URL'" -ForegroundColor White
Write-Host "   • Coller dans la variable DATABASE_URL" -ForegroundColor White

Write-Host "`n4️⃣ REDÉPLOYER L'APPLICATION" -ForegroundColor Cyan
Write-Host "   • Cliquer 'Manual Deploy' → 'Deploy latest commit'" -ForegroundColor White
Write-Host "   • Attendre 2-3 minutes" -ForegroundColor White
Write-Host "   • Vérifier les logs" -ForegroundColor White

Write-Host "`n🧪 TESTS À EFFECTUER" -ForegroundColor Magenta
Write-Host "=" * 25 -ForegroundColor Magenta

Write-Host "`n1. Test de santé :" -ForegroundColor White
Write-Host "   https://votre-app.onrender.com/health" -ForegroundColor Yellow
Write-Host "   Réponse attendue : {'status': 'healthy', 'database': 'connected'}" -ForegroundColor Green

Write-Host "`n2. Test de connexion :" -ForegroundColor White
Write-Host "   https://votre-app.onrender.com/login" -ForegroundColor Yellow
Write-Host "   Utiliser : admin / admin123" -ForegroundColor Green

Write-Host "`n3. Test du dashboard :" -ForegroundColor White
Write-Host "   https://votre-app.onrender.com" -ForegroundColor Yellow
Write-Host "   Vérifier l'affichage du tableau de bord" -ForegroundColor Green

Write-Host "`n🔧 SCRIPT DE DIAGNOSTIC" -ForegroundColor Blue
Write-Host "Pour diagnostiquer automatiquement :" -ForegroundColor White
Write-Host "python diagnostic_deployment.py" -ForegroundColor Yellow

Write-Host "`n📚 DOCUMENTATION DISPONIBLE" -ForegroundColor Blue
Write-Host "• RENDER_DATABASE_SETUP.md - Configuration base de données" -ForegroundColor White
Write-Host "• RENDER_DEPLOY.md - Guide de déploiement complet" -ForegroundColor White
Write-Host "• RENDER_TROUBLESHOOTING.md - Résolution des problèmes" -ForegroundColor White

Write-Host "`n✅ APRÈS CES ÉTAPES" -ForegroundColor Green
Write-Host "Votre Centre FLEM sera accessible avec :" -ForegroundColor White
Write-Host "• URL : https://votre-app.onrender.com" -ForegroundColor Yellow
Write-Host "• Login : admin / admin123" -ForegroundColor Yellow
Write-Host "• Dashboard : Fonctionnel" -ForegroundColor Yellow

Write-Host "`n🚀 BON DÉPLOIEMENT !" -ForegroundColor Green
