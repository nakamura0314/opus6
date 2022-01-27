from django.contrib import admin
from blog.models import Article

# models.pyで作ったモデルを指定すると、
# adminサイトのデータベースで管理することができる
admin.site.register(Article)
