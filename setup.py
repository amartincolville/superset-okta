#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = []

test_requirements = [ ]

setup(
    author="Alex Martin Colville",
    author_email='a.martincolville@stuart.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Okta integration as provider for authentication in Superset",
    entry_points={
        'console_scripts': [
            'superset_okta=superset_okta.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='superset_okta',
    name='superset_okta',
    packages=find_packages(include=['superset_okta', 'superset_okta.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/amartincolville/superset_okta',
    version='0.1.0',
    zip_safe=False,
)
