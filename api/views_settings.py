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
        description="Returns settings editable in admin. Currently only header_title.",
    )
    def get(self, request):
        setting = SiteSetting.objects.first()
        title = setting.header_title if setting else "Авитолог"
        return Response({"header_title": title})
