from setuptools import find_packages
from setuptools import setup

import os


long_description = (
    open("README.txt").read() + "\n" +
    open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
    open(os.path.join("docs", "HISTORY.txt")).read() + "\n" +
    open(os.path.join("docs", "CONTRIBUTORS.txt")).read() + "\n" +
    open(os.path.join("docs", "CREDITS.txt")).read()
)

setup(
    name='collective.cart.shipping',
    version='0.4',
    description="Adds Shipping Methods to collective.cart.core.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",        
        "Programming Language :: Python",
    ],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='https://github.com/taito/collective.cart.shipping',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.cart'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.cart.core',
        'hexagonit.testing',
        'pycountry',
        'setuptools',
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
