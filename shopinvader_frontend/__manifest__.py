# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Shopinvader frontend',
    'description': """The frontend side of shopinvader.""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Camptocamp SA',
    'depends': [
        'website',
        'shopinvader_client',
    ],
    'data': [
        'templates/assets.xml',
        'templates/misc.xml',
        'templates/shop_home.xml',
        'templates/layout/layout_default.xml',
        # account
        'templates/account/account.xml',
        'templates/account/account_index.xml',
        'templates/account/account_address.xml',
        'templates/account/account_address_form.xml',
        'templates/account/account_profile.xml',
        'templates/account/account_quotations.xml',
        # cart / index
        'templates/cart/index/cart_index.xml',
        'templates/cart/index/cart.xml',
        'templates/cart/index/block_cart_lines.xml',
        'templates/cart/index/block_cart_login.xml',
        'templates/cart/index/block_cart_summary.xml',
        # cart / address
        'templates/cart/address/cart_address.xml',
        'templates/cart/address/block_cart_address.xml',
        'templates/cart/address/block_cart_address_list.xml',
        'templates/cart/address/address_form.xml',
        # cart / checkout
        'templates/cart/checkout/cart_checkout.xml',
        # cart / payment
        'templates/cart/payment/payment_bank_transfer.xml',
        # product
        'templates/product/product_page.xml',
        'templates/product/product_qty_input.xml',
        'templates/product/block_product_title.xml',
        'templates/product/block_product_add_to_cart.xml',
        # OLD
        # 'views/pages/layouts/account.xml',
        # 'views/pages/layouts/checkout.xml',
        # 'views/pages/account/account_index.xml',
        # 'views/pages/account/account_quotations.xml',
        # 'views/pages/account/account_profile.xml',
        # 'views/pages/account/account_address.xml',
        # 'views/pages/account/account_address_form.xml',
        # 'views/pages/cart.xml',
        # 'views/pages/product.xml',
        # 'views/pages/templates/product.xml',
        # 'views/sections/cart.xml',
        # 'views/snippets/address_form.xml',
        # 'views/snippets/block_product_add_to_cart.xml',
        # 'views/snippets/block_product_title.xml',
        # 'views/snippets/product_qty_input.xml',
        # 'data/pages/shop.xml',
        # 'templates/layout/assets.xml',
        # 'templates/layout/search.xml',
        # 'views/pages/cart.xml',
        # 'views/pages/product.xml',
        # 'views/pages/layouts/default.xml',
        # 'views/sections/cart.xml',
        # 'views/pages/templates/product.xml',
        # 'views/snippets/block_cart_lines.xml',
        # 'views/snippets/block_cart_summary.xml',
        # 'views/snippets/block_product_add_to_cart.xml',
        # 'views/snippets/block_product_title.xml',
        # 'views/snippets/product_qty_input.xml',
    ],
}
