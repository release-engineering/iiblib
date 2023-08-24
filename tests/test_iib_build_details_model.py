from pytest import fixture, raises, mark

from iiblib.iib_build_details_model import (
    IIBBuildDetailsModel,
    AddModel,
    RmModel,
    RegenerateBundleModel,
    MergeIndexImageModel,
)


@fixture
def fixture_base_build_details_json():
    json = {
        "arches": ["x86_64"],
        "state": "in_progress",
        "state_reason": "state_reason",
        "batch": 1,
        "updated": "updated",
        "user": "user@example.com",
    }
    return json


@fixture
def fixture_full_base_build_details_json(fixture_base_build_details_json):
    json = {
        "state_history": [],
        "batch_annotations": {"batch_annotations": 1},
        "logs": {},
        "organization": "organization",
    }
    json.update(fixture_base_build_details_json)
    return json


@fixture
def fixture_add_build_details_json(fixture_full_base_build_details_json):
    json = {
        "id": 1,
        "request_type": "add",
        "build_tags": ["v4.5-2020-10-10"],
        "check_related_images": True,
        "deprecation_list": [],
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
        "omps_operator_version": {"operator": "1.0"},
        "distribution_scope": "null",
    }
    json.update(fixture_full_base_build_details_json)
    return json


@fixture
def fixture_add_build_details_json2(fixture_add_build_details_json):
    json = fixture_add_build_details_json
    json["check_related_images"] = None
    return json


@fixture
def fixture_rm_build_details_json(fixture_full_base_build_details_json):
    json = {
        "id": 2,
        "request_type": "rm",
        "build_tags": ["v4.5-2020-10-10"],
        "deprecation_list": [],
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
        "distribution_scope": "null",
    }
    json.update(fixture_full_base_build_details_json)
    return json


@fixture
def fixture_regenerate_bundle_build_details_json(fixture_full_base_build_details_json):
    json = {
        "id": 3,
        "request_type": "regenerate-bundle",
        "bundle_image": "bundle_image",
        "from_bundle_image": "from_bundle_image",
        "from_bundle_image_resolved": "from_bundle_image_resolved",
    }
    json.update(fixture_full_base_build_details_json)
    return json


@fixture
def fixture_merge_index_image_build_details_json(fixture_full_base_build_details_json):
    json = {
        "id": 4,
        "request_type": "merge-index-image",
        "build_tags": ["v4.5-2020-10-10"],
        "binary_image": "binary_image",
        "binary_image_resolved": "binary_image_resolved",
        "deprecation_list": [],
        "distribution_scope": "null",
        "index_image": "index_image",
        "source_from_index": "source_from_index",
        "source_from_index_resolved": "source_from_index_resolved",
        "target_index": "target_index",
        "target_index_resolved": "target_index_resolved",
    }
    json.update(fixture_full_base_build_details_json)
    return json


@fixture
def fixture_unknown_request_type_json(fixture_full_base_build_details_json):
    json = {
        "id": 3,
        "request_type": "unknown",
        "bundle_image": "bundle_image",
        "from_bundle_image": "from_bundle_image",
        "from_bundle_image_resolved": "from_bundle_image_resolved",
    }
    json.update(fixture_full_base_build_details_json)
    return json


@fixture
def fixture_bundle_image_missing_json(fixture_full_base_build_details_json):
    json = {
        "id": 3,
        "request_type": "regenerate-bundle",
        "deprecation_list": [],
        "from_bundle_image": "from_bundle_image",
        "from_bundle_image_resolved": "from_bundle_image_resolved",
    }
    json.update(fixture_full_base_build_details_json)
    return json


@fixture
def fixture_optional_args_missing_json(fixture_base_build_details_json):
    json = {
        "id": 3,
        "request_type": "regenerate-bundle",
        "bundle_image": "bundle_image",
        "from_bundle_image": "from_bundle_image",
        "from_bundle_image_resolved": "from_bundle_image_resolved",
        "organization": "organization",
    }
    json.update(fixture_base_build_details_json)
    return json


