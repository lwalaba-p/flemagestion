#!/usr/bin/env python3
"""
Script pour créer automatiquement un dépôt GitHub
et pousser le code du Centre FLEM
"""

import subprocess
import sys
import webbrowser
import os

def run_command(command, description=""):
    """Exécute une commande et affiche le résultat"""
    if description:
        print(f"🔄 {description}")
    print(f"   Commande: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Succès")
        if result.stdout.strip():
            print(f"   Sortie: {result.stdout.strip()}")
    else:
        print(f"❌ Erreur")
        if result.stderr.strip():
            print(f"   Erreur: {result.stderr.strip()}")
    
    return result.returncode == 0

def check_git_status():
    """Vérifie le statut Git"""
    print("🔍 Vérification du statut Git...")
    
    # Vérifier si on est dans un repo Git
    if not os.path.exists('.git'):
        print("❌ Pas de repository Git trouvé")
        return False
    
    # Vérifier s'il y a des changements non commités
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("⚠️  Il y a des changements non commités:")
        print(result.stdout)
        return False
    
    print("✅ Repository Git prêt")
    return True

def get_github_username():
    """Demande le nom d'utilisateur GitHub"""
    print("\n📝 Configuration du repository GitHub")
    username = input("Entrez votre nom d'utilisateur GitHub: ").strip()
    
    if not username:
        print("❌ Nom d'utilisateur requis")
        return None
    
    return username

def create_github_repo_instructions(username):
    """Affiche les instructions pour créer le repo GitHub"""
    print(f"\n🌐 Instructions pour créer le repository GitHub")
    print("="*60)
    
    repo_url = f"https://github.com/{username}/flem-hospital"
    
    print(f"1. Aller sur: https://github.com/new")
    print(f"2. Repository name: flem-hospital")
    print(f"3. Description: Système de gestion hospitalière Centre FLEM")
    print(f"4. Visibilité: Public (recommandé)")
    print(f"5. NE PAS cocher: Add README, .gitignore, license")
    print(f"6. Cliquer 'Create repository'")
    
    print(f"\n📋 Votre repository sera accessible à:")
    print(f"   {repo_url}")
    
    # Ouvrir automatiquement GitHub
    try:
        webbrowser.open("https://github.com/new")
        print("🌐 GitHub ouvert dans votre navigateur")
    except:
        print("⚠️  Ouvrez manuellement https://github.com/new")
    
    input("\n⏸️  Appuyez sur Entrée quand vous avez créé le repository...")
    
    return repo_url

def push_to_github(username):
    """Pousse le code vers GitHub"""
    print(f"\n📤 Poussée du code vers GitHub...")
    
    repo_url = f"https://github.com/{username}/flem-hospital.git"
    
    commands = [
        f"git remote add origin {repo_url}",
        "git branch -M main",
        "git push -u origin main"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"❌ Erreur lors de l'exécution: {cmd}")
            return False
    
    print("✅ Code poussé avec succès vers GitHub!")
    return True

def show_success_info(username):
    """Affiche les informations de succès"""
    repo_url = f"https://github.com/{username}/flem-hospital"
    
    print("\n" + "="*60)
    print("🎉 DÉPÔT GITHUB CRÉÉ AVEC SUCCÈS!")
    print("="*60)
    
    print(f"\n📦 Votre repository:")
    print(f"   {repo_url}")
    
    print(f"\n🚀 Prochaines étapes:")
    print(f"   1. Vérifier votre repository sur GitHub")
    print(f"   2. Suivre le guide DEPLOY_QUICK.md pour déployer")
    print(f"   3. Votre app sera accessible en ligne!")
    
    print(f"\n📚 Fichiers importants:")
    print(f"   - README.md: Documentation du projet")
    print(f"   - DEPLOY_QUICK.md: Guide de déploiement rapide")
    print(f"   - deployment_guide.md: Guide complet")
    
    print(f"\n🔗 Liens utiles:")
    print(f"   - Repository: {repo_url}")
    print(f"   - Déploiement Render: https://render.com")
    print(f"   - Déploiement Railway: https://railway.app")

def main():
    """Fonction principale"""
    print("🏥 CENTRE FLEM - CRÉATION DU DÉPÔT GITHUB")
    print("="*50)
    
    # Vérifications préliminaires
    if not check_git_status():
        print("\n❌ Veuillez d'abord commiter tous vos changements:")
        print("   git add .")
        print("   git commit -m 'Votre message'")
        sys.exit(1)
    
    # Demander le nom d'utilisateur
    username = get_github_username()
    if not username:
        sys.exit(1)
    
    # Instructions pour créer le repo
    repo_url = create_github_repo_instructions(username)
    
    # Pousser vers GitHub
    if push_to_github(username):
        show_success_info(username)
    else:
        print("\n❌ Erreur lors de la poussée vers GitHub")
        print("Vérifiez que:")
        print("1. Le repository a été créé sur GitHub")
        print("2. Votre nom d'utilisateur est correct")
        print("3. Vous avez les permissions d'écriture")

if __name__ == "__main__":
    main()
