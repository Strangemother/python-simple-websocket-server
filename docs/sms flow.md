# Text messages

A session unit may utilise an external text message service for connect authing or other procedures. Any third party is possible, but the builtin will cater for txtlocal, twillo - and some other one ...

Adding the unit to a wesocket session definition in a 'connect' phase can force a user to authenticate their connection by recieving a text message.

## Alerts

Use the text message platform as a server-side alert of an incoming connection. An owner may define a standard text to receive when a new client connects. The owner may optionally accept/deny upon discretion.


## Client Accounts

An option to provide a 2factor layer for incoming clients sends the incoming user a text message to a previously stored phone number. A user may use this to validate their account entry to a session socket. In addition it serves as a passwordless method of user on-boarding.

In this case the client/user/visitor should hae already given their number to the owner service - through a previously trusted form.


### Confirm

Send the client a text message confirming the socket activity:

    > SOCKET: confirm > continue
    ! send text to user "You've just logged in"


### Confirm Reply

Send a text message to the client and wait for a simple validation before accepting
the socket connection:

    ! send text to user # "Is that you logging in? Reply yes to accept."
    < SMS: user reply: YES
    ! server receipt validate
    > SOCKET: confirm > continue


### Send Token

Send the client a text message with a session generated unique number. The client user must input the sms token through the socket - authenticating the session unit layer

    ! send text to user # 1234
    > SOCKET: user key 1234
    ! server receipt validate
    > SOCKET: confirm > continue


### Reply

A client may reply to a text message with a pre-defined response. The response should be stored server-side for verification.

The user may receive the password through a trusted interface to reply through the SMS service:

    > APP: "Please reply '1234' to the SMS..."
    ! send text to user # "Hi, what's on the screen? "
    < SMS: user reply: 1234
    ! server receipt validate
    > SOCKET: confirm > continue

Alternatively a user can reply with an _offline_ stored response, such as a spoken shared password.


