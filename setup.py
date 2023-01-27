# coding: utf-8

"""
    Defect Dojo Api Example
"""


from setuptools import setup, find_packages

NAME = "djconnection"
VERSION = "0.0.2"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["defectdojo-api-v2-client @ git+https://github.com/Retrospected/defectdojo-api-v2-client.git#egg=defectdojo-api-v2-client"]

setup(
    name=NAME,
    version=VERSION,
    description="Defect Dojo API Implementation",
    author="Retrospected",
    url="https://github.com/Retrospected/djconnection",
    keywords=["Defect Dojo API Implementation"],
    packages=find_packages(exclude=["test"]),
    install_requires=REQUIRES,
    include_package_data=True,
    long_description="""\
    Easy implementation of a flow using the Defect Dojo API
    """
)
