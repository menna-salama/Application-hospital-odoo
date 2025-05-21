from odoo import http # type: ignore
from odoo.http import Response # type: ignore


class HMSController(http.Controller):

    @http.route("/hms/api/test", auth="none", methods=["GET"], type="http", csrf=False)
    def test_endpoint(self):
        return Response(
            "Hello from HMS endpoint!", status=200, content_type="text/plain"
        )
