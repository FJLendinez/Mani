from django.core.paginator import Paginator
from django_components import component


@component.register('base_table')
class BaseTableComponent(component.Component):
    headings = []
    fields = []
    template_name = 'table/base_table.html'

    def get_context_data(self, **kwargs):
        context = {**kwargs}
        queryset = context['objects']
        paginator = Paginator(queryset, 10)
        page = context['request'].GET.get('page')
        page_obj = paginator.get_page(page)
        context['data'] = [[f(o) for f in context['fields']] for o in page_obj.object_list]
        context['page'] = page_obj
        return context
