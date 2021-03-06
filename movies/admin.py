from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import *


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Image"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = MovieAdminForm
    readonly_fields = ("get_image",)
    actions = ["publish", "unpublish"]
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster", "get_image")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 post has been updated"
        else:
            message_bit = f"{row_update} records have been updated"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 post has been updated"
        else:
            message_bit = f"{row_update} records have been updated"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Publish"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Unpublish"
    unpublish.allowed_permissions = ('change',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="100"')

    get_image.short_description = "Image"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Image"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "movie", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Image"


admin.site.register(RatingStar)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
