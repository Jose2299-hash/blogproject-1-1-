from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

def registro(request):

    if request.method == 'GET':
        return render(request, 'registro.html',{
            'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #registrarusuario  
            try:
                user = User.objects.create_user(username=request.POST['username'], 
                password=request.POST['password1']) 
                user.save()
                login(request, user)
                return redirect('blogapp:login')
            except IntegrityError:
                return render(request, 'registro.html',{
                    'form': UserCreationForm,
                    "Error": 'El Usuario ya existe'
                })
        return render(request, 'registro.html',{
                    'form': UserCreationForm,
                    "Error": 'Las contrase;as no coinciden'
                })

def inicio_sesion(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'login.html',{
                'form': AuthenticationForm,
                'Error': 'nombre de ususario o contrase;a incorrectos'
                })
        else:
            login(request,user)
            return redirect('blogapp:blog_list')

def Cerrar_sesion(request):
    logout(request)
    return redirect('blogapp:blog_list')

class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})



class ReviewCreateView(CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})


class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blogapp/comment_form.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})

