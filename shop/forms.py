from django import forms


class AddReview(forms.Form):
    name = forms.CharField(label='Имя', required=True, max_length=150,
                           widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}))
    text = forms.CharField(widget=forms.Textarea({'placeholder': 'Ваш коментарий', 'class': 'form-control'}),
                           label='Коментарий', required=True)
    star = forms.ChoiceField(choices=[
                            ('1', '★'),
                            ('2', '★★'),
                            ('3', '★★★'),
                            ('4', '★★★★'),
                            ('5', '★★★★★'),
                                    ],
                             widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), required=True)
