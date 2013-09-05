# -*- coding: utf-8 -*-
"""
This module contains the tool of ftw.shop
"""
import os
from setuptools import setup, find_packages

version = '1.3.1.dev0'

tests_require = ['zope.testing',
                 'Products.PloneTestCase',
                 'pyquery<=0.6.1',
                ]

setup(name='ftw.shop',
      version=version,
      description="A web shop solution for Plone",
      long_description=open("README.rst").read() + "\n" + \
                       open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw shop plone',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.shop',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'plone.app.z3cform',
        'collective.z3cform.wizard',
        'plone.app.registry',
        'simplejson',
        'collective.js.jqueryui',
#        'Products.ATCountryWidget',
      ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'ftw.shop.tests.test_docs.test_suite',

      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
