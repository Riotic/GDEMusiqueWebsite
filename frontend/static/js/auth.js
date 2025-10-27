// Gestion de l'authentification
const API_URL = 'http://localhost:8000/api';

class AuthService {
    constructor() {
        this.currentUser = null;
        this.token = localStorage.getItem('token');
        if (this.token) {
            this.loadCurrentUser();
        }
    }

    async login(email, password) {
        try {
            const formData = new FormData();
            formData.append('username', email); // OAuth2 utilise 'username' même pour l'email
            formData.append('password', password);

            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erreur de connexion');
            }

            const data = await response.json();
            this.token = data.access_token;
            this.currentUser = data.user;
            localStorage.setItem('token', this.token);
            localStorage.setItem('user', JSON.stringify(this.currentUser));

            return this.currentUser;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async register(userData) {
        try {
            const response = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erreur d\'inscription');
            }

            const user = await response.json();
            // Auto-login après inscription
            return await this.login(userData.email, userData.password);
        } catch (error) {
            console.error('Register error:', error);
            throw error;
        }
    }

    async loadCurrentUser() {
        try {
            const response = await fetch(`${API_URL}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (!response.ok) {
                this.logout();
                return null;
            }

            this.currentUser = await response.json();
            localStorage.setItem('user', JSON.stringify(this.currentUser));
            return this.currentUser;
        } catch (error) {
            console.error('Load user error:', error);
            this.logout();
            return null;
        }
    }

    logout() {
        this.token = null;
        this.currentUser = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/';
    }

    isAuthenticated() {
        return !!this.token && !!this.currentUser;
    }

    hasRole(role) {
        return this.currentUser && this.currentUser.role === role;
    }

    getHeaders() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
        };
    }
}

// Instance globale
const authService = new AuthService();

// Afficher/masquer les éléments selon l'authentification
function updateUIForAuth() {
    const isAuth = authService.isAuthenticated();
    
    // Gérer les éléments guest-only (visibles si NON connecté)
    document.querySelectorAll('.guest-only').forEach(el => {
        el.style.display = isAuth ? 'none' : '';
    });
    
    // Gérer les éléments auth-only (visibles si connecté)
    document.querySelectorAll('.auth-only').forEach(el => {
        el.style.display = isAuth ? '' : 'none';
    });
    
    if (isAuth && authService.currentUser) {
        // Afficher l'email de l'utilisateur
        const userEmail = document.getElementById('userEmail');
        if (userEmail) {
            userEmail.textContent = authService.currentUser.email;
        }
        
        // Afficher les sections selon le rôle
        updateUIForRole();
    }
}

function updateUIForRole() {
    const user = authService.currentUser;
    if (!user) return;

    // Afficher les sections admin
    const adminSections = document.querySelectorAll('.admin-only');
    adminSections.forEach(section => {
        section.style.display = (user.role === 'admin') ? '' : 'none';
    });

    // Afficher les sections professeur
    const teacherSections = document.querySelectorAll('.teacher-only');
    teacherSections.forEach(section => {
        section.style.display = (user.role === 'teacher' || user.role === 'admin') ? '' : 'none';
    });

    // Afficher les sections élève
    const studentSections = document.querySelectorAll('.student-only');
    studentSections.forEach(section => {
        section.style.display = (user.role === 'student') ? '' : 'none';
    });
}

// Gestionnaire du formulaire de connexion
function setupLoginModal() {
    const modal = document.getElementById('authModal');
    const loginBtn = document.getElementById('loginBtn');
    const closeBtn = modal?.querySelector('.modal-close');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Ouvrir la modal
    if (loginBtn) {
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (modal) {
                modal.classList.add('active');
            }
        });
    }

    // Fermer la modal
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            if (modal) modal.classList.remove('active');
        });
    }

    // Fermer en cliquant à l'extérieur
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });

    // Gestion des tabs
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            
            // Retirer active de tous les tabs
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Activer le tab sélectionné
            btn.classList.add('active');
            const targetForm = tabName === 'login' ? loginForm : registerForm;
            if (targetForm) targetForm.classList.add('active');
        });
    });

    // Formulaire de connexion
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            try {
                await authService.login(email, password);
                if (modal) modal.classList.remove('active');
                updateUIForAuth();
                showSuccessMessage('Connexion réussie!');
                
                // Charger les données de l'utilisateur
                if (typeof loadMyCourses !== 'undefined') loadMyCourses();
                if (typeof loadMarketplaceItems !== 'undefined') loadMarketplaceItems();
                if (typeof loadSchedule !== 'undefined') loadSchedule();
                
                // Rediriger selon le rôle
                setTimeout(() => {
                    if (authService.hasRole('teacher')) {
                        window.location.href = '#planning';
                    } else if (authService.hasRole('student')) {
                        window.location.href = '#mes-cours';
                    } else if (authService.hasRole('admin')) {
                        window.location.href = '#marketplace';
                    }
                }, 500);
            } catch (error) {
                showErrorMessage(error.message || 'Erreur de connexion');
            }
        });
    }

    // Formulaire d'inscription
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userData = {
                username: document.getElementById('registerUsername').value,
                email: document.getElementById('registerEmail').value,
                first_name: document.getElementById('registerFirstName').value,
                last_name: document.getElementById('registerLastName').value,
                password: document.getElementById('registerPassword').value
            };

            try {
                await authService.register(userData);
                showSuccessMessage('Inscription réussie! Vous pouvez maintenant vous connecter.');
                
                // Basculer vers le tab de connexion
                tabBtns.forEach(b => b.classList.remove('active'));
                tabBtns[0].classList.add('active');
                tabContents.forEach(c => c.classList.remove('active'));
                loginForm.classList.add('active');
                
                registerForm.reset();
            } catch (error) {
                showErrorMessage(error.message || 'Erreur lors de l\'inscription');
            }
        });
    }
}

// Gestionnaire de déconnexion
function setupLogout() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            authService.logout();
        });
    }
}

function showSuccessMessage(message) {
    const toast = document.getElementById('toast');
    if (toast) {
        toast.textContent = message;
        toast.className = 'toast show success';
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

function showErrorMessage(message) {
    const toast = document.getElementById('toast');
    if (toast) {
        toast.textContent = message;
        toast.className = 'toast show error';
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    // Créer l'instance globale du service d'authentification
    window.authService = new AuthService();
    
    updateUIForAuth();
    setupLoginModal();
    setupLogout();
});
