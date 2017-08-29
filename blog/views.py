from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView
from blog.forms import PostForm
from blog.models import Post, Blogger, Hidden


class OwnPosts(ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'my_posts.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OwnPosts, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(OwnPosts, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(OwnPosts, self).get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            bloggers = Blogger.objects.filter(subscriptions=request.user)
            recipients = [b.user.email for b in bloggers]

            if len(recipients) > 0:
                uri = reverse('post_detail', args=(post.user.username, post.pk))
                full_uri = request.build_absolute_uri(uri)

                send_mail('New post',
                          '{} create new post: {}'.format(
                              request.user.username,
                              full_uri),
                          EMAIL_HOST_USER,
                          recipients)

        return self.get(request, *args, **kwargs)


class Feed(ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'posts.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Feed, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(Feed, self).get_queryset()
        subscriptions = Blogger.objects.get(user=self.request.user).subscriptions.all()
        queryset = queryset.filter(user__in=subscriptions)
        hidden = Hidden.objects.filter(user=self.request.user)
        hidden = [i.post.pk for i in hidden]
        queryset = queryset.exclude(pk__in=hidden).order_by('-created')
        return queryset


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'


class Bloggers(ListView):
    model = Blogger
    paginate_by = 10
    context_object_name = 'bloggers'
    template_name = 'blogs.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Bloggers, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(Bloggers, self).get_queryset()
        return queryset.exclude(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(Bloggers, self).get_context_data(**kwargs)
        context['subscriptions'] = Blogger.objects.get(user=self.request.user).subscriptions.all()
        return context


class Subscribe(UpdateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Subscribe, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        blogger = User.objects.get(username=request.POST['user'])
        user = Blogger.objects.get(user=self.request.user)
        user.subscriptions.add(blogger)
        return redirect('bloggers')


class Unsubscribe(UpdateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Unsubscribe, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        blogger = User.objects.get(username=request.POST['user'])
        current_blogger = Blogger.objects.get(user=self.request.user)
        current_blogger.subscriptions.remove(blogger)
        Hidden.objects.filter(user=current_blogger.user, post__user=blogger).delete()
        return redirect('bloggers')


class Hide(UpdateView):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        post = Post.objects.get(pk=request.POST['post'])
        user = User.objects.get(username=self.request.user)
        Hidden(user=user, post=post).save()
        return redirect('feed')
