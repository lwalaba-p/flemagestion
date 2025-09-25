#!/usr/bin/env python3
"""
Script de déploiement pour le Centre FLEM
Ce script aide à préparer l'application pour le déploiement
"""

import os
import subprocess
import sys

def run_command(command):
    """Exécute une commande et affiche le résultat"""
    print(f"🔄 Exécution: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Succès: {command}")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ Erreur: {command}")
        print(result.stderr)
    return result.returncode == 0

def check_git():
    """Vérifie si Git est installé et configuré"""
    print("🔍 Vérification de Git...")
    if not run_command("git --version"):
        print("❌ Git n'est pas installé. Veuillez installer Git d'abord.")
        return False
    
    # Vérifier la configuration Git
    if not run_command("git config user.name"):
        print("⚠️  Configuration Git manquante. Veuillez configurer:")
        print("   git config --global user.name 'Votre Nom'")
        print("   git config --global user.email 'votre@email.com'")
        return False
    
    return True

def init_git_repo():
    """Initialise un repository Git"""
    print("📁 Initialisation du repository Git...")
    
    if os.path.exists('.git'):
        print("✅ Repository Git déjà initialisé")
        return True
    
    commands = [
        "git init",
        "git add .",
        "git commit -m 'Initial commit - Centre FLEM Hospital System'"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            return False
    
    return True

def create_env_file():
    """Crée un fichier .env pour les variables d'environnement"""
    print("🔧 Création du fichier .env...")
    
    env_content = """# Variables d'environnement pour le Centre FLEM
SECRET_KEY=votre_cle_secrete_tres_longue_et_complexe_ici
FLASK_ENV=development
DATABASE_URL=sqlite:///flem_hospital.db

# Pour la production, remplacer par:
# FLASK_ENV=production
# DATABASE_URL=postgresql://user:pass@host:port/dbname
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Fichier .env créé")
    print("⚠️  N'oubliez pas de modifier la SECRET_KEY pour la production!")

def show_deployment_instructions():
    """Affiche les instructions de déploiement"""
    print("\n" + "="*60)
    print("🚀 INSTRUCTIONS DE DÉPLOIEMENT")
    print("="*60)
    
    print("\n1. 📤 Pousser sur GitHub:")
    print("   - Créer un repository sur https://github.com")
    print("   - Exécuter les commandes suivantes:")
    print("     git remote add origin https://github.com/votre-username/flem-hospital.git")
    print("     git branch -M main")
    print("     git push -u origin main")
    
    print("\n2. 🌐 Déployer sur Render.com:")
    print("   - Aller sur https://render.com")
    print("   - Se connecter avec GitHub")
    print("   - Cliquer sur 'New +' → 'Web Service'")
    print("   - Sélectionner votre repository")
    print("   - Configurer:")
    print("     * Name: flem-hospital")
    print("     * Environment: Python 3")
    print("     * Build Command: pip install -r requirements.txt")
    print("     * Start Command: gunicorn app:app")
    
    print("\n3. 🗄️ Créer une base de données PostgreSQL:")
    print("   - Sur Render, créer une base PostgreSQL")
    print("   - Copier l'URL de connexion")
    print("   - L'ajouter dans les variables d'environnement")
    
    print("\n4. 🔒 Variables d'environnement à configurer:")
    print("   - SECRET_KEY: Une clé secrète longue et complexe")
    print("   - DATABASE_URL: L'URL de votre base PostgreSQL")
    print("   - FLASK_ENV: production")
    
    print("\n5. ✅ Votre application sera accessible sur:")
    print("   https://flem-hospital.onrender.com")
    
    print("\n📚 Pour plus de détails, consultez deployment_guide.md")

def main():
    """Fonction principale"""
    print("🏥 CENTRE FLEM - PRÉPARATION AU DÉPLOIEMENT")
    print("="*50)
    
    # Vérifications préliminaires
    if not check_git():
        sys.exit(1)
    
    # Préparation du projet
    if not init_git_repo():
        print("❌ Erreur lors de l'initialisation Git")
        sys.exit(1)
    
    create_env_file()
    
    # Instructions finales
    show_deployment_instructions()
    
    print("\n🎉 Préparation terminée!")
    print("Votre projet est prêt pour le déploiement.")

if __name__ == "__main__":
    main()
