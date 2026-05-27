"""
Setup script for py-care.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='py-care',
    version='0.1.0',
    description='A simple desktop app to reduce screen time fatigue',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='py-care',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=[
        'PyYAML>=6.0.1',
        'pystray>=0.19.5',
        'Pillow>=10.0.0',
    ],
    extras_require={
        'windows': ['pywin32>=306'],
    },
    entry_points={
        'console_scripts': [
            'py-care=src.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Desktop Environment',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
    ],
)
