from django.shortcuts import render, redirect
from django.http import Http404
from django.http.response import JsonResponse
from . import models


def index(request):
    # templates以下のパスを書く(アプリケーション名[blog] / ファイル名[index.html])
    template_name = "blog/index.html"
    """
    render(受け取った第一引数,表示させたいhtmlファイルへのパス)
    第一引数にはこの関数に渡されているHttpRequest
    第二引数はテンプレート名
    第三引数にはテンプレート側に渡す値をまとめた辞書が返される

    クラスベースのビュー
    from django.views.generic import TemplateView

    class index(TemplateView):
    template_name = "blog/index.html" # templates以下のパスを書く
    """
    return render(request, template_name)


def new(request):
    template_name = "blog/new.html"
    # リクエストされたhttpのメソッドがPOSTだった場合
    if request.method == "POST":
        # POSTしたデータはrequestの中に、辞書のような形で格納されている
        # HTMLファイルで指定したname属性を使って、データを呼び出す
        # POSTされたデータは自動的に保存されるわけではない
        # そのため、下記のようにして、データベースへの新規登録
        article = models.Article.objects.create(
            # 下記だと、request.POSTされたtitleというデータを取り出し、titleという変数に格納する
            title=request.POST["title"], text=request.POST["text"])
        """または下記のようにしても可能
        article = models.Article()
        article.title = "新規データの登録テスト"
        article.text = "テスト。テスト。"
        article.save()　~ここで保存してる~"""
        return redirect(view_article, article.pk)
    return render(request, template_name)


# 変数という形で、htmlファイルにデータを渡す
def article_all(request):
    template_name = "blog/article_all.html"
    # htmlファイルでは、{{ articles }}とすることで、
    # models.Article.object.all()のデータを受け取る
    context = {"articles": models.Article.objects.all()}
    # 第三引数に辞書を渡す
    return render(request, template_name, context)


# 第二引数のpkとは、urls.pyの<int:pk>にマッチした数字が入る
def view_article(request, pk):
    template_name = "blog/view_article.html"
    """
    try:
        例外が発生するかもしれないが、実行したい処理
    except エラー名:
        例外発生時に行う処理
    """
    try:
        # models.pyから特定のデータをpkで指定して取得
        # get(pk=pk)では、種キーを利用して記事のデータを取得
        article = models.Article.objects.get(pk=pk)
    # 記事が見当たらなかったときに、ページがないというエラーを出す
    except models.Article.DoesNotExixt:
        # raiseでエラーを指定
        raise Http404
    if request.method == "POST":
        # データベースに投稿されたコメントを保存
        models.Comment.objects.create(
            text=request.POST["text"], article=article)
    context = {"article": article}
    return render(request, template_name, context)


def edit(request, pk):
    template_name = "blog/edit.html"
    try:
        article = models.Article.objects.get(pk=pk)
    except models.Article.DoesNotExist:
        raise Http404
    if request.method == "POST":
        article.title = request.POST["title"]
        article.text = request.POST["text"]
        article.save()
        """
        redirect関数は、別のページに転移する
        そのため、第一引数に転移させたいページのview関数をとる
        第二引数以降は、redirectするページに渡すための引数
        """
        return redirect(view_article, pk)
    context = {"article": article}
    return render(request, template_name, context)


def delete(request, pk):
    try:
        article = models.Article.objects.get(pk=pk)
    except models.Article.DoesNotExist:
        raise Http404
    article.delete()
    return redirect(article_all)


def like(request, pk):
    try:
        article = models.Article.objects.get(pk=pk)
    except models.Article.DoesNotExist:
        raise Http404
    article.like += 1  # ここでいいねを増やす
    article.save()
    return redirect(view_article, pk)


def api_like(request, pk):
    try:
        article = models.Article.objects.get(pk=pk)
    except models.Article.DoesNotExist:
        raise Http404
    article.like += 1
    article.save()
    """
    post = request.user.get_username()
    if post in article.readtext:
        return redirect('like')
    else:
        article.like += 1
        article.goodtext = article.goodtext+" "+post
        article.save()
    """

    # JsonResponseでJson形式のデータを送っている
    return JsonResponse({"like": article.like})
