from pathlib import Path

from setuptools import find_packages, setup

BASE_DIR = Path(__file__).parent

# Load packages from requirements.txt
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

test_packages = []

dev_packages = []

docs_packages = []

setup(
    name="ukkomotif",
    version="0.1",
    license="MIT",
    description="Ukkonen suffix tree tools for de novo motif discovery based on genome-wide evolutionary signature.",
    author="Bernardo Penteado",
    author_email="mail@pbern.com",
    url="https://pbern.com",
    keywords=[
        "suffix-tree",
        "motif-discovery",
        "bioinformatics",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires="==3.7.10",
    packages=find_packages(),
    install_requires=[required_packages],
    extras_require={
        "test": test_packages,
        "dev": test_packages + dev_packages + docs_packages,
        "docs": docs_packages,
    },
    entry_points={
        "console_scripts": [
            "ukkomotif = ukkomotif.cli.main:main",
        ],
    },
)