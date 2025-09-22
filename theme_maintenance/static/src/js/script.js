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
    $(".scroll-left").click(function () {
        $(".blog-carousel").trigger("prev.owl.carousel");
    });

    $(".scroll-right").click(function () {
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

// Multi-level dropdown click functionality
$(document).ready(function () {
    // Disable Bootstrap dropdown behavior on our custom dropdowns
    $('.o_main_nav .dropdown-toggle').removeAttr('data-bs-toggle');

    // Handle click behavior for all dropdown toggles in navigation
    $('.o_main_nav .dropdown-toggle').on('click', function (e) {
        e.preventDefault();
        e.stopPropagation();

        var $this = $(this);
        var $parent = $this.parent('.dropdown');
        var $submenu = $this.next('.dropdown-menu');


        // Check if submenu goes off-screen and adjust position
        if ($submenu.length > 0) {
            setTimeout(function () {
                var submenuOffset = $submenu.offset();
                var submenuWidth = $submenu.outerWidth();
                var windowWidth = $(window).width();

                if (submenuOffset && (submenuOffset.left + submenuWidth) > windowWidth) {
                    $submenu.addClass('dropdown-menu-right');
                } else {
                    $submenu.removeClass('dropdown-menu-right');
                }
            }, 10);
        }

        // Toggle display
        if ($submenu.hasClass('show')) {
            $submenu.removeClass('show');
            $this.attr('aria-expanded', 'false');
            // Also close any child dropdowns
            $submenu.find('.dropdown-menu').removeClass('show');
            $submenu.find('.dropdown-toggle').attr('aria-expanded', 'false');
        } else {
            // Close other dropdowns at the same level
            $parent.siblings('.dropdown').find('.dropdown-menu').removeClass('show');
            $parent.siblings('.dropdown').find('.dropdown-toggle').attr('aria-expanded', 'false');

            // Open current dropdown
            $submenu.addClass('show');
            $this.attr('aria-expanded', 'true');
        }
    });

    // Prevent dropdown from closing when clicking inside submenu
    $('.o_main_nav .dropdown-menu').on('click', function (e) {
        e.stopPropagation();
    });

    // Close all dropdowns when clicking outside
    $(document).on('click', function (e) {
        if (!$(e.target).closest('.o_main_nav').length) {
            $('.o_main_nav .dropdown-menu').removeClass('show');
            $('.o_main_nav .dropdown-toggle').attr('aria-expanded', 'false');
        }
    });
});

// Three columns carousel functionality is now handled by the public widget in snippets.component.js