"""
Forms for filtering jobs.
"""

from django import forms


class JobsFilter(forms.Form):
    """
    Form for filtering jobs.
    """

    def __init__(self, *args, **kwargs):
        self.categories = kwargs.pop("categories")
        self.companies = kwargs.pop("companies")
        super().__init__(*args, **kwargs)

    search = forms.CharField(required=False)
    category = forms.CharField(required=False)
    company = forms.CharField(required=False)
    include_applied = forms.BooleanField(required=False, initial=True)
    order_by = forms.ChoiceField(
        choices=[
            ("posted_date", "Posted Date (Ascending)"),
            ("-posted_date", "Posted Date (Descending)"),
            ("due_date", "Due Date (Ascending)"),
            ("-due_date", "Due Date (Descending)"),
        ],
        required=False,
    )
