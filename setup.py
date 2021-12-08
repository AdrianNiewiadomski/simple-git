from setuptools import setup
from setuptools import find_packages


setup(
	name='simple-git',
	version='0.1.0',
	author='Adrian Niewiadomski',
	packages=find_packages(exclude=('tests*',)),
	entry_points={
		'console_scripts': [
			'simplegit = simple_git.main:main',
		],
	}
)
