let currentIndex = 0;
const slideInterval = 3000; // Time between slides (in milliseconds)
const visibleSlides = 3; // Number of slides visible at a time

function showSlide(index) {
    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    const totalSlides = slides.length;

    // Adjust the index logic to loop properly
    if (index >= totalSlides - visibleSlides + 1) {
        currentIndex = 0; // If we go beyond the last set, loop back to the first
    } else if (index < 0) {
        currentIndex = totalSlides - visibleSlides; // If we go before the first set, go to the last full set
    } else {
        currentIndex = index; // Otherwise, update the current index normally
    }

    // Calculate the translation offset for the slides
    const offset = -currentIndex * (100 / visibleSlides); // Move by one set of slides
    slider.style.transform = `translateX(${offset}%)`;

    // Update the active dot based on the current visible set of slides
    dots.forEach((dot, i) => {
        dot.classList.remove('active');
        // Highlight the correct dot for the visible set of slides
        if (i === Math.floor(currentIndex / visibleSlides)) {
            dot.classList.add('active');
        }
    });
}

function nextSlide() {
    showSlide(currentIndex + 1); // Move to the next slide
}

function prevSlide() {
    showSlide(currentIndex - 1); // Move to the previous slide
}

function currentSlide(index) {
    // Multiply the index by the number of visible slides so clicking a dot moves to the correct set
    showSlide(index * visibleSlides);
}

// Initialize the first slide and dot as active
showSlide(currentIndex);

// Automatically change slides every few seconds
setInterval(nextSlide, slideInterval);
