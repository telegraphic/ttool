from setuptools import setup, find_packages

__version__ = "0.1.0"

install_requires = [
    'astropy',
    'tzwhere',
    'pytz',
    'tzlocal',
    'pyephem',
    'dateparser'
]

entry_points = {
    'console_scripts' :
        ['ttool = ttool.ttool:main']
}

setup(
    name="ttool",
    version=__version__,
    packages=find_packages(),
    install_requires=install_requires,
    entry_points=entry_points,
    author="Danny Price",
    author_email="dancpr [at] berkeley [dot] edu",
    description="Timezone conversion tool for astronomers",
    license="MIT License",
    keywords="astronomy, timezone, lst, sidereal time",
    url="https://github.com/telegraphic/ttool"
)