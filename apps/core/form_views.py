from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ProcessFormView, FormMixin, BaseUpdateView, BaseDeleteView

from apps.core.utils import client_redirect


class HTMXFormView(LoginRequiredMixin, FormMixin, ProcessFormView):
    action_url = ''
    modal_title = 'Crear'
    modal_button = 'Crear'
    template = """
     {% component 'modal' %}
    <h3 class="text-2xl font-semibold mb-3"> {{ modal_title }} </h1>
    <form method="post" action="{% url action_url %}">
    {% for field in form %}
    {% if 'hidden' not in field.field.widget.attrs.class %}
    <div class="mb-3">{{field.label}} {{ field }} </div>
    {% endif %}
    {% endfor %}
        <button type="submit" class="btn btn-primary btn-block mt-4"> {{ modal_button }}</button>
    </form>
    {% endcomponent %}
    """

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        kwargs['action_url'] = self.action_url
        kwargs['modal_title'] = self.modal_title
        kwargs['modal_button'] = self.modal_button
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        return client_redirect('.')

    def form_invalid(self, form):
        for error_msgs in form.errors.values():
            for msg in error_msgs:
                messages.error(self.request, msg)
        return client_redirect('.')


class HTMXObjectFormView(BaseUpdateView, HTMXFormView):
    modal_title = 'Modificar'
    modal_button = 'Editar'
    template = """
      {% component 'modal' %}
     <h3> {{ modal_title }} </h1>
     <form method="post" action="{% url action_url object.pk %}">
            {% for field in form %}
    {% if 'hidden' not in field.field.widget.attrs.class %}
    <div class="mb-3">{{field.label}} {{ field }} </div>
    {% endif %}
    {% endfor %}
         <button type="submit" class="btn btn-primary btn-block mt-4">{{ modal_button }}</button>
     </form>
     {% endcomponent %}
     """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context["object"] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.object:
            kwargs.update({"instance": self.object})
        kwargs["request"] = self.request
        return kwargs

    def get_queryset(self):
        raise NotImplementedError

    def form_valid(self, form):
        self.object = form.save()
        return client_redirect('.')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class HTMXDeleteFormView(LoginRequiredMixin, BaseDeleteView):
    action_url = ''
    template = """
    {% component 'modal' %}
        Quieres eliminar {{ object.pk }}?
        <button hx-post="{% url action_url object.pk %}" class="btn btn-primary">Si</button>
    {% endcomponent %} 
    """

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        kwargs['action_url'] = self.action_url
        return kwargs

    def get_queryset(self):
        raise NotImplementedError

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        return client_redirect(success_url)
