import copy
import pytest
import requests
import requests_mock
from requests import HTTPError

from iiblib.iib_client import (
    IIBClient,
    IIBException,
)
from iiblib.iib_build_details_model import (
    IIBBuildDetailsModel,
    AddModel,
    RmModel,
    RegenerateBundleModel,
    CreateEmptyIndexModel,
)
from iiblib.iib_build_details_pager import IIBBuildDetailsPager


@pytest.fixture
def fixture_add_build_details_json():
    json = {
        "id": 1,
        "arches": ["x86_64"],
        "state": "in_progress",
        "state_reason": "state_reason",
        "request_type": "add",
        "state_history": [],
        "batch": 1,
        "batch_annotations": {"batch_annotations": 1},
        "build_tags": ["v4.5-2020-10-10"],
        "logs": {},
        "deprecation_list": [],
        "updated": "updated",
        "user": "user@example.com",
        "binary_image": "binary_image",
        "binary_image_resolved": "binary_image_resolved",
        "bundles": ["bundles1"],
        "bundle_mapping": {"bundle_mapping": "map"},
        "from_index": "from_index",
        "from_index_resolved": "from_index_resolved",
        "index_image": "index_image",
        "index_image_resolved": "index_image_resolved",
        "internal_index_image_copy": "internal_index_image_copy",
        "internal_index_image_copy_resolved": "index_image_copy_resolved",
        "removed_operators": ["operator1"],
        "organization": "organization",
        "omps_operator_version": {"operator": "1.0"},
        "distribution_scope": "null",
    }
    return json


@pytest.fixture
def fixture_rm_build_details_json():
    json = {
        "id": 2,
        "arches": ["x86_64"],
        "state": "in_progress",
        "state_reason": "state_reason",
        "request_type": "rm",
        "state_history": [],
        "batch": 1,
        "batch_annotations": {"batch_annotations": 1},
        "build_tags": ["v4.5-2020-10-10"],
        "logs": {},
        "deprecation_list": [],
        "updated": "updated",
        "user": "user@example.com",
        "binary_image": "binary_image",
        "binary_image_resolved": "binary_image_resolved",
        "bundles": ["bundles1"],
        "bundle_mapping": {"bundle_mapping": "map"},
        "from_index": "from_index",
        "from_index_resolved": "from_index_resolved",
        "index_image": "index_image",
        "index_image_resolved": "index_image_resolved",
        "internal_index_image_copy": "internal_index_image_copy",
        "internal_index_image_copy_resolved": "index_image_copy_resolved",
        "removed_operators": ["operator1"],
        "organization": "organization",
        "distribution_scope": "null",
    }
    return json


@pytest.fixture
def fixture_deprecation_list_build_details_json():
    json = {
        "id": 2,
        "arches": ["x86_64"],
        "state": "in_progress",
        "state_reason": "state_reason",
        "request_type": "add",
        "state_history": [],
        "batch": 1,
        "batch_annotations": {"batch_annotations": 1},
        "build_tags": [],
        "logs": {},
        "deprecation_list": ["deprecation_list"],
        "updated": "updated",
        "user": "user@example.com",
        "binary_image": "binary_image",
        "binary_image_resolved": "binary_image_resolved",
        "bundles": ["bundles1"],
        "bundle_mapping": {"bundle_mapping": "map"},
        "from_index": "from_index",
        "from_index_resolved": "from_index_resolved",
        "index_image": "index_image",
        "index_image_resolved": "index_image_resolved",
        "internal_index_image_copy": "internal_index_image_copy",
        "internal_index_image_copy_resolved": "index_image_copy_resolved",
        "removed_operators": ["operator1"],
        "organization": "organization",
        "omps_operator_version": {"operator": "1.0"},
        "distribution_scope": "null",
    }
    return json


@pytest.fixture
def fixture_regenerate_bundle_build_details_json():
    json = {
        "id": 3,
        "arches": ["x86_64"],
        "state": "in_progress",
        "state_reason": "state_reason",
        "request_type": "regenerate-bundle",
        "state_history": [],
        "batch": 1,
        "batch_annotations": {"batch_annotations": 1},
        "logs": {},
        "updated": "updated",
        "user": "user@example.com",
        "bundle_image": "bundle_image",
        "from_bundle_image": "from_bundle_image",
        "from_bundle_image_resolved": "from_bundle_image_resolved",
        "organization": "organization",
    }
    return json


