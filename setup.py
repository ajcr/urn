from setuptools import setup, find_packages

from qxy import __version__

long_description = """
...
"""

setup(
    name="qxy",
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
      "Source": "https://github.com/ajcr/qxy/",
      "Tracker": "https://github.com/ajcr/qxy/issues",
    },
    python_requires=">=3.10.0",
    author="Alex Riley",
    license="MIT",
    packages=find_packages(include=["qxy", "qxy.*"]),
    tests_require=["pytest"],
    zip_safe=False,
    entry_points={"console_scripts": ["qxy=qxy.cli:main"]},
)
