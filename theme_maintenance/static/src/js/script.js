$(document).ready(function () {
    // Initialize carousel
    $(".blog-carousel").owlCarousel({
        loop: true,
        margin: 30,
        // autoplay: true,
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
/** Grid ↔ Carousel toggle for “s_three_columns” */
(function ($) {
    const $section = $('section.s_three_columns');
    if (!$section.length) return;

    const $row = $section.find('> .container > .row.d-flex');
    if (!$row.length) return;

    // Heuristic to detect Odoo editor
    function isEditorOpen() {
        return (
            window.location.search.includes('enable_editor=1') ||
            document.documentElement.classList.contains('o_web_editor') ||
            document.querySelector('.o_we_toolbar, .o_we_website_top_actions') !== null
        );
    }

    function toCarousel() {
        if ($row.hasClass('owl-loaded')) return; // already initialized

        // Save original grid classes and strip them so Owl can size items
        $row.children().each(function () {
            const $col = $(this);
            if (!$col.data('grid-classes')) {
                $col.data('grid-classes', $col.attr('class')); // e.g., "col-lg-4 ... pt16 pb16"
            }
            $col.attr('class', 'item'); // let Owl own the width

            // Attach custom nav buttons
            $('.scroll-left').off('click').on('click', function () {
                $row.trigger('prev.owl.carousel');
            });
            $('.scroll-right').off('click').on('click', function () {
                $row.trigger('next.owl.carousel');
            });

        });

        $row.addClass('owl-carousel').owlCarousel({
            loop: false,
            margin: 24,
            nav: false,
            dots: true,
            stagePadding: 35,
            responsive: {
                0: {items: 1},
                576: {items: 1},
                768: {items: 2},
                992: {items: 3} // matches your 3 columns on desktop
            }
        });
    }

    function toGrid() {
        if ($row.hasClass('owl-carousel')) {
            // Destroy Owl and unwrap what it added
            $row.trigger('destroy.owl.carousel')
                .removeClass('owl-carousel owl-loaded');
            $row.find('.owl-stage-outer').children().unwrap();
            $row.find('.owl-stage').children().unwrap();
        }
        // Restore original Bootstrap classes
        $row.children().each(function () {
            const $item = $(this);
            const orig = $item.data('grid-classes');
            if (orig) $item.attr('class', orig);
        });
    }

    function toggle() {
        if (typeof $.fn.owlCarousel !== 'function') return; // Owl not loaded
        isEditorOpen() ? toGrid() : toCarousel();
    }

    // 1) On first load
    $(toggle);

    // 2) If the editor is toggled after load, watch <html> classes and react
    const mo = new MutationObserver(toggle);
    mo.observe(document.documentElement, {attributes: true, attributeFilter: ['class']});

})(jQuery);

