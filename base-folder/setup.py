from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A basic inventory manager package'

# Setting up
setup(
    name="inventory_manager",
    version=VERSION,
    author="Markintosh (Mark Cedrick De Vera)",
    author_email="<devera.markcedrick@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'inventory', 'manager'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)