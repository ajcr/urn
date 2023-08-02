from setuptools import setup, find_packages

from urn import __version__

long_description = """
...
"""

setup(
    name="urn",
    version=__version__,
    description="Quantity probability calculator",
    long_description=long_description,
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Topic :: Scientific/Engineering :: Mathematics",
      "Topic :: Scientific/Engineering :: Visualization",
      "Topic :: Utilities",
      "Typing :: Typed",
      "Intended Audience :: Science/Research",
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3.11",
    ],
    keywords="calculator probability count draw odds hypergeometric",
    project_urls={
      "Source": "https://github.com/ajcr/urn/",
      "Tracker": "https://github.com/ajcr/urn/issues",
    },
    python_requires=">=3.10.0",
    author="Alex Riley",
    license="MIT",
    packages=find_packages(include=["urn", "urn.*"]),
    tests_require=["pytest"],
    zip_safe=False,
    entry_points={"console_scripts": ["urn=urn.cli:main"]},
)