@pytest.fixture
def fixture_create_empty_index_build_details_json():
    json = {
        "id": 3,
        "arches": ["x86_64"],
        "batch": 1,
        "batch_annotations": {"batch_annotations": 1},
        "binary_image": "binary_image",
        "binary_image_resolved": "binary_image_resolved",
        "distribution_scope": "distribution_scope",
        "from_index": "from_index",
        "from_index_resolved": "from_index_resolved",
        "index_image": "index_image",
        "index_image_resolved": "index_image_resolved",
        "labels": {"version": "v1"},
        "logs": {},
        "request_type": "create-empty-index",
        "state": "in_progress",
        "state_history": [],
        "state_reason": "state_reason",
        "updated": "updated",
        "user": "user@example.com",
    }
    return json


@pytest.fixture
def fixture_builds_page1_json(fixture_add_build_details_json):
    json = {
        "items": [fixture_add_build_details_json],
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
def fixture_builds_page2_json(fixture_rm_build_details_json):
    json = {
        "items": [fixture_rm_build_details_json],
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


def test_iib_client(
    fixture_add_build_details_json,
    fixture_rm_build_details_json,
    fixture_regenerate_bundle_build_details_json,
    fixture_create_empty_index_build_details_json,
    fixture_builds_page1_json,
):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "/api/v1/builds/add",
            status_code=200,
            json=fixture_add_build_details_json,
        )
        m.register_uri(
            "POST",
            "/api/v1/builds/rm",
            status_code=200,
            json=fixture_rm_build_details_json,
        )

        m.register_uri(
            "POST",
            "/api/v1/builds/regenerate-bundle",
            status_code=200,
            json=fixture_regenerate_bundle_build_details_json,
        )
        m.register_uri(
            "POST",
            "/api/v1/builds/create-empty-index",
            status_code=200,
            json=fixture_create_empty_index_build_details_json,
        )
        m.register_uri(
            "GET", "/api/v1/builds", status_code=200, json=fixture_builds_page1_json
        )
        m.register_uri(
            "GET",
            "/api/v1/builds/1",
            status_code=200,
            json=fixture_add_build_details_json,
        )
        m.register_uri(
            "GET",
            "/api/v1/builds/2",
            status_code=200,
            json=fixture_rm_build_details_json,
        )
        m.register_uri(
            "GET",
            "/api/v1/builds/3",
            status_code=200,
            json=fixture_regenerate_bundle_build_details_json,
        )
        m.register_uri(
            "GET",
            "/api/v1/builds/4",
            status_code=200,
            json=fixture_create_empty_index_build_details_json,
        )

        iibc = IIBClient("fake-host")
        ret = iibc.add_bundles(
            "index-image", ["bundles-map"], [], binary_image="binary"
        )
        assert ret == AddModel.from_dict(fixture_add_build_details_json)
        ret = iibc.add_bundles(
            "index-image",
            ["bundles-map"],
            [],
            binary_image="binary",
            cnr_token="cnr",
            organization="org",
            overwrite_from_index=True,
            overwrite_from_index_token="str",
            build_tags=["extra-tag1"],
        )
        assert ret == AddModel.from_dict(fixture_add_build_details_json)
        assert (
            iibc.add_bundles(
                "index-image",
                ["bundles-map"],
                [],
                binary_image="binary",
                raw=True,
            )
            == fixture_add_build_details_json
        )
        assert iibc.remove_operators(
            "index-image",
            ["operator1"],
            [],
            binary_image="binary",
            build_tags=["v4.5-2020-10-10"],
            overwrite_from_index=True,
            overwrite_from_index_token="str",
        ) == RmModel.from_dict(fixture_rm_build_details_json)
        assert (
            iibc.remove_operators(
                "index-image", ["operator1"], [], binary_image="binary", raw=True
            )
            == fixture_rm_build_details_json
        )

        assert iibc.regenerate_bundle(
            bundle_image="bundle_image",
            organization="organization",
        ) == RegenerateBundleModel.from_dict(
            fixture_regenerate_bundle_build_details_json
        )
        assert (
            iibc.regenerate_bundle(
                bundle_image="bundle_image", organization="organization", raw=True
            )
            == fixture_regenerate_bundle_build_details_json
        )

        assert iibc.create_empty_index(
            index_image="from_index",
            binary_image="binary_image",
            labels={"version": "v1"},
        ) == CreateEmptyIndexModel.from_dict(
            fixture_create_empty_index_build_details_json
        )
        assert (
            iibc.create_empty_index(
                index_image="from_index",
                binary_image="binary_image",
                labels={"version": "v1"},
                raw=True,
            )
            == fixture_create_empty_index_build_details_json
        )

        # get_builds - request_type is "add"
        assert iibc.get_build(1) == IIBBuildDetailsModel.from_dict(
            fixture_add_build_details_json
        )
        assert iibc.get_build(1, raw=True) == fixture_add_build_details_json

        # get_builds - request_type is "rm"
        assert iibc.get_build(2) == IIBBuildDetailsModel.from_dict(
            fixture_rm_build_details_json
        )
        assert iibc.get_build(2, raw=True) == fixture_rm_build_details_json

        # get_builds - request_type is "regenerate-bundle"
        assert iibc.get_build(3) == IIBBuildDetailsModel.from_dict(
            fixture_regenerate_bundle_build_details_json
        )
        assert (
            iibc.get_build(3, raw=True) == fixture_regenerate_bundle_build_details_json
        )
        # get_builds - request_type is "create-empty-index"
        assert iibc.get_build(4) == IIBBuildDetailsModel.from_dict(
            fixture_create_empty_index_build_details_json
        )
        assert (
            iibc.get_build(4, raw=True) == fixture_create_empty_index_build_details_json
        )

        assert iibc.get_builds() == IIBBuildDetailsPager.from_dict(
            iibc, fixture_builds_page1_json
        )
        assert iibc.get_builds(raw=True) == fixture_builds_page1_json


def test_iib_client_no_overwrite_from_index_or_token(
    fixture_add_build_details_json, fixture_rm_build_details_json
):
    error_msg = (
        "Either both or neither of overwrite-from-index "
        "and overwrite-from-index-token should be specified."
    )
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "/api/v1/builds/add",
            status_code=200,
            json=fixture_add_build_details_json,
        )
        m.register_uri(
            "POST",
            "/api/v1/builds/rm",
            status_code=200,
            json=fixture_rm_build_details_json,
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


def test_iib_client_deprecation_list(
    fixture_add_build_details_json,
    fixture_deprecation_list_build_details_json,
):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "/api/v1/builds/add",
            status_code=200,
            json=fixture_add_build_details_json,
        )
        iibc = IIBClient("fake-host")
        assert iibc.add_bundles(
            "index-image", ["bundles-map"], [], binary_image="binary"
        ) == AddModel.from_dict(fixture_add_build_details_json)

        assert iibc.add_bundles(
            "index-image",
            ["bundles-map"],
            [],
            binary_image="binary",
            cnr_token="cnr",
            organization="org",
            overwrite_from_index=True,
            overwrite_from_index_token="str",
        ) == AddModel.from_dict(fixture_add_build_details_json)

    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "/api/v1/builds/add",
            status_code=200,
            json=fixture_deprecation_list_build_details_json,
        )
        iibc = IIBClient("fake-host")

        assert iibc.add_bundles(
            "index-image",
            ["bundles-map"],
            [],
            binary_image="binary",
            cnr_token="cnr",
            deprecation_list=["deprecation_list"],
            organization="org",
            overwrite_from_index=True,
            overwrite_from_index_token="str",
        ) == AddModel.from_dict(fixture_deprecation_list_build_details_json)


