
from setuptools import setup, find_packages


setup(
    name='McPacker',
    version="1.0",
    url=None,
    license=None,
    author=None,
    author_email=None,
    description='McPacker',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    long_description="McPacker",
    zip_safe=False,
    entry_points={
        'console_scripts': ['mcpacker = McPacker.cli:execute']
    },
    install_requires=[
        "click",
    ],
    python_requires='>=3.11',
)
