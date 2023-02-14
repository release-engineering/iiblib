# -*- coding: utf-8 -*-
"""setup.py"""

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [("tox-args=", "a", "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex

        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def read_content(filepath):
    with open(filepath) as fobj:
        return fobj.read()


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]


long_description = read_content("README.md") + read_content(
    os.path.join("docs/source", "CHANGELOG.md")
)

INSTALL_REQUIRES = ["requests", "requests-kerberos", "kerberos", "tenacity"]

extras_require = {"reST": ["Sphinx"]}

if os.environ.get("READTHEDOCS", None):
    extras_require["reST"].append("recommonmark")

setup(
    name="iiblib",
    version="7.0.0",
    description="IIB client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jindrich Luza",
    author_email="jluza@redhat.com",
    url="https://github.com/release-engineering/iiblib",
    classifiers=classifiers,
    python_requires=">=3.6",
    packages=["iiblib"],
    data_files=[],
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    extras_require=extras_require,
    tests_require=["tox", "mock", "requests_mock"],
    cmdclass={"test": Tox},
)
