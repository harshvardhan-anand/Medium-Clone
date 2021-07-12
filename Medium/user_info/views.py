from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import CreateUserForm
# from django.contrib.auth.models import User
from .models import Person, Membership
from django.views.generic.base import RedirectView
from django.http import HttpResponseRedirect
from .utils import create_activity
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Activity
from django.conf import settings
from django.views.generic.base import ContextMixin, TemplateView
from .signals import create_membership_signal
# Create your views here.

class CreateUser(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy('user_info:login')
    template_name = 'registration/user_registration.html'

    def form_valid(self, form):
        result = super().form_valid(form)  # at this point form.save() statement is executed, i.e user is created but it does not have any password
        cd = form.cleaned_data
        print(cd)
        user = get_object_or_404(Person, username=cd['username'])
        user.set_password(cd['password1'])
        user.save()
        return result
    
class AuthenticatedUser(View, LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            if self.request.user.is_authenticated:
                return super().dispatch(request, *args, **kwargs)
            else:
                return LoginRequiredMixin.dispatch(self, request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

class FollowUser(AuthenticatedUser):
    # To Create FOllow system
    def post(self,*args, **kwargs):
        action = self.request.POST.get('action')
        user_to_be_followed = get_object_or_404(Person, username=self.kwargs['username'])
        user_profile_to_be_followed = get_object_or_404(Profile, user__username=self.kwargs['username'])
        user_profile = Profile.objects.get(user__username=self.request.user) # The Person who want to follow
        print(action)
        if action=='followed':
            user_profile.following.add(user_to_be_followed)
        else:
            user_profile.following.remove(user_to_be_followed)
        create_activity(
            user = self.request.user,
            action = action,
            target=user_profile_to_be_followed,
            action_type='follow'
        )
        return HttpResponseRedirect(reverse_lazy(
            'user_info:authorbio', 
            kwargs={
                'username':self.kwargs['username']
            }
        ))

class AuthorBio(DetailView, FollowUser):
    model = Person
    context_object_name = 'author'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'bio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(Person, username=self.kwargs['username'])
        print(self.request.user.username)
        print(type(context["user"].username), type(self.request.user.username))
        return context

class Notifications(LoginRequiredMixin, ListView):
    template_name = 'notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        x = Activity.objects.filter(profile=self.request.user.profile, action_type='follow')
        return x


class MembershipView(LoginRequiredMixin, TemplateView):

    # render_To_response take the context and render it to template
    # If you get error like "post or get returned None" then render 
    # the context on the given template using render_to_response method    

    template_name = 'membership.html'
    
    def post(self, *args, **kwargs):
        nonce = self.request.POST.get('nonce')
        result = settings.GATEWAY.transaction.sale({
            "amount": "5",
            "payment_method_nonce": nonce,
            "options": {
            "submit_for_settlement": True
            }
        })
        print(result.is_success)
        if result.is_success:
            transaction = result.transaction
            # print(transaction)
            # print(dir(transaction))
            create_membership_signal.send(sender=Membership, user=self.request.user, transaction=transaction)

        context = self.get_context_data(**kwargs)
        return HttpResponseRedirect(reverse_lazy("blog:Home"))                                   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_token'] = settings.GATEWAY.client_token.generate()
        return context
           