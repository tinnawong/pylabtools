import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="py_utility",
    version="2.0.0",
    author="Tinnawong saelao",
    author_email="tinnawong2010@hotmail.com",
    description="python utility for research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires= [],
)
