from setuptools import setup, find_packages

setup(
    name="simppl",
    author='Doron Shem-Tov',
    author_email='doronst5@gmail.com',
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/nrgene/simppl",
    description="simple commands execution pipeline, coupled with unified command-line-interface entry-point",
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
