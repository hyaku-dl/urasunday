from setuptools import find_packages, setup

setup(
    name="urasunday",
    author="whinee",
    author_email="whinyaan@pm.me",
    version='0.0.0.0-alpha.3',
    description='A Basic Urasunday Scraper',
    long_description='''A no-nonsense, simple and easy to use scraper for <a target="_blank" href="https://urasunday.com">urasunday</a>.
    For full information, visit https://ura.hyaku.download''',
    long_description_content_type="text/markdown",
    url="https://github.com/hyaku-dl/urasunday",
    project_urls={
        'Documentation': 'https://ura.hyaku.download',
        'Source': 'https://github.com/hyaku-dl/urasunday',
        'Tracker': 'https://github.com/hyaku-dl/urasunday/issues',
    },
    license="MIT",
    keywords='python windows macos linux cli scraper downloader manga python3 urasunday',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=['rich', 'aiofiles', 'arrow', 'bs4', 'click', 'httpx', 'inquirer', 'lxml', 'msgpack', 'patool', 'pyyaml', 'tabulate', 'toml', 'tqdm', 'yachalk', 'yarl'],
    entry_points = {
        'console_scripts': ['ura=ura.cli:cli'],
    },
)