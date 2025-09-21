/** @odoo-module **/

/**
 * Provides a way to start JS code for snippets' initialization and animations.
 */

import publicWidget from "@web/legacy/js/public/public_widget";

import {_t} from "@web/core/l10n/translation";

publicWidget.registry.snippetComponent = publicWidget.Widget.extend({
    disabledInEditableMode: false,
    selector: '.js_snippet_component',

    start: function () {
        let self = this

        let $component = self.$target.find('owl-component')
        if ($component) {
            if (this.editableMode) {
                $component.empty()
            }
        }
    },
})

publicWidget.registry.threeColumnsCarousel = publicWidget.Widget.extend({
    disabledInEditableMode: false,
    selector: 'section.s_three_columns',

    start: function () {
        this.$row = this.$target.find('> .container > .row.d-flex');
        if (!this.$row.length) return;

        this._updateLayout();
        return this._super.apply(this, arguments);
    },

    _updateLayout: function () {
        if (this.editableMode) {
            this._toGrid();
        } else {
            this._toCarousel();
        }
    },

    _toCarousel: function () {
        if (this.$row.hasClass('owl-loaded')) return;

        // Check if Owl Carousel is available
        if (typeof $.fn.owlCarousel !== 'function') {
            console.warn('Owl Carousel not loaded');
            return;
        }

        // Remove grid mode classes
        this.$row.removeClass('grid-mode');

        // Save original grid classes and prepare for carousel
        this.$row.children().each(function () {
            const $col = $(this);
            if (!$col.data('grid-classes')) {
                $col.data('grid-classes', $col.attr('class'));
            }

            // Remove grid-specific classes and unwrap grid-content
            $col.removeClass('grid-item');
            if ($col.find('.grid-content').length) {
                $col.find('.grid-content').children().unwrap();
                $col.find('.grid-content').remove();
            }

            $col.attr('class', 'item');
        });

        // Initialize carousel
        this.$row.addClass('owl-carousel').owlCarousel({
            loop: false,
            margin: 24,
            nav: false,
            dots: true,
            stagePadding: 35,
            responsive: {
                0: {items: 1},
                576: {items: 1},
                768: {items: 2},
                992: {items: 3}
            }
        });

        // Attach navigation handlers
        this._attachNavigation();
    },

    _toGrid: function () {
        if (this.$row.hasClass('owl-carousel')) {
            // Remove navigation handlers
            this._detachNavigation();

            // Destroy carousel
            this.$row.trigger('destroy.owl.carousel')
                .removeClass('owl-carousel owl-loaded');
            this.$row.find('.owl-stage-outer').children().unwrap();
            this.$row.find('.owl-stage').children().unwrap();
        }

        // Apply grid mode classes
        this.$row.addClass('grid-mode');

        // Restore original classes and add grid-specific classes
        this.$row.children().each(function () {
            const $item = $(this);
            const orig = $item.data('grid-classes');
            if (orig) {
                $item.attr('class', orig + ' grid-item');
            } else {
                $item.addClass('grid-item');
            }

            // Wrap content for better styling control
            if (!$item.find('.grid-content').length) {
                $item.wrapInner('<div class="grid-content"></div>');
            }
        });
    },

    _attachNavigation: function () {
        const self = this;
        $('.scroll-left').off('click.threeColumns').on('click.threeColumns', function (e) {
            e.preventDefault();
            self.$row.trigger('prev.owl.carousel');
        });
        $('.scroll-right').off('click.threeColumns').on('click.threeColumns', function (e) {
            e.preventDefault();
            self.$row.trigger('next.owl.carousel');
        });
    },

    _detachNavigation: function () {
        $('.scroll-left, .scroll-right').off('click.threeColumns');
    },

    destroy: function () {
        this._detachNavigation();
        if (this.$row && this.$row.hasClass('owl-carousel')) {
            this.$row.trigger('destroy.owl.carousel');
        }
        this._super.apply(this, arguments);
    }
})