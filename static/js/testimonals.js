const testimonialContainer = document.getElementById('testimonialContainer');
let scrollAmount = 0;

function autoScroll() {
  scrollAmount += 1; // Adjust scroll speed here
  if (scrollAmount >= testimonialContainer.scrollWidth - testimonialContainer.clientWidth) {
    scrollAmount = 0; // Reset scroll to the beginning
  }
  testimonialContainer.scrollLeft = scrollAmount;
}

// Auto-scroll every 20 milliseconds
setInterval(autoScroll, 40);
