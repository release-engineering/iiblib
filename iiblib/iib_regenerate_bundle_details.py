class RegenerateBundleModel(object): # TODO maybe a new file

    _data_attrs = ["arches", "id", "state", "state_reason", "request_type", "state_history"]
    _kwarttrs = ["bundle_image", "from_bundle_image", "from_bundle_image_resolved", "organization"]

    @classmethod
    def from_dict(cls, data): # TODO na zaklade request type ne class
        return cls(
            data["arches"],
            data["id"],
            data["state"],
            data["state_reason"],
            data["request_type"],
            data["state_history"],
            data["bundle_image"],
            data["from_bundle_image"],
            data["from_bundle_image_resolved"],
            data["organization"],
        )
