from django.db import models

# モデルを更新したらマイグレーションすること


class Article(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    # auto_now_add=Trueとすることで、データが登録された日時を自動的に保存する
    posted_at = models.DateTimeField(auto_now_add=True)
    # auto_now=Trueとすることで、データが更新された日時を自動的に保存する
    last_modify = models.DateTimeField(auto_now=True)
    # IntegerFieldは数値を保存する、いいねの数
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    # コメント本文
    text = models.TextField()
    # コメント投稿日時
    posted_at = models.DateTimeField(auto_now_add=True)
    """ForeignKeyは、1対多のリレーションを持つモデルを構築する
    また、ForeignKeyでは異なるモデルが親子関係になり、ForeignKeyは、子側に設定する
    to=クラス名とすることで、どのクラスの要素に対してリレーションを持つかを指定できる
    related_name='comments'は、Articleクラスから逆参照するための逆引き用の名前
    on_delete=models.CASCADEは、削除の時の振る舞い
    CASCADEは、参照先の記事が削除された際に、その記事に対するコメントも削除をする"""
    article = models.ForeignKey(
        to=Article, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
