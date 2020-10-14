import os
import kerberos
import subprocess
import tempfile


# pylint: disable=bad-option-value,useless-object-inheritance
class IIBAuth(object):
    def __init__(self):
        raise NotImplementedError

    def make_auth(self, iib_session):  # pragma: no cover
        raise NotImplementedError


class IIBBasicAuth(IIBAuth):
    """Basic Auth provider to IIBClient."""

    # pylint: disable=super-init-not-called
    def __init__(self, user, password):
        """
        Args:
            user (str)
                Basic auth user name
            password (str)
                Basic auth password
        """
        self.user = user
        self.password = password

    def make_auth(self, iib_session):
        """Setup IIBSession with basic auth.

        Args:
            iib_session (IIBSession)
                IIBSession instance
        """

        iib_session.session.headers["auth"] = (self.user, self.password)


class IIBKrbAuth(IIBAuth):
    """Kerberos authentication support for IIBClient"""

    # pylint: disable=super-init-not-called
    def __init__(self, krb_princ, service, ktfile=None):
        """
        Args:
            krb_princ (str)
                Kerberos principal for obtaining ticket
            ktfile (str)
                Kerberos client keytab file
            gssapi_name_type (str)
                GSSAPI name type for creating credentials
        """
        self.krb_princ = krb_princ
        self.ktfile = ktfile
        self.service = service

    def _krb_auth_header(self):
        retcode = subprocess.Popen(
            ["klist"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).wait()
        krb5ccname = None
        if retcode or self.ktfile:
            # can I define old_krb5ccname on the higher level out of if?
            old_krb5ccname = os.environ.get("KRB5CCNAME", "")
            _, krb5ccname = tempfile.mkstemp(prefix="krb5cc")
            if self.ktfile:
                retcode = subprocess.Popen(
                    [
                        "kinit",
                        self.krb_princ,
                        "-k",
                        "-t",
                        self.ktfile,
                        "-c",
                        krb5ccname,
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                ).wait()
            else:
                # If keytab path wasn't provided, default location will be attempted
                retcode = subprocess.Popen(
                    ["kinit", self.krb_princ, "-k", "-c", krb5ccname],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                ).wait()
        try:
            if krb5ccname:
                os.environ["KRB5CCNAME"] = krb5ccname
            __, krb_context = kerberos.authGSSClientInit("HTTP@%s" % self.service)
            kerberos.authGSSClientStep(krb_context, "")
            self._krb_context = krb_context
            auth_header = "Negotiate " + kerberos.authGSSClientResponse(krb_context)
        finally:
            if krb5ccname:
                os.environ["KRB5CCNAME"] = old_krb5ccname
                os.unlink(krb5ccname)

        return auth_header

    def make_auth(self, iib_session):
        """Setup IIBSession with kerberos authentication"""
        iib_session.session.headers["Authorization"] = self._krb_auth_header()
