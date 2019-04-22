from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.views.generic import TemplateView

from sms.models import Receipt, TextMessage as TM
from sms.forms import TextMessageForm as F
from sms.forms import ReceiptForm


import base64

print('sms view connecting to session remote manager')
from multiprocessing.managers import BaseManager
m = BaseManager(address=('127.0.0.1', 9018), authkey=b'84ytnp9qyn8p3tu8qcp394tpmj')
m.register('post')
m.register('hello')
m.connect()
m.hello()
print(':',m)

class IndexView(TemplateView):
    template_name = "sms/index.html"

    extra_context = dict(
        company='Octopus Liger'
    )

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs


class ReceiptView(TemplateView):
    """If a client sends an SMS as a reply, the third-party service will
    call the exposed service with a POST.

        POST
        ImmutableMultiDict([
        ('sender', '447480924803'),
        ('content', 'Thanks ?'),
        ('inNumber', '447537402499'),
        ('submit', 'Submit'),
        ('network', ''),
        ('email', 'none'),
        ('keyword', ''),
        ('comments', 'Thanks ?'),
        ('credits', '52'),
        ('msgId', '99173112889'),
        ('rcvd', '2019-04-20 20:13:32'),
        ('firstname', 'Jay'),
        ('lastname', 'Jagpal'),
        ('custom1', ''),
        ('custom2', ''),
        ('custom3', '')])
        95.138.131.86 - - [20/Apr/2019 19:52:37] "POST / HTTP/1.1" 200 -
    """

    template_name = "sms/index.html"

    @csrf_exempt(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """As a third-party
        """
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        # auth, up_set = self.http_auth(request)
        # if auth is False:
        #     return self.http_auth_fail()
        # print('Post Response')

        #d = dict(request.AUTH)
        # Data must be x-www-form-encoded to accept correctly.
        f = ReceiptForm(request.POST)

        if f.is_valid():
            d = f.cleaned_data
            print('valid Receipt', d)
            mo = Receipt.from_post(d)
            mo.save()
            m.post('receipt', model_to_dict(mo))

        else:
            print(f.errors)

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


from django.forms.models import model_to_dict

class ReplyView(TemplateView):
    """Receive the third-party call to 'receipt_url' of an outbound SMS.
    The receipt contains a validity statement of a sent message.

    The message should be verified for authenticity, stored to an account
    and the session notified through a pipe connection.


        POST
        ImmutableMultiDict([('number', '447480924803'),
        ('status', 'D'),
        ('submit', 'Submit'),
        ('customID', ''),
        ('datetime', '2019-04-20 20:13:33')])

    """
    template_name = "sms/index.html"


    @csrf_exempt(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """As a third-party
        """
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        auth, up_set = self.http_auth(request)
        if auth is False:
            return self.http_auth_fail()
        print('Post Response')

        #d = dict(request.AUTH)
        # Data must be x-www-form-encoded to accept correctly.
        f = F(request.POST)

        if f.is_valid():
            print('valid reply')
            mo = TM.from_post(f.cleaned_data)
            mo.save()
            m.post('reply', model_to_dict(mo))
        else:
            print(f.errors)

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def http_auth(self, request):

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                # NOTE: We are only support basic authentication for now.
                print('Authorized', auth)
                if auth[0].lower() == "basic":
                    au_by = auth[1].encode('utf')
                    uname, passwd = base64.b64decode(au_by).split(b':')
                    return True, (uname, passwd,)
        return False, None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        auth, up_set = self.http_auth(request)
        if auth is False:
            return self.http_auth_fail()

        return self.render_to_response(context)

    def http_auth_fail(self):
        response = HttpResponse()
        realm = ''
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        return response
