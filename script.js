const form = document.getElementById("uploadForm");
const loading = document.getElementById("loading");
const dropArea = document.getElementById("dropArea");
const fileInput = document.getElementById("fileInput");

form.addEventListener("submit", function () {
    loading.style.display = "block";
});

// Drag & drop
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.background = "rgba(255,255,255,0.2)";
});

dropArea.addEventListener("dragleave", () => {
    dropArea.style.background = "transparent";
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.style.background = "transparent";
    fileInput.files = e.dataTransfer.files;
});