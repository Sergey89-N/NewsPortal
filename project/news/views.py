from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group, User
from .models import Post
from django.shortcuts import get_object_or_404, render, redirect
from .models import Category
from .tasks import send_new_post_notification




# Новости
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

class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/news_create.html'
    fields = ['title', 'content', 'categories']
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.post_type = 'NW'
        form.instance.author = self.request.user.author
        return super().form_valid(form)
        send_new_post_notification.delay(self.object.pk)
        return response


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/news_edit.html'
    fields = ['title', 'content', 'categories']
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')

# Статьи
class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/article_create.html'
    fields = ['title', 'content', 'categories']
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.post_type = 'AR'
        form.instance.author = self.request.user.author
        return super().form_valid(form)
        send_new_post_notification.delay(self.object.pk)
        return response


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/article_edit.html'
    fields = ['title', 'content', 'categories']
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('news_list')

# Поиск
class NewsSearchView(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        author = self.request.GET.get('author')
        date = self.request.GET.get('date')

        if query:
            queryset = queryset.filter(title__icontains=query)
        if author:
            queryset = queryset.filter(author__user__username__icontains=author)
        if date:
            queryset = queryset.filter(created_at__gte=date)

        return queryset.filter(post_type='NW').order_by('-created_at')

# Редактирование профиля
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile_edit.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

# Стать автором
@login_required
def become_author(request):
    authors_group = Group.objects.get(name='authors')
    request.user.groups.add(authors_group)
    return redirect('news_list')

@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect('category_detail', category_id=category_id)

@login_required
def unsubscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)
    return redirect('category_detail', category_id=category_id)
