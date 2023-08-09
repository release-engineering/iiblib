import pytest
import requests_mock


from iiblib.iib_build_details_model import IIBBuildDetailsModel
from iiblib.iib_client import IIBClient


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
        "build_tags": [],
        "check_related_images": True,
        "logs": {},
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
        "deprecation_list": [],
    }
    return json


@pytest.fixture
def fixture_add_build_details_json2():
    json = {
        "id": 2,
        "arches": ["x86_64"],
        "state": "in_progress",
        "state_reason": "state_reason",
        "request_type": "add",
        "state_history": [],
        "batch": 2,
        "batch_annotations": {"batch_annotations": 2},
        "build_tags": [],
        "check_related_images": True,
        "logs": {},
        "updated": "updated",
        "user": "user@example.com",
        "binary_image": "binary_image",
        "binary_image_resolved": "binary_image_resolved",
        "bundles": ["bundles1"],
        "bundle_mapping": {"bundle_mapping": "map"},
        "from_index": "from_index",
        "from_index_resolved": "from_index_resolved",
        "internal_index_image_copy": "internal_index_image_copy",
        "internal_index_image_copy_resolved": "index_image_copy_resolved",
        "index_image": "index_image",
        "index_image_resolved": "index_image_resolved",
        "removed_operators": ["operator1"],
        "organization": "organization",
        "omps_operator_version": {"operator": "1.0"},
        "distribution_scope": "null",
        "deprecation_list": [],
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
def fixture_builds_page2_json(fixture_add_build_details_json2):
    json = {
        "items": [fixture_add_build_details_json2],
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


def test_iib_build_details_pager(
    fixture_builds_page1_json,
    fixture_builds_page2_json,
    fixture_add_build_details_json,
    fixture_add_build_details_json2,
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
