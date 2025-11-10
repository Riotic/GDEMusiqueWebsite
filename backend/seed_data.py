"""
Script de peuplement de la base de données avec des données de test
"""
from datetime import datetime, timedelta
from backend.database import SessionLocal, engine
from backend.models import (
    Base, User, Instrument, Course, Lesson, MarketplaceItem,
    ScheduleItem, Enrollment, RoleEnum
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def seed_database():
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Vérifier si la base est déjà peuplée
        if db.query(User).first():
            print("✅ La base de données contient déjà des données. Seed skippé.")
            return
        
        print("🎵 Peuplement de la base de données GDE Musique...")
        
        # ========== UTILISATEURS ==========
        print("  👤 Création des utilisateurs...")
        
        # Admin
        admin = User(
            email="admin@gde-musique.fr",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            first_name="Jean",
            last_name="Dupont",
            role=RoleEnum.ADMIN,
            is_active=True
        )
        db.add(admin)
        
        # Professeurs
        prof_piano = User(
            email="prof.piano@gde-musique.fr",
            username="marie_leclerc",
            hashed_password=get_password_hash("prof123"),
            first_name="Marie",
            last_name="Leclerc",
            role=RoleEnum.TEACHER,
            is_active=True
        )
        db.add(prof_piano)
        
        prof_guitare = User(
            email="prof.guitare@gde-musique.fr",
            username="pierre_martin",
            hashed_password=get_password_hash("prof123"),
            first_name="Pierre",
            last_name="Martin",
            role=RoleEnum.TEACHER,
            is_active=True
        )
        db.add(prof_guitare)
        
        # Élèves
        eleve1 = User(
            email="alice@example.com",
            username="alice_dubois",
            hashed_password=get_password_hash("eleve123"),
            first_name="Alice",
            last_name="Dubois",
            role=RoleEnum.STUDENT,
            is_active=True
        )
        db.add(eleve1)
        
        eleve2 = User(
            email="lucas@example.com",
            username="lucas_bernard",
            hashed_password=get_password_hash("eleve123"),
            first_name="Lucas",
            last_name="Bernard",
            role=RoleEnum.STUDENT,
            is_active=True
        )
        db.add(eleve2)
        
        eleve3 = User(
            email="emma@example.com",
            username="emma_rousseau",
            hashed_password=get_password_hash("eleve123"),
            first_name="Emma",
            last_name="Rousseau",
            role=RoleEnum.STUDENT,
            is_active=True
        )
        db.add(eleve3)
        
        db.commit()
        
        # ========== INSTRUMENTS ==========
        print("  🎸 Création des instruments...")
        
        piano = Instrument(
            name="Piano",
            description="Instrument à clavier, roi des instruments",
            image_url="/static/images/instruments/piano.jpg"
        )
        db.add(piano)
        
        guitare = Instrument(
            name="Guitare",
            description="Instrument à cordes pincées, acoustique ou électrique",
            image_url="/static/images/instruments/guitare.jpg"
        )
        db.add(guitare)
        
        chant = Instrument(
            name="Chant",
            description="Technique vocale et interprétation",
            image_url="/static/images/instruments/chant.jpg"
        )
        db.add(chant)
        
        batterie = Instrument(
            name="Batterie",
            description="Percussion, rythme et coordination",
            image_url="/static/images/instruments/batterie.jpg"
        )
        db.add(batterie)
        
        violon = Instrument(
            name="Violon",
            description="Instrument à cordes frottées",
            image_url="/static/images/instruments/violon.jpg"
        )
        db.add(violon)
        
        solfege = Instrument(
            name="Solfège",
            description="Théorie musicale et formation de l'oreille",
            image_url="/static/images/instruments/solfege.jpg"
        )
        db.add(solfege)
        
        db.commit()
        
        # Associer les instruments aux utilisateurs
        eleve1.instruments.extend([piano, solfege])
        eleve2.instruments.extend([guitare, batterie])
        eleve3.instruments.extend([chant, piano])
        
        db.commit()
        
        # ========== COURS ==========
        print("  📚 Création des cours...")
        
        # Cours de Piano
        cours_piano_debutant = Course(
            title="Piano Débutant",
            description="Découverte du piano et des bases de la musique",
            instrument_id=piano.id,
            level="Débutant",
            image_url="/static/images/courses/piano-debutant.jpg"
        )
        db.add(cours_piano_debutant)
        
        cours_piano_inter = Course(
            title="Piano Intermédiaire",
            description="Approfondissement de la technique et du répertoire",
            instrument_id=piano.id,
            level="Intermédiaire",
            image_url="/static/images/courses/piano-inter.jpg"
        )
        db.add(cours_piano_inter)
        
        # Cours de Guitare
        cours_guitare_debutant = Course(
            title="Guitare Débutant",
            description="Les bases de la guitare acoustique et électrique",
            instrument_id=guitare.id,
            level="Débutant",
            image_url="/static/images/courses/guitare-debutant.jpg"
        )
        db.add(cours_guitare_debutant)
        
        cours_guitare_avance = Course(
            title="Guitare Avancé",
            description="Techniques avancées et improvisation",
            instrument_id=guitare.id,
            level="Avancé",
            image_url="/static/images/courses/guitare-avance.jpg"
        )
        db.add(cours_guitare_avance)
        
        # Cours de Chant
        cours_chant = Course(
            title="Technique Vocale",
            description="Travail de la voix et de l'interprétation",
            instrument_id=chant.id,
            level="Tous niveaux",
            image_url="/static/images/courses/chant.jpg"
        )
        db.add(cours_chant)
        
        db.commit()
        
        # Associer les professeurs aux cours
        prof_piano.taught_courses.extend([cours_piano_debutant, cours_piano_inter])
        prof_guitare.taught_courses.extend([cours_guitare_debutant, cours_guitare_avance])
        
        db.commit()
        
        # ========== LEÇONS ==========
        print("  📖 Création des leçons avec partitions et accords...")
        
        # Leçons Piano Débutant
        lesson1 = Lesson(
            course_id=cours_piano_debutant.id,
            title="Introduction au Piano",
            description="Découverte de l'instrument et position des mains",
            song_name="Ode à la Joie - Beethoven",
            song_history="L'Ode à la Joie est un hymne composé par Ludwig van Beethoven en 1824 pour sa 9ème symphonie. C'est l'une des œuvres les plus célèbres de la musique classique et est devenue l'hymne européen.",
            chord_help="Cette mélodie simple se joue avec la main droite. Pas d'accords complexes pour commencer.\nNotes: Mi Mi Fa Sol | Sol Fa Mi Ré | Do Do Ré Mi | Mi Ré Ré",
            sheet_music_url="/static/partitions/ode-joie.pdf",
            video_url="https://www.youtube.com/watch?v=example1",
            order=1
        )
        db.add(lesson1)
        
        lesson2 = Lesson(
            course_id=cours_piano_debutant.id,
            title="Les Accords de Base",
            description="Apprendre les accords majeurs et mineurs",
            song_name="Let It Be - The Beatles",
            song_history="'Let It Be' a été écrite par Paul McCartney en 1968. Inspirée par un rêve de sa mère décédée, c'est devenue l'une des chansons les plus emblématiques des Beatles.",
            chord_help="Accords utilisés:\n- Do Majeur (C): Do - Mi - Sol\n- Sol Majeur (G): Sol - Si - Ré\n- La mineur (Am): La - Do - Mi\n- Fa Majeur (F): Fa - La - Do\n\nProgression: C - G - Am - F",
            sheet_music_url="/static/partitions/let-it-be.pdf",
            video_url="https://www.youtube.com/watch?v=example2",
            order=2
        )
        db.add(lesson2)
        
        # Leçons Guitare Débutant
        lesson3 = Lesson(
            course_id=cours_guitare_debutant.id,
            title="Les Premiers Accords",
            description="Mi mineur, La mineur, Ré majeur",
            song_name="Knockin' on Heaven's Door - Bob Dylan",
            song_history="Écrite par Bob Dylan en 1973 pour le film 'Pat Garrett et Billy le Kid', cette chanson est devenue un classique du folk-rock, reprise par de nombreux artistes.",
            chord_help="Accords de base:\n- Sol Majeur (G): 320003\n- Ré Majeur (D): xx0232\n- La mineur (Am): x02210\n- Do Majeur (C): x32010\n\nGrattage: Bas Bas Haut Haut Bas Haut",
            sheet_music_url="/static/partitions/knockin.pdf",
            video_url="https://www.youtube.com/watch?v=example3",
            order=1
        )
        db.add(lesson3)
        
        lesson4 = Lesson(
            course_id=cours_guitare_debutant.id,
            title="Le Rythme au Médiator",
            description="Techniques de grattage et de picking",
            song_name="Horse With No Name - America",
            song_history="Sortie en 1971, cette chanson du groupe America raconte l'histoire d'un voyage dans le désert. Sa simplicité avec seulement 2 accords en fait un excellent morceau pour débuter.",
            chord_help="Seulement 2 accords!\n- Em: 022000\n- D6/9: xx0200\n\nAlternez entre ces deux accords tout au long de la chanson.\nRythme: Bas Haut Bas Haut Bas Haut Bas Haut",
            sheet_music_url="/static/partitions/horse-no-name.pdf",
            video_url="https://www.youtube.com/watch?v=example4",
            order=2
        )
        db.add(lesson4)
        
        db.commit()
        
        # ========== INSCRIPTIONS ==========
        print("  📝 Création des inscriptions...")
        
        enrollment1 = Enrollment(student_id=eleve1.id, course_id=cours_piano_debutant.id, progress=45)
        enrollment2 = Enrollment(student_id=eleve2.id, course_id=cours_guitare_debutant.id, progress=60)
        enrollment3 = Enrollment(student_id=eleve3.id, course_id=cours_chant.id, progress=30)
        enrollment4 = Enrollment(student_id=eleve3.id, course_id=cours_piano_inter.id, progress=20)
        
        db.add_all([enrollment1, enrollment2, enrollment3, enrollment4])
        db.commit()
        
        # ========== MARKETPLACE (Petites Ventes) ==========
        print("  🛒 Création des articles de la marketplace...")
        
        item1 = MarketplaceItem(
            title="Guitare Acoustique Yamaha F310",
            description="Guitare acoustique en excellent état, parfaite pour débutants. Livrée avec housse de protection et médiators.",
            price=150.00,
            image_url="/static/images/marketplace/guitare-yamaha.jpg",
            seller_id=admin.id,
            is_sold=False
        )
        db.add(item1)
        
        item2 = MarketplaceItem(
            title="Clavier Numérique Casio CT-S300",
            description="Clavier 61 touches avec différents sons et rythmes. Idéal pour s'entraîner à la maison. Fonctionne sur secteur ou piles.",
            price=200.00,
            image_url="/static/images/marketplace/clavier-casio.jpg",
            seller_id=admin.id,
            is_sold=False
        )
        db.add(item2)
        
        item3 = MarketplaceItem(
            title="Métronome Mécanique Wittner",
            description="Métronome mécanique traditionnel en bois, excellent état. Sans piles, totalement mécanique.",
            price=45.00,
            image_url="/static/images/marketplace/metronome.jpg",
            seller_id=admin.id,
            is_sold=False
        )
        db.add(item3)
        
        item4 = MarketplaceItem(
            title="Pupitre en Métal Réglable",
            description="Pupitre robuste en métal noir, hauteur et angle réglables. Pliable pour faciliter le transport.",
            price=25.00,
            image_url="/static/images/marketplace/pupitre.jpg",
            seller_id=admin.id,
            is_sold=False
        )
        db.add(item4)
        
        item5 = MarketplaceItem(
            title="Lot de Partitions Classiques",
            description="Collection de 20 partitions classiques pour piano (Bach, Mozart, Chopin, etc.). Très bon état.",
            price=35.00,
            image_url="/static/images/marketplace/partitions.jpg",
            seller_id=admin.id,
            is_sold=True  # Déjà vendu
        )
        db.add(item5)
        
        item6 = MarketplaceItem(
            title="Accordeur Chromatique Électronique",
            description="Accordeur numérique à pince pour guitare, basse, violon. Écran LCD rétroéclairé.",
            price=15.00,
            image_url="/static/images/marketplace/accordeur.jpg",
            seller_id=admin.id,
            is_sold=False
        )
        db.add(item6)
        
        db.commit()
        
        # ========== PLANNING ==========
        print("  📅 Création des plannings...")
        
        # Planning du professeur de piano
        today = datetime.now()
        
        # Cours avec Alice (lundi 14h-15h)
        schedule1 = ScheduleItem(
            user_id=prof_piano.id,
            title="Cours Piano - Alice Dubois",
            description="Cours particulier de piano débutant",
            start_time=today + timedelta(days=(7 - today.weekday() + 0) % 7, hours=14 - today.hour),
            end_time=today + timedelta(days=(7 - today.weekday() + 0) % 7, hours=15 - today.hour),
            course_id=cours_piano_debutant.id,
            reminder_text="Revoir: Ode à la Joie, exercices de gammes",
            is_teacher_view=True
        )
        db.add(schedule1)
        
        # Cours avec Emma (mercredi 16h-17h)
        schedule2 = ScheduleItem(
            user_id=prof_piano.id,
            title="Cours Piano - Emma Rousseau",
            description="Cours particulier de piano intermédiaire",
            start_time=today + timedelta(days=(7 - today.weekday() + 2) % 7, hours=16 - today.hour),
            end_time=today + timedelta(days=(7 - today.weekday() + 2) % 7, hours=17 - today.hour),
            course_id=cours_piano_inter.id,
            reminder_text="Travailler: Sonate au Clair de Lune (Beethoven), arpèges",
            is_teacher_view=True
        )
        db.add(schedule2)
        
        # Planning de l'élève Alice
        schedule3 = ScheduleItem(
            user_id=eleve1.id,
            title="Cours de Piano",
            description="Cours avec Mme Leclerc",
            start_time=today + timedelta(days=(7 - today.weekday() + 0) % 7, hours=14 - today.hour),
            end_time=today + timedelta(days=(7 - today.weekday() + 0) % 7, hours=15 - today.hour),
            course_id=cours_piano_debutant.id,
            reminder_text="À préparer: Ode à la Joie jusqu'à la mesure 16, gammes de Do majeur",
            is_teacher_view=False
        )
        db.add(schedule3)
        
        # Planning du professeur de guitare
        schedule4 = ScheduleItem(
            user_id=prof_guitare.id,
            title="Cours Guitare - Lucas Bernard",
            description="Cours particulier de guitare débutant",
            start_time=today + timedelta(days=(7 - today.weekday() + 1) % 7, hours=15 - today.hour),
            end_time=today + timedelta(days=(7 - today.weekday() + 1) % 7, hours=16 - today.hour),
            course_id=cours_guitare_debutant.id,
            reminder_text="Revoir: Accords de base Em, Am, C, G. Changements fluides",
            is_teacher_view=True
        )
        db.add(schedule4)
        
        # Planning de l'élève Lucas
        schedule5 = ScheduleItem(
            user_id=eleve2.id,
            title="Cours de Guitare",
            description="Cours avec M. Martin",
            start_time=today + timedelta(days=(7 - today.weekday() + 1) % 7, hours=15 - today.hour),
            end_time=today + timedelta(days=(7 - today.weekday() + 1) % 7, hours=16 - today.hour),
            course_id=cours_guitare_debutant.id,
            reminder_text="Cette semaine: Pratiquer les transitions Em-Am-C-G (10 min/jour), apprendre 'Knockin on Heaven's Door'",
            is_teacher_view=False
        )
        db.add(schedule5)
        
        db.commit()
        
        print("✅ Base de données peuplée avec succès!")
        print("\n📊 Résumé:")
        print(f"  - {db.query(User).count()} utilisateurs créés")
        print(f"  - {db.query(Instrument).count()} instruments")
        print(f"  - {db.query(Course).count()} cours")
        print(f"  - {db.query(Lesson).count()} leçons")
        print(f"  - {db.query(MarketplaceItem).count()} articles marketplace")
        print(f"  - {db.query(ScheduleItem).count()} événements de planning")
        
        print("\n🔑 Comptes de test:")
        print("  Admin:")
        print("    Email: admin@gde-musique.fr")
        print("    Password: admin123")
        print("\n  Professeur Piano:")
        print("    Email: prof.piano@gde-musique.fr")
        print("    Password: prof123")
        print("\n  Professeur Guitare:")
        print("    Email: prof.guitare@gde-musique.fr")
        print("    Password: prof123")
        print("\n  Élève Alice:")
        print("    Email: alice@example.com")
        print("    Password: eleve123")
        print("\n  Élève Lucas:")
        print("    Email: lucas@example.com")
        print("    Password: eleve123")
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
