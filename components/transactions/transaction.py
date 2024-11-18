from django_components import component


@component.register('transaction_row')
class TransactionRowComponent(component.Component):
    template = """
    <div hx-get="{% url 'transaction-update-form' transaction.id %}" hx-target="#modal-content" class="px-4 mx-4 my-2 pb-4 border-b border-gray-300 flex justify-between">
    <div class="">
    <div class="text-md text-gray-600 font-medium">{{transaction.description}}</div>
    <div class="text-sm text-gray-500 font-medium ">{{transaction.category.name|default:"Sin categorizar"}}</div>
    <div class="text-sm text-gray-500 font-medium ">{{transaction.date}}</div>
    </div>
    <div class="text-right">
    <div class="text-lg font-medium {% if transaction.type == transaction.TransactionType.EXPENSE %}text-red-300{% else %}text-blue-300{% endif %} text-nowrap">
    {% if transaction.type == transaction.TransactionType.EXPENSE %}-{% endif %}{{transaction.amount}} €
    </div>
    {% if transaction.last_amount %}
    <div class="text-sm text-gray-500 font-medium ">{{transaction.last_amount|floatformat:2}} €</div>
    {% endif %}
    <div class="flex">
    {% if transaction.goal %}
    <div class="text-sm text-gray-500 font-medium ">Objetivo: {{transaction.goal.name|default:"-"}}</div>
    {% endif %}
    {% if transaction.debt %}
    <div class="text-sm text-gray-500 font-medium ">Deuda: {{transaction.debt.name|default:"-"}}</div>
    {% endif %}
    </div>
</div>
    </div>
    """