def test_client_wait_for_build(fixture_add_build_details_json):
    iibc = IIBClient("fake-host", poll_interval=1)
    bdetails_finished = copy.copy(fixture_add_build_details_json)
    bdetails_finished["state"] = "complete"
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/api/v1/builds/1",
            [
                {"json": fixture_add_build_details_json, "status_code": 200},
                {"json": bdetails_finished, "status_code": 200},
            ],
        )
        iibc.wait_for_build(
            IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)
        )

    bdetails_finished["state"] = "failed"
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/api/v1/builds/1",
            [
                {"json": fixture_add_build_details_json, "status_code": 200},
                {"json": bdetails_finished, "status_code": 200},
            ],
        )
        iibc.wait_for_build(
            IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)
        )


# add model used
def test_client_wait_for_build_retry(fixture_add_build_details_json):
    iibc = IIBClient("fake-host.test", poll_interval=1, retries=10, backoff_factor=0)

    with pytest.raises(
        requests.exceptions.RequestException, match=".*Max retries exceeded*."
    ):
        iibc.wait_for_build(
            IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)
        )


# add model used
def test_client_wait_for_build_timeout(fixture_add_build_details_json):
    # set wait timeout for 2 seconds
    iibc = IIBClient("fake-host.test", poll_interval=1, wait_for_build_timeout=2)

    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/api/v1/builds/{}".format(fixture_add_build_details_json["id"]),
            status_code=200,
            json=fixture_add_build_details_json,
        )

        with pytest.raises(IIBException, match="Timeout*."):
            iibc.wait_for_build(
                IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)
            )


@pytest.mark.xfail
def test_health():
    iibc = IIBClient("fake-host")
    iibc.health()


@pytest.mark.xfail
def test_rebuild_index():
    iibc = IIBClient("fake-host")
    iibc.rebuild_index("some index")


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
