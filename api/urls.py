from django.urls import path
from .views import HelloView
from .views_auth import RegisterView, LoginView, MeView
from .views_ads import AdsListView, ResolveAdView, AdDetailView

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/me/", MeView.as_view(), name="auth-me"),

    # Ads domain
    path("ads", AdsListView.as_view(), name="ads-list"),
    path("ads/resolve", ResolveAdView.as_view(), name="ads-resolve"),
    path("ads/<str:ad_id>", AdDetailView.as_view(), name="ads-detail"),
]
