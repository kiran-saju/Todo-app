from django.views.generic.list import ListView
from todoapp.models import Task
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'Task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Task'] = context['Task'].filter(user=self.request.user)
        context['count'] = context['Task'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['Task'] = context['Task'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context

    

    

class TaskDetails(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name= 'Task'
    template_name='todoapp/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description']
    success_url= reverse_lazy('task')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)
    

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model =Task
    fields =['title','description','complete']
    success_url =reverse_lazy('task')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name ='task'
    success_url =reverse_lazy('task')

class CustomLoginView(LoginView):
    template_name='todoapp/login.html'
    fields='__all__'
    redirect_authenticated_user=False
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(CustomLoginView,self).get(*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('task')
    
#logout code
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    


class RegisterPage(FormView):
    template_name='todoapp/register.html'
    form_class= UserCreationForm
    redirect_authenticated_user= True
    success_url =reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage,self).get(*args,**kwargs)


    
