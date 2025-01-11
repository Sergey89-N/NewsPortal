from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Post


class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
    paginate_by = 10


class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'

class NewsSearchView(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q') # поиск по названию
        author = self.request.GET.get('author') # поиск по автору
        date = self.request.GET.get('date') # поиск по дате

        if query:
            queryset = queryset.filter(title__icontains=query)
        if author:
            queryset = queryset.filter(author__user__username__icontains=author)
        if date:
            queryset = queryset.filter(created_at__gte=date)

        return queryset.filter(post_type='NW').order_by('-created_at')


class NewsCreateView(CreateView):
    model = Post
    template_name = 'news/news_create.html'
    fields = ['title', 'content', 'categories'] # поля для создания новости
    success_url = reverse_lazy('news_list') # перенаправление

    def form_valid(self, form):
        form.instance.post_type = 'NW'
        form.instnce.author = self.request.user.author # устанавливаем автора
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    model = Post
    template_name = 'news/news_edit.html'
    fields = ['title', 'content', 'categories']  # поля для редактирования
    success_url = reverse_lazy('news_list')  # перенаправление


class NewsDeleteView(DetailView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreateView(CreateView):
    model = Post
    template_name = 'news/article_create.html'
    fields = ['title', 'content', 'categories']
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'AR'
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Post
    template_name = 'news/article_edit.html'
    fields = ['title', 'content', 'categories']
    success_url = reverse_lazy('news_list')


class ArticleDeleteView(DetailView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url =reverse_lazy('news_list')
