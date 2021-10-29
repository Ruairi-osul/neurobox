from setuptools import setup, find_packages

with open("requirements.txt") as f:
    reqs = f.read().splitlines()

with open("README.md", "r") as fh:
    long_discription = fh.read()

description = "Analysis framework for systems neuroscience data."
setup(
    name="neurobox",
    description=description,
    long_discription=long_discription,
    long_discription_content_type="text/markdown",
    version="0.0.1",
    url="https://github.com/Ruairi-osul/neurobox",
    author="Ruairi O'Sullivan",
    author_email="ruairi.osullivan.work@gmail.com",
    include_package_data=True,
    license="GNU GPLv3",
    keywords="data-analysis neuroscience systems-neuroscience",
    project_urls={"Source": "https://github.com/Ruairi-osul/neurobox"},
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=reqs,
)
