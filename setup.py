#!/usr/bin/env python3
from setuptools import setup

setup(
	name = 'mindustryd',
	version = '0.0.1',
	packages = ['mindustryd'],
	entry_points = {
		'console_scripts': [
			'mindustryd = mindustryd.__main__:main'
		]
	})
