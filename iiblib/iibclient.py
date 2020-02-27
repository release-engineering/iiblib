import time

import gssapi
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_gssapi import HTTPSPNEGOAuth


# pylint: disable=bad-option-value,useless-object-inheritance
class IIBAuth(object):
    def __init__(self):
        raise NotImplementedError

    def make_auth(self, iib_session):  # pragma: no cover
        raise NotImplementedError


class IIBBuildDetailsModel(object):
    """Model class handling data about index build task"""

    def __init__(
        self,
        _id,
        state,
        reason,
        state_history,
        from_index,
        from_index_resolved,
        bundles,
        removed_operators,
        organization,
        binary_image,
        binary_image_resolved,
        index_image,
        request_type,
        arches,
        bundle_mapping,
    ):
        """
        Args:
            _id (int)
                Id of build
            state (str)
                State of build
            state (str)
                Reason for state change
            from_index (str)
                Reference of index image used as source for rebuild
            from_index_resolved (str)
                Reference of new index image
            bundles (list)
                List of bundles to be added to index image
            removed_operators (list)
                List of operators to be removed from index image
            organization (str)
                Name of organization to push to in the legacy app registry
            binary_image (str)
                Reference of binary image used for rebuilding
            binary_image_resolved (str)
                Checksum reference of binary image that was used for rebuilding
            index_image (str)
                Reference of index image to rebuild
            request_type (str)
                Type of iib build task (add or remove)
            arches (list)
                List of architectures supported in new index image
            bundle_mapping (dict)
                Operator names in "bundles" map to: list of "bundles" which
                map to the operator key
        """
        self.id = _id
        self.state = state
        self.reason = reason
        self.state_history = state_history
        self.from_index = from_index
        self.from_index_resolved = from_index_resolved
        self.bundles = bundles
        self.removed_operators = removed_operators
        self.organization = organization
        self.binary_image = binary_image
        self.binary_image_resolved = binary_image_resolved
        self.index_image = index_image
        self.request_type = request_type
        self.arches = arches
        self.bundle_mapping = bundle_mapping

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["state"],
            data["state_reason"],
            data["state_history"],
            data["from_index"],
            data["from_index_resolved"],
            data.get("bundles", []),
            data.get("removed_operators", []),
            data.get("organization"),
            data["binary_image"],
            data["binary_image_resolved"],
            data["index_image"],
            data["request_type"],
            data["arches"],
            data["bundle_mapping"],
        )

    def __eq__(self, other):
        if (
            self.id == other.id
            and self.state == other.state
            and self.reason == other.reason
            and self.state_history == other.state_history
            and self.from_index == other.from_index
            and self.from_index_resolved == other.from_index_resolved
            and self.bundles == other.bundles
            and self.removed_operators == other.removed_operators
            and self.organization == other.organization
            and self.binary_image == other.binary_image
            and self.binary_image_resolved == other.binary_image_resolved
            and self.index_image == other.index_image
            and self.request_type == other.request_type
            and self.arches == other.arches
            and self.bundle_mapping == other.bundle_mapping
        ):
            return True
        return False


class IIBBuildDetailsPager(object):
    def __init__(self, iibclient, page):
        """
        Args:
            iibclient (IIBClient)
                IIBClient instance
            page (int)
                page where start listing items
        """
        self.page = page
        self.iibclient = iibclient
        self._items = []
        self.meta = {}

    def reload_page(self):
        """Reload items for current page"""

        ret = self.iibclient.get_builds(self.page, raw=True)
        self.meta = ret["meta"]
        self._items = [IIBBuildDetailsModel.from_dict(x) for x in ret["items"]]

    def next(self):
        """Load items for next page and set it as current"""

        self.page += 1
        self.reload_page()

    def prev(self):
        """Load items for previous page and set it as current"""

        if self.page > 1:
            self.page -= 1
        self.reload_page()

    def items(self):
        """Return items for current page"""
        return self._items

    @classmethod
    def from_dict(cls, iibclient, _dict):
        ret = cls(iibclient, _dict["meta"]["page"])
        ret.meta = _dict["meta"]
        ret._items = [IIBBuildDetailsModel.from_dict(x) for x in _dict["items"]]
        return ret

    def __eq__(self, other):
        return (
            self._items == other._items
            and self.iibclient == other.iibclient
            and self.meta == other.meta
        )


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
    def __init__(self, krb_name, ktfile=None, gssapi_name_type=gssapi.NameType.user):
        """
        Args:
            krb_name (str)
                Kerberos name for obtaining ticket
            ktfile (str)
                Kerberos client keytab file
            gssapi_name_type (str)
                GSSAPI name type for creating credentials
        """
        self.krb_name = krb_name
        self.ktfile = ktfile
        self.gssapi_name_type = gssapi_name_type

    def _krb_auth_header(self):
        name = gssapi.Name(base=self.krb_name, name_type=self.gssapi_name_type)
        store = None
        if self.ktfile:
            store = {"client_keytab": "FILE:%s" % self.ktfile}

        creds = gssapi.Credentials.acquire(name, usage="initiate", store=store)

        gssapi_auth = HTTPSPNEGOAuth(creds=creds)
        return gssapi_auth

    def make_auth(self, iib_session):
        """Setup IIBSession with kerberos authentication"""
        iib_session.session.auth = self._krb_auth_header()


