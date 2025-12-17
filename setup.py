# 
# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# [... Full text of the GNU General Public License v3.0 goes here ...]

# Copyright (C) 2025 Kris Kirby


from setuptools import setup, find_packages
import os

# Utility function to read the README file for long description
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pyhpfec',
    version='1.0.0',
    description='High-Performance Forward Error Correction (FEC) library with Numba optimization.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='[Your Name/Company Name]', # Replace with your actual name/entity
    author_email='[Your Email]',       # Replace with your actual email
    url='[Your Project Repository URL]', # Replace with the actual URL
    
    # Automatically find all packages in the 'pyhpfec' directory
    packages=find_packages(include=['pyhpfec', 'pyhpfec.*']), 
    
    # Define dependencies. Numba is critical.
    install_requires=[
        'numpy>=1.20.0',
        'numba>=0.55.0',
        # Set other dependencies if needed (e.g., 'scipy')
    ],
    
    # Include non-Python files (like the man page)
    # The 'share' directory is a common place for documentation on Unix-like systems.
    data_files=[
        ('man/man3', ['man/pyhpfec.3']),
        ('.', ['LICENSE', 'README.md'])
    ],
    
    # Keywords related to the project
    keywords=[
        'fec', 'error-correction', 'bch', 'ldpc', 'turbo', 'polar', 'numba', 
        'high-performance', 'coding-theory', 'galois-field'
    ],
    
    # Classifiers help users find your project on PyPI
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.8',
)

