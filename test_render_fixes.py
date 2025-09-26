#!/usr/bin/env python3
"""
Script de test pour vérifier les corrections sur Render
Teste les endpoints et la fonctionnalité de connexion
"""

import requests
import json
import sys
from datetime import datetime

def test_health_endpoint(base_url):
    """Tester l'endpoint de santé"""
    print(f"🏥 Test de l'endpoint de santé: {base_url}/health")
    print("-" * 50)
    
    try:
        response = requests.get(f"{base_url}/health", timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Endpoint de santé accessible")
                print(f"📊 Status: {data.get('status', 'unknown')}")
                print(f"🗄️  Database: {data.get('database', 'unknown')}")
                print(f"⏰ Timestamp: {data.get('timestamp', 'unknown')}")
                
                if data.get('database') == 'connected':
                    print("✅ Base de données connectée")
                    return True
                else:
                    print("❌ Problème de connexion à la base de données")
                    return False
            except json.JSONDecodeError:
                print("❌ Réponse non-JSON reçue")
                print(f"Contenu: {response.text[:200]}...")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"Contenu: {response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - L'application met du temps à répondre")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion - Vérifiez l'URL")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def test_favicon_endpoint(base_url):
    """Tester l'endpoint favicon"""
    print(f"\n🔗 Test de l'endpoint favicon: {base_url}/favicon.ico")
    print("-" * 50)
    
    try:
        response = requests.get(f"{base_url}/favicon.ico", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 204:
            print("✅ Favicon endpoint fonctionne (204 No Content)")
            return True
        elif response.status_code == 200:
            print("✅ Favicon endpoint fonctionne (200 OK)")
            return True
        else:
            print(f"⚠️  Status inattendu: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_login_page(base_url):
    """Tester la page de connexion"""
    print(f"\n🔐 Test de la page de connexion: {base_url}/login")
    print("-" * 50)
    
    try:
        response = requests.get(f"{base_url}/login", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Page de connexion accessible")
            
            # Vérifier le contenu
            if "Centre FLEM" in response.text:
                print("✅ Interface FLEM détectée")
            else:
                print("⚠️  Interface FLEM non détectée")
                
            if "admin" in response.text and "admin123" in response.text:
                print("✅ Comptes de test détectés")
            else:
                print("⚠️  Comptes de test non détectés")
                
            return True
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_login_functionality(base_url):
    """Tester la fonctionnalité de connexion"""
    print(f"\n🧪 Test de la fonctionnalité de connexion")
    print("-" * 50)
    
    session = requests.Session()
    
    # Test avec le compte admin
    try:
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        print("🔑 Tentative de connexion avec admin/admin123...")
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 302:
            redirect_url = response.headers.get('Location', '')
            print(f"✅ Redirection détectée vers: {redirect_url}")
            
            if 'login' in redirect_url:
                print("❌ Redirection vers login - Échec de connexion")
                return False
            else:
                print("✅ Connexion réussie")
                
                # Tester l'accès au dashboard
                dashboard_response = session.get(f"{base_url}/")
                if dashboard_response.status_code == 200:
                    if "Centre FLEM" in dashboard_response.text or "Tableau de bord" in dashboard_response.text:
                        print("✅ Dashboard accessible après connexion")
                        return True
                    else:
                        print("⚠️  Dashboard chargé mais contenu inattendu")
                        return False
                else:
                    print(f"❌ Erreur accès dashboard: {dashboard_response.status_code}")
                    return False
        else:
            print(f"❌ Pas de redirection - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 TEST DES CORRECTIONS RENDER - FLEM HOSPITAL")
    print("=" * 60)
    print(f"⏰ Test effectué le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Demander l'URL
    base_url = input("\n🌐 Entrez l'URL de votre application (ex: https://flem.onrender.com): ").strip()
    
    if not base_url:
        print("❌ URL non fournie")
        return
    
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'https://' + base_url
    
    print(f"\n🔍 Test de l'application: {base_url}")
    
    # Tests
    health_ok = test_health_endpoint(base_url)
    favicon_ok = test_favicon_endpoint(base_url)
    login_page_ok = test_login_page(base_url)
    login_func_ok = test_login_functionality(base_url) if health_ok else False
    
    # Résumé
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    tests = [
        ("Endpoint de santé", health_ok),
        ("Endpoint favicon", favicon_ok),
        ("Page de connexion", login_page_ok),
        ("Fonctionnalité de connexion", login_func_ok)
    ]
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS")
    print("-" * 30)
    
    if not health_ok:
        print("🔧 Problème de base de données :")
        print("  1. Vérifier que DATABASE_URL est définie")
        print("  2. Créer une base PostgreSQL sur Render")
        print("  3. Redéployer l'application")
    
    if not favicon_ok:
        print("🔧 Problème favicon (non critique) :")
        print("  1. Vérifier que la route favicon est ajoutée")
        print("  2. Redéployer l'application")
    
    if not login_page_ok:
        print("🔧 Problème de page de connexion :")
        print("  1. Vérifier les templates")
        print("  2. Vérifier les routes")
        print("  3. Vérifier les logs Render")
    
    if not login_func_ok and health_ok:
        print("🔧 Problème de fonctionnalité de connexion :")
        print("  1. Vérifier la configuration de la base de données")
        print("  2. Vérifier les utilisateurs de test")
        print("  3. Vérifier les sessions")
    
    # Score final
    passed_tests = sum(1 for _, result in tests if result)
    total_tests = len(tests)
    score = (passed_tests / total_tests) * 100
    
    print(f"\n🎯 SCORE: {passed_tests}/{total_tests} ({score:.1f}%)")
    
    if score == 100:
        print("🎉 Tous les tests sont passés ! Votre application fonctionne correctement.")
    elif score >= 75:
        print("✅ La plupart des tests sont passés. Quelques ajustements nécessaires.")
    else:
        print("❌ Plusieurs problèmes détectés. Vérifiez les recommandations ci-dessus.")

if __name__ == "__main__":
    main()
