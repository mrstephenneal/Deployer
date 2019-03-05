from setuptools import setup, find_packages

setup(
    name='DeployPyPi',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[
        'twine>=1.12.1',
        'PySimpleGUI>=3.9.0',
        'awscli>=1.16.117'
    ],
    url='https://github.com/mrstephenneal/PyPiDistributor',
    entry_points={
        'console_scripts': [
            'deploypipy = DeployPyPi.deploy:main'
        ]
    },
    license='',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Utility for distributing packages to DeployPyPi'
)
