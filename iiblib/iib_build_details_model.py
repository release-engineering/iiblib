class IIBBuildDetailsModel(object):
    """
    Model class handling data about index build task

    Args:
        id (int)
            An id of build
        arches (list)
            A list of architectures supported in new index image
        state (str)
            A state of build
        state_reason (str)
            A reason for state change
        request_type (str)
            A type of iib build task
        batch (int)
            A number of batches included in the request
        updated (str)
            Time when was the request updated
        user (str)
            A user kerberos (email)
        state_history (list) - optional
            A list of directories where is state, state_reason and updated
        batch_annotations (dict) - optional
            An annotation of the batch
        logs (dict) - optional
            A dictionary contains url of the log and expiration date
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

    _accepted_request_type = ""

    def __init__(self, *args, **kwargs):
        self._data = self._get_args(kwargs)

    @classmethod
    def _validate_data(cls, request_types_and_models, data):
        """
        Validate data with class accepted request type

        Args:
            request_types_and_models (dict)
                A key is request type and a value is a specific model
            data (dict)
                JSON dictionary with response data

        Raises:
            KeyError
                The request type is not defined in model
            TypeError
                The request type doesn't match with model
        Returns:
            None
        """

        if data["request_type"] not in request_types_and_models:
            raise KeyError("Unsupported request type: %s" % data["request_type"])

        if (
            cls._accepted_request_type != data["request_type"]
            and cls.__name__ != IIBBuildDetailsModel.__name__
        ):
            raise TypeError(
                "Class %s doesn't accept %s request type"
                % (cls.__name__, data["request_type"]),
            )

    @classmethod
    def from_dict(cls, data):
        """
        Create an object from a dictionary

        Args:
            data (dict)
                JSON dictionary with response data
        Returns:
            Generate a specific model (AddModel, RmModel or
            RegenerateBundleModel) and return the object
        """

        request_types_and_classes = {}
        for sub_cls in IIBBuildDetailsModel.__subclasses__():
            request_types_and_classes[sub_cls._accepted_request_type] = sub_cls

        cls._validate_data(request_types_and_classes, data)

        return request_types_and_classes[data["request_type"]](**data)

    def _get_args(self, data):
        """
        Store data in an instance  "_data" dictionary

        Args:
            data (dict)
                A dictionary with response data
        Returns:
            A dictionary which is stored in an instance _data dictionary
        """
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
        """
        Return a dictionary from the object

        Returns:
            A dictionary from the object
        """
        return self._data

    def __eq__(self, other):
        """
        Compare an instance with it's class and data stored in _data dictionary
        Args:
            other (object)
                An instance of specific model
        Returns:
            A boolean value
        """
        return isinstance(other, self.__class__) and self._data == other._data

    def __getattribute__(self, name):
        """
        Return value of the variable which is stored
        in an instance _data dictionary or as an instance variable
        Args:
            name (str)
                A name of variable
        Returns:
            An expected variable
        """

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
    AddModel class handling data from "builds/add" endpoint, and
    data from "builds" and "builds/<id>" IIB endpoints defined by
    "add" request_type.
    AddModel class inherits arguments and behaviours
    from IIBBuildDetailsModel.
    For a complete list of arguments check IIBBuildDetailsModel.

    Args:
        binary_image (str)
            A reference of binary image used for rebuilding
        binary_image_resolved (str)
            A checksum reference of binary image that was used for rebuilding
        bundles (list)
            A list of bundles to be added to index image
        bundle_mapping (dict)
            Operator names in "bundles" map to: list of "bundles" which map to the operator key
        from_index (str)
            A reference of index image used as source for rebuild
        from_index_resolved (str)
            A reference of new index image
        index_image (str)
            A reference of index image to rebuild
        removed_operators (list)
            A list of operators to be removed from index image
        organization (str)
            A name of organization to push to in the legacy app registry
        omps_operator_version (dict)
            An operator version returned from OMPS API call used for Add request
        distribution_scope (str)
            A distribution where is the product used (prod, stage, etc.)
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

    _accepted_request_type = "add"


class RmModel(IIBBuildDetailsModel):
    """
    RmModel class handling data from "builds/rm" endpoint, and
    data from "builds" and "builds/<id>" IIB endpoints defined by
    "rm" request_type .
    RmModel class inherits arguments from IIBBuildDetailsModel.
    For a complete list of arguments check IIBBuildDetailsModel.

    Args:
        binary_image (str)
            A reference of binary image used for rebuilding
        binary_image_resolved (str)
            A checksum reference of binary image that was used for rebuilding
        bundles (list)
            A list of bundles to be added to index image
        bundle_mapping (dict)
            Operator names in "bundles" map to: list of "bundles" which map to the operator key
        from_index (str)
            A reference of index image used as source for rebuild
        from_index_resolved (str)
            A reference of new index image
        index_image (str)
            A reference of index image to rebuild
        removed_operators (list)
            A list of operators to be removed from index image
        organization (str)
            A name of organization to push to in the legacy app registry
        distribution_scope (str)
            A distribution where is the product used (prod, stage, etc.)
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

    _accepted_request_type = "rm"


class RegenerateBundleModel(IIBBuildDetailsModel):
    """
    RegenerateBundleModel class handling data from
    "builds/regenerate-bundle" endpoint, and data from "builds"
    and "builds/<id>" IIB endpoints defined by
    "regenerate-bundle" request_type.
    RegenerateBundleModel class inherits arguments from
    IIBBuildDetailsModel.
    For a complete list of arguments check IIBBuildDetailsModel.

    Args:
        bundle_image (str)
            A reference of bundle image to rebuild
        from_bundle_image (str)
            A reference of bundle image used as source for rebuild
        from_bundle_image_resolved (str)
            A reference of new bundle image
        organization (str)
            A name of organization to push to in the legacy app registry
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

    _accepted_request_type = "regenerate-bundle"
