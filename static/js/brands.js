let currentSlide = 0;
let autoSlideInterval;

function moveSlider(direction) {
    const slides = document.querySelectorAll('.brand-slide');
    const totalSlides = slides.length;
    const sliderContainer = document.querySelector('.brand-slider');
    const containerWidth = document.querySelector('.slider-container').offsetWidth;
    
    // Calculate the width of one slide including margin
    const slideWidth = slides[0].offsetWidth + parseFloat(window.getComputedStyle(slides[0]).marginRight);

    // Calculate how many slides are visible within the container
    const visibleSlides = Math.floor(containerWidth / slideWidth);

    // Update current slide index based on direction
    currentSlide += direction;

    // Loop back to the beginning if at the last slide
    if (currentSlide >= totalSlides - visibleSlides + 1) {
        currentSlide = 0;  // Start from the first slide
    } else if (currentSlide < 0) {
        currentSlide = totalSlides - visibleSlides;  // Jump to the last set of slides
    }

    // Move the slider by changing the transform property
    sliderContainer.style.transform = translateX(${-currentSlide * slideWidth}px);
}

function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
        moveSlider(1);  // Move to the next slide automatically
    }, 3000);  // Adjust the timing as needed (3000ms = 3 seconds)
}

function stopAutoSlide() {
    clearInterval(autoSlideInterval);  // Stop auto-sliding
}

// Start auto-sliding when the page loads
window.onload = () => {
    startAutoSlide();
};