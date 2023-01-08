from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="simppl",
    author='NRGene',
    author_email='open-source@nrgene.com',
    version="1.0.7",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/nrgene/simppl",
    description="simple commands execution pipeline, coupled with unified command-line-interface entry-point",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'colorama',
        'pytest'
    ],
    python_requires='>3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
