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
    'name': 'pydiffparser'
}

setup(**config)