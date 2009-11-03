# -*- coding: utf-8 -*-
"""
This module contains the tool of amnesty.shop
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('amnesty', 'shop', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='amnesty.shop',
      version=version,
      description="A web shop for the amnesty website",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='Thomas Buchberger',
      author_email='t.buchberger@4teamwork.ch',
      url='http://www.4teamwork.ch',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['amnesty', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
#        'Products.ATCountryWidget',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'amnesty.shop.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
            
      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list
      """,
      paster_plugins = ["ZopeSkel"],
      )