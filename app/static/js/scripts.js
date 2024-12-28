// Function to toggle a menu
function toggleMenu() {
    const menu = document.getElementById("menu");
    menu.classList.toggle("hidden");
}

// Function to display a confirmation before deleting
function confirmDelete(message) {
    return confirm(message || "Are you sure you want to delete this?");
}
