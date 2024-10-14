let currentSlide = 0;

function moveSlider(direction) {
    const slides = document.querySelectorAll('.brand-slide');
    const totalSlides = slides.length;
    const sliderContainer = document.querySelector('.brand-slider');
    const containerWidth = document.querySelector('.slider-container1').offsetWidth;
    const slideWidth = slides[0].offsetWidth + 20; // Add margin between slides

    // Calculate how many slides fit within the container
    const visibleSlides = Math.floor(containerWidth / slideWidth);

    // Update current slide index
    currentSlide += direction;

    // Ensure the current slide stays within bounds
    if (currentSlide > totalSlides - visibleSlides) currentSlide = totalSlides - visibleSlides;
    if (currentSlide < 0) currentSlide = 0;

    // Move the slider based on currentSlide and slide width
    sliderContainer.style.transform = `translateX(${-currentSlide * slideWidth}px)`;
}

function openBrandPage(page) {
    window.location.href = page; // Redirect to the specified page
}
