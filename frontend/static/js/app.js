// API Base URL
const API_URL = '/api';

// Mobile menu toggle
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const navLinks = document.getElementById('navLinks');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const icon = mobileMenuToggle.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    });
}

// Smooth scroll pour les liens de navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            // Fermer le menu mobile après le clic
            navLinks.classList.remove('active');
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// Charger les cours
async function loadCourses() {
    const coursesGrid = document.getElementById('coursesGrid');
    if (!coursesGrid) return;

    // Données statiques des cours
    const courses = [
        {
            title: 'Piano',
            description: 'Apprenez le piano classique et moderne avec nos professeurs diplômés',
            level: 'Tous niveaux',
            price: '45€/h',
            image: '/static/images/placeholder-cover.svg'
        },
        {
            title: 'Guitare',
            description: 'Guitare acoustique, électrique et basse pour tous les styles',
            level: 'Débutant à Avancé',
            price: '40€/h',
            image: '/static/images/placeholder-cover.svg'
        },
        {
            title: 'Chant',
            description: 'Technique vocale, interprétation et présence scénique',
            level: 'Tous niveaux',
            price: '50€/h',
            image: '/static/images/placeholder-cover.svg'
        },
        {
            title: 'Batterie',
            description: 'Rythme, coordination et improvisation',
            level: 'Débutant à Intermédiaire',
            price: '45€/h',
            image: '/static/images/placeholder-cover.svg'
        },
        {
            title: 'Violon',
            description: 'Apprentissage classique et contemporain du violon',
            level: 'Tous niveaux',
            price: '48€/h',
            image: '/static/images/placeholder-cover.svg'
        },
        {
            title: 'Solfège',
            description: 'Théorie musicale, lecture de partitions et harmonie',
            level: 'Débutant à Avancé',
            price: '35€/h',
            image: '/static/images/placeholder-cover.svg'
        }
    ];

    courses.forEach(course => {
        const courseCard = createCourseCard(course);
        coursesGrid.appendChild(courseCard);
    });
}

function createCourseCard(course) {
    const card = document.createElement('div');
    card.className = 'course-card';
    card.innerHTML = `
        <img src="${course.image}" alt="${course.title}" class="course-image">
        <div class="course-content">
            <h3>${course.title}</h3>
            <p>${course.description}</p>
            <div class="course-meta">
                <span class="course-level">${course.level}</span>
                <span class="course-price">${course.price}</span>
            </div>
        </div>
    `;
    return card;
}

// Charger les événements
async function loadEvents() {
    const eventsGrid = document.getElementById('eventsGrid');
    if (!eventsGrid) return;

    // Données statiques des événements
    const events = [
        {
            day: '15',
            month: 'DÉC',
            title: 'Concert de Noël',
            location: 'Auditorium GDE',
            time: '19h00',
            description: 'Concert annuel de fin d\'année avec tous nos élèves. Un moment magique à partager en famille !',
        },
        {
            day: '22',
            month: 'DÉC',
            title: 'Masterclass Jazz',
            location: 'Salle principale',
            time: '14h00',
            description: 'Masterclass exceptionnelle avec le pianiste de jazz renommé Jean Dupont.',
        },
        {
            day: '10',
            month: 'JAN',
            title: 'Portes Ouvertes',
            location: 'École GDE',
            time: '10h - 18h',
            description: 'Découvrez notre école, rencontrez nos professeurs et testez nos instruments gratuitement.',
        }
    ];

    events.forEach(event => {
        const eventCard = createEventCard(event);
        eventsGrid.appendChild(eventCard);
    });
}

function createEventCard(event) {
    const card = document.createElement('div');
    card.className = 'event-card';
    card.innerHTML = `
        <div class="event-date-box">
            <div class="event-day">${event.day}</div>
            <div class="event-month">${event.month}</div>
        </div>
        <div class="event-content">
            <h3>${event.title}</h3>
            <div class="event-meta">
                <span><i class="fas fa-map-marker-alt"></i>${event.location}</span>
                <span><i class="fas fa-clock"></i>${event.time}</span>
            </div>
            <p class="event-description">${event.description}</p>
            <a href="#contact" class="btn-event">S'inscrire</a>
        </div>
    `;
    return card;
}

// Contact form
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Simuler l'envoi du formulaire
        alert('Merci pour votre message ! Nous vous répondrons dans les plus brefs délais.');
        contactForm.reset();
    });
}

// Newsletter form
const newsletterForms = document.querySelectorAll('.newsletter-form');
newsletterForms.forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Merci de vous être inscrit à notre newsletter !');
        form.reset();
    });
});

// Initialiser le contenu au chargement
document.addEventListener('DOMContentLoaded', () => {
    loadCourses();
    loadEvents();
});
