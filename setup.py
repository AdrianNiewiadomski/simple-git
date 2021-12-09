from setuptools import setup


setup(
	name='simple-git',
	version='0.1.0',
	author='Adrian Niewiadomski',
	packages=['simple_git'],
	package_dir={'simple_git': 'simple_git'},
	package_data={'simple_git': ['help/*.txt']},
	entry_points={
		'console_scripts': [
			'simplegit = simple_git.main:main',
		],
	}
)
