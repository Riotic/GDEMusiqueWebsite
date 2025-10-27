// Gestion des cours et leçons

async function loadMyCourses() {
    if (!authService.isAuthenticated()) {
        const container = document.getElementById('myCoursesContainer');
        if (container) {
            container.innerHTML = '<p class="info-message">Connectez-vous pour voir vos cours personnalisés selon vos instruments.</p>';
        }
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/courses/my-courses`, {
            headers: authService.getHeaders()
        });
        const courses = await response.json();
        
        const container = document.getElementById('myCoursesContainer');
        if (!container) return;
        
        if (courses.length === 0) {
            container.innerHTML = `
                <p class="info-message">
                    Aucun cours disponible pour vos instruments. 
                    <a href="#" onclick="showInstrumentSelection()">Sélectionnez vos instruments</a>
                </p>
            `;
            return;
        }
        
        container.innerHTML = courses.map(course => `
            <div class="course-card" data-course-id="${course.id}">
                <div class="course-image">
                    <img src="${course.image_url || '/static/images/placeholder-cover.svg'}" alt="${course.title}">
                    <span class="course-level">${course.level}</span>
                </div>
                <div class="course-content">
                    <h3>${course.title}</h3>
                    <p class="course-instrument">${course.instrument.name}</p>
                    <p class="course-description">${course.description || ''}</p>
                    <button class="btn-primary" onclick="viewCourseLessons(${course.id})">
                        Voir les leçons
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading courses:', error);
    }
}

async function viewCourseLessons(courseId) {
    try {
        const response = await fetch(`${API_URL}/courses/${courseId}/lessons`, {
            headers: authService.getHeaders()
        });
        const lessons = await response.json();
        
        displayLessons(lessons, courseId);
    } catch (error) {
        console.error('Error loading lessons:', error);
    }
}

function displayLessons(lessons, courseId) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'lessonsModal';
    modal.style.display = 'block';
    
    modal.innerHTML = `
        <div class="modal-content large">
            <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
            <h2>Leçons du cours</h2>
            <div class="lessons-list">
                ${lessons.map(lesson => `
                    <div class="lesson-card" onclick="viewLessonDetails(${lesson.id})">
                        <div class="lesson-number">${lesson.order}</div>
                        <div class="lesson-info">
                            <h3>${lesson.title}</h3>
                            ${lesson.song_name ? `<p class="lesson-song">🎵 ${lesson.song_name}</p>` : ''}
                            <p class="lesson-description">${lesson.description || ''}</p>
                        </div>
                        <div class="lesson-arrow">→</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

async function viewLessonDetails(lessonId) {
    try {
        const response = await fetch(`${API_URL}/courses/lessons/${lessonId}`, {
            headers: authService.getHeaders()
        });
        const lesson = await response.json();
        
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.id = 'lessonDetailModal';
        modal.style.display = 'block';
        
        modal.innerHTML = `
            <div class="modal-content large">
                <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
                <div class="lesson-detail">
                    <h2>${lesson.title}</h2>
                    
                    ${lesson.song_name ? `
                        <div class="lesson-section">
                            <h3>🎵 Morceau: ${lesson.song_name}</h3>
                        </div>
                    ` : ''}
                    
                    ${lesson.description ? `
                        <div class="lesson-section">
                            <h3>📝 Description</h3>
                            <p>${lesson.description}</p>
                        </div>
                    ` : ''}
                    
                    ${lesson.song_history ? `
                        <div class="lesson-section">
                            <h3>📖 Histoire de la chanson</h3>
                            <p>${lesson.song_history}</p>
                        </div>
                    ` : ''}
                    
                    ${lesson.chord_help ? `
                        <div class="lesson-section">
                            <h3>🎸 Aide sur les accords</h3>
                            <pre class="chord-help">${lesson.chord_help}</pre>
                        </div>
                    ` : ''}
                    
                    ${lesson.sheet_music_url ? `
                        <div class="lesson-section">
                            <h3>🎼 Partition</h3>
                            <a href="${lesson.sheet_music_url}" target="_blank" class="btn-primary">
                                📄 Télécharger la partition
                            </a>
                        </div>
                    ` : ''}
                    
                    ${lesson.video_url ? `
                        <div class="lesson-section">
                            <h3>🎥 Vidéo explicative</h3>
                            <a href="${lesson.video_url}" target="_blank" class="btn-primary">
                                ▶️ Voir la vidéo
                            </a>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Fermer le modal précédent
        const previousModal = document.getElementById('lessonsModal');
        if (previousModal) previousModal.remove();
        
    } catch (error) {
        console.error('Error loading lesson details:', error);
    }
}

async function loadInstruments() {
    try {
        const response = await fetch(`${API_URL}/courses/instruments`);
        const instruments = await response.json();
        return instruments;
    } catch (error) {
        console.error('Error loading instruments:', error);
        return [];
    }
}

async function showInstrumentSelection() {
    const instruments = await loadInstruments();
    const userInstruments = authService.currentUser?.instruments || [];
    
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'instrumentsModal';
    modal.style.display = 'block';
    
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
            <h2>Sélectionnez vos instruments</h2>
            <p>Choisissez les instruments que vous souhaitez apprendre:</p>
            <div class="instruments-grid">
                ${instruments.map(instrument => {
                    const isSelected = userInstruments.some(ui => ui.id === instrument.id);
                    return `
                        <div class="instrument-option ${isSelected ? 'selected' : ''}" 
                             data-instrument-id="${instrument.id}"
                             onclick="toggleInstrument(${instrument.id}, this)">
                            <div class="instrument-icon">🎵</div>
                            <h4>${instrument.name}</h4>
                            <p>${instrument.description || ''}</p>
                        </div>
                    `;
                }).join('')}
            </div>
            <button class="btn-primary" onclick="saveInstruments()">Sauvegarder</button>
        </div>
    `;
    
    document.body.appendChild(modal);
}

async function toggleInstrument(instrumentId, element) {
    element.classList.toggle('selected');
}

async function saveInstruments() {
    const selected = document.querySelectorAll('.instrument-option.selected');
    const instrumentIds = Array.from(selected).map(el => parseInt(el.dataset.instrumentId));
    
    try {
        // Retirer tous les instruments actuels
        for (const instrument of authService.currentUser.instruments) {
            await fetch(`${API_URL}/auth/me/instruments/${instrument.id}`, {
                method: 'DELETE',
                headers: authService.getHeaders()
            });
        }
        
        // Ajouter les nouveaux instruments
        for (const instrumentId of instrumentIds) {
            await fetch(`${API_URL}/auth/me/instruments/${instrumentId}`, {
                method: 'POST',
                headers: authService.getHeaders()
            });
        }
        
        // Recharger l'utilisateur et les cours
        await authService.loadCurrentUser();
        showSuccessMessage('Instruments mis à jour');
        document.getElementById('instrumentsModal').remove();
        loadMyCourses();
    } catch (error) {
        console.error('Error saving instruments:', error);
    }
}

// Initialiser
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('myCoursesContainer')) {
        loadMyCourses();
    }
});
