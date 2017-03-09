from setuptools import setup

setup(
    name='cosmos-osm',
    version='0.0.1',
    description='Package for easy OSM data download',
    url='https://github.com/astrosat/cOSMos',
    author='Waldemar Franczak',
    author_email='waldemar.franczak@astrosat.biz',
    packages=['cosmos'],
    install_requires=[
        'requests==2.13.0',
        'geojson==1.3.3',
        'geopy==1.11.0',
        'click==6.7',
        'shapely==1.5.17'
    ],
    entry_points={
        'console_scripts': ['cosmos=cosmos.cli:main']
    },
    license='MIT',
    test_suite='tests'
)
