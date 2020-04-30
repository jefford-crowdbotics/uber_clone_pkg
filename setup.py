import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uber-clone-pkg-CROWDBOTICS", # Replace with your own username
    version="0.0.1",
    author="Crowdbotics",
    author_email="dev@crowdbotics.com",
    description="A small custom package for an Uber clone app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crowdbotics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'osmapi',
        'geopy'
    ],
)