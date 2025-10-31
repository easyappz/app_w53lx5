from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import CommentSerializer, CreateCommentSerializer, ErrorSerializer
from .state import create_comment, list_comments
from .store_ads import ads_store


class CommentListCreateView(APIView):
    """
    List comments for an ad (GET) and create a comment (POST).
    Data is stored purely in in-process memory and is cleared on server restart.
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
            200: CommentSerializer(many=True),
            404: ErrorSerializer,
        },
        tags=["comments"],
        summary="List comments for an ad",
        description=(
            "Return comments for given ad id, sorted by created_at ascending.\n"
            "All data is kept in process memory and will be lost after server restart."
        ),
    )
    def get(self, request, ad_id: str):
        # 404 if ad does not exist
        if not ads_store.get_public(ad_id):
            return Response({"detail": "Ad not found"}, status=status.HTTP_404_NOT_FOUND)
        items = list_comments(ad_id)
        return Response(items, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="ad_id", type=str, location=OpenApiParameter.PATH, required=True),
        ],
        request=CreateCommentSerializer,
        responses={
            201: CommentSerializer,
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
            "All data is kept in process memory and will be lost after server restart."
        ),
    )
    def post(self, request, ad_id: str):
        # 404 if ad does not exist
        if not ads_store.get_public(ad_id):
            return Response({"detail": "Ad not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateCommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = getattr(request.user, "username", None)
        if not username:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        text = serializer.validated_data["text"]
        comment = create_comment(ad_id=ad_id, username=username, text=text)
        return Response(comment, status=status.HTTP_201_CREATED)
