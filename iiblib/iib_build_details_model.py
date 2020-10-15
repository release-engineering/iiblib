class IIBBuildDetailsModel(object):
    """
    Model class handling data about index build task

    Args:
        id (int)
            Id of build
        arches (list)
            List of architectures supported in new index image
        state (str)
            State of build
        state_reason (str)
            Reason for state change
        request_type (str)
            Type of iib build task
        batch (int)
            Number of batches included in the request
        updated (str)
            Time when was the request updated
        user (str)
            User kerberos (email)
        state_history (list) - optional
            List of directories where is state, state_reason and updated
        batch_annotations (dict) - optional
            Annotation of the batch
        logs (dict) - optional
            Dictionary contains url of the log and expiration date
    """

    __slots__ = [
        "id",
        "arches",
        "state",
        "state_reason",
        "request_type",
        "batch",
        "updated",
        "user",
        "state_history",
        "batch_annotations",
        "logs",
        "_data",
    ]

    _general_attrs = [
        "id",
        "arches",
        "state",
        "state_reason",
        "request_type",
        "batch",
        "updated",
        "user",
    ]

    _optional_attrs = {
        "state_history": lambda: list(),
        "batch_annotations": lambda: dict(),
        "logs": lambda: dict(),
    }

    _operation_attrs = []

    def __init__(self, *args, **kwargs):
        self._data = self._get_args(kwargs)

    @classmethod
    def from_dict(cls, data):
        if data["request_type"] == "add":
            return AddModel(**data)
        elif data["request_type"] == "rm":
            return RmModel(**data)
        elif data["request_type"] == "regenerate-bundle":
            return RegenerateBundleModel(**data)
        raise KeyError("Unsupported request type: %s" % data["request_type"])

    def _get_args(self, data):
        attrs = {}
        for general_attr in self._general_attrs:
            attrs[general_attr] = data[general_attr]
        for optional_attr, default_maker in self._optional_attrs.items():
            if optional_attr in data:
                attrs[optional_attr] = data[optional_attr]
            else:
                attrs[optional_attr] = default_maker()
        for operation_attr in self._operation_attrs:
            attrs[operation_attr] = data[operation_attr]
        return attrs

    def to_dict(self):
        return self._data

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._data == other._data

    def __getattribute__(self, name):
        if (
            name in object.__getattribute__(self, "_operation_attrs")
            or name in object.__getattribute__(self, "_optional_attrs")
            or name in object.__getattribute__(self, "_general_attrs")
        ):
            return object.__getattribute__(self, "_data")[name]
        else:
            return object.__getattribute__(self, name)


class AddModel(IIBBuildDetailsModel):
    """
    AddModel class handling data from builds/add endpoint, and
    data from builds and builds/<id> IIB endpoints defined by
    "add" request_type.
    AddModel class inherits arguments and behaviours
    from IIBBuildDetailsModel.
    For complete list of arguments check IIBBuildDetailsModel.

    Args:
        binary_image (str)
            Reference of binary image used for rebuilding
        binary_image_resolved (str)
            Checksum reference of binary image that was used for rebuilding
        bundles (list)
            List of bundles to be added to index image
        bundle_mapping (dict)
            Operator names in "bundles" map to: list of "bundles" which map to the operator key
        from_index (str)
            Reference of index image used as source for rebuild
        from_index_resolved (str)
            Reference of new index image
        index_image (str)
            Reference of index image to rebuild
        removed_operators (list)
            List of operators to be removed from index image
        organization (str)
            Name of organization to push to in the legacy app registry
        omps_operator_version (dict)
            Operator version returned from OMPS API call used for Add request
        distribution_scope (str)
            Distribution where is the product used (prod, stage, etc.)
    """

    __slots__ = [
        "binary_image",
        "binary_image_resolved",
        "bundles",
        "bundle_mapping",
        "from_index",
        "from_index_resolved",
        "index_image",
        "removed_operators",
        "organization",
        "omps_operator_version",
        "distribution_scope",
    ]

    _operation_attrs = [
        "binary_image",
        "binary_image_resolved",
        "bundles",
        "bundle_mapping",
        "from_index",
        "from_index_resolved",
        "index_image",
        "removed_operators",
        "organization",
        "omps_operator_version",
        "distribution_scope",
    ]


class RmModel(IIBBuildDetailsModel):
    """
    RmModel class handling data from builds/rm endpoint, and
    data from builds and builds/<id> IIB endpoints defined by
    "rm" request_type .
    RmModel class inherits arguments from IIBBuildDetailsModel.
    For complete list of arguments check IIBBuildDetailsModel.

    Args:
        binary_image (str)
            Reference of binary image used for rebuilding
        binary_image_resolved (str)
            Checksum reference of binary image that was used for rebuilding
        bundles (list)
            List of bundles to be added to index image
        bundle_mapping (dict)
            Operator names in "bundles" map to: list of "bundles" which map to the operator key
        from_index (str)
            Reference of index image used as source for rebuild
        from_index_resolved (str)
            Reference of new index image
        index_image (str)
            Reference of index image to rebuild
        removed_operators (list)
            List of operators to be removed from index image
        organization (str)
            Name of organization to push to in the legacy app registry
        distribution_scope (str)
            Distribution where is the product used (prod, stage, etc.)
    """

    __slots__ = [
        "binary_image",
        "binary_image_resolved",
        "bundles",
        "bundle_mapping",
        "from_index",
        "from_index_resolved",
        "index_image",
        "removed_operators",
        "organization",
        "distribution_scope",
    ]
    _operation_attrs = [
        "binary_image",
        "binary_image_resolved",
        "bundles",
        "bundle_mapping",
        "from_index",
        "from_index_resolved",
        "index_image",
        "removed_operators",
        "organization",
        "distribution_scope",
    ]


class RegenerateBundleModel(IIBBuildDetailsModel):
    """
    RegenerateBundleModel class handling data from
    builds/regenerate-bundle endpoint, and data from builds
    and builds/<id> IIB endpoints defined by
    "regenerate-bundle" request_type.
    RegenerateBundleModel class inherits arguments from
    IIBBuildDetailsModel.
    For complete list of arguments check IIBBuildDetailsModel.

    Args:
        bundle_image (str)
            Reference of bundle image to rebuild
        from_bundle_image (str)
            Reference of bundle image used as source for rebuild
        from_bundle_image_resolved (str)
            Reference of new bundle image
        organization (str)
            Name of organization to push to in the legacy app registry
    """

    __slots__ = [
        "bundle_image",
        "from_bundle_image",
        "from_bundle_image_resolved",
        "organization",
    ]
    _operation_attrs = [
        "bundle_image",
        "from_bundle_image",
        "from_bundle_image_resolved",
        "organization",
    ]
