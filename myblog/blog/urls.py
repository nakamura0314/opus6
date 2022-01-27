from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # views.pyのindex関数を呼び出している
    path("new/", views.new, name="new"),
    path("article/all/", views.article_all, name="article_all"),
    # 特定の記事を指定して呼び出す
    path("article/<int:pk>/", views.view_article, name="view_article"),
    path("article/<int:pk>/edit/", views.edit, name="edit"),
    path("article/<int:pk>/delete/", views.delete, name="delete"),
    path("article/<int:pk>/like/", views.like, name="like"),
    # web APIにアクセスするための入り口URL
    path("api/like/<int:pk>/", views.api_like, name="api_like"),
]

"""
クラスベースの場合
path("",views.index.as_view(),name="index"),
"""
