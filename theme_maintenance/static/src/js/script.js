$(document).ready(function () {
    // Check if jQuery and Owl Carousel are available
    if (typeof $ === 'undefined' || typeof $.fn.owlCarousel !== 'function') {
        console.warn('jQuery or Owl Carousel not loaded');
        return;
    }

    // Blog carousel
    $(".blog-carousel").owlCarousel({
        loop: true,
        margin: 30,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        nav: false,
        responsive: {
            0: {items: 1},
            768: {items: 2},
            1200: {items: 3}
        }
    });

    // Blog carousel navigation
    $(".blog-scroll-left").click(function () {
        $(".blog-carousel").trigger("prev.owl.carousel");
    });

    $(".blog-scroll-right").click(function () {
        $(".blog-carousel").trigger("next.owl.carousel");
    });

    // Testimonials carousel
    $(".testimonials-carousel").owlCarousel({
        loop: true,
        margin: 30,
        nav: false,
        dots: true,
        responsive: {
            0: {items: 1},
            768: {items: 2},
        }
    });
});

// Three columns carousel functionality is now handled by the public widget in snippets.component.js



