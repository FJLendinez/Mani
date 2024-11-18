from django_components import component


@component.register('transaction_list')
class TransactionListComponent(component.Component):
    template = """    
    {% for transaction in transactions %}
        {% component 'transaction_row' transaction=transaction %}{% endcomponent %}
    {% endfor %}"""

    def get_context_data(self, transactions):
        return {"transactions": transactions}
