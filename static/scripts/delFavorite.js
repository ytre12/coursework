function removeFavorite(forestId, buttonElement) {
    fetch('/api/toggle_favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ forest_id: forestId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'removed') {
            const row = buttonElement.closest('tr');
            row.remove();
        }
    })
    .catch(error => console.error('Помилка видалення:', error));
}