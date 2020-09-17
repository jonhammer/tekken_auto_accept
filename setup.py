#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from glob import glob
from os.path import basename, splitext

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r") as fs:
    requirements = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]

setup(
    name='tekken_auto_accept',
    version='0.1.0',
    description="Auto accepts ranked matches in Tekken",
    long_description=readme,
    author="Jonathan Hammer",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    entry_points={
        'console_scripts': [
            'tekken_auto_accept = tekken_auto_accept.cli:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='tekken_auto_accept',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
)
