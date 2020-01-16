from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rstmarcutree',
    version='1.0.4',
    description='A project to load rst discourse tree enriched with Marcu attribute from .dis files',
    long_description=long_description,
    author='Christian Colonna',
    license='BSD',
    long_description_content_type='text/plain',
    url='https://github.com/Christian-Nja/rstmarcutree',
    author_email='christian.colonna@studio.unibo.it',
    classifiers=[  
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages("src"),
    package_dir = {'': "src"},
    install_requires=['networkx==2.2','discoursegraphs'],
)
