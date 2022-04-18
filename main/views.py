from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views import View
from .forms import UserRegisterForm


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
            return redirect("home")
        context = self.get_context_data()
        context.update({"form": form})
        return render(request, self.template_name, context)
