from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ims/__init__.py
from ims import __version__ as version

setup(
	name="ims",
	version=version,
	description="IMS",
	author="SOUL",
	author_email="soul@soul.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
