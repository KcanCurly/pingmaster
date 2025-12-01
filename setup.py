from setuptools import setup, find_packages

setup(
    name="pingmaster",
    version="1.0.0",
    description="Ping protocols to test firewall rules",
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
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "pm=pingmaster.pingmain:main",
            "pm-analyzer=pingmaster.analyzer:main",
            "pm-client=pingmaster.client:main",
            "pm-server=pingmaster.server:main",
        ],
    },
)
