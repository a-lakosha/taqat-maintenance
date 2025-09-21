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
// (function ($) {
//     const $section = $('section.s_three_columns');
//     if (!$section.length) return;
//
//     const $row = $section.find('> .container > .row.d-flex');
//     if (!$row.length) return;
//
//     // Heuristic to detect Odoo editor
//     function isEditorOpen() {
//         return (
//             window.location.search.includes('enable_editor=1') ||
//             document.documentElement.classList.contains('o_web_editor') ||
//             document.querySelector('.o_we_toolbar, .o_we_website_top_actions') !== null
//         );
//     }
//
//     function toCarousel() {
//         if ($row.hasClass('owl-loaded')) return; // already initialized
//
//         // Save original grid classes and strip them so Owl can size items
//         $row.children().each(function () {
//             const $col = $(this);
//             if (!$col.data('grid-classes')) {
//                 $col.data('grid-classes', $col.attr('class')); // e.g., "col-lg-4 ... pt16 pb16"
//             }
//             $col.attr('class', 'item'); // let Owl own the width
//
//             // Attach custom nav buttons
//             $('.scroll-left').off('click').on('click', function () {
//                 $row.trigger('prev.owl.carousel');
//             });
//             $('.scroll-right').off('click').on('click', function () {
//                 $row.trigger('next.owl.carousel');
//             });
//
//         });
//
//         $row.addClass('owl-carousel').owlCarousel({
//             loop: false,
//             margin: 24,
//             nav: false,
//             dots: true,
//             stagePadding: 35,
//             responsive: {
//                 0: {items: 1},
//                 576: {items: 1},
//                 768: {items: 2},
//                 992: {items: 3} // matches your 3 columns on desktop
//             }
//         });
//     }
//
//     function toGrid() {
//         if ($row.hasClass('owl-carousel')) {
//             // Destroy Owl and unwrap what it added
//             $row.trigger('destroy.owl.carousel')
//                 .removeClass('owl-carousel owl-loaded');
//             $row.find('.owl-stage-outer').children().unwrap();
//             $row.find('.owl-stage').children().unwrap();
//         }
//         // Restore original Bootstrap classes
//         $row.children().each(function () {
//             const $item = $(this);
//             const orig = $item.data('grid-classes');
//             if (orig) $item.attr('class', orig);
//         });
//     }
//
//     function toggle() {
//         if (typeof $.fn.owlCarousel !== 'function') return; // Owl not loaded
//         isEditorOpen() ? toGrid() : toCarousel();
//     }
//
//     // 1) On first load
//     $(toggle);
//
//     // 2) If the editor is toggled after load, watch <html> classes and react
//     const mo = new MutationObserver(toggle);
//     mo.observe(document.documentElement, {attributes: true, attributeFilter: ['class']});
//
// })(jQuery);

(function ($) {
    const $section = $('section.s_three_columns');
    if (!$section.length) return;

    const $row = $section.find('> .container > .row.d-flex').first();
    if (!$row.length) return;

    // Create a non-editable proxy after the grid
    let $proxy = $('<div class="owl-proxy o_not_editable"></div>').insertAfter($row);
    let owlInited = false;

    // Detect if the Odoo editor is open
    function isEditorOpen() {
        return (
            window.location.search.includes('enable_editor=1') ||
            document.documentElement.classList.contains('o_web_editor') ||
            document.querySelector('.o_we_toolbar, .o_we_website_top_actions') !== null
        );
    }

    // Build proxy content from the grid (clone cards, keep all styles)
    function buildProxyFromGrid() {
        $proxy.empty();
        $row.children().each(function () {
            const $clone = $(this).clone(true, true);
            // Owl wants direct .item children; wrap each card in .item
            const $item = $('<div class="item"></div>').append($clone);
            $proxy.append($item);
        });
    }

    function initOwl() {
        if (owlInited) return;
        buildProxyFromGrid();

        // Use your existing nav buttons if you have them:
        //   .scroll-left  and  .scroll-right
        $proxy.addClass('owl-carousel').owlCarousel({
            loop: false,
            margin: 24,
            nav: false,
            dots: true,
            stagePadding: 35,
            responsive: {
                0: {items: 1},
                576: {items: 1},
                768: {items: 2},
                992: {items: 3} // keep your desktop 3 cols
            }
        });

        // Hook custom nav to this proxy only
        $('.scroll-left').off('click.owlProxy').on('click.owlProxy', function () {
            $proxy.trigger('prev.owl.carousel');
        });
        $('.scroll-right').off('click.owlProxy').on('click.owlProxy', function () {
            $proxy.trigger('next.owl.carousel');
        });

        // Show proxy, hide original grid
        $row.addClass('d-none');
        $proxy.removeClass('d-none');

        owlInited = true;
    }

    function destroyOwl() {
        if (!owlInited) return;

        try {
            $proxy.trigger('destroy.owl.carousel')
                .removeClass('owl-carousel owl-loaded');
            $proxy.find('.owl-stage-outer').children().unwrap();
            $proxy.find('.owl-stage').children().unwrap();
        } catch (e) {
            // ignore if already torn down by editor
        }
        $proxy.empty(); // drop cloned nodes

        // Show original grid
        $row.removeClass('d-none');
        $proxy.addClass('d-none');

        // Unbind custom nav
        $('.scroll-left').off('click.owlProxy');
        $('.scroll-right').off('click.owlProxy');

        owlInited = false;
    }

    // Toggle based on editor state
    function toggle() {
        if (typeof $.fn.owlCarousel !== 'function') return;
        if (isEditorOpen()) {
            destroyOwl();
        } else {
            initOwl();
        }
    }

    // 1) On first load
    $(toggle);

    // 2) React to editor open/close by watching <html> class changes
    const mo = new MutationObserver(toggle);
    mo.observe(document.documentElement, {attributes: true, attributeFilter: ['class']});

    // 3) Extra safety: when content inside the grid changes in editor, ensure Owl is destroyed
    const rowObserver = new MutationObserver(() => {
        if (isEditorOpen()) destroyOwl();
    });
    rowObserver.observe($row.get(0), {childList: true, subtree: true});

})(jQuery);


$(document).ready(function () {
    // Blog carousel (existing)
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

    $(".scroll-left").click(function () {
        $(".blog-carousel").trigger("prev.owl.carousel");
    });

    $(".scroll-right").click(function () {
        $(".blog-carousel").trigger("next.owl.carousel");
    });

    // Testimonials carousel (new)
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



