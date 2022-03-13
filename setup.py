import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyAMT",
    version="0.0.2",
    author="Roberto Castellotti",
    author_email="me@rcastellotti.dev",
    description="An unofficial wrapper for AMT Genova undocumented API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rcastellotti/pyAMT",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
       "requests",
       "xmltodict",
   ],
)