from django_components import component


@component.register('category_row')
class CategoryRowComponent(component.Component):
    template = """
    <a href="{% url 'category_detail' category.id %}" class="px-4 mx-4 my-2 pb-4 border-b border-gray-300 flex justify-between">
    <div class="">
    <div class="text-md text-gray-600 font-medium">{{category.name}}</div>
    <div class="text-sm text-gray-500 font-medium ">{{category.description|default:"Sin descripción"}}</div>
    </div>
    <div class="text-right">
    <div class="text-lg font-medium text-nowrap">
    {{ category.total_expenses|default:0|floatformat:2 }} €
    </div>
    <div class="text-sm text-gray-500 font-medium ">{{category.estimated|floatformat:2}} €</div>
</div>
    </a>
    """
