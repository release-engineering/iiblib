from mock import patch, MagicMock, call

from iiblib.iib_authentication import IIBAuth, IIBBasicAuth, IIBKrbAuth
from iiblib.iib_client import IIBClient


def test_client_auth():
    auth = IIBBasicAuth("foo", "bar")
    iibc = IIBClient("fake-host", auth=auth)
    assert iibc.iib_session.session.headers["auth"] == ("foo", "bar")


def test_iib_basic_auth():
    session = MagicMock()
    session.session.headers = {}
    auth = IIBBasicAuth("foo", "bar")
    auth.make_auth(session)
    assert session.session.headers["auth"] == ("foo", "bar")


@patch("subprocess.Popen")
@patch("kerberos.authGSSClientStep")
@patch("kerberos.authGSSClientResponse")
@patch("kerberos.authGSSClientInit")
def test_iib_krb_auth(
    mocked_auth_gss_client_init,
    mocked_auth_gss_client_response,
    mocked_auth_gss_client_step,
    mocked_popen,
):
    mocked_auth_gss_client_init.return_value = ("", None)
    mocked_auth_gss_client_response.return_value = ""
    session = MagicMock()
    session.session.headers = {}
    auth = IIBKrbAuth("test_principal", "someservice")
    auth.make_auth(session)
    mocked_auth_gss_client_init.assert_called_with("HTTP@someservice")
    mocked_popen.assert_has_calls([call(["klist"], stderr=-1, stdout=-1)])

    auth = IIBKrbAuth("test_principal", "someservice", ktfile="/some/kt/file")
    auth.make_auth(session)
    mocked_auth_gss_client_init.assert_called_with("HTTP@someservice")


@patch("os.unlink")
@patch("tempfile.mkstemp")
@patch("subprocess.Popen.wait")
@patch("subprocess.Popen")
@patch("kerberos.authGSSClientStep")
@patch("kerberos.authGSSClientResponse")
@patch("kerberos.authGSSClientInit")
def test_iib_krb_auth_no_keytab(
    mocked_auth_gss_client_init,
    mocked_auth_gss_client_response,
    mocked_auth_gss_client_step,
    mocked_popen,
    mocked_popen_wait,
    mocked_mkstemp,
    mocked_os_unlink,
):
    mocked_mkstemp.return_value = (None, "/tmp/krb5ccomuHss")
    mocked_popen_wait.side_effect = [1, 0]
    mocked_auth_gss_client_init.return_value = ("", None)
    mocked_auth_gss_client_response.return_value = ""
    session = MagicMock()
    session.session.headers = {}
    auth = IIBKrbAuth("test_principal", "someservice")
    auth.make_auth(session)
    mocked_auth_gss_client_init.assert_called_with("HTTP@someservice")
    mocked_popen.assert_has_calls(
        [
            call(
                ["kinit", "test_principal", "-k", "-c", "/tmp/krb5ccomuHss"],
                stderr=-1,
                stdout=-1,
            )
        ]
    )


def test_iibauth_abstract():
    try:
        IIBAuth()
        raise AssertionError("Should raise NotImplementedError")
    except NotImplementedError:
        pass
