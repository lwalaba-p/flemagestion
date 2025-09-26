from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import logging
from sqlalchemy import text

app = Flask(__name__)

# Configuration du logging pour Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration pour la production
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Configuration PostgreSQL pour la production
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    logger.info("Configuration PostgreSQL détectée")
else:
    # Configuration SQLite pour le développement local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flem_hospital.db'
    logger.info("Configuration SQLite pour le développement local")

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'flem_hospital_secret_key_2024_dev')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Gestionnaire d'erreurs global
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Erreur non gérée: {str(e)}")
    return render_template('error.html', error=str(e)), 500

# Route pour favicon.ico
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Route de redirection pour les URLs non trouvées
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('login'))

# Route de test de la base de données
@app.route('/health')
def health_check():
    try:
        # Test de connexion à la base de données
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

db = SQLAlchemy(app)

# Décorateur pour vérifier l'authentification
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Décorateur pour vérifier le rôle
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            user = User.query.get(session['user_id'])
            if not user or user.role != role:
                flash('Accès non autorisé', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Modèles de données
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, medecin, pharmacien
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(20), default='actif')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True)
    adresse = db.Column(db.Text)
    numero_securite_sociale = db.Column(db.String(20), unique=True)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    rendez_vous = db.relationship('RendezVous', backref='patient', lazy=True)
    consultations = db.relationship('Consultation', backref='patient', lazy=True)

class Personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    specialite = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_embauche = db.Column(db.Date, nullable=False)
    statut = db.Column(db.String(20), default='actif')  # actif, inactif
    
    # Relations
    rendez_vous = db.relationship('RendezVous', backref='personnel', lazy=True)
    consultations = db.relationship('Consultation', backref='personnel', lazy=True)

class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    date_rdv = db.Column(db.DateTime, nullable=False)
    type_consultation = db.Column(db.String(100), nullable=False)
    statut = db.Column(db.String(20), default='programme')  # programme, confirme, annule, termine
    notes = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    date_consultation = db.Column(db.DateTime, nullable=False)
    diagnostic = db.Column(db.Text)
    traitement = db.Column(db.Text)
    ordonnance = db.Column(db.Text)
    notes_medecin = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

class Chambre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    type_chambre = db.Column(db.String(50), nullable=False)  # simple, double, VIP
    statut = db.Column(db.String(20), default='libre')  # libre, occupee, maintenance
    prix_nuit = db.Column(db.Float, nullable=False)

