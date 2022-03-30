from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="cottage",
    version="0.0.1",
    author="Kirill Podkov",
    author_email="kirill.podkov@outlook.com",
    description="Cottage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kpodkov/cottage",
    packages=find_packages(),
    install_requires=['click', 'tenacity', 'pandas'],
    entry_points='''
        [console_scripts]
        cottage=src.app:main
    ''',
)
