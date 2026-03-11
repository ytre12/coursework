// Знаходимо всі кнопки
const windowSettings = document.getElementById('seting-btn');
const forestOneBtn = document.getElementById('forestOne-btn');
const forestTwoBtn = document.getElementById('forestTwo-btn');
const forestThreeBtn = document.getElementById('forestThree-btn');

const closeBtn = document.getElementById('close-modal');
const modal = document.querySelector('.modal-overlay');
const container = document.getElementById('forest-container');

let localForestsData = [];       
let currentRenderedData = [];    
let isMainModal = true;          

// Універсальна функція для відкриття модалки
function openModalWithData(forestNameFilter = null) {
    modal.style.display = 'flex';

    if (localForestsData.length === 0) {
        container.innerHTML = 'Завантаження...';
        fetch('/api/forests')
            .then(response => response.json())
            .then(data => {
                localForestsData = data; 
                processAndRender(forestNameFilter);
            })
            .catch(err => {
                container.innerHTML = 'Помилка завантаження даних.';
                console.error(err);
            });
    } else {
        processAndRender(forestNameFilter);
    }
}

// Функція фільтрації та виклику малювання
function processAndRender(forestNameFilter) {
    if (forestNameFilter) {
        currentRenderedData = localForestsData.filter(item => item.mainForest === forestNameFilter);
        isMainModal = false; 
    } else {
        currentRenderedData = [...localForestsData]; 
        isMainModal = true; 
    }
    
    renderData(currentRenderedData);
}

// ЄДИНА функція для відтворення HTML
function renderData(data) {
    container.innerHTML = ''; 

    const sortMainBtn = document.getElementById('sort-main-forest');

    data.forEach(item => {
        const div = document.createElement('div');
        div.className = 'db-conteiner'; 
        
        let htmlContent = '';
        
        if (isMainModal) {
            htmlContent += `<p>${item.mainForest}</p>`;
            if (sortMainBtn) sortMainBtn.style.display = 'inline-block';
        } else {
            if (sortMainBtn) sortMainBtn.style.display = 'none';
        }
        
        // НОВЕ: Перевіряємо статус фаворита і вибираємо іконку
        // Якщо item.is_favorite == true, малюємо зафарбоване сердечко, інакше - пусте
        let heartIcon = item.is_favorite ? '❤️' : '🤍';
        
        // НОВЕ: Додав кнопку сердечка в кінці рядка
        htmlContent += `
            <p>${item.forest}</p>
            <p>${item.typeCutting}</p>
            <p>${item.quarter}</p> 
            <p>${item.department}</p>
            <p>${item.area}</p>
            <p>${item.volumeForestManagement}</p> 
            <p>${item.month}</p>
            <p>${item.decade}</p> 
            <p>${item.year}</p>
            <button class="fav-btn" style="background: none; border: none; cursor: pointer; font-size: 1.2em;" 
                    onclick="toggleFavorite(${item.id}, this)">
                ${heartIcon}
            </button>
        `;
        
        div.innerHTML = htmlContent;
        container.appendChild(div);
    });
}

// Оновлене сортування 
function sortData(field) {
    if (currentRenderedData.length === 0) return;

    currentRenderedData.sort((a, b) => {
        let valA = a[field];
        let valB = b[field];

        if (typeof valA === 'number' && typeof valB === 'number') {
            return valA - valB;
        }
        
        valA = valA ? valA.toString() : '';
        valB = valB ? valB.toString() : '';
        
        return valA.localeCompare(valB);
    });

    renderData(currentRenderedData);
}

// НОВЕ: Функція для збереження/видалення з фаворитів
function toggleFavorite(forestId, btnElement) {
    fetch('/api/toggle_favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ forest_id: forestId })
    })
    .then(response => {
        if (response.status === 401) {
            alert('Будь ласка, увійдіть в акаунт, щоб зберігати вирубки.');
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return; // Якщо була помилка 401, зупиняємось

        // Знаходимо цей об'єкт у нашому головному масиві даних
        let item = localForestsData.find(f => f.id === forestId);

        if (data.status === 'added') {
            btnElement.innerHTML = '❤️';
            if (item) item.is_favorite = true; // Оновлюємо стан у пам'яті
        } else if (data.status === 'removed') {
            btnElement.innerHTML = '🤍';
            if (item) item.is_favorite = false; // Оновлюємо стан у пам'яті
        }
    })
    .catch(err => console.error('Помилка фаворитів:', err));
}

// Слухачі подій
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

windowSettings.addEventListener('click', () => openModalWithData(null));
forestOneBtn.addEventListener('click', () => openModalWithData('Звернігородське'));
forestTwoBtn.addEventListener('click', () => openModalWithData('Корсунь-Шевченківське'));
forestThreeBtn.addEventListener('click', () => openModalWithData('Черкаське'));