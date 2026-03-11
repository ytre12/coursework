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
        
        let heartIcon = item.is_favorite ? '❤️' : '🤍';
        
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
        if (!data) return;

        let item = localForestsData.find(f => f.id === forestId);

        if (data.status === 'added') {
            btnElement.innerHTML = '❤️';
            if (item) item.is_favorite = true;
        } else if (data.status === 'removed') {
            btnElement.innerHTML = '🤍';
            if (item) item.is_favorite = false;
        }
    })
    .catch(err => console.error('Помилка фаворитів:', err));
}

closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

windowSettings.addEventListener('click', () => openModalWithData(null));
forestOneBtn.addEventListener('click', () => openModalWithData('Звернігородське'));
forestTwoBtn.addEventListener('click', () => openModalWithData('Корсунь-Шевченківське'));
forestThreeBtn.addEventListener('click', () => openModalWithData('Черкаське'));