import pytest
import requests_mock


from iiblib.iib_build_details_model import IIBBuildDetailsModel
from iiblib.iib_client import IIBClient


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
