
from service.contrib.base import SessionCallable
import urllib.parse
import urllib.request
import uuid;

SMS_API = "https://api.txtlocal.com"


class TextLocal(SessionCallable):
    """Send a text to the owner or client/user of the connection during a 'connect'
    phase.

    To use first apply the routine to the client details:

         ('contrib.connect.sms.TextLocalAnnounce',
            {
                'apikey': '/13-456789',
                # The user must reply on text.
                'sms_confirm': True,
                'ask_random': True,
                # catch-all endpoint for receipts
                'receipt_url': 'http://emaple.com:8000/sms/receipt/',

                # 'tel': '447412344683',
                # 'debug': True,
            },),

    the 'tel' and 'debug' argument may be given through the API - or here if required.
    'on_connect' will send a confirmation text message.

    if 'sms_confim' the user must reply - send to 'session_recv_reply'.

    A receipt from the third-party is pushed through the manager > session connection
    to 'session_recv_receipt'.

    If 'ask_random' an 8 digit key sent via sms must be applied through the socket.
    Any messages before the assert_valid are currently dropped
    """


    # def recv_msg(self, data, binary=False):
    def example(self, name, index):
        contact_number = self.data['tel']
        apikey = self.data['apikey']
        test = self.data.get('debug', self.client_space.get('debug'))
        resp =  send_sms(apikey, contact_number,'SMS Verify', test)
        self.log(resp)

        resp, code = get_inboxes(apikey)
        self.log('inboxes', resp)

        iid= 9#'Simply Reply Service'
        resp, code = get_sms(apikey, iid)
        self.log('get_sms', resp)


    def created(self, name, index):
        """Build mini-state.
        """
        # The state must ensure an SMS did send
        keys = ('receipt', )
        if self.data.get('sms_confirm', None) is True:
            # The user must reply through the SMS service
            keys += ('reply', )

        if self.data.get('ask_random', None) is True:
            # The user must provide the txt'd key through the socket.
            keys += ('random', )

        # Generate a falsed dict as the init state.
        state = {x: False for x in keys}
        # We can persist temporary data within the routine, as the session will
        # maintain this instance through the life of the flows running routine.
        self.data['state'] = state
        self.log(f'Set state: {self.client_space.uuid} {state}')

    def on_connect(self):
        """Send a text message to the delivery number announcing the connection.
        """
        to_numbers = self.data.get('tel', None)
        self.log('on_connect', to_numbers)
        r = self.session['request']

        # protocols', []
        # peer', 'tcp:127.0.0.1:57345'
        # path', '/txt'
        # params', {'api_key': ['test1']}
        # origin', 'file://'
        # host', '127.0.0.1'

        # Wait for SMS reply
        wait_confirm = self.data.get('sms_confirm', None)
        ask_random = self.data.get('ask_random', None)
        content = f'A new connection "{r.peer}" through: {r.path}'

        if ask_random:
            hu = uuid.uuid4().hex.upper()
            rand = f"{hu[0:4]} {hu[5:9]}"
            self.data['rand'] = rand
            content = f'{content}\n\nPlease enter "{rand}" to your session.'

        if wait_confirm:
            content = f"{content}\n\nAccept?"

        # ensure one sms only.
        assert len(content) < 160

        self.send_txt_msg(to_numbers, content,
                         receipt_url=self.data.get('receipt_url'))

    def send_txt_msg(self, to_numbers, content, **kw):

        apikey = self.data['apikey']
        kw['custom'] = f'{self.client_space.uuid}'

        is_test = self.data.get('debug', self.client_space.debug)
        kw['test'] = "true" if is_test is True else "false"

        kw['simple_reply'] = 'true' if self.data.get('sms_confirm', False) else 'false'

        self.log(f'Sending SMS:\nTO: {to_numbers}\n{content}\n\n{kw}\n')

        send_result = send_sms(apikey, to_numbers, content, **kw)
        if is_test is True:
            # receipt cannot occur as the sms will never send.
            self.log(f"!! -- Simulating 'receipt' as sms 'test' is True")
            self.set_state('receipt', True)

        return send_result

    def recv_msg(self, payload, binary=False):
        """Receive a message from the session - in this case from a third-party
        through the Manager pipe (delivered by the Session)

        """
        method_name = f'session_recv_{payload[0]}'
        if hasattr(self, method_name) is False:
            self.unknown_payload(payload, binary)
            return

        method = getattr(self, method_name)
        return method(payload, binary)

    def unknown_payload(self, payload, binary=False):
        # A message through the pipe.

        if self.data.get('ask_random') is False:
            self.log(f"TextLocalAnnounce.recv_msg unexpected payload: {payload}")

        # A message is expected. test against on_connect generated key
        self.log('Accepted payload for random key.')
        if payload.decode('utf') != self.data['rand']:
            self.log(f"Assert invalid random: {payload} != {self.data['rand']}")
            return

        self.log('Assert Correct random key')
        self.set_state('random', True)
        return

    def session_recv_reply(self, payload, binary=False):
        """The user has replied through the session - connected through the custom
        id presented to the third-party.
        """
        if self.data.get('sms_confirm', False) is False:
            # The third-party confirm to push the receipt
            self.log("running routine received a text message but didn't expect one?")

        self.log('TextLocalAnnounce.recv_msg reply.')
        self.set_state('reply', True)

    def session_recv_receipt(self, payload, binary=False):
        """
            a 'receipt' is given from the third-party through thr web-hook pipe
            upon _sending_ a message confirmation.

            A session object through the recv_msg from the session pipe.
            validate and confirm, then push the mini state.
        """

        if self.data.get('sms_confirm', False) is True:
            # some friendly log.
            self.log('TXT Message recv_msg does not need reply validation - (state machine should assert_valid)')

        # more friendly
        self.log('TextLocalAnnounce.recv_msg receipt; wait for "reply"')
        self.set_state('receipt', True)

    def set_state(self, key, value):
        """Set the given key value to the session, assert the change and
        validate if required.
        """
        st = self.data['state']
        st[key] = value
        self.data['state'] = st

        # The simpliest state test -
        state_r = set(st.values()) == set([True])
        self.log('Set state change', key, value, 'new state:', state_r)

        if state_r is True:
            return self.assert_valid()

        # Print some feedback
        actions = [x for x in st if st[x] is False]
        ms = f"Required actions for SMS completion: {actions}"
        self.log(ms)


# http://api.txtlocal.com/docs/sendsms
def send_sms(apikey, numbers, message, test=False, **kw):
    rdata = {
        'apikey': apikey,
        'numbers': numbers,
        'message' : message,
        'test': test,
        'receipt_url': kw.get('receipt_url', None),
        # ! Must pass 'true' - not a True boolean for the third-party to accept.
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
