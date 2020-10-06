class RegenerateBundleModel(object):

    _kwarttrs = ["bundle_image", "from_bundle_image", "from_bundle_image_resolved"]

    @classmethod
    def from_dict(cls, data):
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
