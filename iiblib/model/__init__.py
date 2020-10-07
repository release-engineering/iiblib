#!/usr/bin/env python
# -*- coding: utf-8 -*-

class IIBBuildDetailsModel(object):
    """Model class handling data about index build task"""

    _data_attrs = []
    _kwattrs = []

    def __init__(self, *args, **kwargs):
        self.data = {}
        for attr, attr_val in zip(args, self._data_attrs):
            self.data[attr_val] = attr
        for key in self._kwattrs:
            self.data[key] = kwargs[key]

    @classmethod
    def from_dict(cls, data):
        if data['request_type'] == "add":
            return AddModel._from_dict(data)
        if data['request_type'] == "rm":
            return RmModel._from_dict(data)
        if data['request_type'] == "regenerate-bundle":
            return RegenerateBundleModel._from_dict(data)
        raise KeyError("Unsupported request type: %s" % data['request_type'])

    @classmethod
    def _from_dict(cls, data):
        args = []
        kwargs = {}
        for attr in cls._data_attrs:
            args.append(data[attr])
        for attr in cls._kwattrs:
            kwargs[attr] = data[attr]
        return cls(*args, **kwargs)

    def to_dict(self):
        result = []
        for key in self._data_attrs:
            result[key] = self.data[key]
        for key in self._kwattrs:
            result[key] = self.data[key]
        return result

    def __eq__(self, other):
        return isinstance(other, IIBBuildDetailsModel) and self.data == other.data


class AddModel(IIBBuildDetailsModel):
    # TODO description of data_attrs
    _data_attrs = ["arches", "id", "state", "state_reason", "request_type", "state_history", "organization"]
    _kwattrs = ["binary_image", "binary_image_resolved", "bundles", "bundle_mapping", "from_index", "from_index_resolved", "index_image",  "removed_operators"]


class RegenerateBundleModel(IIBBuildDetailsModel):
    _data_attrs = ["arches", "id", "state", "state_reason", "request_type", "state_history", "organization"]
    _kwattrs = ["bundle_image", "from_bundle_image", "from_bundle_image_resolved"]


class RmModel(IIBBuildDetailsModel):
    _data_attrs = ["arches", "id", "state", "state_reason", "request_type", "state_history", "organization"]
    _kwattrs = ["binary_image", "binary_image_resolved", "bundles", "bundle_mapping", "from_index", "from_index_resolved", "index_image",  "removed_operators"]


class IIBBuildDetailsPager(object):
    def __init__(self, iibclient, page):
        """
        Args:
            iibclient (IIBClient)
                IIBClient instance
            page (int)
                page where start listing items
        """
        self.page = page
        self.iibclient = iibclient
        self._items = []
        self.meta = {}

    def reload_page(self):
        """Reload items for current page"""

        ret = self.iibclient.get_builds(self.page, raw=True)
        self.meta = ret["meta"]
        self._items = [IIBBuildDetailsModel.from_dict(x) for x in ret["items"]]

    def next(self):
        """Load items for next page and set it as current"""

        self.page += 1
        self.reload_page()

    def prev(self):
        """Load items for previous page and set it as current"""

        if self.page > 1:
            self.page -= 1
        self.reload_page()

    def items(self):
        """Return items for current page"""
        return self._items

    @classmethod
    def from_dict(cls, iibclient, _dict):
        ret = cls(iibclient, _dict["meta"]["page"])
        ret.meta = _dict["meta"]
        ret._items = [IIBBuildDetailsModel.from_dict(x) for x in _dict["items"]]
        return ret

    def __eq__(self, other):
        return (
            self._items == other._items
            and self.iibclient == other.iibclient
            and self.meta == other.meta
        )

