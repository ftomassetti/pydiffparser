try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Diff files parser for Python',
    'author': 'Federico Tomassetti',
    'url': 'https://github.com/ftomassetti/pydiffparser',
    'author_email': 'Federico Tomassetti',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['pydiffparser'],
    'scripts': [],
    'name': 'pydiffparser',
    'classifiers': [
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha']
}

setup(**config)