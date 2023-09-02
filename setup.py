import setuptools
import os

setuptools.setup(
    name="Sonarr-AnimeDownloader",
    version=os.getenv('VERSION'),
    author="MainKronos",
    url="https://github.com/MainKronos/Sonarr-AnimeDownloader",
    packages=setuptools.find_packages(),
)