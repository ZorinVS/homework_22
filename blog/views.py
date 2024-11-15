from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Article
from .forms import ArticleForm


class ArticleListView(ListView):
    model = Article
    status_dict = {
        "publications": "Публикации",
        "drafts": "Черновики",
    }

    def get_queryset(self):
        status_key = self.kwargs.get("status")
        self.status = self.status_dict.get(status_key)
        if not self.status:
            raise Http404("Category not found")
        is_published = status_key == "publications"
        return Article.objects.filter(is_published=is_published)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = self.status
        return context


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    # fields = ["title", "body", "preview"]
    success_url = reverse_lazy("blog:article_list", kwargs={"status": "publications"})

    def form_valid(self, form):
        if self.request.POST.get("action") == "publish":
            form.instance.is_published = True
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    # fields = ["title", "body", "preview"]
    success_url = reverse_lazy("blog:article_list", kwargs={"status": "publications"})

    def form_valid(self, form):
        if self.request.POST.get("action") == "publish":
            form.instance.is_published = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:article_detail", args=[self.kwargs.get("pk")])


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("blog:article_list", kwargs={"status": "publications"})

