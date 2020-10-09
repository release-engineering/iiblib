from .iib_build_details_model import IIBBuildDetailsModel


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
            self._items == other._items  # can I rather use function self.items?
            and self.iibclient == other.iibclient
            and self.meta == other.meta
        )
