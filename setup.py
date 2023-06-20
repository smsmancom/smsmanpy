from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["aiohttp"]

setup(
    name="smsmanpy",
    version="0.0.2",
    author="Alexandr Lebedchenko",
    author_email="alex_leb@sms-man.com",
    description="A package to simplify work with the sms-man API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/smsmancom/smsmanpy/", #url from smsmangithab
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requiers=">3.6"
)