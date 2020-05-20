import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="python_homie4",
    version="1.0.0",
    description="Homie 4.0.0 Implementation",
    author="Michael Cumming, Juuso Korhonen",
    author_email="mike@4831.com, juusokorhonen on github.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juusokorhonen/python_homie4",
    keywords=["HOMIE", "MQTT"],
    packages=setuptools.find_packages(exclude=("tests", "examples", )),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "paho-mqtt>=1.3.0",
        "netifaces>=0.10.6"],
    extras_require={
        'dev': [
            'pycodestyle',
            'flake8',
            'pytest',
            'pytest-flake8',
            'pytest-pycodestyle',
        ]
    }
)
