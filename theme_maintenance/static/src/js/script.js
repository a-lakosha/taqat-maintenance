$(document).ready(function () {
    // Initialize carousel
    $(".blog-carousel").owlCarousel({
        loop: true,
        margin: 30,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        nav: false, // disable default nav, we’ll use custom buttons
        responsive: {
            0: {items: 1},
            768: {items: 2},
            1200: {items: 3}
        }
    });

    // Custom navigation buttons
    $(".scroll-left").click(function () {
        $(".blog-carousel").trigger("prev.owl.carousel");
    });

    $(".scroll-right").click(function () {
        $(".blog-carousel").trigger("next.owl.carousel");
    });
});
$(document).ready(function () {
    // Initialize carousel
    $(".client-carousel").owlCarousel({
        loop: true,
        margin: 30,
        autoplay: true,
        // autoplayTimeout: 3000,
        autoplayHoverPause: true,
        nav: false, // disable default nav, we’ll use custom buttons
        responsive: {
            0: {items: 1}
        }
    });

    // Custom navigation buttons
    $(".scroll-left").click(function () {
        $(".client-carousel").trigger("prev.owl.carousel");
    });

    $(".scroll-right").click(function () {
        $(".client-carousel").trigger("next.owl.carousel");
    });
});
