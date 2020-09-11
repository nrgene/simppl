from setuptools import setup, find_packages

setup(
    name="simppl",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/nrgene/simppl",
    description="simple commands execution pipeline, coupled with command-line-interface support",
    install_requires=[
        'colorama',
        'pytest'
    ],
)
