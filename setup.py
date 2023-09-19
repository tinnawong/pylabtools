import setuptools
import subprocess
import os

cf_remote_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

if "-" in cf_remote_version:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v,i,s = cf_remote_version.split("-")
    cf_remote_version = v + "+" + i + ".git." + s

assert "-" not in cf_remote_version
assert "." in cf_remote_version

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="py_utility",
    version=cf_remote_version,
    author="Tinnawong saelao",
    author_email="tinnawong2010@hotmail.com",
    description="python utility for research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tinnawong/py_utility",
    packages=setuptools.find_packages(),
    package_data={"py_utility": ["VERSION"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires= [
        "minio==7.1.15",
    ],
)