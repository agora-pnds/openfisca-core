# -*- coding: utf-8 -*-

import sys


TAX_BENEFIT_SYSTEM_OPTIONS = {
    'country_package': {
        'short': 'c',
        'help': 'country package to use. If not provided, an automatic detection will be attempted by scanning the python packages installed in your environment which name contains the word "openfisca".'
        },
    'extensions': {
        'short': 'e',
        'help': 'extensions to load',
        'nargs': '*'
        },
    'reforms': {
        'short': 'r',
        'help': 'reforms to apply to the country package',
        'nargs': '*'
        }
    }


def add_tax_benefit_system_arguments(parser):
    for option, properties in TAX_BENEFIT_SYSTEM_OPTIONS.iteritems():
        parser.add_argument(
            '-{}'.format(properties['short']),
            '--{}'.format(option),
            action = 'store',
            help = properties['help'],
            nargs = properties.get('nargs')
            )

    return parser


def detect_country_package():
    import pkgutil
    from importlib import import_module

    installed_country_packages = []

    for module_description in pkgutil.iter_modules():
        module_name = module_description[1]
        if module_name.lower().find('openfisca') >= 0:
            module = import_module(module_name)
            if hasattr(module, 'CountryTaxBenefitSystem'):
                installed_country_packages.append(module_name)

    if len(installed_country_packages) == 0:
        print('ERROR: No country package has been detected on your environment. If your country package is installed but not detected, please use the --country_package option.')
        sys.exit(1)
    if len(installed_country_packages) > 1:
        print('WARNING: Several country packages detected : `{}`. Using `{}` by default. To use another package, please use the --country_package option.'.format(', '.join(installed_country_packages), installed_country_packages[0]))
    return installed_country_packages[0]
