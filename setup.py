from setuptools import setup, find_packages


setup(
    name="ChikkarPy",
    description="Python version of Chikkar, a library for using the Sudachi synonym dictionary",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="",
    license="Apache-2.0",
    author="Works Applications",
    packages=find_packages(include=["chikkarpy", "chikkarpy.*"]),
    install_requires=[
        "dartsclone~=0.9.0",
        "sortedcontainers~=2.1.0"
    ]
)