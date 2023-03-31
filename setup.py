import cryptpandas as crp
from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = [x for x in f.read().splitlines() if "#" not in x]


setup(
    name="CryptPandas",
    version=crp.__version__,
    author=crp.__author__,
    author_email=crp.__email__,
    description=crp.__about__,
    url=crp.__url__,
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude="tests"),
    install_requires=requirements,
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"],
    python_requires=">=3.6",
)
