const productImage = document.querySelector('.product-image');
const zoomedView = document.querySelector('.zoomed-view');
const productInfo = document.querySelector('.product-info');
const mainProductImage = document.getElementById('mainProductImage');

// Change the main product image when a related image is clicked
function changeMainImage(element) {
    const newImageSrc = element.getAttribute('data-image');
    mainProductImage.src = newImageSrc;
}

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

productImage.addEventListener('mouseenter', () => {
    zoomedView.style.display = 'block';
});

productImage.addEventListener('mouseleave', () => {
    zoomedView.style.display = 'none';
});


const collapsible = document.querySelector(".collapsible");
const content = document.querySelector(".content");
const caret = document.querySelector(".caret");

collapsible.addEventListener("click", function() {
    this.classList.toggle("active");
    if (content.style.display === "block") {
        content.style.display = "none";
        caret.classList.add("collapsed"); // Add the collapsed class to rotate the caret
        caret.innerHTML = "&#x25B6;"; // Right arrow
    } else {
        content.style.display = "block";
        caret.classList.remove("collapsed"); // Remove the collapsed class to rotate the caret back
        caret.innerHTML = "&#x25BC;"; // Down arrow
    }
});