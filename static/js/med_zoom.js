// Get elements
const productImage = document.querySelector('.medicine-image'); // Main product image
const zoomedView = document.querySelector('.zoomed-view');
const productInfo = document.querySelector('.medicine-info');
const mainMedicineImage = document.getElementById('mainMedicineImage'); // Main medicine image

// Change the main product image when a related image is clicked
function changeMainImage(element) {
    const newImageSrc = element.getAttribute('data-image');
    mainMedicineImage.src = newImageSrc;
}

// Zoom functionality
productImage.addEventListener('mousemove', (e) => {
    const { left, top, width, height } = productImage.getBoundingClientRect();
    const x = e.clientX - left;
    const y = e.clientY - top;
    const backgroundPositionX = (x / width) * 100;
    const backgroundPositionY = (y / height) * 100;

    zoomedView.style.backgroundImage = `url('${productImage.src}')`;
    zoomedView.style.backgroundSize = `${width * 2}px ${height * 2}px`; // Adjust zoom level
    zoomedView.style.backgroundPosition = `${backgroundPositionX}% ${backgroundPositionY}%`;

    const infoRect = productInfo.getBoundingClientRect();
    zoomedView.style.left = `${infoRect.left}px`; 
    zoomedView.style.top = `${infoRect.top}px`; 
});

// Show the zoomed view when mouse enters the product image
productImage.addEventListener('mouseenter', () => {
    zoomedView.style.display = 'block';
});

// Hide the zoomed view when mouse leaves the product image
productImage.addEventListener('mouseleave', () => {
    zoomedView.style.display = 'none';
});

// Collapsible sections functionality
const collapsibles = document.querySelectorAll('.collapsible'); // Get all collapsibles

collapsibles.forEach(collapsible => {
    const content = collapsible.nextElementSibling; // Get the corresponding content
    const caret = document.createElement('span'); // Create caret element
    caret.classList.add('caret');
    caret.innerHTML = "&#x25B6;"; // Right arrow
    collapsible.appendChild(caret); // Append caret to the collapsible button

    collapsible.addEventListener("click", function() {
        this.classList.toggle("active");
        if (content.style.display === "block") {
            content.style.display = "none";
            caret.innerHTML = "&#x25B6;"; // Right arrow
        } else {
            content.style.display = "block";
            caret.innerHTML = "&#x25BC;"; // Down arrow
        }
    });
});
