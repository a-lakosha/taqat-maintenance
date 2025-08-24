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