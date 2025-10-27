// Gestion de la marketplace (Petites Ventes)

async function loadMarketplaceItems() {
    try {
        const response = await fetch(`${API_URL}/marketplace/`);
        const items = await response.json();
        
        const container = document.getElementById('marketplaceItems');
        if (!container) return;
        
        container.innerHTML = items.map(item => `
            <div class="marketplace-card" data-item-id="${item.id}">
                <div class="marketplace-image">
                    <img src="${item.image_url || '/static/images/placeholder-cover.svg'}" alt="${item.title}">
                    ${item.is_sold ? '<span class="sold-badge">VENDU</span>' : ''}
                </div>
                <div class="marketplace-content">
                    <h3>${item.title}</h3>
                    <p class="marketplace-description">${item.description || ''}</p>
                    <div class="marketplace-footer">
                        <span class="price">${item.price.toFixed(2)} €</span>
                        ${!item.is_sold && authService.hasRole('admin') ? `
                            <button class="btn-small btn-sold" onclick="markAsSold(${item.id})">
                                Marquer vendu
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading marketplace:', error);
    }
}

async function markAsSold(itemId) {
    if (!confirm('Marquer cet article comme vendu?')) return;
    
    try {
        const response = await fetch(`${API_URL}/marketplace/${itemId}/mark-sold`, {
            method: 'PATCH',
            headers: authService.getHeaders()
        });
        
        if (response.ok) {
            showSuccessMessage('Article marqué comme vendu');
            loadMarketplaceItems();
        }
    } catch (error) {
        console.error('Error marking as sold:', error);
    }
}

function openAddItemModal() {
    const modal = document.getElementById('addItemModal');
    if (modal) modal.style.display = 'block';
}

function setupMarketplace() {
    // Charger les items si on est sur la page marketplace
    if (document.getElementById('marketplaceItems')) {
        loadMarketplaceItems();
    }
    
    // Setup du formulaire d'ajout d'item (admin only)
    const addItemForm = document.getElementById('addItemForm');
    if (addItemForm) {
        addItemForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const itemData = {
                title: document.getElementById('itemTitle').value,
                description: document.getElementById('itemDescription').value,
                price: parseFloat(document.getElementById('itemPrice').value),
                image_url: document.getElementById('itemImageUrl').value
            };
            
            try {
                const response = await fetch(`${API_URL}/marketplace/`, {
                    method: 'POST',
                    headers: authService.getHeaders(),
                    body: JSON.stringify(itemData)
                });
                
                if (response.ok) {
                    showSuccessMessage('Article ajouté avec succès');
                    document.getElementById('addItemModal').style.display = 'none';
                    addItemForm.reset();
                    loadMarketplaceItems();
                }
            } catch (error) {
                console.error('Error adding item:', error);
            }
        });
    }
}

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', setupMarketplace);
