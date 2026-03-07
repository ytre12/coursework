// Знаходимо всі кнопки
const windowSettings = document.getElementById('seting-btn');
const forestOneBtn = document.getElementById('forestOne-btn');
const forestTwoBtn = document.getElementById('forestTwo-btn');
const forestThreeBtn = document.getElementById('forestThree-btn');

const closeBtn = document.getElementById('close-modal');
const modal = document.querySelector('.modal-overlay'); // У нас тепер тільки ОДНА модалка
const container = document.getElementById('forest-container');

let localForestsData = [];       // Тут зберігаємо ВСЮ базу
let currentRenderedData = [];    // Тут зберігаємо те, що зараз показується на екрані
let isMainModal = true;          // Прапорець, щоб знати, чи показувати колонку "mainForest"

// Універсальна функція для відкриття модалки
function openModalWithData(forestNameFilter = null) {
    modal.style.display = 'flex';

    // Якщо база ще порожня - завантажуємо з бекенду
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
        // Якщо дані вже є в пам'яті, просто фільтруємо і малюємо
        processAndRender(forestNameFilter);
    }
}

// Функція фільтрації та виклику малювання
function processAndRender(forestNameFilter) {
    if (forestNameFilter) {
        // Якщо передали назву (наприклад 'Лісництво 1'), фільтруємо масив
        currentRenderedData = localForestsData.filter(item => item.mainForest === forestNameFilter);
        isMainModal = false; // Це конкретне лісництво, колонку mainForest можна не показувати
    } else {
        // Якщо натиснули "Налаштування" - показуємо все
        currentRenderedData = [...localForestsData]; 
        isMainModal = true; 
    }
    
    renderData(currentRenderedData);
}
// ЄДИНА функція для відтворення HTML
function renderData(data) {
    container.innerHTML = ''; 

    // Знаходимо кнопку сортування Main Forest
    const sortMainBtn = document.getElementById('sort-main-forest');

    data.forEach(item => {
        const div = document.createElement('div');
        div.className = 'db-conteiner'; 
        
        let htmlContent = '';
        
        // Якщо це загальна таблиця, показуємо назву головного лісництва і кнопку
        if (isMainModal) {
            htmlContent += `<p>${item.mainForest}</p>`;
            if (sortMainBtn) sortMainBtn.style.display = 'inline-block';
        } else {
            // Якщо конкретне лісництво - ховаємо зайву кнопку сортування
            if (sortMainBtn) sortMainBtn.style.display = 'none';
        }
        
        // Додаємо ВСІ поля у правильному порядку (як кнопки в HTML)
        htmlContent += `
            <p>${item.forest}</p>
            <p>${item.typeCutting}</p>
            <p>${item.quarter}</p> 
            <p>${item.department}</p>
            <p>${item.area}</p>
            <p>${item.volumeForestManagement}</p> <p>${item.month}</p>
            <p>${item.decade}</p> <p>${item.year}</p>
        `;
        
        div.innerHTML = htmlContent;
        container.appendChild(div);
    });
}

// Оновлене сортування (сортує тільки те, що ЗАРАЗ на екрані)
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

// Слухачі подій
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Налаштування (показує всі дані)
// Налаштування (показує всі дані)
windowSettings.addEventListener('click', () => openModalWithData(null));

// Відкриваємо те саме вікно, але ПРОСИМО JS ВІДФІЛЬТРУВАТИ дані:
forestOneBtn.addEventListener('click', () => openModalWithData('Звернігородське'));
forestTwoBtn.addEventListener('click', () => openModalWithData('Корсунь-Шевченківське'));
forestThreeBtn.addEventListener('click', () => openModalWithData('Черкаське'));