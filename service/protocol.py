from autobahn.asyncio.websocket import WebSocketServerProtocol
import connect

from wlog import color_plog
log = color_plog('green').announce(__spec__)

"""
    'CLOSE_STATUS_CODES_ALLOWED', 'CLOSE_STATUS_CODE_ABNORMAL_CLOSE',
    'CLOSE_STATUS_CODE_GOING_AWAY', 'CLOSE_STATUS_CODE_INTERNAL_ERROR',
    'CLOSE_STATUS_CODE_INVALID_PAYLOAD', 'CLOSE_STATUS_CODE_MANDATORY_EXTENSION',
    'CLOSE_STATUS_CODE_MESSAGE_TOO_BIG', 'CLOSE_STATUS_CODE_NORMAL',
    'CLOSE_STATUS_CODE_NULL', 'CLOSE_STATUS_CODE_POLICY_VIOLATION',
    'CLOSE_STATUS_CODE_PROTOCOL_ERROR', 'CLOSE_STATUS_CODE_RESERVED1',
    'CLOSE_STATUS_CODE_SERVICE_RESTART', 'CLOSE_STATUS_CODE_TLS_HANDSHAKE_FAILED',
    'CLOSE_STATUS_CODE_TRY_AGAIN_LATER', 'CLOSE_STATUS_CODE_UNASSIGNED1',
    'CLOSE_STATUS_CODE_UNSUPPORTED_DATA', 'CONFIG_ATTRS',
    'CONFIG_ATTRS_CLIENT', 'CONFIG_ATTRS_COMMON',
    'CONFIG_ATTRS_SERVER', 'DEFAULT_SPEC_VERSION',
    'MESSAGE_TYPE_BINARY', 'MESSAGE_TYPE_TEXT',
    'PROTOCOL_TO_SPEC_VERSION', 'SEND_STATE_GROUND',
    'SEND_STATE_INSIDE_MESSAGE', 'SEND_STATE_INSIDE_MESSAGE_FRAME',
    'SEND_STATE_MESSAGE_BEGIN', 'SPEC_TO_PROTOCOL_VERSION',
    'STATE_CLOSED', 'STATE_CLOSING',
    'STATE_CONNECTING', 'STATE_OPEN',
    'STATE_PROXY_CONNECTING', 'SUPPORTED_PROTOCOL_VERSIONS',
    'SUPPORTED_SPEC_VERSIONS', '_QUEUED_WRITE_DELAY',
    '_WS_MAGIC',
    '_closeConnection',
    '_connectionLost',
    '_connectionMade',
    '_consume',
    '_dataReceived',
    '_fail_connection',
    '_invalid_payload',
    '_is_public',
    '_onClose',
    '_onMessage',
    '_onMessageBegin',
    '_onMessageEnd',
    '_onMessageFrame',
    '_onMessageFrameBegin',
    '_onMessageFrameData',
    '_onMessageFrameEnd',
    '_onOpen',
    '_onPing',
    '_onPong',
    '_parseExtensionsHeader',
    '_perMessageCompress',
    '_protocol_violation',
    '_send',
    '_sendAutoPing',
    '_trigger',
    '_wskey',
    'allowNullOrigin',
    'allowedOrigins',
    'allowedOriginsPatterns',
    'applyMask',
    'autoFragmentSize',
    'autoPingInterval',
    'autoPingPending',
    'autoPingPendingCall',
    'autoPingSize',
    'autoPingTimeout',
    'autoPingTimeoutCall',
    'beginMessage',
    'beginMessageFrame',
    'broadcast_message',
    'closeHandshakeTimeout',
    'closeHandshakeTimeoutCall',
    'closedByMe',
    'connectionLost',
    'connection_lost',
    'connection_made',
    'consumeData',
    'data',
    'data_received',
    'dropConnection',
    'droppedByMe',
    'echoCloseCodeReason',
    'endMessage', 'eof_received', 'factory', 'failByDrop', 'failHandshake',
    'failedByMe', 'flashSocketPolicy', 'get_channel_id', 'http_headers',
    'http_request_data', 'http_request_host', 'http_request_params',
    'http_request_path', 'http_request_uri', 'http_status_line', 'is_closed',
    'localCloseCode', 'localCloseReason', 'log', 'logFrames', 'logOctets',
    'logRxFrame', 'logRxOctets', 'logTxFrame', 'logTxOctets', 'maskServerFrames',
    'maxConnections', 'maxFramePayloadSize', 'maxMessagePayloadSize',
    'onAutoPingTimeout', 'onClose', 'onCloseFrame', 'onCloseHandshakeTimeout',
    'onConnect', 'onFrameBegin', 'onFrameData', 'onFrameEnd', 'onMessage',
    'onMessageBegin', 'onMessageEnd', 'onMessageFrame', 'onMessageFrameBegin', 'o
    nMessageFrameData', 'onMessageFrameEnd', 'onOpen', 'onOpenHandshakeTimeout',
    'onPing', 'onPong', 'onServerConnectionDropTimeout', 'openHandshakeTimeout',
    'openHandshakeTimeoutCall', 'pause_writing', 'peer',
    'perMessageCompressionAccept', 'processControlFrame', 'processData',
    'processHandshake', 'processProxyConnect', 'receive_queue', 'registerProducer',
    'remoteCloseCode', 'remoteCloseReason', 'requireMaskedClientFrames',
    'resume_writing', 'sendClose', 'sendCloseFrame', 'sendData', 'sendFrame',
    'sendHtml', 'sendHttpErrorResponse', 'sendMessage', 'sendMessageFrame',
    'sendMessageFrameData', 'sendPing', 'sendPong',
    'sendPreparedMessage', 'sendRedirect', 'sendServerStatus', 'send_queue',
    'send_state', 'serveFlashSocketPolicy', 'setTrackTimings', 'state',
    'succeedHandshake', 'tcpNoDelay', 'trackTimings', 'trackedTimings',
    'trafficStats', 'transport', 'triggered', 'trustXForwardedFor',
    'unregisterProducer', 'utf8validateIncoming', 'utf8validator', 'versions',
    'waiter', 'wasClean', 'wasCloseHandshakeTimeout', 'wasMaxFramePayloadSizeExceeded',
    'wasMaxMessagePayloadSizeExceeded', 'wasNotCleanReason',
    'wasOpenHandshakeTimeout', 'wasServerConnectionDropTimeout',
    'wasServingFlashSocketPolicyFile', 'webStatus', 'websocket_extensions',
    'websocket_origin', 'websocket_protocols', 'websocket_version'
"""

