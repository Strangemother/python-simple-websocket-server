from django.db import models
from datetime import datetime

# Create your models here.
class Receipt(models.Model):
    number = models.CharField(max_length=20)
    status = models.CharField(max_length=1)
    submit = models.CharField(max_length=100)
    custom = models.CharField(max_length=255)
    datetime = models.DateTimeField()

    @staticmethod
    def from_post(data):

        # map special names of which cannot be applied automatically.
        fields = (
            'number',
            'status',
            'submit',
            'custom',
            'datetime',
        )

        md = {}
        for key in fields:
            md[key] = data.get(key)

        recv = md['datetime']
        if isinstance(recv, str):
            # '2019-04-20 20:13:32
            recv = datetime.strptime(recv, '%Y-%m-%d %H:%M:%S')
        md['datetime'] = recv

        return Receipt(**md)


class TextMessage(models.Model):
    sender =  models.CharField(max_length=20,
                               help_text=" Example: '447480924803'")
    content =  models.TextField(help_text=" Example: 'Thanks ?'")
    in_number =  models.CharField(max_length=20,
                                 help_text=" Example: '447537402499'")
    submit =  models.CharField(max_length=100,
                               help_text=" Example: 'Submit'")
    network =  models.CharField(max_length=20,
                                help_text=" Example:  ''")
    email =  models.CharField(max_length=20,
                              help_text=" Example: 'none'")
    keyword =  models.CharField(max_length=20,
                                help_text=" Example:  ''")
    comments =  models.TextField(help_text=" Example: 'Thanks ?'")
    credits =  models.CharField(max_length=20, null=True, blank=True,
                                help_text=" Example: '52'")
    msg_id =  models.CharField(max_length=20,
                              help_text=" Example: '99173112889'")
    created =  models.DateTimeField(auto_now_add=True)
    received =  models.DateTimeField(help_text=" Example: '2019-04-20 20:13:32'")
    firstname =  models.CharField(max_length=100,
                                  help_text=" Example: 'Jay'")
    lastname =  models.CharField(max_length=100,
                                 help_text=" Example: 'Jagpal'")
    custom1 =  models.CharField(max_length=255,
                                help_text=" Example:  ''")
    custom2 =  models.CharField(max_length=255,
                                help_text=" Example:  ''")
    custom3 =  models.CharField(max_length=255,
                                help_text=" Example:  ''")

    @staticmethod
    def from_post(data):
        """Given the dict from a response object through the third-party exposure,
        created a new model. This model is not saved.

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
            m = TextMessage.from_post(d)
        """

        # map special names of which cannot be applied automatically.
        fields = (
            'sender',
            'content',
            'submit',
            'network',
            'email',
            'keyword',
            'comments',
            'credits',
            'firstname',
            'lastname',
            'custom1',
            'custom2',
            'custom3',
        )

        _map = dict(
            #='447537402499',
            inNumber='in_number',
            #'99173112889',
            msgId='msg_id',
            #'2019-04-20 20:13:32',
            rcvd='received',
            )

        md = {}
        for key in fields:
            md[key] = data.get(key)

        for key in  _map:
            md[_map[key]] = data.get(key)

        recv = md['received']
        if isinstance(recv, str):
            # '2019-04-20 20:13:32
            recv = datetime.strptime(recv, '%Y-%m-%d %H:%M:%S')
        md['received'] = recv

        return TextMessage(**md)
