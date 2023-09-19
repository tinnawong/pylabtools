import setuptools
import subprocess
import os

remote_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

if "-" in remote_version:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v,i,s = remote_version.split("-")
    remote_version = v + "+" + i + ".git." + s

assert "-" not in remote_version
assert "." in remote_version

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pylabtools",
    version=remote_version,
    author="Tinnawong saelao",
    author_email="tinnawong2010@hotmail.com",
    description="python utility for research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tinnawong/pylabtools",
    packages=setuptools.find_packages(),
    package_data={"pylabtools": ["VERSION"]},
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