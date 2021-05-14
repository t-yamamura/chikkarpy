from setuptools import setup, find_packages


setup(
    name="ChikkarPy",
    packages=find_packages(include=["chikkarpy", "chikkarpy.*"]),
    install_requires=[
        "dartsclone~=0.9.0",
        "sortedcontainers~=2.1.0"
    ]
)