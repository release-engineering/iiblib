class IIBBuildDetailsModel(object):
    """Model class handling data about index build task"""

    def __init__(
        self,
        _id,
        state,
        reason,
        state_history,
        from_index,
        from_index_resolved,
        bundles,
        removed_operators,
        organization,
        binary_image,
        binary_image_resolved,
        index_image,
        request_type,
        arches,
        bundle_mapping,
        omps_operator_version,
    ):
        """
        Args:
            _id (int)
                Id of build
            state (str)
                State of build
            state (str)
                Reason for state change
            from_index (str)
                Reference of index image used as source for rebuild
            from_index_resolved (str)
                Reference of new index image
            bundles (list)
                List of bundles to be added to index image
            removed_operators (list)
                List of operators to be removed from index image
            organization (str)
                Name of organization to push to in the legacy app registry
            binary_image (str)
                Reference of binary image used for rebuilding
            binary_image_resolved (str)
                Checksum reference of binary image that was used for rebuilding
            index_image (str)
                Reference of index image to rebuild
            request_type (str)
                Type of iib build task (add or remove)
            arches (list)
                List of architectures supported in new index image
            bundle_mapping (dict)
                Operator names in "bundles" map to: list of "bundles" which
                map to the operator key
            omps_operator_version (dict)
                Operator version returned from OMPS API call used for Add request
        """
        self.id = _id
        self.state = state
        self.reason = reason
        self.state_history = state_history
        self.from_index = from_index
        self.from_index_resolved = from_index_resolved
        self.bundles = bundles
        self.removed_operators = removed_operators
        self.organization = organization
        self.binary_image = binary_image
        self.binary_image_resolved = binary_image_resolved
        self.index_image = index_image
        self.request_type = request_type
        self.arches = arches
        self.bundle_mapping = bundle_mapping
        self.omps_operator_version = omps_operator_version

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["state"],
            data["state_reason"],
            data.get("state_history", []),
            data["from_index"],
            data["from_index_resolved"],
            data.get("bundles", []),
            data.get("removed_operators", []),
            data.get("organization"),
            data["binary_image"],
            data["binary_image_resolved"],
            data["index_image"],
            data["request_type"],
            data["arches"],
            data["bundle_mapping"],
            data.get("omps_operator_version", {}),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "state": self.state,
            "state_reason": self.reason,
            "state_history": self.state_history,
            "from_index": self.from_index,
            "from_index_resolved": self.from_index,
            "bundles": self.bundles,
            "removed_operators": self.removed_operators,
            "organization": self.organization,
            "binary_image": self.binary_image,
            "binary_image_resolved": self.binary_image_resolved,
            "index_image": self.index_image,
            "request_type": self.request_type,
            "arches": self.arches,
            "bundle_mapping": self.bundle_mapping,
            "omps_operator_version": self.omps_operator_version,
        }

    def __eq__(self, other):
        if (
            self.id == other.id
            and self.state == other.state
            and self.reason == other.reason
            and self.state_history == other.state_history
            and self.from_index == other.from_index
            and self.from_index_resolved == other.from_index_resolved
            and self.bundles == other.bundles
            and self.removed_operators == other.removed_operators
            and self.organization == other.organization
            and self.binary_image == other.binary_image
            and self.binary_image_resolved == other.binary_image_resolved
            and self.index_image == other.index_image
            and self.request_type == other.request_type
            and self.arches == other.arches
            and self.bundle_mapping == other.bundle_mapping
            and self.omps_operator_version == other.omps_operator_version
        ):
            return True
        return False