"""
    dict_keys(['is_closed', 'factory', 'transport', 'receive_queue', 'waiter',
    'peer', 'logOctets', 'logFrames', 'trackTimings', 'utf8validateIncoming',
    'applyMask', 'maxFramePayloadSize', 'maxMessagePayloadSize',
    'autoFragmentSize', 'failByDrop', 'echoCloseCodeReason', 'openHandshakeTimeout',
    'closeHandshakeTimeout', 'tcpNoDelay', 'autoPingInterval', 'autoPingTimeout',
    'autoPingSize', 'versions', 'webStatus', 'requireMaskedClientFrames',
     'maskServerFrames', 'perMessageCompressionAccept',
    'serveFlashSocketPolicy', 'flashSocketPolicy', 'allowedOrigins',
    'allowedOriginsPatterns', 'allowNullOrigin', 'maxConnections',
    'trustXForwardedFor', '_perMessageCompress', 'trackedTimings',
    'trafficStats', 'state', 'send_state', 'data', 'send_queue', 'triggered',
    'utf8validator', 'wasMaxFramePayloadSizeExceeded',
    'wasMaxMessagePayloadSizeExceeded', 'closedByMe', 'failedByMe', 'droppedByMe',
    'wasClean', 'wasNotCleanReason', 'wasServerConnectionDropTimeout',
    'wasOpenHandshakeTimeout', 'wasCloseHandshakeTimeout',
    'wasServingFlashSocketPolicyFile', 'localCloseCode', 'localCloseReason',
    'remoteCloseCode', 'remoteCloseReason', 'openHandshakeTimeoutCall',
     'closeHandshakeTimeoutCall', 'autoPingTimeoutCall', 'autoPingPending',
     'autoPingPendingCall', 'http_request_data', 'http_status_line',
     'http_headers', 'http_request_uri', 'http_request_path', 'http_request_params',
     'http_request_host', 'websocket_version', 'websocket_protocols',
     'websocket_origin', 'websocket_extensions', '_wskey',
     'websocket_protocol_in_use', 'websocket_extensions_in_use',
     'http_response_data', 'inside_message', 'current_frame',
     'current_frame_masker', '_isMessageCompressed',
     'utf8validateIncomingCurrentMessage', 'utf8validateLast', 'message_is_binary',
     'message_data', 'message_data_total_length', 'frame_length', 'frame_data'])
"""
class ServerProtocolReporter(WebSocketServerProtocol):
    """A 'per client' protocol to manage a users incoming
    request and farm to the worker tools.
    """
    def _closeConnection(self, *a, **kw):
        #log('_closeConnection', a, kw)
        return super()._closeConnection(*a, **kw)

    def _connectionLost(self, *a, **kw):
        #log('_connectionLost', a, kw)
        return super()._connectionLost(*a, **kw)

    def _connectionMade(self, *a, **kw):
        #log('_connectionMade', a, kw)
        return super()._connectionMade(*a, **kw)

    def _consume(self, *a, **kw):
        #log('_consume', a, kw)
        return super()._consume(*a, **kw)

    def _dataReceived(self, *a, **kw):
        #log('_dataReceived', a, kw)
        return super()._dataReceived(*a, **kw)

    def _fail_connection(self, *a, **kw):
        #log('_fail_connection', a, kw)
        return super()._fail_connection(*a, **kw)

    def _invalid_payload(self, *a, **kw):
        #log('_invalid_payload', a, kw)
        return super()._invalid_payload(*a, **kw)

    def _is_public(self, *a, **kw):
        #log('_is_public', a, kw)
        return super()._is_public(*a, **kw)

    def _onClose(self, *a, **kw):
        #log('_onClose', a, kw)
        return super()._onClose(*a, **kw)

    def _onMessage(self, *a, **kw):
        #log('_onMessage', a, kw)
        return super()._onMessage(*a, **kw)

    def _onMessageBegin(self, *a, **kw):
        #log('_onMessageBegin', a, kw)
        return super()._onMessageBegin(*a, **kw)

    def _onMessageEnd(self, *a, **kw):
        #log('_onMessageEnd', a, kw)
        return super()._onMessageEnd(*a, **kw)

    def _onMessageFrame(self, *a, **kw):
        #log('_onMessageFrame', a, kw)
        return super()._onMessageFrame(*a, **kw)

    def _onMessageFrameBegin(self, *a, **kw):
        #log('_onMessageFrameBegin', a, kw)
        return super()._onMessageFrameBegin(*a, **kw)

    def _onMessageFrameData(self, *a, **kw):
        #log('_onMessageFrameData', a, kw)
        return super()._onMessageFrameData(*a, **kw)

    def _onMessageFrameEnd(self, *a, **kw):
        #log('_onMessageFrameEnd', a, kw)
        return super()._onMessageFrameEnd(*a, **kw)

    def _onOpen(self, *a, **kw):
        #log('_onOpen', a, kw)
        return super()._onOpen(*a, **kw)

    def _onPing(self, *a, **kw):
        #log('_onPing', a, kw)
        return super()._onPing(*a, **kw)

    def _onPong(self, *a, **kw):
        #log('_onPong', a, kw)
        return super()._onPong(*a, **kw)


