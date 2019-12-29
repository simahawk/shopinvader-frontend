/* Getting a first rough shopinvader working based on the demo
 * Here are all the config that seem to be needed 
 *
 * Yes in the global js object !?
 */
// TODO: all this stuff should come from backend settings
var default_role = 'default';

// this should be move to algolia specific module
var algolia_params = {
    'api_key': "75575d3910b3ac55428bcdfa1b0e6784",
    "app_id": "GH41KF783Z",
    "categories_index": "demo_site_10_category_en_US",
    "products_index": "demo_site_10_product_en_US",
    "translations": {
        'clear_all' : "Clear All",
        'filter_current' : "Current filters",
        'filter_other_item': "filter_other_item",
        'result_number': 'Resultat(s)',
        'per_page' : "per page",
        'price':  "Price",
        'result_empty': "no result !",
    },
};

var currencies = {
    'items': {
        'CHF': { "default_locale": "fr-CH", "rate": 1 },
        'EUR': { "default_locale": "fr-FR", "rate": 0.9},
    },
    'selected':"CHF",
};
