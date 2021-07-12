from django.views.generic import ListView
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from .models import Post, Tag, Comment, Clap
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.base import RedirectView, TemplateView
from user_info.models import Profile, Activity
from .signals import profile_create_signal
from django.http import HttpResponseRedirect
from user_info.models import Profile
import numpy as np
from faker import Faker
from django.db.models import F
# Create your views here.

def test(request):
    # raise Exception('Not Allowed To view')
    all_tags = ['Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5', 'Tag6', 'Tag7', 'Tag8', 'Tag9', 'Tag10']
    tag_finder = lambda : [np.random.choice(all_tags) for _ in range(4)]
    Faker.seed(589)
    faker = Faker()    
    for _ in range(200):
        username=faker.profile().get('username')
        password='123'
        user = User.objects.create_user(username=username, password=password)
        title = faker.sentence()
        slug = title.replace(' ', '-').replace('.', '')
        body = faker.paragraph(nb_sentences=20)
        post = Post(title=title, author=user, body=body, status=np.random.choice(['draft', 'published']), slug=slug, total_claps=np.random.randint(1, 2000))

        try:
            user.save()
            post.save()
        except:
            print('passed', end='\t')
            pass
        profile_create_signal.send(sender=Profile, user=user, target=post)

        tag_obj = [Tag.objects.get_or_create(tag=tag)[0] for tag in tag_finder()]
        post.tags.add(*tag_obj)
        print(_)
    return HttpResponse('Done')

# Create your views here.

# Redirect authenticated user to some other view
# https://stackoverflow.com/a/51284713
class PersonalizedContent(View):
    '''
    If user is authenticated then redirect to other view
    to show personalized content else redirect to Home 
    '''
    def dispatch(self, request, *args, **kwargs):
        # print(dir(self.request.user))
        if self.request.user.is_authenticated:
            self.authenticated_user = True
        else:
            self.authenticated_user = False
        return super().dispatch(request, *args, **kwargs)

class Home(PersonalizedContent,ListView):
    context_object_name = 'all_posts'
    template_name = 'post_list_home_nologin.html'

    def get_context_data(self, **kwargs):
        # provide 9 topics/tags for anonymous users.
        context = super().get_context_data(**kwargs)
        # print(dir(self.request.user))
        if self.authenticated_user:
        # Topics/ tags person follow
            context['other_posts'] = Post.objects.exclude(status='draft').exclude(author__id__in=self.following_ids).exclude(author=self.request.user).exclude(tags__tag__in=self.following_tags).select_related('author')
        context["tags"] = Tag.objects.all()[:9]
        # context['info'] = self.request.META
        return context

    
    def get_queryset(self):
        # providing 6 trending post to anonymous user
        # provide 10 trending posts to anonymous user except the above 6
        if self.authenticated_user:  # Posts from creator user follow
            if self.request.user.profile.following.exists() or self.request.user.profile.tags.exists():
                self.following_ids = self.request.user.profile.following.values_list('id', flat=True)
                self.following_tags = self.request.user.profile.tags.values_list('tag', flat = True)
                posts_from_following = Post.objects.filter(author__id__in=self.following_ids, status='published').select_related('author')
                posts_from_following_tags = Post.objects.exclude(author__id__in=self.following_ids).exclude(author=self.request.user).filter(tags__tag__in = self.following_tags, status='published').select_related('author')
                return (posts_from_following | posts_from_following_tags).distinct()
            return Post.objects.filter(status='published')[:16]  # if user has not followed either person or tag then show him random posts
        else:
            return Post.objects.filter(status='published')[:16]

    def get_template_names(self):
        if self.authenticated_user:
            return ['post_list_home_login.html']
        else:
            return ['post_list_home_nologin.html']

# How to look with other attributes than pk and slug in DetailView
# https://stackoverflow.com/a/43730657
class CreateBookmarkCommentClap(LoginRequiredMixin, View):

    def create_comment(self, data, post):
        Comment.objects.create(
            user = self.request.user, 
            post = post, 
            comment = data.get('comment')
        )

    def post(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        user_profile = get_object_or_404(Profile, user=self.request.user)
        if self.request.POST.get('action')=='bookmark':
            self.request.user.profile.bookmark.add(post)
        elif self.request.POST.get('action')=='unbookmark':
            self.request.user.profile.bookmark.remove(post)
        elif self.request.POST.get('action')=='clap':
            clap_obj, _ = Clap.objects.get_or_create(user=self.request.user, post=post)
            clap_obj.claps_given=F('claps_given')+1
            post.total_claps=F('total_claps')+1
            clap_obj.save()
            post.save() 
            clap_obj.refresh_from_db()
            post.refresh_from_db()
        elif self.request.POST.get('action')=='comment':
            data = self.request.POST
            print(data)
            self.create_comment(data, post)

        return HttpResponseRedirect(reverse_lazy('blog:post_detail',
                                kwargs={'author':self.kwargs.get('author'), 'pk':self.kwargs.get('pk'), 'slug':self.kwargs.get('slug')}))
                                

class PostDetail(DetailView, CreateBookmarkCommentClap):
    model = Post
    login_url = 'user_info:login'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.object)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.method=='POST':
            return CreateBookmarkCommentClap.dispatch(self, request, *args, **kwargs)
        return DetailView.dispatch(self,request, *args, **kwargs)
    


class FollowTagMixin(View,LoginRequiredMixin):

    login_url = 'user_info:login'

    def dispatch(self, request, *args, **kwargs):
        if request.method=='POST':
            if self.request.user.is_authenticated:
                # return self.post(*args, **kwargs)  # any of the statement can be executed(line - 89 or 90). Both are same.
                return View.dispatch(self, request, *args, **kwargs)
            else:
                return LoginRequiredMixin.dispatch(self, request,*args, **kwargs)
        # return self.get(self, request, *args, **kwargs) # any of the statement can be executed(line - 93 or 94). Both are same.
        return View.dispatch(self, request, *args, **kwargs)

    def post(self, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user__username=self.request.user)
        tag = get_object_or_404(Tag, tag=self.kwargs.get('tag'))
        if self.request.POST.get('action') == 'follow':
            user_profile.tags.add(tag)
        else:
            user_profile.tags.remove(tag)
        return HttpResponseRedirect(reverse_lazy('blog:TagRelatedPost', kwargs={'tag':self.kwargs.get('tag')}))
    

class TagRelatedPost(ListView, FollowTagMixin):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_filter_tag.html'

    def get_queryset(self):
        tag = self.kwargs.get('tag') # this tag is written in url <str:tag>
        all_posts = Post.objects.select_related('author').filter(tags__tag=tag) # Huge Optimization from 24ms to 2ms
        return all_posts
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["tag_obj"] = get_object_or_404(Tag, tag=self.kwargs.get('tag'))
        context["tag"] = self.kwargs.get('tag')
        return context

class PrintToPDF(TemplateView):
    template_name = 'pdf.html'
