from django.contrib import admin

from .models import Ad, Comment, SiteSetting


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "view_count", "published_at", "created_at")
    search_fields = ("title", "source_url", "category")
    list_filter = ("category",)
    readonly_fields = ("created_at", "updated_at", "view_count")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "ad", "user", "created_at")
    search_fields = ("text", "user__username")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("header_title",)

    def has_add_permission(self, request):  # enforce single row in admin
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)
