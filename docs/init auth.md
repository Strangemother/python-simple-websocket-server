# Authentication

a set of routines a user may authenticate their websocket application.
Initially the standard methods apply; sign-up, api-key, origin, peer...

The user must present an API key to connect. If they have defined an 'open' port
- a websocket for very public consumption, they must present another application
through the api sign-up. Then assign cookie-style auths to their client - essentially a mini auth.


## CSRF

In addition to an API key, perhaps the connection should contain a CSRF token.


## Challenge response

An optional method of authentication may be applied to the routine. The 'late auth' performs after the 'onConnect' _init auth_ has onboarded a user to the server.
The long-process of client processing occurs whilst the connected user waits for
a channel or data stream.

During the 'application wait' state, the api key, username and connection method are tested.
A challenge after the initial request from a client through the socket must be answered (correctly) by the client. Options configure the depth.


### Silent Challenge.

Once a waiting client is connected the server offers no response, but wait for a first - correct request from the waiting client.
The _first_ message should comply with the application rules - set by the owner. If the message fails validation, a prompt and silent server-side disconnect removes the client without warning. Too many requests in the same manner incurs a time penalty.


### Partial response

The server offers many half;questions. The user must answer (partially?) the other-half of the correct question and the answer.

Potentially the user should offer a chosen set of elements from a full password.


### Auth client

using 2factor, the user should supply the 6 digit pin from an auth app.

