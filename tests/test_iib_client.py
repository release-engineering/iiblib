import copy

import pytest
import requests
import requests_mock
from mock import patch, MagicMock, call
from requests import HTTPError

from iiblib.iibclient import (
    IIBBuildDetailsModel,
    IIBBuildDetailsPager,
    IIBAuth,
    IIBBasicAuth,
    IIBKrbAuth,
    IIBClient,
    IIBSession,
    IIBException,
)


@pytest.fixture
def fixture_build_details_json():
    json = {
        "id": 1,
        "state": "in_progress",
        "state_reason": "state_reason",
        "state_history": [],
        "from_index": "from_index",
        "from_index_resolved": "from_index_resolved",
        "bundles": ["bundles1"],
        "removed_operators": ["operator1"],
        "organization": "organization",
        "binary_image": "binary_image",
        "binary_image_resolved": "binary_image_resolved",
        "index_image": "index_image",
        "request_type": "request_type",
        "arches": ["x86_64"],
        "bundle_mapping": {"bundle_mapping": "map"},
        "omps_operator_version": {"operator": "1.0"},
    }
    return json


@pytest.fixture
def fixture_build_details_json2():
    json = {
        "id": 2,
        "state": "in_progress",
        "state_reason": "state_reason",
        "state_history": [],
        "from_index": "from_index",
        "from_index_resolved": "from_index_resolved",
        "bundles": ["bundles1"],
        "removed_operators": ["operator1"],
        "organization": "organization",
        "binary_image": "binary_image",
        "binary_image_resolved": "binary_image_resolved",
        "index_image": "index_image",
        "request_type": "request_type",
        "arches": ["x86_64"],
        "bundle_mapping": {"bundle_mapping": "map"},
        "omps_operator_version": {"operator": "1.0"},
    }
    return json


@pytest.fixture
def fixture_build_details_json3():
    json = {
        "id": 1,
        "state": "in_progress",
        "state_reason": "state_reason",
        "state_history": [],
        "from_index": "from_index",
        "from_index_resolved": "from_index_resolved",
        "bundles": ["bundles1"],
        "removed_operators": ["operator1"],
        "organization": "organization",
        "binary_image": "mapped_binary_image",
        "binary_image_resolved": "mapped_binary_image_resolved",
        "index_image": "index_image",
        "request_type": "request_type",
        "arches": ["x86_64"],
        "bundle_mapping": {"bundle_mapping": "map"},
        "omps_operator_version": {"operator": "1.0"},
    }
    return json


@pytest.fixture
def fixture_builds_page1_json(fixture_build_details_json):
    json = {
        "items": [fixture_build_details_json],
        "meta": {
            "first": "",
            "last": "",
            "next": "",
            "page": 1,
            "pages": 2,
            "per_page": 1,
            "previous": "",
            "total": 2,
        },
    }
    return json


@pytest.fixture
def fixture_builds_page2_json(fixture_build_details_json2):
    json = {
        "items": [fixture_build_details_json2],
        "meta": {
            "first": "",
            "last": "",
            "next": "",
            "page": 2,
            "pages": 2,
            "per_page": 1,
            "previous": "",
            "total": 2,
        },
    }
    return json


@patch("requests.Session.get")
@patch("requests.Session.post")
@patch("requests.Session.put")
@patch("requests.Session.delete")
def test_iib_session_methods(patched_delete, patched_put, patched_post, patched_get):
    iibs = IIBSession("fake-host")
    iibs.get("fake-end-point")
    iibs.post("fake-end-point")
    iibs.put("fake-end-point")
    iibs.delete("fake-end-point")

    patched_get.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
    patched_post.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
    patched_put.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
    patched_delete.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )


