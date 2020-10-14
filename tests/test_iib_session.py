from mock import patch

from iiblib.iib_session import IIBSession


@patch("requests.Session.get")
@patch("requests.Session.post")
@patch("requests.Session.put")
@patch("requests.Session.delete")
def test_iib_session_methods(patched_delete, patched_put, patched_post, patched_get):
    iibs = IIBSession("fake-host")
    iibs.get("fake-end-point")
    iibs.post("fake-end-point")
    iibs.put("fake-end-point")
    iibs.delete("fake-end-point")

    patched_get.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
    patched_post.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
    patched_put.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
    patched_delete.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
