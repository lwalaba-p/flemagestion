#!/usr/bin/env python3
"""
Script de diagnostic pour le déploiement FLEM Hospital
Vérifie la configuration et les problèmes courants
"""

import os
import sys
import requests
from urllib.parse import urlparse

def check_environment_variables():
    """Vérifier les variables d'environnement"""
    print("🔍 Vérification des variables d'environnement...")
    
    required_vars = ['SECRET_KEY', 'FLASK_ENV']
    optional_vars = ['DATABASE_URL', 'PYTHON_VERSION']
    
    print("\n📋 Variables requises :")
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"  ✅ {var}: {'*' * len(value)} (définie)")
        else:
            print(f"  ❌ {var}: NON DÉFINIE")
    
    print("\n📋 Variables optionnelles :")
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            print(f"  ✅ {var}: {'*' * len(value)} (définie)")
        else:
            print(f"  ⚠️  {var}: NON DÉFINIE")
    
    # Vérifier DATABASE_URL spécifiquement
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        try:
            parsed = urlparse(database_url)
            if parsed.scheme == 'postgresql':
                print(f"  ✅ Base de données PostgreSQL configurée")
                print(f"  📍 Host: {parsed.hostname}")
                print(f"  📍 Port: {parsed.port}")
                print(f"  📍 Database: {parsed.path[1:]}")
            else:
                print(f"  ⚠️  Type de base de données: {parsed.scheme}")
        except Exception as e:
            print(f"  ❌ Erreur parsing DATABASE_URL: {e}")
    else:
        print("  ❌ DATABASE_URL non définie - Utilisation de SQLite local")

def check_app_health(app_url):
    """Vérifier la santé de l'application"""
    print(f"\n🏥 Test de santé de l'application: {app_url}")
    
    try:
        response = requests.get(f"{app_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Application accessible")
            print(f"  📊 Status: {data.get('status', 'unknown')}")
            print(f"  🗄️  Database: {data.get('database', 'unknown')}")
            print(f"  ⏰ Timestamp: {data.get('timestamp', 'unknown')}")
            return True
        else:
            print(f"  ❌ Erreur HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erreur de connexion: {e}")
        return False

def check_login_page(app_url):
    """Vérifier la page de connexion"""
    print(f"\n🔐 Test de la page de connexion: {app_url}/login")
    
    try:
        response = requests.get(f"{app_url}/login", timeout=10)
        if response.status_code == 200:
            print("  ✅ Page de connexion accessible")
            if "Centre FLEM" in response.text:
                print("  ✅ Interface FLEM détectée")
            else:
                print("  ⚠️  Interface FLEM non détectée")
            return True
        else:
            print(f"  ❌ Erreur HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erreur de connexion: {e}")
        return False

def check_dashboard_access(app_url):
    """Vérifier l'accès au dashboard"""
    print(f"\n📊 Test d'accès au dashboard: {app_url}")
    
    try:
        response = requests.get(app_url, timeout=10)
        if response.status_code == 200:
            if "login" in response.url.lower():
                print("  ⚠️  Redirection vers login - Session expirée")
                return False
            elif "Centre FLEM" in response.text or "Tableau de bord" in response.text:
                print("  ✅ Dashboard accessible")
                return True
            else:
                print("  ⚠️  Page chargée mais contenu inattendu")
                return False
        else:
            print(f"  ❌ Erreur HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erreur de connexion: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    print("🏥 DIAGNOSTIC FLEM HOSPITAL - DÉPLOIEMENT")
    print("=" * 50)
    
    # Vérifier les variables d'environnement
    check_environment_variables()
    
    # Demander l'URL de l'application
    app_url = input("\n🌐 Entrez l'URL de votre application (ex: https://flem-hospital.onrender.com): ").strip()
    
    if not app_url:
        print("❌ URL non fournie. Arrêt du diagnostic.")
        return
    
    if not app_url.startswith(('http://', 'https://')):
        app_url = 'https://' + app_url
    
    print(f"\n🔍 Diagnostic de: {app_url}")
    
    # Tests de l'application
    health_ok = check_app_health(app_url)
    login_ok = check_login_page(app_url)
    dashboard_ok = check_dashboard_access(app_url)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    
    if health_ok:
        print("✅ Application fonctionnelle")
    else:
        print("❌ Application non accessible")
    
    if login_ok:
        print("✅ Page de connexion accessible")
    else:
        print("❌ Page de connexion non accessible")
    
    if dashboard_ok:
        print("✅ Dashboard accessible")
    else:
        print("❌ Dashboard non accessible - Problème de connexion")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS")
    print("-" * 30)
    
    if not health_ok:
        print("🔧 Actions à effectuer :")
        print("  1. Vérifier que l'application est déployée")
        print("  2. Vérifier les logs Render")
        print("  3. Redémarrer le service")
    
    if not login_ok:
        print("🔧 Actions à effectuer :")
        print("  1. Vérifier la configuration des routes")
        print("  2. Vérifier les templates")
        print("  3. Vérifier les logs d'erreur")
    
    if not dashboard_ok and login_ok:
        print("🔧 Actions à effectuer :")
        print("  1. Vérifier la configuration de la base de données")
        print("  2. Ajouter la variable DATABASE_URL")
        print("  3. Créer une base PostgreSQL sur Render")
        print("  4. Redéployer l'application")
    
    print("\n📚 Documentation disponible :")
    print("  - RENDER_DATABASE_SETUP.md")
    print("  - RENDER_DEPLOY.md")
    print("  - RENDER_TROUBLESHOOTING.md")

if __name__ == "__main__":
    main()
