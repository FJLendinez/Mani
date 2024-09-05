from datetime import date

from django import forms


class DateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial and isinstance(self.initial, date):
            self.initial = self.initial.isoformat()
        self.widget.input_type = "date"
