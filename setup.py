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
    install_requires=['click==8.0.3', 'loguru==0.5.3', 'pandas==1.4.1', 'python-slugify==6.1.1', 'openpyxl==3.0.9'],
    entry_points='''
        [console_scripts]
        cottage=src.app:main
    ''',
)
