# -*- coding: utf-8 -*-

{
    "name": "Đại lý vé số",
    "description": """""",
    "summary": "",
    "category": "Lottery/Backend",
    "version": "15.0.1.0.1",
    'author': '',
    'company': '',
    'maintainer': '',
    'website': "",
    "depends": ['base'],
    "data": [
        'security/ir.model.access.csv',
        'views/planed.xml',
        'wizard/create_plan.xml',
        'views/customer.xml',
        'views/res_users.xml',
        'wizard/create_customer.xml',
    ],
    'assets': {
        'web.assets_backend': {

        },
        'web.assets_frontend': {

        },
        'web.assets_qweb': {

        },
    },
    'images': [

    ],
    'license': 'LGPL-3',
    # 'pre_init_hook': 'test_pre_init_hook',
    # 'post_init_hook': 'test_post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': True,
}
