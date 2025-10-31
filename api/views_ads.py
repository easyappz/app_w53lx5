from typing import Any, Dict

from django.db.models import F, Case, When, IntegerField
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import (
    AdModelSerializer,
    AdsQuerySerializer,
    ResolveSerializer,
)
from .avito import fetch_avito_data
from .models import Ad


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
                    "results": AdModelSerializer(many=True),
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

        qs = Ad.objects.all()

        # Category filter: empty/"Все"/"All" means no filter
        if category is not None:
            cat_norm = (category or "").strip().lower()
            if cat_norm and cat_norm not in ("все", "all"):
                qs = qs.filter(category__iexact=category.strip())

        if sort == "date":
            # Order by published_at DESC with nulls last, then created_at DESC
            qs = qs.annotate(
                pub_is_null=Case(
                    When(published_at__isnull=True, then=1),
                    default=0,
                    output_field=IntegerField(),
                )
            ).order_by("pub_is_null", "-published_at", "-created_at")
        else:
            qs = qs.order_by("-view_count")

        total = qs.count()
        results = list(qs[offset: offset + limit])
        data = AdModelSerializer(results, many=True).data
        return Response({
            "count": total,
            "limit": limit,
            "offset": offset,
            "results": data,
        })


class ResolveAdView(APIView):
    """Resolve by Avito URL: return existing or create new ad in DB."""

    @extend_schema(
        request=ResolveSerializer,
        responses={200: AdModelSerializer, 201: AdModelSerializer, 400: {"type": "object", "properties": {"detail": {"type": "string"}}}},
        description="If ad with given source URL exists, return it; otherwise fetch from Avito and create a new ad.",
    )
    def post(self, request):
        serializer = ResolveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data["url"].strip()

        existing = Ad.objects.filter(source_url=url).first()
        if existing:
            return Response(AdModelSerializer(existing).data, status=status.HTTP_200_OK)

        fetched = fetch_avito_data(url) or {}
        title = fetched.get("title")
        image_url = fetched.get("image_url")
        category = fetched.get("category") or "Без категории"

        # Parse published_at ISO string
        published_at = None
        fetched_published = fetched.get("published_at")
        if isinstance(fetched_published, str) and fetched_published:
            try:
                from datetime import datetime, timezone as dt_tz
                v = fetched_published
                if v.endswith("Z"):
                    v = v[:-1] + "+00:00"
                dt = datetime.fromisoformat(v)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=dt_tz.utc)
                published_at = dt.astimezone(dt_tz.utc)
            except Exception:
                published_at = None

        new_ad = Ad.objects.create(
            source_url=url,
            title=title,
            image_url=image_url,
            published_at=published_at,
            category=category,
            view_count=0,
        )
        return Response(AdModelSerializer(new_ad).data, status=status.HTTP_201_CREATED)


class AdDetailView(APIView):
    """Return an ad by id and increment its view_count."""

    @extend_schema(
        responses={200: AdModelSerializer, 404: {"type": "object", "properties": {"detail": {"type": "string"}}}},
        description="Return ad by id and increment its view_count.",
    )
    def get(self, request, ad_id: str):
        ad = Ad.objects.filter(id=ad_id).first()
        if not ad:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        Ad.objects.filter(id=ad.id).update(view_count=F("view_count") + 1, updated_at=timezone.now())
        ad_refreshed = Ad.objects.get(id=ad.id)
        return Response(AdModelSerializer(ad_refreshed).data)
