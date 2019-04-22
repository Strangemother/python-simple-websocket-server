
from contrib.base import SessionCallable
import urllib.parse
import urllib.request

class TextLocal(SessionCallable):

    # def recv_msg(self, data, binary=False):
    def xcreated(self, name, index):
        contact_number = self.data['tel']
        apikey = self.data['apikey']
        test = self.data.get('debug', self.client_space.debug)
        resp =  send_sms(apikey, contact_number,'SMS Verify', test)
        self.log(resp)

        resp, code = get_inboxes(apikey)
        self.log('inboxes', resp)

        iid= 9#'Simply Reply Service'
        resp, code = get_sms(apikey, iid)
        self.log('get_sms', resp)


class TextLocalAnnounce(TextLocal):
    """Send a text to the owner or client/user of the connection during a 'connect'
    phase.
    """

    def on_connect(self):
        """Send a text message to the delivery number announcing the connection.
        """
        to_numbers = self.data.get('tel', None)
        self.log('on_connect', to_numbers)
        r=self.session['request']

        # protocols', []
        # peer', 'tcp:127.0.0.1:57345'
        # path', '/txt'
        # params', {'api_key': ['test1']}
        # origin', 'file://'
        # host', '127.0.0.1'

        # Wait for SMS reply
        wait_confirm = self.data.get('sms_confirm', None)
        content = f'Incoming connection from "{r.peer}" through: {r.path}'

        if wait_confirm:
            content = f"{content}\n\nAccept?"

        # ensure one sms only.
        assert len(content) < 160

        self.send_txt_msg(to_numbers, content,
                         receipt_url=self.data.get('receipt_url'))

    def send_txt_msg(self, to_numbers, content, **kw):
        is_test = self.data.get('debug', self.client_space.debug)
        apikey = self.data['apikey']
        kw['custom'] = f'{self.client_space.uuid}'
        kw['test'] = kw.get('test', is_test)
        kw['simple_reply'] = 'true' if self.data.get('sms_confirm', False) else 'false'

        self.log(f'Sending SMS:\nTO: {to_numbers}\n{content}\n\n{kw}\n')
        send_result = send_sms(apikey, to_numbers, content, **kw)

        return send_result


SMS_API = "https://api.txtlocal.com"


# http://api.txtlocal.com/docs/sendsms
def send_sms(apikey, numbers, message, test=False, **kw):
    rdata = {
        'apikey': apikey,
        'numbers': numbers,
        'message' : message,
        'test': test,
        'receipt_url': kw.get('receipt_url', None),
        # ! Must pass 'true' - not a True boolean to function
        'simple_reply': kw.get('simple_reply', False)
    }

    rdata.update(kw)
    print(f'!! Send SMS: {rdata}')

    data =  urllib.parse.urlencode(rdata)

    data = data.encode('utf-8')
    request = urllib.request.Request(f"{SMS_API}/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return fr


def get_inboxes(apikey):
    params = {'apikey': apikey}
    f = urllib.request.urlopen(f'{SMS_API}/get_inboxes/?'
        + urllib.parse.urlencode(params))
    return (f.read(), f.code)




def get_sms(apikey, iid):
    params = {'apikey': apikey, 'inbox_id' : iid}
    f = urllib.request.urlopen(f'{SMS_API}/get_messages/?'
        + urllib.parse.urlencode(params))
    return (f.read(), f.code)
