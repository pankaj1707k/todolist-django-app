from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

from .forms import TaskCreationForm, UserLoginForm, UserRegisterForm


class HomeView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "tOdO | Home"
        return context


class RegisterView(TemplateView):
    template_name = "main/register.html"
    form_class = UserRegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "tOdO | Register"
        return context

    def get(self, request):
        form = self.form_class()
        context = self.get_context_data()
        context.update({"form": form})
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have been registered! Login now!")
            return redirect("home")
        context = self.get_context_data()
        context.update({"form": form})
        return render(request, self.template_name, context)


class LoginView(TemplateView):
    template_name = "main/login.html"
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "tOdO | Login"
        return context

    def get(self, request):
        form = self.form_class()
        context = self.get_context_data()
        context.update({"form": form})
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Successfully logged in")
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials")
        context = self.get_context_data()
        context.update({"form": form})
        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class TaskCreationView(LoginRequiredMixin, TemplateView):
    form_class = TaskCreationForm
    template_name = "main/add_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "tOdO | Add Task"
        return context

    def get(self, request):
        form = self.form_class()
        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            messages.success(request, "Task added")
            return redirect("home")
        context = self.get_context_data()
        context.update({"form": form})
        return render(request, self.template_name, context)


class TaskListView(LoginRequiredMixin, TemplateView):
    template_name = "main/pending_tasks.html"

    def get(self, request):
        tasks = Task.objects.filter(user=self.request.user, completed=False)
        context = super().get_context_data()
        context.update({"title": "tOdO | Pending", "tasks": tasks})
        return render(request, self.template_name, context)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "main/edit_task.html"
    model = Task
    form_class = TaskCreationForm
    success_url = "/tasks/pending/"
