# Auth

The websockets are inherently insecure so we can bridge security layers before and _through_ a socket session.

The auth should consider the owner - authenticating their account - and a user authenticating an owners socket.

A number of authentication and encryption methods may apply to a socket, through owner choice.

## Login

A owner may log into their web session - all sockets are accessible through server side tickets.

A socket connection may have an 'authentication' url. Of which a connection requires a standard web post to a separate url. The user connects to a socket and their session is checked serverside with a given one-time token.

### Path

Define access through a distinct URL. Ensuring an endpoint cannot be 'attacked' by discovery. A user may define the path - and use it within their logic


### API key

The user must apply an API key to their session. This provides a level of encryption through the supplied libraries.

A user must present their API key to the service before they can access an application.

Calling this an 'app key' and utilizing the string for encryption. Only the server and the owner may know an key.


### One time password

Login through google auth to 2-factor an account. Once a user has two-factor, they must validate with an external authenticator.

The same can occur on a socket. An owner provides a qrcode for authenticator scanning and a connecting user applies the time code to the initial connection.


### Other Factor

Implement a standard email, phone or text service with socket 'wait'. The third-party must validate a factor - for an external service to connect  the waiting socket client for verification

### Challenge response

A user must verify a socket with a correct response to a question posed by the server. The server prepares a question for the socket. The socket will pick the correct partial from the statement and return + a secret key.


### Offer Challenge

The user must offer without prompt, a set of credentials and pass parameters without prompt.
The server socket receives a user connection and implements a standard 'good' connection. The next statements from the user must be authentication strings - such as a secret key and a google auth token.

If the user fails, lockout, timeout or honeypot can occur.


### User server Ident

A connecting user may need to identify they're connecting to the correct service - give a challenge by the server to agree. If the user is presented with information they do not recognise, they may choose to drop. If verification is required, the user should answer a relative question.

For example, an owner may have setup a special ascii character to display for the user to 'auth' visually.


### E2E encryption.

Client-side libraries will encrypt the information for server delivery. Providing libraries to encrypt locally - push and the server decrypts outside the handled session.

Therefore sniffing yields encrypted packets only

### SMS
### EMAIL
### AUTH APP

---

A user may opt for another layer of encryption for their own socket purposes - yielding another security option. for an example client in a production mode their full stack may authenticate from browser (sender) to client (consumer)

An owner (or by choice a connecting user) may may authenicate before websocket connection through an account:

    Login via SSL: https://app.com/login
    login, store user auth
    > Login via websocket
    check auth against server record
    ... kick or proceed

User JS connecting to owner account:

    Login via SSL url: https://owners-socket.app.com/fancy_app_path?myid=bob
    > key [automatic]
    > one time pass [manual]
    > SMS > validate [manual interception]
    < Challenge Question [auto]
    > Partial Answer [auto]
    < Challenge (or kick) [auto]
    > answer (capta/user server identification)
    (accept or espionage)

    Encrypt personal packet: 1234 >> "AO3MF9CJS0CJWN"
    >> send message
    (broadcast)


For a less secure (open socket) - the auth and encrypt layers are optional:

    Login via SSL Socket
    > key [auto]
    < challenge + email
