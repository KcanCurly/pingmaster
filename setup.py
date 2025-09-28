from setuptools import setup, find_packages

setup(
    name="pingmaster",
    version="0.0.1",
    description="Ping things",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="kcancurly",
    url="https://github.com/kcancurly/pingmaster",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "scapy",
        "netifaces"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "pm=pingmaster.pingmain:main",
            "pm-analyzer=pingmaster.analyzer:main",
        ],
    },
)
