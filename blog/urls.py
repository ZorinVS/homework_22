from blog import views
from blog.apps import BlogConfig
from django.urls import path

app_name = BlogConfig.name

urlpatterns = [
    path("create/", views.ArticleCreateView.as_view(), name="article_create"),
    path("publications/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/update/", views.ArticleUpdateView.as_view(), name="article_update"),
    path("<int:pk>/delete/", views.ArticleDeleteView.as_view(), name="article_delete"),
    path("<str:status>/", views.ArticleListView.as_view(), name="article_list"),
]