class Medicament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    code_medicament = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    prix_unitaire = db.Column(db.Float, nullable=False)
    quantite_stock = db.Column(db.Integer, default=0)
    seuil_minimum = db.Column(db.Integer, default=10)
    date_expiration = db.Column(db.Date)
    fournisseur = db.Column(db.String(100))
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    prescriptions = db.relationship('Prescription', backref='medicament', lazy=True)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medicament_id = db.Column(db.Integer, db.ForeignKey('medicament.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    posologie = db.Column(db.Text, nullable=False)  # Comment prendre le médicament
    date_prescription = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(20), default='en_attente')  # en_attente, delivre, annule
    notes = db.Column(db.Text)

class Hospitalisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    chambre_id = db.Column(db.Integer, db.ForeignKey('chambre.id'), nullable=False)
    date_admission = db.Column(db.DateTime, default=datetime.utcnow)
    date_sortie = db.Column(db.DateTime)
    motif_admission = db.Column(db.Text)
    statut = db.Column(db.String(20), default='hospitalise')  # hospitalise, sorti, transfere
    notes = db.Column(db.Text)
    
    # Relations
    patient = db.relationship('Patient', backref='hospitalisations')
    chambre = db.relationship('Chambre', backref='hospitalisations')
    factures = db.relationship('Facture', backref='hospitalisation', lazy=True)

class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_facture = db.Column(db.String(50), unique=True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    hospitalisation_id = db.Column(db.Integer, db.ForeignKey('hospitalisation.id'))
    date_facture = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.Date)
    montant_total = db.Column(db.Float, nullable=False)
    montant_paye = db.Column(db.Float, default=0.0)
    statut = db.Column(db.String(20), default='en_attente')  # en_attente, payee, partielle, annulee
    type_facture = db.Column(db.String(30), nullable=False)  # hospitalisation, consultation, medicaments
    notes = db.Column(db.Text)
    
    # Relations
    patient = db.relationship('Patient', backref='factures')
    details = db.relationship('DetailFacture', backref='facture', lazy=True, cascade='all, delete-orphan')

class DetailFacture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facture_id = db.Column(db.Integer, db.ForeignKey('facture.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quantite = db.Column(db.Integer, default=1)
    prix_unitaire = db.Column(db.Float, nullable=False)
    montant = db.Column(db.Float, nullable=False)
    type_service = db.Column(db.String(50))  # chambre, consultation, medicament, examen

# Routes d'authentification
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            if not username or not password:
                flash('Veuillez remplir tous les champs', 'error')
                return render_template('login.html')
            
            # Test de connexion à la base de données
            try:
                db.session.execute(text('SELECT 1'))
            except Exception as db_error:
                logger.error(f"Erreur de connexion à la base de données: {str(db_error)}")
                flash('Problème de connexion à la base de données. Veuillez réessayer plus tard.', 'error')
                return render_template('login.html')
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password) and user.statut == 'actif':
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                logger.info(f"Utilisateur {username} connecté avec succès")
                flash(f'Bienvenue {user.prenom} {user.nom}!', 'success')
                return redirect(url_for('index'))
            else:
                logger.warning(f"Tentative de connexion échouée pour {username}")
                flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
        
        return render_template('login.html')
    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {str(e)}")
        flash('Une erreur s\'est produite lors de la connexion', 'error')
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Validation des mots de passe
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Le mot de passe doit contenir au moins 6 caractères', 'error')
            return render_template('register.html')
        
        user = User(
            username=request.form['username'],
            email=request.form['email'],
            role=request.form['role'],
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            telephone=request.form['telephone']
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Compte créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de la création du compte. Nom d\'utilisateur ou email déjà utilisé.', 'error')
    
    return render_template('register.html')

@app.route('/admin/register', methods=['GET', 'POST'])
@role_required('admin')
def admin_register():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            email=request.form['email'],
            role=request.form['role'],
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            telephone=request.form['telephone']
        )
        user.set_password(request.form['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Utilisateur créé avec succès!', 'success')
            return redirect(url_for('users'))
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de la création de l\'utilisateur', 'error')
    
    return render_template('admin_register.html')

# Routes principales
@app.route('/')
@login_required
def index():
    stats = {
        'total_patients': Patient.query.count(),
        'total_personnel': Personnel.query.count(),
        'rdv_aujourd_hui': RendezVous.query.filter(
            db.func.date(RendezVous.date_rdv) == date.today()
        ).count(),
        'chambres_libres': Chambre.query.filter_by(statut='libre').count()
    }
    return render_template('index.html', stats=stats)

# Routes pour les patients
@app.route('/patients')
@login_required
def patients():
    patients = Patient.query.order_by(Patient.nom).all()
    return render_template('patients.html', patients=patients)

@app.route('/patients/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_patient():
    if request.method == 'POST':
        patient = Patient(
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            date_naissance=datetime.strptime(request.form['date_naissance'], '%Y-%m-%d').date(),
            telephone=request.form['telephone'],
            email=request.form['email'],
            adresse=request.form['adresse'],
            numero_securite_sociale=request.form['numero_securite_sociale']
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient ajouté avec succès!', 'success')
        return redirect(url_for('patients'))
    return render_template('ajouter_patient.html')

@app.route('/patients/<int:id>')
@login_required
def detail_patient(id):
    patient = Patient.query.get_or_404(id)
    rendez_vous = RendezVous.query.filter_by(patient_id=id).order_by(RendezVous.date_rdv.desc()).all()
    consultations = Consultation.query.filter_by(patient_id=id).order_by(Consultation.date_consultation.desc()).all()
    return render_template('detail_patient.html', patient=patient, rendez_vous=rendez_vous, consultations=consultations)

# Routes pour le personnel
@app.route('/personnel')
@login_required
def personnel():
    personnel_list = Personnel.query.order_by(Personnel.nom).all()
    return render_template('personnel.html', personnel=personnel_list)

@app.route('/personnel/ajouter', methods=['GET', 'POST'])
@role_required('admin')
def ajouter_personnel():
    if request.method == 'POST':
        personnel = Personnel(
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            specialite=request.form['specialite'],
            telephone=request.form['telephone'],
            email=request.form['email'],
            date_embauche=datetime.strptime(request.form['date_embauche'], '%Y-%m-%d').date()
        )
        db.session.add(personnel)
        db.session.commit()
        flash('Personnel ajouté avec succès!', 'success')
        return redirect(url_for('personnel'))
    return render_template('ajouter_personnel.html')

# Routes pour les rendez-vous
@app.route('/rendez-vous')
@login_required
def rendez_vous():
    rdv = RendezVous.query.order_by(RendezVous.date_rdv).all()
    return render_template('rendez_vous.html', rendez_vous=rdv)

@app.route('/rendez-vous/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_rendez_vous():
    if request.method == 'POST':
        rdv = RendezVous(
            patient_id=request.form['patient_id'],
            personnel_id=request.form['personnel_id'],
            date_rdv=datetime.strptime(request.form['date_rdv'], '%Y-%m-%dT%H:%M'),
            type_consultation=request.form['type_consultation'],
            notes=request.form['notes']
        )
        db.session.add(rdv)
        db.session.commit()
        flash('Rendez-vous ajouté avec succès!', 'success')
        return redirect(url_for('rendez_vous'))
    
    patients = Patient.query.order_by(Patient.nom).all()
    personnel = Personnel.query.order_by(Personnel.nom).all()
    return render_template('ajouter_rendez_vous.html', patients=patients, personnel=personnel)

# Routes pour les chambres
@app.route('/chambres')
@login_required
def chambres():
    chambres = Chambre.query.order_by(Chambre.numero).all()
    return render_template('chambres.html', chambres=chambres)

@app.route('/chambres/ajouter', methods=['GET', 'POST'])
@role_required('admin')
def ajouter_chambre():
    if request.method == 'POST':
        chambre = Chambre(
            numero=request.form['numero'],
            type_chambre=request.form['type_chambre'],
            prix_nuit=float(request.form['prix_nuit'])
        )
        db.session.add(chambre)
        db.session.commit()
        flash('Chambre ajoutée avec succès!', 'success')
        return redirect(url_for('chambres'))
    return render_template('ajouter_chambre.html')

# API pour obtenir les données
@app.route('/api/patients')
def api_patients():
    patients = Patient.query.all()
    return jsonify([{
        'id': p.id,
        'nom': p.nom,
        'prenom': p.prenom,
        'telephone': p.telephone
    } for p in patients])

@app.route('/api/personnel')
def api_personnel():
    personnel = Personnel.query.all()
    return jsonify([{
        'id': p.id,
        'nom': p.nom,
        'prenom': p.prenom,
        'specialite': p.specialite
    } for p in personnel])

# Routes pour les utilisateurs
@app.route('/users')
@role_required('admin')
def users():
    users = User.query.order_by(User.nom).all()
    return render_template('users.html', users=users)

# Routes pour la pharmacie
@app.route('/pharmacie')
@login_required
def pharmacie():
    medicaments = Medicament.query.order_by(Medicament.nom).all()
    prescriptions = Prescription.query.order_by(Prescription.date_prescription.desc()).limit(10).all()
    return render_template('pharmacie.html', medicaments=medicaments, prescriptions=prescriptions)

@app.route('/pharmacie/medicaments')
@role_required('pharmacien')
def medicaments():
    medicaments = Medicament.query.order_by(Medicament.nom).all()
    return render_template('medicaments.html', medicaments=medicaments)

@app.route('/pharmacie/medicaments/ajouter', methods=['GET', 'POST'])
@role_required('pharmacien')
def ajouter_medicament():
    if request.method == 'POST':
        medicament = Medicament(
            nom=request.form['nom'],
            code_medicament=request.form['code_medicament'],
            description=request.form['description'],
            prix_unitaire=float(request.form['prix_unitaire']),
            quantite_stock=int(request.form['quantite_stock']),
            seuil_minimum=int(request.form['seuil_minimum']),
            date_expiration=datetime.strptime(request.form['date_expiration'], '%Y-%m-%d').date() if request.form['date_expiration'] else None,
            fournisseur=request.form['fournisseur']
        )
        db.session.add(medicament)
        db.session.commit()
        flash('Médicament ajouté avec succès!', 'success')
        return redirect(url_for('medicaments'))
    return render_template('ajouter_medicament.html')

@app.route('/pharmacie/prescriptions')
@login_required
def prescriptions():
    prescriptions = Prescription.query.order_by(Prescription.date_prescription.desc()).all()
    return render_template('prescriptions.html', prescriptions=prescriptions)

@app.route('/pharmacie/prescriptions/<int:id>/delivrer', methods=['POST'])
@role_required('pharmacien')
def delivrer_prescription(id):
    prescription = Prescription.query.get_or_404(id)
    medicament = prescription.medicament
    
    if medicament.quantite_stock >= prescription.quantite:
        medicament.quantite_stock -= prescription.quantite
        prescription.statut = 'delivre'
        db.session.commit()
        flash('Prescription délivrée avec succès!', 'success')
    else:
        flash('Stock insuffisant pour délivrer cette prescription', 'error')
    
    return redirect(url_for('prescriptions'))

# Routes pour l'hospitalisation
@app.route('/hospitalisation')
@login_required
def hospitalisation():
    hospitalisations = Hospitalisation.query.filter_by(statut='hospitalise').order_by(Hospitalisation.date_admission.desc()).all()
    return render_template('hospitalisation.html', hospitalisations=hospitalisations)

@app.route('/hospitalisation/admettre', methods=['GET', 'POST'])
@login_required
def admettre_patient():
    if request.method == 'POST':
        # Vérifier si la chambre est libre
        chambre = Chambre.query.get(request.form['chambre_id'])
        if chambre.statut != 'libre':
            flash('Cette chambre n\'est pas disponible', 'error')
            return redirect(url_for('admettre_patient'))
        
        # Créer l'hospitalisation
        hospitalisation = Hospitalisation(
            patient_id=request.form['patient_id'],
            chambre_id=request.form['chambre_id'],
            motif_admission=request.form['motif_admission'],
            notes=request.form['notes']
        )
        db.session.add(hospitalisation)
        
        # Marquer la chambre comme occupée
        chambre.statut = 'occupee'
        
        db.session.commit()
        flash('Patient admis avec succès!', 'success')
        return redirect(url_for('hospitalisation'))
    
    patients = Patient.query.order_by(Patient.nom).all()
    chambres_libres = Chambre.query.filter_by(statut='libre').all()
    return render_template('admettre_patient.html', patients=patients, chambres=chambres_libres)

@app.route('/hospitalisation/<int:id>/sortie', methods=['POST'])
@login_required
def sortie_patient(id):
    hospitalisation = Hospitalisation.query.get_or_404(id)
    hospitalisation.date_sortie = datetime.utcnow()
    hospitalisation.statut = 'sorti'
    
    # Libérer la chambre
    hospitalisation.chambre.statut = 'libre'
    
    db.session.commit()
    flash('Patient sorti avec succès!', 'success')
    return redirect(url_for('hospitalisation'))

# Routes pour la facturation
@app.route('/facturation')
@login_required
def facturation():
    factures = Facture.query.order_by(Facture.date_facture.desc()).all()
    stats = {
        'total_factures': Facture.query.count(),
        'factures_impayees': Facture.query.filter(Facture.statut.in_(['en_attente', 'partielle'])).count(),
        'montant_impaye': db.session.query(db.func.sum(Facture.montant_total - Facture.montant_paye)).filter(Facture.statut.in_(['en_attente', 'partielle'])).scalar() or 0
    }
    return render_template('facturation.html', factures=factures, stats=stats)

@app.route('/facturation/nouvelle', methods=['GET', 'POST'])
@login_required
def nouvelle_facture():
    if request.method == 'POST':
        # Générer un numéro de facture unique
        numero_facture = f"FLEM-{datetime.now().strftime('%Y%m%d')}-{Facture.query.count() + 1:04d}"
        
        facture = Facture(
            numero_facture=numero_facture,
            patient_id=request.form['patient_id'],
            hospitalisation_id=request.form.get('hospitalisation_id') or None,
            type_facture=request.form['type_facture'],
            date_echeance=datetime.strptime(request.form['date_echeance'], '%Y-%m-%d').date() if request.form['date_echeance'] else None,
            notes=request.form['notes']
        )
        
        # Calculer le montant total
        montant_total = 0
        services = request.form.getlist('services[]')
        quantites = request.form.getlist('quantites[]')
        prix = request.form.getlist('prix[]')
        descriptions = request.form.getlist('descriptions[]')
        
        for i, service in enumerate(services):
            if service and quantites[i] and prix[i]:
                detail = DetailFacture(
                    description=descriptions[i],
                    quantite=int(quantites[i]),
                    prix_unitaire=float(prix[i]),
                    montant=int(quantites[i]) * float(prix[i]),
                    type_service=service
                )
                facture.details.append(detail)
                montant_total += detail.montant
        
        facture.montant_total = montant_total
        db.session.add(facture)
        db.session.commit()
        
        flash('Facture créée avec succès!', 'success')
        return redirect(url_for('detail_facture', id=facture.id))
    
    patients = Patient.query.order_by(Patient.nom).all()
    hospitalisations = Hospitalisation.query.filter_by(statut='hospitalise').all()
    chambres = Chambre.query.all()
    medicaments = Medicament.query.all()
    return render_template('nouvelle_facture.html', patients=patients, hospitalisations=hospitalisations, chambres=chambres, medicaments=medicaments)

@app.route('/facturation/<int:id>')
@login_required
def detail_facture(id):
    facture = Facture.query.get_or_404(id)
    return render_template('detail_facture.html', facture=facture)

@app.route('/facturation/<int:id>/paiement', methods=['POST'])
@login_required
def enregistrer_paiement(id):
    facture = Facture.query.get_or_404(id)
    montant_paye = float(request.form['montant_paye'])
    
    facture.montant_paye += montant_paye
    
    if facture.montant_paye >= facture.montant_total:
        facture.statut = 'payee'
    elif facture.montant_paye > 0:
        facture.statut = 'partielle'
    
    db.session.commit()
    flash('Paiement enregistré avec succès!', 'success')
    return redirect(url_for('detail_facture', id=id))

# Routes CRUD pour les patients
@app.route('/patients/<int:id>/modifier', methods=['GET', 'POST'])
@login_required
def modifier_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient.nom = request.form['nom']
        patient.prenom = request.form['prenom']
        patient.date_naissance = datetime.strptime(request.form['date_naissance'], '%Y-%m-%d').date()
        patient.telephone = request.form['telephone']
        patient.email = request.form['email']
        patient.adresse = request.form['adresse']
        patient.numero_securite_sociale = request.form['numero_securite_sociale']
        db.session.commit()
        flash('Patient modifié avec succès!', 'success')
        return redirect(url_for('detail_patient', id=id))
    return render_template('modifier_patient.html', patient=patient)

@app.route('/patients/<int:id>/supprimer', methods=['POST'])
@role_required('admin')
def supprimer_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient supprimé avec succès!', 'success')
    return redirect(url_for('patients'))

# Routes CRUD pour le personnel
@app.route('/personnel/<int:id>/modifier', methods=['GET', 'POST'])
@role_required('admin')
def modifier_personnel(id):
    personnel = Personnel.query.get_or_404(id)
    if request.method == 'POST':
        personnel.nom = request.form['nom']
        personnel.prenom = request.form['prenom']
        personnel.specialite = request.form['specialite']
        personnel.telephone = request.form['telephone']
        personnel.email = request.form['email']
        personnel.date_embauche = datetime.strptime(request.form['date_embauche'], '%Y-%m-%d').date()
        db.session.commit()
        flash('Personnel modifié avec succès!', 'success')
        return redirect(url_for('personnel'))
    return render_template('modifier_personnel.html', personnel=personnel)

@app.route('/personnel/<int:id>/supprimer', methods=['POST'])
@role_required('admin')
def supprimer_personnel(id):
    personnel = Personnel.query.get_or_404(id)
    db.session.delete(personnel)
    db.session.commit()
    flash('Personnel supprimé avec succès!', 'success')
    return redirect(url_for('personnel'))

# Routes CRUD pour les chambres
@app.route('/chambres/<int:id>/modifier', methods=['GET', 'POST'])
@role_required('admin')
def modifier_chambre(id):
    chambre = Chambre.query.get_or_404(id)
    if request.method == 'POST':
        chambre.numero = request.form['numero']
        chambre.type_chambre = request.form['type_chambre']
        chambre.prix_nuit = float(request.form['prix_nuit'])
        db.session.commit()
        flash('Chambre modifiée avec succès!', 'success')
        return redirect(url_for('chambres'))
    return render_template('modifier_chambre.html', chambre=chambre)

@app.route('/chambres/<int:id>/supprimer', methods=['POST'])
@role_required('admin')
def supprimer_chambre(id):
    chambre = Chambre.query.get_or_404(id)
    if chambre.statut == 'occupee':
        flash('Impossible de supprimer une chambre occupée', 'error')
        return redirect(url_for('chambres'))
    db.session.delete(chambre)
    db.session.commit()
    flash('Chambre supprimée avec succès!', 'success')
    return redirect(url_for('chambres'))

# Routes CRUD pour les médicaments
@app.route('/pharmacie/medicaments/<int:id>/modifier', methods=['GET', 'POST'])
@role_required('pharmacien')
def modifier_medicament(id):
    medicament = Medicament.query.get_or_404(id)
    if request.method == 'POST':
        medicament.nom = request.form['nom']
        medicament.code_medicament = request.form['code_medicament']
        medicament.description = request.form['description']
        medicament.prix_unitaire = float(request.form['prix_unitaire'])
        medicament.quantite_stock = int(request.form['quantite_stock'])
        medicament.seuil_minimum = int(request.form['seuil_minimum'])
        medicament.fournisseur = request.form['fournisseur']
        if request.form['date_expiration']:
            medicament.date_expiration = datetime.strptime(request.form['date_expiration'], '%Y-%m-%d').date()
        db.session.commit()
        flash('Médicament modifié avec succès!', 'success')
        return redirect(url_for('medicaments'))
    return render_template('modifier_medicament.html', medicament=medicament)

@app.route('/pharmacie/medicaments/<int:id>/supprimer', methods=['POST'])
@role_required('pharmacien')
def supprimer_medicament(id):
    medicament = Medicament.query.get_or_404(id)
    db.session.delete(medicament)
    db.session.commit()
    flash('Médicament supprimé avec succès!', 'success')
    return redirect(url_for('medicaments'))

# Routes CRUD pour les utilisateurs
@app.route('/users/<int:id>/modifier', methods=['GET', 'POST'])
@role_required('admin')
def modifier_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.nom = request.form['nom']
        user.prenom = request.form['prenom']
        user.telephone = request.form['telephone']
        user.role = request.form['role']
        if request.form['password']:
            user.set_password(request.form['password'])
        db.session.commit()
        flash('Utilisateur modifié avec succès!', 'success')
        return redirect(url_for('users'))
    return render_template('modifier_user.html', user=user)

@app.route('/users/<int:id>/supprimer', methods=['POST'])
@role_required('admin')
def supprimer_user(id):
    user = User.query.get_or_404(id)
    if user.id == session['user_id']:
        flash('Vous ne pouvez pas supprimer votre propre compte', 'error')
        return redirect(url_for('users'))
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès!', 'success')
    return redirect(url_for('users'))

# Routes CRUD pour les rendez-vous
@app.route('/rendez-vous/<int:id>/modifier', methods=['GET', 'POST'])
@login_required
def modifier_rendez_vous(id):
    rdv = RendezVous.query.get_or_404(id)
    if request.method == 'POST':
        rdv.patient_id = request.form['patient_id']
        rdv.personnel_id = request.form['personnel_id']
        rdv.date_rdv = datetime.strptime(request.form['date_rdv'], '%Y-%m-%dT%H:%M')
        rdv.type_consultation = request.form['type_consultation']
        rdv.statut = request.form['statut']
        rdv.notes = request.form['notes']
        db.session.commit()
        flash('Rendez-vous modifié avec succès!', 'success')
        return redirect(url_for('rendez_vous'))
    patients = Patient.query.order_by(Patient.nom).all()
    personnel = Personnel.query.order_by(Personnel.nom).all()
    return render_template('modifier_rendez_vous.html', rdv=rdv, patients=patients, personnel=personnel)

@app.route('/rendez-vous/<int:id>/supprimer', methods=['POST'])
@login_required
def supprimer_rendez_vous(id):
    rdv = RendezVous.query.get_or_404(id)
    db.session.delete(rdv)
    db.session.commit()
    flash('Rendez-vous supprimé avec succès!', 'success')
    return redirect(url_for('rendez_vous'))

# Route pour le profil utilisateur
@app.route('/profil')
@login_required
def profil():
    user = User.query.get(session['user_id'])
    return render_template('profil.html', user=user)

@app.route('/profil/modifier', methods=['GET', 'POST'])
@login_required
def modifier_profil():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.nom = request.form['nom']
        user.prenom = request.form['prenom']
        user.email = request.form['email']
        user.telephone = request.form['telephone']
        
        # Vérifier si un nouveau mot de passe est fourni
        new_password = request.form.get('new_password', '')
        if new_password:
            confirm_password = request.form.get('confirm_password', '')
            if new_password != confirm_password:
                flash('Les mots de passe ne correspondent pas', 'error')
                return render_template('modifier_profil.html', user=user)
            if len(new_password) < 6:
                flash('Le mot de passe doit contenir au moins 6 caractères', 'error')
                return render_template('modifier_profil.html', user=user)
            user.set_password(new_password)
        
        db.session.commit()
        flash('Profil mis à jour avec succès!', 'success')
        return redirect(url_for('profil'))
    
    return render_template('modifier_profil.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Ajouter des données de test si la base est vide
        if User.query.count() == 0:
            # Créer l'administrateur par défaut
            admin = User(
                username='admin',
                email='admin@flem.fr',
                role='admin',
                nom='Administrateur',
                prenom='FLEM',
                telephone='0123456789'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Créer un médecin de test
            medecin = User(
                username='medecin1',
                email='medecin@flem.fr',
                role='medecin',
                nom='Martin',
                prenom='Dr. Marie',
                telephone='0987654321'
            )
            medecin.set_password('medecin123')
            db.session.add(medecin)
            
            # Créer un pharmacien de test
            pharmacien = User(
                username='pharmacien1',
                email='pharmacien@flem.fr',
                role='pharmacien',
                nom='Dupont',
                prenom='Jean',
                telephone='0555666777'
            )
            pharmacien.set_password('pharmacien123')
            db.session.add(pharmacien)
            
            db.session.commit()
        
        if Patient.query.count() == 0:
            # Ajouter un patient de test
            patient_test = Patient(
                nom="Dupont",
                prenom="Jean",
                date_naissance=date(1980, 5, 15),
                telephone="0123456789",
                email="jean.dupont@email.com",
                adresse="123 Rue de la Paix, Paris",
                numero_securite_sociale="1234567890123"
            )
            db.session.add(patient_test)
            
            # Ajouter du personnel de test
            medecin_test = Personnel(
                nom="Martin",
                prenom="Dr. Marie",
                specialite="Médecine générale",
                telephone="0987654321",
                email="marie.martin@flem.fr",
                date_embauche=date(2020, 1, 15)
            )
            db.session.add(medecin_test)
            
            # Ajouter des chambres de test
            chambre1 = Chambre(numero="101", type_chambre="simple", prix_nuit=50000.0)
            chambre2 = Chambre(numero="102", type_chambre="double", prix_nuit=80000.0)
            chambre3 = Chambre(numero="201", type_chambre="VIP", prix_nuit=150000.0)
            
            db.session.add_all([chambre1, chambre2, chambre3])
            
            # Ajouter des médicaments de test
            medicament1 = Medicament(
                nom="Paracétamol 500mg",
                code_medicament="PAR500",
                description="Antalgique et antipyrétique",
                prix_unitaire=500.0,
                quantite_stock=100,
                seuil_minimum=20,
                fournisseur="Pharma Congo"
            )
            medicament2 = Medicament(
                nom="Amoxicilline 1g",
                code_medicament="AMO1000",
                description="Antibiotique à large spectre",
                prix_unitaire=2500.0,
                quantite_stock=50,
                seuil_minimum=10,
                fournisseur="MediCorp"
            )
            medicament3 = Medicament(
                nom="Ibuprofène 400mg",
                code_medicament="IBU400",
                description="Anti-inflammatoire non stéroïdien",
                prix_unitaire=800.0,
                quantite_stock=75,
                seuil_minimum=15,
                fournisseur="Pharma Congo"
            )
            
            db.session.add_all([medicament1, medicament2, medicament3])
            db.session.commit()
    
    # Configuration pour le déploiement
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 8080))
        debug_mode = os.environ.get('FLASK_ENV') != 'production'
        app.run(debug=debug_mode, host='0.0.0.0', port=port)
