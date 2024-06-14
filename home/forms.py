from django import forms

class SearchForm(forms.Form):
    
    contact_widget_form = {'class': 'form-control',
                        'size': '30', 
                        'style': 'box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);',
                        'placeholder': 'Search city',
                    }
    
    search_city = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs=contact_widget_form))