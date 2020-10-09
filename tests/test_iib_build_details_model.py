import pytest

from iiblib.iib_build_details_model import IIBBuildDetailsModel


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
