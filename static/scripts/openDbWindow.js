const windowSettings = document.getElementById('seting-btn');
const closeBtn = document.getElementById('close-modal');
const modal = document.querySelector('.modal-overlay');
const container = document.getElementById('forest-container');

// Глобальна змінна для даних
let localForestsData = [];

// Оновлена функція відкриття: тепер вона ще й завантажує дані
const openSettingsWindow = () => {
    modal.style.display = 'flex';
    // Якщо дані ще не завантажені, завантажуємо їх
    if (localForestsData.length === 0) {
        openModalAndLoad();
    }
}

const closeModal = () => {
    modal.style.display = 'none';
}

function openModalAndLoad() {
    container.innerHTML = 'Завантаження...'; // Тимчасовий текст
    fetch('/api/forests')
        .then(response => response.json())
        .then(data => {
            localForestsData = data; 
            renderForests(localForestsData); 
        })
        .catch(err => {
            container.innerHTML = 'Помилка завантаження даних.';
            console.error(err);
        });
}

function renderForests(data) {
    container.innerHTML = ''; 

    data.forEach(item => {
        const div = document.createElement('div');
        div.className = 'db-conteiner'; // Використовуємо твій клас із CSS
        div.innerHTML = `
            <p><strong>Головний ліс:</strong> ${item.mainForest}</p>
            <p><strong>Ліс:</strong> ${item.forest}</p>
            <p><strong>Тип рубки:</strong> ${item.typeCutting}</p>
            <p><strong>Квартал:</strong> ${item.quarter} | <strong>Виділ:</strong> ${item.department}</p>
            <p><strong>Площа:</strong> ${item.area} га</p>
            <p><strong>Рік:</strong> ${item.year} | <strong>Місяць:</strong> ${item.month}</p>
            <hr>
        `;
        container.appendChild(div);
    });
}

function sortData(field) {
    if (localForestsData.length === 0) return;

    localForestsData.sort((a, b) => {
        let valA = a[field];
        let valB = b[field];

        // Перевірка на числа
        if (typeof valA === 'number' && typeof valB === 'number') {
            return valA - valB;
        }
        
        // Перевірка на рядки (щоб не було помилок, якщо поле порожнє)
        valA = valA ? valA.toString() : '';
        valB = valB ? valB.toString() : '';
        
        return valA.localeCompare(valB);
    });

    renderForests(localForestsData);
}

windowSettings.addEventListener('click', openSettingsWindow);
closeBtn.addEventListener('click', closeModal);