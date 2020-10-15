import pytest

from iiblib.iib_build_details_model import (
    IIBBuildDetailsModel,
    AddModel,
    RmModel,
    RegenerateBundleModel,
)


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
        "removed_operators": ["operator1"],
        "organization": "organization",
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
def fixture_unknown_build_details_json():
    json = {
        "id": 3,
        "arches": ["x86_64"],
        "state": "in_progress",
        "state_reason": "state_reason",
        "request_type": "unknown",
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
def fixture_bundle_image_missing_json():
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
        "from_bundle_image": "from_bundle_image",
        "from_bundle_image_resolved": "from_bundle_image_resolved",
        "organization": "organization",
    }
    return json


@pytest.fixture
def fixture_optional_args_missing_json():
    json = {
        "id": 3,
        "arches": ["x86_64"],
        "state": "in_progress",
        "state_reason": "state_reason",
        "request_type": "regenerate-bundle",
        "batch": 1,
        "updated": "updated",
        "user": "user@example.com",
        "bundle_image": "bundle_image",
        "from_bundle_image": "from_bundle_image",
        "from_bundle_image_resolved": "from_bundle_image_resolved",
        "organization": "organization",
    }
    return json


def test_from_dict_success(
    fixture_add_build_details_json,
    fixture_rm_build_details_json,
    fixture_regenerate_bundle_build_details_json,
    fixture_optional_args_missing_json,
):
    add_model = AddModel(
        id=1,
        arches=["x86_64"],
        state="in_progress",
        state_reason="state_reason",
        request_type="add",
        state_history=[],
        batch=1,
        batch_annotations={"batch_annotations": 1},
        logs={},
        updated="updated",
        user="user@example.com",
        binary_image="binary_image",
        binary_image_resolved="binary_image_resolved",
        bundles=["bundles1"],
        bundle_mapping={"bundle_mapping": "map"},
        from_index="from_index",
        from_index_resolved="from_index_resolved",
        index_image="index_image",
        removed_operators=["operator1"],
        organization="organization",
        omps_operator_version={"operator": "1.0"},
        distribution_scope="null",
    )
    rm_model = RmModel(
        id=2,
        arches=["x86_64"],
        state="in_progress",
        state_reason="state_reason",
        request_type="rm",
        state_history=[],
        batch=1,
        batch_annotations={"batch_annotations": 1},
        logs={},
        updated="updated",
        user="user@example.com",
        binary_image="binary_image",
        binary_image_resolved="binary_image_resolved",
        bundles=["bundles1"],
        bundle_mapping={"bundle_mapping": "map"},
        from_index="from_index",
        from_index_resolved="from_index_resolved",
        index_image="index_image",
        removed_operators=["operator1"],
        organization="organization",
        distribution_scope="null",
    )

    regenerate_bundle_model = RegenerateBundleModel(
        id=3,
        arches=["x86_64"],
        state="in_progress",
        state_reason="state_reason",
        request_type="regenerate-bundle",
        state_history=[],
        batch=1,
        batch_annotations={"batch_annotations": 1},
        logs={},
        updated="updated",
        user="user@example.com",
        bundle_image="bundle_image",
        from_bundle_image="from_bundle_image",
        from_bundle_image_resolved="from_bundle_image_resolved",
        organization="organization",
    )

    optional_args_empty = RegenerateBundleModel(
        id=3,
        arches=["x86_64"],
        state="in_progress",
        state_reason="state_reason",
        request_type="regenerate-bundle",
        batch=1,
        updated="updated",
        user="user@example.com",
        state_history=[],
        batch_annotations={},
        logs={},
        bundle_image="bundle_image",
        from_bundle_image="from_bundle_image",
        from_bundle_image_resolved="from_bundle_image_resolved",
        organization="organization",
    )

    model1 = IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)
    assert model1 == add_model

    model2 = IIBBuildDetailsModel.from_dict(fixture_rm_build_details_json)
    assert model2 == rm_model

    model3 = IIBBuildDetailsModel.from_dict(
        fixture_regenerate_bundle_build_details_json
    )
    assert model3 == regenerate_bundle_model

    model4 = IIBBuildDetailsModel.from_dict(fixture_optional_args_missing_json)
    assert model4 == optional_args_empty