# pylint: disable=bad-option-value,useless-object-inheritance
class IIBSession(object):
    """Helper class to support iib requests and authentication"""

    def __init__(self, hostname, retries=3, verify=True):
        """
        Args:
            hostname (str)
                hostname of IIB service
            retries (int)
                Number of http retries
        """
        self.session = requests.Session()
        self.hostname = hostname
        self.verify = verify

        retry = Retry(
            total=retries, read=retries, connect=retries, status_forcelist=[500]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, endpoint, **kwargs):
        """HTTP get request against ibb server API

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return self.session.get(self._api_url(endpoint), verify=self.verify, **kwargs)

    def post(self, endpoint, **kwargs):
        """HTTP post request against ibb server API

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return self.session.post(self._api_url(endpoint), verify=self.verify, **kwargs)

    def put(self, endpoint, **kwargs):
        """HTTP put request against ibb server API

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return self.session.put(self._api_url(endpoint), verify=self.verify, **kwargs)

    def delete(self, endpoint, **kwargs):
        """HTTP delete request against ibb server API

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return self.session.delete(
            self._api_url(endpoint), verify=self.verify, **kwargs
        )

    def _api_url(self, endpoint):
        """Kerberos authentication support for IIBClient

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return "https://%s/api/v1/%s" % (self.hostname, endpoint)


# pylint: disable=bad-option-value,useless-object-inheritance
class IIBClient(object):
    """IIB requests wrapper"""

    def __init__(
        self, hostname, retries=3, auth=None, poll_interval=30, ssl_verify=True
    ):
        """
        Args:
            hostname (str)
                IIB service hostname
            retries (int)
                number of http retries for IIB requests
            auth (IIBAuth)
                IIBAuth subclass instance
            poll_interval (int)
                number of seconds to wait before fetching new status of task in wait_for_task
        """
        self.iib_session = IIBSession(hostname, retries=retries, verify=ssl_verify)
        self.poll_interval = poll_interval
        if auth:
            auth.make_auth(self.iib_session)

    def add_bundles(
        self,
        index_image,
        binary_image,
        bundles,
        arches,
        cnr_token=None,
        organization=None,
        raw=False,
    ):
        """Rebuild index image with new bundles to be added.

        Args:
            index_image (str)
                Index image ref used as source to rebuild
            binary_image (str)
                Image with binary used to rebuild existing index image
            bundles (list)
                List of references to bundle images to be added to index image
            arches (list)
                List of architectures supported in new index image
            cnr_token (srt)
                optional. CNR token.
            organization (str)
                optional. Name of the organization in the legacy app registry.
            raw (bool)
                Return raw json response instead of model instance

        Returns:
            IIBBuildDetailsModel or dict
              if raw == True return dict with json response otherwise
              return IIBBuildDetailsModel instance.
        """

        resp = self.iib_session.post(
            "builds/add",
            json={
                "from_index": index_image,
                "binary_image": binary_image,
                "bundles": bundles,
                "add_arches": arches,
                "cnr_token": cnr_token,
                "organization": organization,
            },
        )
        resp.raise_for_status()
        if raw:
            return resp.json()
        return IIBBuildDetailsModel.from_dict(resp.json())

    def remove_operators(
        self, index_image, binary_image, operators, arches, raw=False,
    ):
        """Rebuild index image with existing operators to be removed.

        Args:
            index_image (str)
                Index image ref used as source to rebuild
            binary_image (str)
                Image with binary used to rebuild existing index image
            operators (list)
                List of operators to be removed from existing index image
            arches (list)
                List of architectures supported in new index image
            raw (bool)
                Return raw json response instead of model instance

        Returns:
            IIBBuildDetailsModel or dict
              if raw == True return dict with json response otherwise
              return IIBBuildDetailsModel instance.
        """

        resp = self.iib_session.post(
            "builds/rm",
            json={
                "from_index": index_image,
                "binary_image": binary_image,
                "operators": operators,
                "add_arches": arches,
            },
        )
        resp.raise_for_status()
        if raw:
            return resp.json()
        return IIBBuildDetailsModel.from_dict(resp.json())

    def get_builds(self, page=1, raw=False):
        """Get all historical builds of index image.

        Args:
            page (int)
                Offset page to start listing results
            raw (bool)
                Return raw json response instead of model instance

        Returns:
            IIBBuildDetailsPager or dict
              if raw == True return dict with json response otherwise
              return IIBBuildDetailsPager instance.
        """

        resp = self.iib_session.get("builds", params={"page": page})
        resp.raise_for_status()
        if raw:
            return resp.json()
        return IIBBuildDetailsPager.from_dict(self, resp.json())

    def get_build(self, bid, raw=False):
        """Get specific index image build

        Args:
            bid (int)
                Build id of requested build
            raw (bool)
                Return raw json response instead of model instance

        Returns:
            `IIBBuildDetailsModel` or dict
              if raw == True return dict with json response otherwise
              return `IIBBuildDetailsModel` instance.
        """

        resp = self.iib_session.get("builds/%s" % bid)
        resp.raise_for_status()
        if raw:
            return resp.json()
        return IIBBuildDetailsModel.from_dict(resp.json())

    def wait_for_build(self, build):
        """Wait until specific build is finished

        Args:
            build (IIBBuildDetailsModel)
                Instance of `IIBBuildDetailsModel` class
        """

        while True:
            build_details = self.get_build(build.id)
            if build_details.state in ("complete", "failed"):
                return build_details
            time.sleep(self.poll_interval)

    def rebuild_index(self, index_image):
        raise NotImplementedError

    def health(self):
        raise NotImplementedError
