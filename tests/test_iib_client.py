import copy
from mock import patch, MagicMock

from iiblib.iibclient import (
    IIBBuildDetailsModel,
    IIBBuildDetailsPager,
    IIBAuth,
    IIBBasicAuth,
    IIBKrbAuth,
    IIBClient,
    IIBSession,
)

import pytest
import requests_mock
import requests_kerberos


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
            "index-image", "binary", ["bundles-map"], []
        ) == IIBBuildDetailsModel.from_dict(fixture_build_details_json)
        assert iibc.add_bundles(
            "index-image",
            "binary",
            ["bundles-map"],
            [],
            cnr_token="cnr",
            organization="org",
        ) == IIBBuildDetailsModel.from_dict(fixture_build_details_json)
        assert (
            iibc.add_bundles("index-image", "binary", ["bundles-map"], [], raw=True)
            == fixture_build_details_json
        )
        assert iibc.remove_operators(
            "index-image", "binary", ["operator1"], []
        ) == IIBBuildDetailsModel.from_dict(fixture_build_details_json)
        assert (
            iibc.remove_operators("index-image", "binary", ["operator1"], [], raw=True)
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


def test_iib_krb_auth():
    session = MagicMock()
    session.session.headers = {}
    auth = IIBKrbAuth("test_principal", ktfile="/some/kt/file")
    auth.make_auth(session)
    assert isinstance(session.session.auth, requests_kerberos.HTTPKerberosAuth)


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
    )
    model = IIBBuildDetailsModel.from_dict(fixture_build_details_json)
    assert model == expected_model
    assert model != unexpected_model


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