def test_from_dict_failure(
    fixture_add_build_details_json,
    fixture_rm_build_details_json,
    fixture_bundle_image_missing_json,
    fixture_unknown_build_details_json,
):

    error_msg = "Unsupported request type: unknown"

    add_model_state_finished = AddModel(
        id=1,
        arches=["x86_64"],
        state="finished",
        state_reason="state_reason",
        request_type="add",
        state_history=[],
        batch=1,
        batch_annotations={"batch_annotations": 1},
        logs={},
        updated="updated",
        user="user@example.com",
        binary_image="binary_image",
        binary_image_resolved="binary_image_resolved",
        bundles=["bundles1"],
        bundle_mapping={"bundle_mapping": "map"},
        from_index="from_index",
        from_index_resolved="from_index_resolved",
        index_image="index_image",
        removed_operators=["operator1"],
        organization="organization",
        omps_operator_version={"operator": "1.0"},
        distribution_scope="null",
    )

    model1 = IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)
    assert model1 != add_model_state_finished

    model2 = IIBBuildDetailsModel.from_dict(fixture_rm_build_details_json)
    assert model2 != model1

    with pytest.raises(KeyError):
        IIBBuildDetailsModel.from_dict(fixture_bundle_image_missing_json)

    with pytest.raises(KeyError, match=error_msg):
        IIBBuildDetailsModel.from_dict(fixture_unknown_build_details_json)


def test_to_dict_success(fixture_rm_build_details_json):

    rm_model = RmModel(
        id=2,
        arches=["x86_64"],
        state="in_progress",
        state_reason="state_reason",
        request_type="rm",
        state_history=[],
        batch=1,
        batch_annotations={"batch_annotations": 1},
        logs={},
        updated="updated",
        user="user@example.com",
        binary_image="binary_image",
        binary_image_resolved="binary_image_resolved",
        bundles=["bundles1"],
        bundle_mapping={"bundle_mapping": "map"},
        from_index="from_index",
        from_index_resolved="from_index_resolved",
        index_image="index_image",
        removed_operators=["operator1"],
        organization="organization",
        distribution_scope="null",
    )

    model = IIBBuildDetailsModel.from_dict(fixture_rm_build_details_json).to_dict()
    assert model == rm_model.to_dict()


def test_general_attributes(fixture_add_build_details_json):
    model = IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)

    assert model.id == model._data["id"]
    assert model.arches == model._data["arches"]
    assert model.state == model._data["state"]
    assert model.state_reason == model._data["state_reason"]
    assert model.request_type == model._data["request_type"]
    assert model.batch == model._data["batch"]
    assert model.updated == model._data["updated"]
    assert model.user == model._data["user"]


def test_optional_attributes(fixture_add_build_details_json):
    model = IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)

    assert model.state_history == model._data["state_history"]
    assert model.batch_annotations == model._data["batch_annotations"]
    assert model.logs == model._data["logs"]


def test_add_model_attributes(fixture_add_build_details_json):
    model = IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)

    assert model.binary_image == model._data["binary_image"]
    assert model.binary_image_resolved == model._data["binary_image_resolved"]
    assert model.bundles == model._data["bundles"]
    assert model.bundle_mapping == model._data["bundle_mapping"]
    assert model.from_index == model._data["from_index"]
    assert model.from_index_resolved == model._data["from_index_resolved"]
    assert model.index_image == model._data["index_image"]
    assert model.removed_operators == model._data["removed_operators"]
    assert model.organization == model._data["organization"]
    assert model.omps_operator_version == model._data["omps_operator_version"]
    assert model.distribution_scope == model._data["distribution_scope"]


def test_rm_model_attributes(fixture_rm_build_details_json):
    model = IIBBuildDetailsModel.from_dict(fixture_rm_build_details_json)

    assert model.binary_image == model._data["binary_image"]
    assert model.binary_image_resolved == model._data["binary_image_resolved"]
    assert model.bundles == model._data["bundles"]
    assert model.bundle_mapping == model._data["bundle_mapping"]
    assert model.from_index == model._data["from_index"]
    assert model.from_index_resolved == model._data["from_index_resolved"]
    assert model.index_image == model._data["index_image"]
    assert model.removed_operators == model._data["removed_operators"]
    assert model.organization == model._data["organization"]
    assert model.distribution_scope == model._data["distribution_scope"]


def test_regenerate_bundle_model_attributes(
    fixture_regenerate_bundle_build_details_json,
):
    model = IIBBuildDetailsModel.from_dict(fixture_regenerate_bundle_build_details_json)

    assert model.bundle_image == model._data["bundle_image"]
    assert model.from_bundle_image == model._data["from_bundle_image"]
    assert model.from_bundle_image_resolved == model._data["from_bundle_image_resolved"]
    assert model.organization == model._data["organization"]
