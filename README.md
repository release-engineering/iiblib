iiblib
======

IIB lib is python IIB client library that allows user to operate with IIB service



Requirements
------------

* Python 3.7 over

Setup
-----


    # pip install -r requirements.txt
    $ python -m pip install --user iiblib
    or
    (venv)$ python -m pip install iiblib

Usage
-----

Basic usage of IIBClient from iiblib is following

    $ python
    >>> from iiblib.iib_client import IIBClient
    >>> from iiblib.iib_authentication import IIBKrbAuth
    >>> krbauth = IIBKrbAuth()
    >>> iibc = IIBClient('iib-host', auth=krbauth)
    >>> build = iibc.add_bundles('index_image', 'binary_image', ['bundle1','bundle2'], ['amd64'])
    >>> iibc.wait_for_build(build)
    >>>
    >>> iibc.remove_operators('index_image', 'binary_image', ['operator1'], ['amd64'])

