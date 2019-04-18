
from contrib.base import SessionCallable
import urllib.parse
import urllib.request

class TextLocal(SessionCallable):

    # def recv_msg(self, data, binary=False):
    def created(self, index):
        contact_number = self.data['tel']
        apikey = self.data['apikey']
        resp =  send_sms(apikey, contact_number,'SMS Verify')
        self.log(resp)

# http://api.txtlocal.com/docs/sendsms
def send_sms(apikey, numbers, message):
    data =  urllib.parse.urlencode({
        'apikey': apikey,
        'numbers': numbers,
        'message' : message,
        #'test': True,
    })
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.txtlocal.com/send/?")
    print(f'!! Send SMS: {data}')
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return fr