def test_iib_client(fixture_build_details_json, fixture_builds_page1_json):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "/api/v1/builds/add",
            status_code=200,
            json=fixture_build_details_json,
        )
        m.register_uri(
            "POST",
            "/api/v1/builds/rm",
            status_code=200,
            json=fixture_build_details_json,
        )
        m.register_uri(
            "GET", "/api/v1/builds", status_code=200, json=fixture_builds_page1_json
        )
        m.register_uri(
            "GET", "/api/v1/builds/1", status_code=200, json=fixture_build_details_json
        )

        iibc = IIBClient("fake-host")
        assert iibc.add_bundles(
            "index-image", ["bundles-map"], [], binary_image="binary"
        ) == IIBBuildDetailsModel.from_dict(fixture_build_details_json)
        assert (
            iibc.add_bundles(
                "index-image",
                ["bundles-map"],
                [],
                binary_image="binary",
                cnr_token="cnr",
                organization="org",
                overwrite_from_index=True,
                overwrite_from_index_token="str",
            )
            == IIBBuildDetailsModel.from_dict(fixture_build_details_json)
        )
        assert (
            iibc.add_bundles(
                "index-image", ["bundles-map"], [], binary_image="binary", raw=True
            )
            == fixture_build_details_json
        )
        assert (
            iibc.remove_operators(
                "index-image",
                ["operator1"],
                [],
                binary_image="binary",
                overwrite_from_index=True,
                overwrite_from_index_token="str",
            )
            == IIBBuildDetailsModel.from_dict(fixture_build_details_json)
        )
        assert (
            iibc.remove_operators(
                "index-image", ["operator1"], [], binary_image="binary", raw=True
            )
            == fixture_build_details_json
        )
        assert iibc.get_build(1) == IIBBuildDetailsModel.from_dict(
            fixture_build_details_json
        )
        assert iibc.get_build(1, raw=True) == fixture_build_details_json

        assert iibc.get_builds() == IIBBuildDetailsPager.from_dict(
            iibc, fixture_builds_page1_json
        )
        assert iibc.get_builds(raw=True) == fixture_builds_page1_json


def test_iib_client_failure(fixture_build_details_json):
    error_msg = (
        "Either both or neither of overwrite-from-index "
        "and overwrite-from-index-token should be specified."
    )
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "/api/v1/builds/add",
            status_code=200,
            json=fixture_build_details_json,
        )
        m.register_uri(
            "POST",
            "/api/v1/builds/rm",
            status_code=200,
            json=fixture_build_details_json,
        )
        iibc = IIBClient("fake-host")
        with pytest.raises(ValueError, match=error_msg):
            iibc.remove_operators(
                "index-image",
                ["operator1"],
                [],
                binary_image="binary",
                overwrite_from_index=True,
            )
        with pytest.raises(ValueError, match=error_msg):
            iibc.remove_operators(
                "index-image",
                ["operator1"],
                [],
                binary_image="binary",
                overwrite_from_index_token="str",
            )
        with pytest.raises(ValueError, match=error_msg):
            iibc.add_bundles(
                "index-image",
                ["bundles-map"],
                [],
                binary_image="binary",
                cnr_token="cnr",
                organization="org",
                overwrite_from_index=True,
            )
        with pytest.raises(ValueError, match=error_msg):
            iibc.add_bundles(
                "index-image",
                ["bundles-map"],
                [],
                binary_image="binary",
                cnr_token="cnr",
                organization="org",
                overwrite_from_index_token="str",
            )


def test_iib_client_no_binary_image(fixture_build_details_json3):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "/api/v1/builds/add",
            status_code=200,
            json=fixture_build_details_json3,
        )
        m.register_uri(
            "POST",
            "/api/v1/builds/rm",
            status_code=200,
            json=fixture_build_details_json3,
        )

        iibc = IIBClient("fake-host")
        assert iibc.add_bundles(
            "index-image", ["bundles-map"], []
        ) == IIBBuildDetailsModel.from_dict(fixture_build_details_json3)
        assert (
            iibc.add_bundles(
                "index-image",
                ["bundles-map"],
                [],
                cnr_token="cnr",
                organization="org",
                overwrite_from_index=True,
                overwrite_from_index_token="str",
            )
            == IIBBuildDetailsModel.from_dict(fixture_build_details_json3)
        )
        assert (
            iibc.add_bundles("index-image", ["bundles-map"], [], raw=True)
            == fixture_build_details_json3
        )
        assert (
            iibc.remove_operators(
                "index-image",
                ["operator1"],
                [],
                overwrite_from_index=True,
                overwrite_from_index_token="str",
            )
            == IIBBuildDetailsModel.from_dict(fixture_build_details_json3)
        )
        assert (
            iibc.remove_operators("index-image", ["operator1"], [], raw=True)
            == fixture_build_details_json3
        )


def test_client_wait_for_build(fixture_build_details_json):
    iibc = IIBClient("fake-host", poll_interval=1)
    bdetails_finished = copy.copy(fixture_build_details_json)
    bdetails_finished["state"] = "complete"
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/api/v1/builds/1",
            [
                {"json": fixture_build_details_json, "status_code": 200},
                {"json": bdetails_finished, "status_code": 200},
            ],
        )
        iibc.wait_for_build(IIBBuildDetailsModel.from_dict(fixture_build_details_json))

    bdetails_finished["state"] = "failed"
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/api/v1/builds/1",
            [
                {"json": fixture_build_details_json, "status_code": 200},
                {"json": bdetails_finished, "status_code": 200},
            ],
        )
        iibc.wait_for_build(IIBBuildDetailsModel.from_dict(fixture_build_details_json))


