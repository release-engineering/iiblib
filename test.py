from iiblib.iibclient import IIBClient, IIBKrbAuth
import gssapi
import gssapi_console
import json


auth = IIBKrbAuth("jluza@REDHAT.COM", gssapi_name_type=gssapi.NameType.user)
iibc = IIBClient("iib.engineering.redhat.com", auth=auth, ssl_verify=False)
print(
    json.dumps(
        iibc.get_build(3, raw=True), indent=4, sort_keys=True, separators=(", ", ": ")
    )
)
