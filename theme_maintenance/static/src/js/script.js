document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector('.cards_container');
    if (container) {
        const testimonials = container.querySelectorAll('.testimonial-card');

        if (testimonials.length === 1) {
            container.classList.remove('justify-content-start');
            container.classList.add('justify-content-center');
        } else {
            container.classList.remove('justify-content-center');
            container.classList.add('justify-content-start');
        }
    }
});
