$(document).ready(function () {
    $(".testimonial-carousel").owlCarousel({
        loop: true,
        center: true,
        items: 1,
        stagePadding: 200,
        margin: 64,
        autoplay: true,
        autoplayTimeout: 20000,
        responsive: {
            0: {stagePadding: 0, items: 1},
            768: {stagePadding: 100, items: 1.9}
        }
    });
    $(".testimonial-blogs").owlCarousel({
        loop: true,
        margin: 39,
        nav: true,
        navText: ["<i class='bi bi-arrow-left'></i>", "<i class='bi bi-arrow-right'></i>"],
        dots: true,
        autoplay: true,
        autoplayTimeout: 20000,
        responsive: {
            0: {items: 1},
            768: {items: 2},
            1200: {items: 3}
        }
    });
});
$(".carousel-about").owlCarousel({
    loop: true,
    center: true,
    items: 1,
    stagePadding: 200,
    margin: 32,
    autoplay: true,
    autoplayTimeout: 20000,
    responsive: {
        0: {stagePadding: 0, items: 1},
        768: {stagePadding: 100, items: 1.9},
        1200: {stagePadding: 200, items: 1.9}
    }
});
$(".team").owlCarousel({
    loop: true,
    margin: 39,
    nav: true,
    navText: ["<i class='bi bi-arrow-left'></i>", "<i class='bi bi-arrow-right'></i>"],
    dots: true,
    autoplay: true,
    autoplayTimeout: 20000,
    responsive: {
        0: {items: 1},
        768: {items: 2},
        1200: {items: 4}
    }
});


