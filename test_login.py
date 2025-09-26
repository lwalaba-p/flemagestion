#!/usr/bin/env python3
"""
Script de test pour la fonctionnalité de connexion FLEM Hospital
Teste les comptes de test et la redirection vers le dashboard
"""

import requests
import sys
from urllib.parse import urljoin

def test_login_functionality(base_url):
    """Tester la fonctionnalité de connexion"""
    print(f"🔐 Test de connexion sur: {base_url}")
    print("-" * 50)
    
    # Test des comptes de test
    test_accounts = [
        {"username": "admin", "password": "admin123", "role": "admin"},
        {"username": "medecin1", "password": "medecin123", "role": "medecin"},
        {"username": "pharmacien1", "password": "pharmacien123", "role": "pharmacien"}
    ]
    
    session = requests.Session()
    
    for account in test_accounts:
        print(f"\n🧪 Test du compte: {account['username']} ({account['role']})")
        
        # 1. Accéder à la page de connexion
        try:
            login_page = session.get(f"{base_url}/login")
            if login_page.status_code != 200:
                print(f"  ❌ Erreur accès page login: {login_page.status_code}")
                continue
            print("  ✅ Page de connexion accessible")
        except Exception as e:
            print(f"  ❌ Erreur connexion: {e}")
            continue
        
        # 2. Tenter la connexion
        try:
            login_data = {
                'username': account['username'],
                'password': account['password']
            }
            
            login_response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
            
            if login_response.status_code == 302:  # Redirection
                redirect_url = login_response.headers.get('Location', '')
                if 'login' in redirect_url:
                    print(f"  ❌ Redirection vers login - Échec de connexion")
                else:
                    print(f"  ✅ Connexion réussie - Redirection vers: {redirect_url}")
                    
                    # 3. Tester l'accès au dashboard
                    dashboard_response = session.get(f"{base_url}/")
                    if dashboard_response.status_code == 200:
                        if "Centre FLEM" in dashboard_response.text or "Tableau de bord" in dashboard_response.text:
                            print(f"  ✅ Dashboard accessible pour {account['role']}")
                        else:
                            print(f"  ⚠️  Dashboard chargé mais contenu inattendu")
                    else:
                        print(f"  ❌ Erreur accès dashboard: {dashboard_response.status_code}")
            else:
                print(f"  ❌ Erreur de connexion: {login_response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Erreur lors de la connexion: {e}")
        
        # Déconnexion pour le test suivant
        session.get(f"{base_url}/logout")
    
    return True

def test_health_endpoint(base_url):
    """Tester l'endpoint de santé"""
    print(f"\n🏥 Test de l'endpoint de santé: {base_url}/health")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Endpoint accessible")
            print(f"  📊 Status: {data.get('status', 'unknown')}")
            print(f"  🗄️  Database: {data.get('database', 'unknown')}")
            
            if data.get('database') == 'connected':
                print("  ✅ Base de données connectée")
                return True
            else:
                print("  ❌ Problème de connexion à la base de données")
                return False
        else:
            print(f"  ❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Erreur de connexion: {e}")
        return False

def main():
    """Fonction principale"""
    print("🏥 TEST FLEM HOSPITAL - FONCTIONNALITÉ DE CONNEXION")
    print("=" * 60)
    
    # Demander l'URL
    base_url = input("🌐 Entrez l'URL de votre application (ex: https://flem-hospital.onrender.com): ").strip()
    
    if not base_url:
        print("❌ URL non fournie")
        return
    
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'https://' + base_url
    
    print(f"\n🔍 Test de l'application: {base_url}")
    
    # Test de l'endpoint de santé
    health_ok = test_health_endpoint(base_url)
    
    # Test de la fonctionnalité de connexion
    if health_ok:
        test_login_functionality(base_url)
    else:
        print("\n❌ L'application n'est pas accessible. Vérifiez :")
        print("  1. Que l'application est déployée")
        print("  2. Que l'URL est correcte")
        print("  3. Que l'application n'est pas en veille")
        print("  4. Les logs Render pour les erreurs")
    
    print("\n📋 RÉSUMÉ")
    print("-" * 20)
    if health_ok:
        print("✅ Application accessible")
        print("✅ Tests de connexion effectués")
        print("\n💡 Si les connexions échouent :")
        print("  1. Vérifier la configuration de la base de données")
        print("  2. Vérifier les variables d'environnement")
        print("  3. Redéployer l'application")
    else:
        print("❌ Application non accessible")
        print("\n💡 Actions à effectuer :")
        print("  1. Vérifier le déploiement sur Render")
        print("  2. Vérifier les logs d'erreur")
        print("  3. Redémarrer le service")

if __name__ == "__main__":
    main()
