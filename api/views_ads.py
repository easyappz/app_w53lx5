from typing import Any, Dict

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import (
    AdSerializer,
    AdsQuerySerializer,
    ResolveSerializer,
)
from .store_ads import ads_store
from .avito import fetch_avito_data


class AdsListView(APIView):
    """List ads with sorting, filtering and pagination."""

    @extend_schema(
        parameters=[
            OpenApiParameter(name="sort", type=str, required=False, description="popular | date"),
            OpenApiParameter(name="category", type=str, required=False),
            OpenApiParameter(name="limit", type=int, required=False),
            OpenApiParameter(name="offset", type=int, required=False),
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "count": {"type": "integer"},
                    "limit": {"type": "integer"},
                    "offset": {"type": "integer"},
                    "results": AdSerializer(many=True),
                },
            }
        },
        description="Return ads list sorted by popularity or date with optional category filter.",
    )
    def get(self, request):
        query = AdsQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        sort = query.validated_data.get("sort", "popular")
        category = query.validated_data.get("category")
        limit = query.validated_data.get("limit", 20)
        offset = query.validated_data.get("offset", 0)

        items, total = ads_store.get_list(sort=sort, category=category, limit=limit, offset=offset)
        return Response({
            "count": total,
            "limit": limit,
            "offset": offset,
            "results": items,
        })


class ResolveAdView(APIView):
    """Resolve by Avito URL: return existing or create new in-memory ad."""

    @extend_schema(
        request=ResolveSerializer,
        responses={200: AdSerializer, 201: AdSerializer, 400: {"type": "object", "properties": {"detail": {"type": "string"}}}},
        description="If ad with given source URL exists, return it; otherwise fetch from Avito and create a new in-memory ad.",
    )
    def post(self, request):
        serializer = ResolveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data["url"]

        ad_dict, created = ads_store.resolve(url, fetch_avito_data)
        return Response(ad_dict, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class AdDetailView(APIView):
    """Return an ad by id and increment its view_count."""

    @extend_schema(
        responses={200: AdSerializer, 404: {"type": "object", "properties": {"detail": {"type": "string"}}}},
        description="Return ad by id and increment its view_count.",
    )
    def get(self, request, ad_id: str):
        ad_dict = ads_store.get_and_increment(ad_id)
        if not ad_dict:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ad_dict)
