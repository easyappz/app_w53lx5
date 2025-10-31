from django.urls import path
from .views import HelloView
from .views_auth import RegisterView, LoginView, MeView
from .views_ads import AdsListView, ResolveAdView, AdDetailView
from .views_comments import CommentListCreateView
from .views_settings import SettingsView

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/me/", MeView.as_view(), name="auth-me"),

    # Ads domain
    path("ads", AdsListView.as_view(), name="ads-list"),
    path("ads/resolve", ResolveAdView.as_view(), name="ads-resolve"),
    path("ads/<str:ad_id>", AdDetailView.as_view(), name="ads-detail"),

    # Comments (nested under ad)
    path("ads/<str:ad_id>/comments", CommentListCreateView.as_view(), name="ad-comments"),

    # Settings
    path("settings", SettingsView.as_view(), name="settings"),
]
