import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="Launchpad",
    version="1.0.0",
    author="ramadan8",
    author_email="ramadan8@riseup.net",
    description="Interface for Launchpad devices",
    long_description=long_description,
    long_description_type="text/markdown",
    url="https://github.com/ramadan8/Launchpad",
    project_urls={
        "Bug Tracker": "https://github.com/ramadan8/Launchpad/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=["launchpad"]
)