class SendMixin(object):

    def send_text(self, text):
        return self.sendMessage(bytes(text, encoding='utf8'))


class MyServerProtocol(ServerProtocolReporter, SendMixin):

    def connection_made(self, transport):
        self.uuid = id(self)
        log('Connection', self.uuid)
        super().connection_made(transport)

    def onConnect(self, request):
        """Send a post of the request to the connect.connection_manager
        Return 'auth' headers for pelimary acceptance.

        A user is given an initial "space" - of which may not be authenticated.
        """
        log("Client connecting: {0}".format(request.peer), connect)
        # Send to connection manager for session.SessionManager
        # start or pickup
        ok, space = connect.connection_manager(self.uuid, request, self)
        if ok is False:
            # break
            log('Bad client')
        #self.sendMessage('Authenicating')
        headers = self.get_headers(request)
        return (None, headers)

    def session_message(self, content):
        """A Message from the recv_session_message(msg) - pushed through the
        session pipe from a third party.
        """
        log(f'Protocol session_message {self.uuid}', content)

        if content[0] == 'receipt':
            connect.message(self.uuid, content)

        self.send_text(content)

    def get_headers(self, request):
        headers = {}
        internal_header = 'custom_pre_auth_header'
        external_header = 'ExternalHeaderName'
        if internal_header in request.headers:
            headers[external_header] = request.headers[internal_header]
        return headers

    def broadcast_message(self, payload, isBinary):
        if not isBinary:
            msg = "{} from {}".format(payload.decode('utf8'), self.peer)
            self.factory.broadcast(msg)

    def connectionLost(self, reason):
        """unregister this socket from the factory client list.
        """
        ok, space = connect.close_manager(self.uuid, (reason,), self)
        self.factory.close(self, reason=reason)
        super().connectionLost(reason)

    def onOpen(self):
        """Register socket client with the factory client list"""
        ok, space = connect.open_manager(self.uuid, self)
        self.factory.register(self)
        log("WebSocket connection open.")
        # Wait for confirmation

    def onMessage(self, payload, isBinary):
        if isBinary:
            log("Binary message received: {0} bytes".format(len(payload)))
        else:
            log("Text message received: {0}".format(payload.decode('utf8')))
        ok, action = connect.message_manager(self.uuid, payload, isBinary)
        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        log("WebSocket connection closed: {0}".format(reason))
        err = wasClean, code, reason
        ok, space = connect.close_manager(self.uuid, err, self)
        self.factory.close(self, wasClean=wasClean, code=code, reason=reason)

    # def sendHtml(self, html):
        # """
        # Send HTML page HTTP response.
        # """
        # responseBody = html.encode('utf8')
        # response = "HTTP/1.1 200 OK\x0d\x0a"
        # if self.factory.server is not None and self.factory.server != "":
        #     response += "Server: %s\x0d\x0a" % self.factory.server
        # response += "Content-Type: text/html; charset=UTF-8\x0d\x0a"
        # response += "Content-Length: %d\x0d\x0a" % len(responseBody)
        # response += "\x0d\x0a"
        # self.sendData(response.encode('utf8'))
        # self.sendData(responseBody)


    def sendServerStatus(self, redirectUrl=None, redirectAfter=0):
        """
        Used to send out server status/version upon receiving a HTTP/GET without
        upgrade to WebSocket header (and option serverStatus is True).
        """
        if redirectUrl:
            redirect = """<meta http-equiv="refresh" content="%d;URL='%s'">""" % (redirectAfter, redirectUrl)
        else:
            redirect = ""
        self.sendHtml("Woops! %s" % (redirect))
