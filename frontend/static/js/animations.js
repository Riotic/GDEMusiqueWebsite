// Animations avec GSAP et ScrollTrigger

gsap.registerPlugin(ScrollTrigger);

// Animation du hero au chargement
gsap.from('.hero-title', {
    duration: 1.2,
    y: -100,
    opacity: 0,
    ease: 'power3.out'
});

gsap.from('.hero-subtitle', {
    duration: 1,
    y: -50,
    opacity: 0,
    delay: 0.3,
    ease: 'power3.out'
});

gsap.from('.hero-buttons', {
    duration: 1,
    scale: 0.8,
    opacity: 0,
    delay: 0.6,
    ease: 'back.out(1.7)'
});

gsap.from('.scroll-indicator', {
    duration: 1,
    opacity: 0,
    delay: 1,
    ease: 'power3.out'
});

// Animation de la navbar au scroll
let lastScroll = 0;

// Animation des sections au scroll
const sections = document.querySelectorAll('section:not(.hero-section)');

sections.forEach((section, index) => {
    // Animation du header de section
    const sectionHeader = section.querySelector('.section-header');
    if (sectionHeader) {
        gsap.from(sectionHeader, {
            scrollTrigger: {
                trigger: section,
                start: 'top 80%',
                toggleActions: 'play none none none'
            },
            duration: 0.8,
            y: 50,
            opacity: 0,
            ease: 'power3.out'
        });
    }

    // Animation des cartes de cours
    const courseCards = section.querySelectorAll('.course-card');
    if (courseCards.length > 0) {
        gsap.from(courseCards, {
            scrollTrigger: {
                trigger: section,
                start: 'top 70%',
                toggleActions: 'play none none none'
            },
            duration: 0.6,
            y: 50,
            opacity: 0,
            stagger: 0.15,
            ease: 'power3.out'
        });
    }

    // Animation des cartes d'événements
    const eventCards = section.querySelectorAll('.event-card');
    if (eventCards.length > 0) {
        gsap.from(eventCards, {
            scrollTrigger: {
                trigger: section,
                start: 'top 70%',
                toggleActions: 'play none none none'
            },
            duration: 0.6,
            x: -50,
            opacity: 0,
            stagger: 0.2,
            ease: 'power3.out'
        });
    }

    // Animation des feature cards
    const featureCards = section.querySelectorAll('.feature-card');
    if (featureCards.length > 0) {
        gsap.from(featureCards, {
            scrollTrigger: {
                trigger: section,
                start: 'top 70%',
                toggleActions: 'play none none none'
            },
            duration: 0.6,
            scale: 0.8,
            opacity: 0,
            stagger: 0.15,
            ease: 'back.out(1.3)'
        });
    }

    // Animation des stats
    const statCards = section.querySelectorAll('.stat-card');
    if (statCards.length > 0) {
        gsap.from(statCards, {
            scrollTrigger: {
                trigger: section,
                start: 'top 70%',
                toggleActions: 'play none none none'
            },
            duration: 0.8,
            scale: 0.5,
            opacity: 0,
            stagger: 0.1,
            ease: 'back.out(1.5)'
        });

        // Animation des chiffres
        statCards.forEach(card => {
            const numberElement = card.querySelector('.stat-number');
            if (numberElement) {
                const finalNumber = parseInt(numberElement.textContent.replace(/\D/g, ''));
                const suffix = numberElement.textContent.replace(/[0-9]/g, '');
                
                ScrollTrigger.create({
                    trigger: card,
                    start: 'top 80%',
                    onEnter: () => {
                        gsap.to(numberElement, {
                            duration: 2,
                            textContent: finalNumber,
                            snap: { textContent: 1 },
                            ease: 'power1.out',
                            onUpdate: function() {
                                numberElement.textContent = Math.ceil(this.targets()[0].textContent) + suffix;
                            }
                        });
                    }
                });
            }
        });
    }

    // Animation du contenu about
    const aboutText = section.querySelector('.about-text');
    const aboutImage = section.querySelector('.about-image');
    if (aboutText && aboutImage) {
        gsap.from(aboutText, {
            scrollTrigger: {
                trigger: section,
                start: 'top 70%',
                toggleActions: 'play none none none'
            },
            duration: 0.8,
            x: -50,
            opacity: 0,
            ease: 'power3.out'
        });

        gsap.from(aboutImage, {
            scrollTrigger: {
                trigger: section,
                start: 'top 70%',
                toggleActions: 'play none none none'
            },
            duration: 0.8,
            x: 50,
            opacity: 0,
            ease: 'power3.out'
        });
    }

    // Animation du formulaire de contact
    const contactForm = section.querySelector('.contact-form');
    const contactInfo = section.querySelector('.contact-info');
    if (contactForm && contactInfo) {
        gsap.from(contactInfo, {
            scrollTrigger: {
                trigger: section,
                start: 'top 70%',
                toggleActions: 'play none none none'
            },
            duration: 0.8,
            x: -50,
            opacity: 0,
            ease: 'power3.out'
        });

        gsap.from(contactForm, {
            scrollTrigger: {
                trigger: section,
                start: 'top 70%',
                toggleActions: 'play none none none'
            },
            duration: 0.8,
            x: 50,
            opacity: 0,
            delay: 0.2,
            ease: 'power3.out'
        });
    }
});

// Animation du footer
const footer = document.querySelector('.footer');
if (footer) {
    const footerSections = footer.querySelectorAll('.footer-section');
    gsap.from(footerSections, {
        scrollTrigger: {
            trigger: footer,
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        duration: 0.6,
        y: 30,
        opacity: 0,
        stagger: 0.1,
        ease: 'power3.out'
    });
}

// Parallax léger sur le hero
document.addEventListener('mousemove', (e) => {
    const hero = document.querySelector('.hero-content');
    if (!hero) return;
    
    const x = (e.clientX / window.innerWidth - 0.5) * 30;
    const y = (e.clientY / window.innerHeight - 0.5) * 30;
    
    gsap.to(hero, {
        duration: 1,
        x: x,
        y: y,
        ease: 'power2.out'
    });
});

// Hover effects sur les boutons
document.querySelectorAll('.btn-hero-primary, .btn-hero-secondary, .btn-nav-cta, .btn-submit, .btn-event').forEach(btn => {
    btn.addEventListener('mouseenter', () => {
        gsap.to(btn, {
            duration: 0.3,
            scale: 1.05,
            ease: 'back.out(1.7)'
        });
    });
    
    btn.addEventListener('mouseleave', () => {
        gsap.to(btn, {
            duration: 0.3,
            scale: 1,
            ease: 'power2.out'
        });
    });
});

// Animation du scroll indicator
gsap.to('.scroll-indicator', {
    duration: 1.5,
    y: 10,
    repeat: -1,
    yoyo: true,
    ease: 'power1.inOut'
});
