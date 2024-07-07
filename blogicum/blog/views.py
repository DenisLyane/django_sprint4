from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm, ProfileEditForm
from .models import Category, Comment, Post, User


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', self.kwargs[self.pk_url_kwarg])


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post,
            pk=self.kwargs[self.pk_url_kwarg]
        )
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(
            Comment,
            pk=self.kwargs[self.pk_url_kwarg]
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
        )


class PostMixin(LoginRequiredMixin, OnlyAuthorMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class PostListView(ListView):
    model = Post
    queryset = Post.published.commen_count()
    paginate_by = settings.POSTS_ON_PAGE
    template_name = 'blog/index.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user.username
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': user}
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        post_individual = get_object_or_404(
            Post, pk=self.kwargs[self.pk_url_kwarg]
        )
        post_manager = Post.objects.all() if (
            post_individual.author == self.request.user
        ) else Post.published
        context['post'] = get_object_or_404(
            post_manager,
            pk=self.kwargs[self.pk_url_kwarg]
        )
        context['comments'] = self.object.comments.select_related('author')
        return context


class PostUpdateView(PostMixin, UpdateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
        )


class PostDeleteView(PostMixin, DeleteView):

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CategoryListView(ListView):
    model = Post
    paginate_by = settings.POSTS_ON_PAGE
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs[self.slug_url_kwarg],
            is_published=True
        )
        return category.posts(manager='published').order_by(
            '-pub_date'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs[self.slug_url_kwarg],
            is_published=True
        )
        return context


class ProfileListView(ListView):
    model = Post
    paginate_by = settings.POSTS_ON_PAGE
    template_name = 'blog/profile.html'

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        post_manager = Post.objects if (
            self.author == self.request.user
        ) else Post.published

        return post_manager.filter(author=self.author).commen_count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentCreateView(CommentMixin, CreateView):
    pk_url_kwarg = 'post_id'


class CommentUpdateView(CommentMixin, OnlyAuthorMixin, UpdateView):
    pk_url_kwarg = 'comment_id'


class CommentDeleteView(CommentMixin, OnlyAuthorMixin, DeleteView):
    pk_url_kwarg = 'comment_id'
