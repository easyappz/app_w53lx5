from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import SiteSetting


class SettingsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: {"type": "object", "properties": {"header_title": {"type": "string"}}}},
        tags=["settings"],
        summary="Get site settings",
        description=(
            "Returns settings editable in admin. Currently only header_title. "
            "Response is not cached (Cache-Control: no-store, no-cache, must-revalidate, max-age=0; Pragma: no-cache; Expires: 0)."
        ),
    )
    def get(self, request):
        setting = SiteSetting.objects.first()
        title = setting.header_title if setting else "Авитолог"
        resp = Response({"header_title": title})
        resp["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp["Pragma"] = "no-cache"
        resp["Expires"] = "0"
        return resp
