import setuptools
import subprocess
import os

remote_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

if remote_version.startswith("v"):
    if "-" in remote_version:
        v,i,s = remote_version.split("-")
        remote_version = v + "+" + i + ".git." + s

    assert "-" not in remote_version
    assert "." in remote_version

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="py_utility",
    version=remote_version,
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
        "tqdm==4.64.1"
    ],
)