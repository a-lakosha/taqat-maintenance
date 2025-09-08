/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.addressForm = publicWidget.Widget.extend({
    selector: '.s_website_form',
    disabledInEditableMode: false,
    events: {
        'change select[name="country_id"]': '_onCountryChange',
        'change select[name="state_id"]': '_onStateChange',
        'change select[name="city_id"]': '_onCityChange',
    },
    _onCountryChange: function (ev) {
        ev.preventDefault();
        let self = this;
        let CurrentTarget = self.$(ev.currentTarget);
        let states_selector = $('select[name="state_id"]') || false
        let cities_selector = $('select[name="city_id"]') || false
        let districts_selector = $('select[name="district_id"]') || false
        if (states_selector) {
            let states = states_selector.find('option')
            if (CurrentTarget.val() === '') {
                states.each(function () {
                    if ($(this).val() === '') {
                        states_selector.val(states_selector.find("option:first").val());
                    } else {
                        $(this).hide()
                    }
                })
                if (cities_selector) {
                    let cities = cities_selector.find('option')
                    cities.each(function () {
                        if ($(this).val() === '') {
                            cities_selector.val(cities_selector.find("option:first").val());
                        } else {
                            $(this).hide()
                        }
                    })
                }
                if (districts_selector) {
                    let districts = districts_selector.find('option')
                    districts.each(function () {
                        if ($(this).val() === '') {
                            districts_selector.val(districts_selector.find("option:first").val());
                        } else {
                            $(this).hide()
                        }
                    })
                }
            } else {
                states_selector.val(states_selector.find("option:first").val());
                let countryID = +CurrentTarget.val()
                states.each(function () {
                    if ($(this).data('state-id') === countryID || $(this).val() === '') {
                        $(this).show()
                    } else {
                        $(this).hide()
                    }
                })
            }
        }
    },
    _onStateChange: function (ev) {
        let self = this;
        let CurrentTarget = self.$(ev.currentTarget);
        let cities_selector = $('select[name="city_id"]') || false
        let districts_selector = $('select[name="district_id"]') || false
        if (cities_selector) {
            let cities = cities_selector.find('option')
            if (CurrentTarget.val() === '') {
                cities_selector.prop("disabled", true)
                cities.each(function () {
                    if ($(this).val() === '') {
                        cities_selector.val(cities_selector.find("option:first").val());
                    } else {
                        $(this).hide()
                    }
                })
                if (districts_selector) {
                    let districts = districts_selector.find('option')
                    districts.each(function () {
                        if ($(this).val() === '') {
                            districts_selector.val(districts_selector.find("option:first").val());
                        } else {
                            $(this).hide()
                        }
                    })
                }
            } else {
                cities_selector.removeAttr("disabled").val(cities_selector.find("option:first").val());
                let stateID = +CurrentTarget.val()
                cities.each(function () {
                    if ($(this).data('state-id') === stateID || $(this).val() === '') {
                        $(this).show()
                    } else {
                        $(this).hide()
                    }
                })
            }
        }
    },
    _onCityChange: function (ev) {
        let self = this;
        let CurrentTarget = self.$(ev.currentTarget);
        let districts_selector = $('select[name="district_id"]') || false
        if (districts_selector) {
            let districts = districts_selector.find('option')
            if (CurrentTarget.val() === '') {
                districts.each(function () {
                    if ($(this).val() === '') {
                        districts_selector.val(districts_selector.find("option:first").val());
                    } else {
                        $(this).hide()
                    }
                })
            } else {
                districts_selector.val(districts_selector.find("option:first").val());
                let cityID = +CurrentTarget.val()
                districts.each(function () {
                    if ($(this).data('city-id') === cityID || $(this).val() === '') {
                        $(this).show()
                    } else {
                        $(this).hide()
                    }
                })
            }
        }
    },
});