def test_from_dict_success(
    fixture_add_build_details_json,
    fixture_add_build_details_json2,
    fixture_rm_build_details_json,
    fixture_regenerate_bundle_build_details_json,
    fixture_optional_args_missing_json,
    fixture_merge_index_image_build_details_json,
):
    model1 = IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)
    assert model1 == AddModel(**fixture_add_build_details_json)

    model2 = IIBBuildDetailsModel.from_dict(fixture_add_build_details_json2)
    assert model2 == AddModel(**fixture_add_build_details_json2)

    model3 = IIBBuildDetailsModel.from_dict(fixture_rm_build_details_json)
    assert model3 == RmModel(**fixture_rm_build_details_json)

    model4 = IIBBuildDetailsModel.from_dict(
        fixture_regenerate_bundle_build_details_json
    )
    assert model4 == RegenerateBundleModel(
        **fixture_regenerate_bundle_build_details_json
    )

    model5 = IIBBuildDetailsModel.from_dict(fixture_optional_args_missing_json)
    assert model5 == RegenerateBundleModel(**fixture_optional_args_missing_json)

    model6 = IIBBuildDetailsModel.from_dict(
        fixture_merge_index_image_build_details_json
    )
    assert model6 == MergeIndexImageModel(
        **fixture_merge_index_image_build_details_json
    )


def test_from_dict_failure(
    fixture_add_build_details_json,
    fixture_rm_build_details_json,
    fixture_bundle_image_missing_json,
    fixture_unknown_request_type_json,
):
    key_error_msg = "Unsupported request type: unknown"
    type_error_msg = "Class AddModel doesn't accept rm request type"

    add_model_state_finished = AddModel(
        id=1,
        arches=["x86_64"],
        state="finished",
        state_reason="state_reason",
        request_type="add",
        state_history=[],
        batch=1,
        batch_annotations={"batch_annotations": 1},
        check_related_images=True,
        logs={},
        deprecation_list=[],
        updated="updated",
        user="user@example.com",
        binary_image="binary_image",
        binary_image_resolved="binary_image_resolved",
        build_tags=[],
        bundles=["bundles1"],
        bundle_mapping={"bundle_mapping": "map"},
        from_index="from_index",
        from_index_resolved="from_index_resolved",
        index_image="index_image",
        index_image_resolved="index_image_resolved",
        internal_index_image_copy="internal_index_image_copy",
        internal_index_image_copy_resolved="index_image_copy_resolved",
        removed_operators=["operator1"],
        organization="organization",
        omps_operator_version={"operator": "1.0"},
        distribution_scope="null",
    )

    add_model_wrong_request_type = {
        "id": 1,
        "arches": ["x86_64"],
        "state": "in_progress",
        "state_reason": "state_reason",
        "request_type": "rm",
        "state_history": [],
        "batch": 1,
        "batch_annotations": {"batch_annotations": 1},
        "check_related_images": True,
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
        "removed_operators": ["operator1"],
        "organization": "organization",
        "omps_operator_version": {"operator": "1.0"},
        "distribution_scope": "null",
    }

    model1 = IIBBuildDetailsModel.from_dict(fixture_add_build_details_json)
    assert model1 != add_model_state_finished

    model2 = IIBBuildDetailsModel.from_dict(fixture_rm_build_details_json)
    assert model2 != model1

    with raises(KeyError):
        IIBBuildDetailsModel.from_dict(fixture_bundle_image_missing_json)

    with raises(KeyError, match=key_error_msg):
        IIBBuildDetailsModel.from_dict(fixture_unknown_request_type_json)

    with raises(TypeError, match=type_error_msg):
        AddModel.from_dict(add_model_wrong_request_type)


def test_to_dict_rm(fixture_rm_build_details_json):
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
        build_tags=["v4.5-2020-10-10"],
        bundles=["bundles1"],
        bundle_mapping={"bundle_mapping": "map"},
        from_index="from_index",
        from_index_resolved="from_index_resolved",
        index_image="index_image",
        index_image_resolved="index_image_resolved",
        internal_index_image_copy="internal_index_image_copy",
        internal_index_image_copy_resolved="index_image_copy_resolved",
        removed_operators=["operator1"],
        organization="organization",
        distribution_scope="null",
        deprecation_list=[],
    )

    model = RmModel.from_dict(fixture_rm_build_details_json).to_dict()
    assert model == rm_model.to_dict()


def test_to_dict_merg_index_image(fixture_merge_index_image_build_details_json):
    mii_model = MergeIndexImageModel(
        arches=["x86_64"],
        batch=1,
        batch_annotations={"batch_annotations": 1},
        binary_image="binary_image",
        binary_image_resolved="binary_image_resolved",
        build_tags=["v4.5-2020-10-10"],
        deprecation_list=[],
        distribution_scope="null",
        id=4,
        index_image="index_image",
        logs={},
        request_type="merge-index-image",
        source_from_index_resolved="source_from_index_resolved",
        source_from_index="source_from_index",
        state_history=[],
        state="in_progress",
        state_reason="state_reason",
        target_index_resolved="target_index_resolved",
        target_index="target_index",
        updated="updated",
        user="user@example.com",
    )
    model = MergeIndexImageModel.from_dict(
        fixture_merge_index_image_build_details_json
    ).to_dict()
    assert model == mii_model.to_dict()


