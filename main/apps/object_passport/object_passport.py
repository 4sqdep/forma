from django.urls import include, path

app_name = "object_passport"


urlpatterns = [
    path(
        "object/",
        include(
            ("main.apps.object_passport.urls.object", "main.apps.object_passport.urls.object"),
            namespace="object",
        ),
    ),
path(
        "object-gallery/",
        include(
            ("main.apps.object_passport.urls.object_gallery", "main.apps.object_passport.urls.object-gallery"),
            namespace="object_gallery",
        ),
    )
]