def test_client_wait_for_build_retry(fixture_build_details_json):
    iibc = IIBClient("fake-host.test", poll_interval=1, retries=10, backoff_factor=0)

    with pytest.raises(
        requests.exceptions.RequestException, match=".*Max retries exceeded*."
    ):
        iibc.wait_for_build(IIBBuildDetailsModel.from_dict(fixture_build_details_json))


def test_client_wait_for_build_timeout(fixture_build_details_json):
    # set wait timeout for 2 seconds
    iibc = IIBClient("fake-host.test", poll_interval=1, wait_for_build_timeout=2)

    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/api/v1/builds/{}".format(fixture_build_details_json["id"]),
            status_code=200,
            json=fixture_build_details_json,
        )

        with pytest.raises(IIBException, match="Timeout*."):
            iibc.wait_for_build(
                IIBBuildDetailsModel.from_dict(fixture_build_details_json)
            )


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


@pytest.mark.xfail
def test_health():
    iibc = IIBClient("fake-host")
    iibc.health()


@pytest.mark.xfail
def test_rebuild_index():
    iibc = IIBClient("fake-host")
    iibc.rebuild_index("some index")


def test_iibauth_abstract():
    try:
        IIBAuth()
        raise AssertionError("Should raise NotImplementedError")
    except NotImplementedError:
        pass


def test_iibbuilddetailsmodel(fixture_build_details_json):
    unexpected_model = IIBBuildDetailsModel(
        1,
        "finished",
        "state_reason",
        [],
        "from_index",
        "from_index_resolved",
        ["bundles1"],
        ["operator1"],
        "organization",
        "binary_image",
        "binary_image_resolved",
        "index_image",
        "request_type",
        ["x86_64"],
        {"bundle_mapping": "map"},
        {"operator": "1.0"},
    )
    expected_model = IIBBuildDetailsModel(
        1,
        "in_progress",
        "state_reason",
        [],
        "from_index",
        "from_index_resolved",
        ["bundles1"],
        ["operator1"],
        "organization",
        "binary_image",
        "binary_image_resolved",
        "index_image",
        "request_type",
        ["x86_64"],
        {"bundle_mapping": "map"},
        {"operator": "1.0"},
    )
    model = IIBBuildDetailsModel.from_dict(fixture_build_details_json)
    assert model == expected_model
    assert model != unexpected_model

    model = IIBBuildDetailsModel.from_dict(fixture_build_details_json).to_dict()
    assert model == expected_model.to_dict()
    assert model != unexpected_model.to_dict()


def test_iibbuilddetails_pager(
    fixture_builds_page1_json,
    fixture_builds_page2_json,
    fixture_build_details_json,
    fixture_build_details_json2,
):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET", "/api/v1/builds", status_code=200, json=fixture_builds_page1_json
        )
        m.register_uri(
            "GET",
            "/api/v1/builds?page=2",
            status_code=200,
            json=fixture_builds_page2_json,
        )
        m.register_uri(
            "GET",
            "/api/v1/builds?page=1",
            status_code=200,
            json=fixture_builds_page1_json,
        )

        iibc = IIBClient("fake-host")
        pager = iibc.get_builds()
        assert pager.items() == [
            IIBBuildDetailsModel.from_dict(fixture_builds_page1_json["items"][0])
        ]
        pager.next()
        assert pager.items() == [
            IIBBuildDetailsModel.from_dict(fixture_builds_page2_json["items"][0])
        ]
        pager.prev()
        assert pager.items() == [
            IIBBuildDetailsModel.from_dict(fixture_builds_page1_json["items"][0])
        ]


def test_http_error_response():
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/api/v1/builds",
            status_code=400,
            text="An ugly HTTP error has occurred!",
        )

        iibc = IIBClient("fake-host")
        with pytest.raises(HTTPError):
            iibc.get_builds()


def test_iib_error_response():
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/api/v1/builds",
            status_code=400,
            json={"error": "An ugly error has occurred!"},
        )

        iibc = IIBClient("fake-host")
        with pytest.raises(IIBException):
            iibc.get_builds()
