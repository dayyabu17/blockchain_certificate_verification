// Simple fade-in animation for pages
document.addEventListener("DOMContentLoaded", () => {
    const content = document.querySelector(".container");
    if (content) {
        content.style.opacity = 0;
        setTimeout(() => {
            content.style.transition = "opacity 0.7s";
            content.style.opacity = 1;
        }, 100);
    }
});

// Preview selected passport photo before upload
function previewPassport(event) {
    const img = document.getElementById("passportPreview");
    img.src = URL.createObjectURL(event.target.files[0]);
    img.style.display = "block";
}

// Disable submit button after clicking (prevents double upload)
function disableSubmit(btn) {
    btn.innerHTML = "Uploading...";
    btn.disabled = true;
}
