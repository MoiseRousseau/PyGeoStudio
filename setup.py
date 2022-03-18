from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='PyGeoStudio', 
    version='0.1.0',  # Required
    description='Python library allowing reading/writing GeoStudio .gsz files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MoiseRousseau/PyGeoStudio',
    author='Moise Rousseau',  # Optional
    author_email='rousseau.moise@gmail.com', 
    classifiers=[ 
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
    ],
    keywords='topology optimization, mechanics, numerical simulation', 
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=['numpy', 'matplotlib'],
    project_urls={ 
        'Bug Reports': 'https://github.com/MoiseRousseau/PyGeoStudio/issues',
        'Source': 'https://github.com/MoiseRousseau/PyGeoStudio/',
    },
)

