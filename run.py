#!/usr/bin/env python3
"""
Script de lancement pour l'application Centre FLEM
"""
import os
import sys
from app import app, db

def main():
    print("=" * 50)
    print("🏥 CENTRE FLEM - SYSTÈME DE GESTION HOSPITALIÈRE")
    print("=" * 50)
    print()
    
    # Vérifier si la base de données existe
    if not os.path.exists('flem_hospital.db'):
        print("📊 Création de la base de données...")
        with app.app_context():
            db.create_all()
        print("✅ Base de données créée avec succès!")
        print()
    
    print("🚀 Démarrage du serveur...")
    print("📱 Accédez à l'application sur: http://127.0.0.1:8080")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter le serveur")
    print("=" * 50)
    print()
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8080)
    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage: {e}")
        print("💡 Essayez de changer le port dans le fichier run.py")

if __name__ == '__main__':
    main()