@mark.parametrize(
    "schema",
    [
        "fixture_merge_index_image_build_details_json",
        "fixture_regenerate_bundle_build_details_json",
        "fixture_rm_build_details_json",
        "fixture_add_build_details_json",
    ],
)
def test_general_attributes(schema, request):
    model = IIBBuildDetailsModel.from_dict(request.getfixturevalue(schema))

    assert model.id == model._data["id"]
    assert model.arches == model._data["arches"]
    assert model.state == model._data["state"]
    assert model.state_reason == model._data["state_reason"]
    assert model.request_type == model._data["request_type"]
    assert model.batch == model._data["batch"]
    assert model.updated == model._data["updated"]
    assert model.user == model._data["user"]


@mark.parametrize(
    "schema",
    [
        "fixture_merge_index_image_build_details_json",
        "fixture_regenerate_bundle_build_details_json",
        "fixture_rm_build_details_json",
        "fixture_add_build_details_json",
    ],
)
def test_optional_attributes(schema, request):
    model = IIBBuildDetailsModel.from_dict(request.getfixturevalue(schema))

    assert model.state_history == model._data["state_history"]
    assert model.batch_annotations == model._data["batch_annotations"]
    assert model.logs == model._data["logs"]


def test_add_model_attributes(fixture_add_build_details_json):
    model = AddModel.from_dict(fixture_add_build_details_json)

    assert model.binary_image == model._data["binary_image"]
    assert model.binary_image_resolved == model._data["binary_image_resolved"]
    assert model.bundles == model._data["bundles"]
    assert model.bundle_mapping == model._data["bundle_mapping"]
    assert model.check_related_images == model._data["check_related_images"]
    assert model.from_index == model._data["from_index"]
    assert model.from_index_resolved == model._data["from_index_resolved"]
    assert model.index_image == model._data["index_image"]
    assert model.internal_index_image_copy == model._data["internal_index_image_copy"]
    assert (
        model.internal_index_image_copy_resolved
        == model._data["internal_index_image_copy_resolved"]
    )
    assert model.removed_operators == model._data["removed_operators"]
    assert model.organization == model._data["organization"]
    assert model.omps_operator_version == model._data["omps_operator_version"]
    assert model.distribution_scope == model._data["distribution_scope"]
    assert model.deprecation_list == model._data["deprecation_list"]


def test_rm_model_attributes(fixture_rm_build_details_json):
    model = RmModel.from_dict(fixture_rm_build_details_json)

    assert model.binary_image == model._data["binary_image"]
    assert model.binary_image_resolved == model._data["binary_image_resolved"]
    assert model.bundles == model._data["bundles"]
    assert model.bundle_mapping == model._data["bundle_mapping"]
    assert model.from_index == model._data["from_index"]
    assert model.from_index_resolved == model._data["from_index_resolved"]
    assert model.index_image == model._data["index_image"]
    assert model.internal_index_image_copy == model._data["internal_index_image_copy"]
    assert (
        model.internal_index_image_copy_resolved
        == model._data["internal_index_image_copy_resolved"]
    )
    assert model.removed_operators == model._data["removed_operators"]
    assert model.organization == model._data["organization"]
    assert model.distribution_scope == model._data["distribution_scope"]
    assert model.deprecation_list == model._data["deprecation_list"]


def test_regenerate_bundle_model_attributes(
    fixture_regenerate_bundle_build_details_json,
):
    model = RegenerateBundleModel.from_dict(
        fixture_regenerate_bundle_build_details_json
    )

    assert model.bundle_image == model._data["bundle_image"]
    assert model.from_bundle_image == model._data["from_bundle_image"]
    assert model.from_bundle_image_resolved == model._data["from_bundle_image_resolved"]
    assert model.organization == model._data["organization"]


def test_merge_index_image_model_attributes(
    fixture_merge_index_image_build_details_json,
):
    model = MergeIndexImageModel.from_dict(fixture_merge_index_image_build_details_json)

    assert model.binary_image == model._data["binary_image"]
    assert model.binary_image_resolved == model._data["binary_image_resolved"]
    assert model.deprecation_list == model._data["deprecation_list"]
    assert model.distribution_scope == model._data["distribution_scope"]
    assert model.index_image == model._data["index_image"]
    assert model.source_from_index == model._data["source_from_index"]
    assert model.source_from_index_resolved == model._data["source_from_index_resolved"]
    assert model.target_index == model._data["target_index"]
    assert model.target_index_resolved == model._data["target_index_resolved"]
