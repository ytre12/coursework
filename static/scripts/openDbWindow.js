const windeowSettings = document.getElementById('seting-btn');

const modal = document.querySelector('.modal-overlay');

const openSettingsWindow = () => {
    modal.style.display = 'flex';
}

windeowSettings.addEventListener('click', openSettingsWindow)