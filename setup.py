from pathlib import Path

from setuptools import find_packages, setup

test_packages = [
    "pytest==7.1.2",
    "pytest-cov==3.0.0"
]

dev_packages = []

docs_packages = []

setup(
    name="ukkomotif",
    version="1.0",
    license="MIT",
    description="Genomic motif discovery based on Ukkonen's suffix tree implementation.",
    author="Bernardo Penteado",
    author_email="mail@pbern.com",
    url="https://pbern.com",
    keywords=[
        "suffix-tree",
        "motif-discovery",
        "bioinformatics",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">3.7",
    packages=find_packages(),
    install_requires=[
        "click>=7.0"
    ],
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