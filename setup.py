from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name='partnext',
    version=version,
    description='Dataset toolkit for using PartNeXt dataset',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/AuthorityWang/PartNeXt',
    author='AuthorityWang',
    author_email='wangph12025@shanghaitech.edu.cn',
    packages=find_packages()
)