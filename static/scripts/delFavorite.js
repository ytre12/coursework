function removeFavorite(forestId, buttonElement) {
            // Робимо запит на наш існуючий маршрут
            fetch('/api/toggle_favorite', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ forest_id: forestId })
            })
            .then(response => response.json())
            .then(data => {
                // Якщо сервер відповів, що успішно видалено
                if (data.status === 'removed') {
                    // Знаходимо рядок (tr), у якому знаходиться натиснута кнопка
                    const row = buttonElement.closest('tr');
                    // Видаляємо цей рядок з екрану
                    row.remove();
                }
            })
            .catch(error => console.error('Помилка видалення:', error));
        }