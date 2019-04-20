from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import TemplateView

import base64


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

from django.views.decorators.csrf import csrf_exempt


class ReplyView(TemplateView):
    """Receive the third-party call to 'receipt_url' of an outbound SMS.
    The receipt contains a validity statement of a sent message.

    The message should be verified for authenticity, stored to an account
    and the session notified through a pipe connection.
    """

    template_name = "sms/index.html"

    @csrf_exempt(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """As a third-party
        """
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ReceiptView(TemplateView):
    """Receive the third-party call to 'receipt_url' of an outbound SMS.
    The receipt contains a validity statement of a sent message.

    The message should be verified for authenticity, stored to an account
    and the session notified through a pipe connection.
    """

    template_name = "sms/index.html"


    @csrf_exempt(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """As a third-party
        """
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                # NOTE: We are only support basic authentication for now.
                print('Authorized', auth)
                if auth[0].lower() == "basic":
                    au_by = auth[1].encode('utf')
                    uname, passwd = base64.b64decode(au_by).split(b':')
            return self.render_to_response(context)

        response = HttpResponse()
        realm = ''
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        return response
