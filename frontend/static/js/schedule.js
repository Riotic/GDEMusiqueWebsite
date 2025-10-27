// Gestion du planning (Schedule)

async function loadSchedule() {
    if (!authService.isAuthenticated()) {
        const container = document.getElementById('scheduleContainer');
        if (container) {
            container.innerHTML = '<p class="info-message">Connectez-vous pour voir votre planning.</p>';
        }
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/schedule/week`, {
            headers: authService.getHeaders()
        });
        const scheduleItems = await response.json();
        
        displaySchedule(scheduleItems);
    } catch (error) {
        console.error('Error loading schedule:', error);
    }
}

function displaySchedule(items) {
    const container = document.getElementById('scheduleContainer');
    if (!container) return;
    
    const isTeacher = authService.hasRole('teacher');
    const isStudent = authService.hasRole('student');
    
    if (items.length === 0) {
        container.innerHTML = '<p class="info-message">Aucun événement dans votre planning cette semaine.</p>';
        return;
    }
    
    // Grouper par jour
    const itemsByDay = items.reduce((acc, item) => {
        const date = new Date(item.start_time);
        const dayKey = date.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });
        if (!acc[dayKey]) acc[dayKey] = [];
        acc[dayKey].push(item);
        return acc;
    }, {});
    
    container.innerHTML = `
        <div class="schedule-view">
            <div class="schedule-header">
                <h2>
                    ${isTeacher ? '📅 Planning Professeur' : '📅 Mon Planning'}
                </h2>
                <button class="btn-primary" onclick="openAddScheduleModal()">
                    ➕ Ajouter un événement
                </button>
            </div>
            
            <div class="schedule-days">
                ${Object.entries(itemsByDay).map(([day, dayItems]) => `
                    <div class="schedule-day">
                        <h3 class="day-header">${day}</h3>
                        <div class="schedule-items">
                            ${dayItems.map(item => {
                                const startTime = new Date(item.start_time).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
                                const endTime = new Date(item.end_time).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
                                
                                return `
                                    <div class="schedule-item ${isTeacher ? 'teacher-view' : 'student-view'}">
                                        <div class="schedule-time">
                                            <span class="time-badge">${startTime} - ${endTime}</span>
                                        </div>
                                        <div class="schedule-content">
                                            <h4>${item.title}</h4>
                                            ${item.description ? `<p class="schedule-description">${item.description}</p>` : ''}
                                            ${item.reminder_text ? `
                                                <div class="schedule-reminder">
                                                    <strong>📝 ${isTeacher ? 'Points à couvrir' : 'À préparer'}:</strong>
                                                    <p>${item.reminder_text}</p>
                                                </div>
                                            ` : ''}
                                        </div>
                                        <button class="btn-delete" onclick="deleteScheduleItem(${item.id})" title="Supprimer">
                                            🗑️
                                        </button>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function openAddScheduleModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'addScheduleModal';
    modal.style.display = 'block';
    
    // Date et heure par défaut (prochain jour à 14h)
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(14, 0, 0, 0);
    const defaultDate = tomorrow.toISOString().slice(0, 16);
    
    const endTime = new Date(tomorrow);
    endTime.setHours(15, 0, 0, 0);
    const defaultEndDate = endTime.toISOString().slice(0, 16);
    
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
            <h2>Ajouter un événement au planning</h2>
            
            <form id="addScheduleForm" class="form">
                <div class="form-group">
                    <label for="scheduleTitle">Titre *</label>
                    <input type="text" id="scheduleTitle" required>
                </div>
                
                <div class="form-group">
                    <label for="scheduleDescription">Description</label>
                    <textarea id="scheduleDescription" rows="3"></textarea>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="scheduleStartTime">Début *</label>
                        <input type="datetime-local" id="scheduleStartTime" value="${defaultDate}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="scheduleEndTime">Fin *</label>
                        <input type="datetime-local" id="scheduleEndTime" value="${defaultEndDate}" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="scheduleReminder">Sujets à préparer / Points à couvrir</label>
                    <textarea id="scheduleReminder" rows="3" 
                        placeholder="${authService.hasRole('teacher') ? 'Exercices à réviser, morceaux à travailler...' : 'Ce que vous devez préparer pour ce cours...'}"></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="button" class="btn-secondary" onclick="this.closest('.modal').remove()">
                        Annuler
                    </button>
                    <button type="submit" class="btn-primary">
                        Ajouter
                    </button>
                </div>
            </form>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Setup form submission
    document.getElementById('addScheduleForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await addScheduleItem();
    });
}

async function addScheduleItem() {
    const scheduleData = {
        title: document.getElementById('scheduleTitle').value,
        description: document.getElementById('scheduleDescription').value,
        start_time: new Date(document.getElementById('scheduleStartTime').value).toISOString(),
        end_time: new Date(document.getElementById('scheduleEndTime').value).toISOString(),
        reminder_text: document.getElementById('scheduleReminder').value
    };
    
    try {
        const response = await fetch(`${API_URL}/schedule/`, {
            method: 'POST',
            headers: authService.getHeaders(),
            body: JSON.stringify(scheduleData)
        });
        
        if (response.ok) {
            showSuccessMessage('Événement ajouté au planning');
            document.getElementById('addScheduleModal').remove();
            loadSchedule();
        }
    } catch (error) {
        console.error('Error adding schedule item:', error);
    }
}

async function deleteScheduleItem(itemId) {
    if (!confirm('Supprimer cet événement du planning?')) return;
    
    try {
        const response = await fetch(`${API_URL}/schedule/${itemId}`, {
            method: 'DELETE',
            headers: authService.getHeaders()
        });
        
        if (response.ok) {
            showSuccessMessage('Événement supprimé');
            loadSchedule();
        }
    } catch (error) {
        console.error('Error deleting schedule item:', error);
    }
}

// Afficher la liste des élèves (pour les professeurs)
async function loadStudentsList() {
    if (!authService.hasRole('teacher')) return;
    
    try {
        const response = await fetch(`${API_URL}/schedule/students`, {
            headers: authService.getHeaders()
        });
        const students = await response.json();
        
        const container = document.getElementById('studentsListContainer');
        if (!container) return;
        
        container.innerHTML = `
            <div class="students-list">
                <h3>👥 Mes Élèves</h3>
                ${students.length === 0 ? '<p>Aucun élève inscrit pour le moment.</p>' : ''}
                ${students.map(student => `
                    <div class="student-card">
                        <div class="student-info">
                            <h4>${student.first_name} ${student.last_name}</h4>
                            <p class="student-email">${student.email}</p>
                            <p class="student-course">📚 ${student.course}</p>
                        </div>
                        <div class="student-progress">
                            <span>Progression: ${student.progress}%</span>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${student.progress}%"></div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        console.error('Error loading students:', error);
    }
}

// Initialiser
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('scheduleContainer')) {
        loadSchedule();
    }
    if (document.getElementById('studentsListContainer')) {
        loadStudentsList();
    }
});
