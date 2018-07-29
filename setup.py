from setuptools import setup

setup(
    name='steemconnect',
    version='0.0.3',
    packages=['steemconnect'],
    url='https://github.com/emre/steemconnect',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='Python client library of SteemConnect',
    install_requires=["requests", "responses"]
)