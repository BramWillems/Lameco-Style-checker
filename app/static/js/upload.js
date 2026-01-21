const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const dropzone = document.getElementById("dropzone");

function setName(f) {
  fileName.textContent = f ? `Selected: ${f.name}` : "";
}

fileInput.addEventListener("change", (e) => {
  setName(e.target.files[0]);
});

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("drag");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("drag");
});

dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("drag");
  if (e.dataTransfer.files.length) {
    fileInput.files = e.dataTransfer.files;
    setName(e.dataTransfer.files[0]);
  }
});
