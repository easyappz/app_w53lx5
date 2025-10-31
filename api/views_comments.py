from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import CommentModelSerializer, CreateCommentSerializer, ErrorSerializer
from .models import Ad, Comment


@method_decorator(csrf_exempt, name='dispatch')
class CommentListCreateView(APIView):
    """
    List comments for an ad (GET) and create a comment (POST).
    Data is stored in SQLite DB.
    """

    def get_permissions(self):
        if self.request.method.lower() == "post":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="ad_id", type=str, location=OpenApiParameter.PATH, required=True),
        ],
        responses={
            200: CommentModelSerializer(many=True),
            404: ErrorSerializer,
        },
        tags=["comments"],
        summary="List comments for an ad",
        description=(
            "Return comments for given ad id, sorted by created_at ascending.\n"
            "Data is persisted in SQLite."
        ),
    )
    def get(self, request, ad_id: str):
        ad = Ad.objects.filter(id=ad_id).first()
        if not ad:
            return Response({"detail": "Ad not found"}, status=status.HTTP_404_NOT_FOUND)

        items = Comment.objects.filter(ad_id=ad.id).select_related("user").order_by("created_at")
        data = CommentModelSerializer(items, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="ad_id", type=str, location=OpenApiParameter.PATH, required=True),
        ],
        request=CreateCommentSerializer,
        responses={
            201: CommentModelSerializer,
            400: ErrorSerializer,
            401: ErrorSerializer,
            404: ErrorSerializer,
        },
        tags=["comments"],
        summary="Create a comment for an ad",
        description=(
            "Create a comment for the ad. JWT token must be provided in Authorization header (Bearer <token>).\n"
            "Comment id is UUIDv4, username is taken from token, created_at is current time in UTC.\n"
            "Text length 1..2000.\n"
            "Data is persisted in SQLite."
        ),
    )
    def post(self, request, ad_id: str):
        ad = Ad.objects.filter(id=ad_id).first()
        if not ad:
            return Response({"detail": "Ad not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateCommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not getattr(user, "is_authenticated", False):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        text = serializer.validated_data["text"]
        comment = Comment.objects.create(ad=ad, user=user, text=text)
        return Response(CommentModelSerializer(comment).data, status=status.HTTP_201_CREATED)
