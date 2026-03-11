const openCommitsModal = document.getElementById("open-commit");
const commitModal = document.querySelector(".commit-modal");
const closeCommitModal = document.getElementById("commit-modal-close");

openCommitsModal.addEventListener("click", function() {
    commitModal.style.display = "block";
});

closeCommitModal.addEventListener("click", function() {
    commitModal.style.display = "none";
});

