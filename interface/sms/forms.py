from django import forms
from . import models

class TextMessageForm(forms.Form):
    """

        from sms.models import TextMessage as TM
        from sms.forms import TextMessageForm as F

        response = {
            'sender': '447480924803',
            'content': 'Thanks ?',
            'inNumber': '447537402499',
            'submit': 'Submit',
            'network': '',
            'email': 'none',
            'keyword': '',
            'comments': 'Thanks ?',
            'credits': '52',
            'msgId': '99173112889',
            'rcvd': '2019-04-20 20:13:32',
            'firstname': 'Jay',
            'lastname': 'Jagpal',
            'custom1': '',
            'custom2': '',
            'custom3': ''
        }

        d = dict(response)
        f = F(d)

        if f.is_valid():
            print('valid')
            m = TM.from_post(f.cleaned_data)
        else:
            print(f.errors)
    """
    sender =  forms.CharField(max_length=20,
                               help_text=" Example: '447480924803'")
    content =  forms.CharField(help_text=" Example: 'Thanks ?'")
    inNumber =  forms.CharField(max_length=20,
                                 help_text=" Example: '447537402499'")
    submit =  forms.CharField(max_length=100,
                               help_text=" Example: 'Submit'")
    network =  forms.CharField(max_length=20, required=False,
                                help_text=" Example:  ''")
    email =  forms.CharField(max_length=20,
                              help_text=" Example: 'none'")
    keyword =  forms.CharField(max_length=20, required=False,
                                help_text=" Example:  ''")
    comments =  forms.CharField(help_text=" Example: 'Thanks ?'")
    credits =  forms.CharField(max_length=20,
                                help_text=" Example: '52'")
    msgId =  forms.CharField(max_length=20,
                              help_text=" Example: '99173112889'")

    rcvd =  forms.DateTimeField(help_text=" Example: '2019-04-20 20:13:32'")
    firstname =  forms.CharField(max_length=100,
                                  help_text=" Example: 'Jay'")
    lastname =  forms.CharField(max_length=100,
                                 help_text=" Example: 'Jagpal'")
    custom1 =  forms.CharField(max_length=255, required=False,
                                help_text=" Example:  ''")
    custom2 =  forms.CharField(max_length=255, required=False,
                                help_text=" Example:  ''")
    custom3 =  forms.CharField(max_length=255, required=False,
                                help_text=" Example:  ''")

    class Meta:
        model = models.TextMessage


class ReceiptForm(forms.Form):
    number = forms.CharField(max_length=20)
    status = forms.CharField(max_length=1)
    submit = forms.CharField(max_length=100)
    customID = forms.CharField(max_length=255, required=False)
    datetime = forms.CharField(max_length=30)
