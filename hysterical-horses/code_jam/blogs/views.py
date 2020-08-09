import random

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView
from users.mixins import level_check

from .filters import PostFilter
from .forms import CommentForm, CreatePostForm
from .models import Comment, Post


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog_detail', args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = 'blogs_list.html'

    filterset_class = PostFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(
            self.request.GET, queryset=queryset
        )
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class BlogDetailView(DetailView):
    model = Post
    template_name = "blog_detail.html"

    def get_parent_id(self):
        """
        If the comment is sent via the reply version of the comment form,
        the form will be sent with a hidden input that is named 'parent_id'
        and has the value of the head comment.
        """
        try:
            parent_id = int(self.request.POST.get('parent_id'))
        except Exception as e:
            print(e)
            parent_id = None

        return parent_id

    def post(self, request, *args, **kwargs):
        print("POST METHOD RUNNING")

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            self.object = self.get_object()  # Required for context data
            context = super(BlogDetailView, self).get_context_data(**kwargs)
            comment_post = context['post']

            # If it is a reply comment, add parent_obj
            if parent_id := self.get_parent_id():
                new_comment = comment_form.save(commit=False)

                parent_obj = Comment.objects.get(id=parent_id)
                new_comment.parent = parent_obj

            new_comment = comment_form.save(commit=False)
            new_comment.post = comment_post
            new_comment.author = request.user
            new_comment.save()  # Save to database
            return HttpResponseRedirect(self.request.path_info)  # Refresh

    def get_context_data(self, **kwargs):
        """Runs when GET is called."""
        print("CONTEXT DATA RUNNING")

        context = super().get_context_data(**kwargs)
        blog_post = context['post']

        # Comments
        comments = blog_post.comments.filter(
            active=True, parent__isnull=True
        )  # Non-reply comments only
        context['comments'] = comments

        # Comment form
        comment_form = CommentForm()
        context['comment_form'] = comment_form

        # Total likes
        context['total_likes'] = blog_post.total_likes
        return context


# @login_required()
# def create_post(request):
#     form = CreatePostForm(request.POST or None)
#
#     if form.is_valid():
#         form.title = request.POST.get('title')
#         form.content = request.POST.get('content')
#         new_post = form.save(commit=False)
#
#         new_post.author = request.user
#         new_post.save()
#
#         return HttpResponseRedirect(request.path_info)
#
#     quote = random.choice((  # Remove this if necessary
#         "Unleash your creativity!",
#         "What's on your mind?",
#         "Say 'Hello, world!'"
#     ))
#
#     context = {
#         'form': form,
#         'quote': quote
#     }
#     return render(request, 'posts/create_post.html', context)

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def test_func(self):
        return level_check(self.request.user, unlock=5)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        return redirect("dashboard-index")
