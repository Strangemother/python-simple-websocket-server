# Web Auth

authenticate a client socket with a web database record through a manager connection listening and sending request data.

A user may have an account with a website - such as the `interface`. In this case it's a django site. A user can authenticate their websocket session though administration of their web account. The login/logout actions should persist to the running routine for a user.

The manager can host the throughput as a third-party - given endpoints or a
connection through a manager client.


## Assert Logged In

Test if the connecting user has logged into the connected web session. The socket Session should connect to the website [database] with a client ID and assert 'currently logged in'. If False the session should wait for a login (through a manager client connection) and assert_valid


## Client ID Entry.

A User stores their socket uuid to the web interface. The action will evoke a signal back to the session or allow the user to prompt a manual test.

1. User opens socket
2. Runs to 'web connect' routine
3. User independently provides the socket ID to the web service


An automated signal is sent to the session with user login verification. At this point another step (all or one) of the routine may apply:

+ The automated signal detects the UUID assigned to the same browser session as the login user
+ The user received a 'key' to enter into the socket session.


### User entry; [ID] Socket > [ID] website ...

A user provides an ID into the socket with a previously agreed website store. This may be their username (not preferred). The user independantly logs into the website. The socket receives a signal of login with the UUID and asserts the login.

1. User opens socket
2. User sends ID credential through the socket
3. Session asserts the ID through the website client connection
4. Assert login

For machines:

+ user open
+ user socket send id
+ session assert id in website


### Key entry; [ID] Website [KEY] > [KEY] socket ...

A user will provide a `key` from the website login to the session socket. The session will assert the validity of the key and assert login.

1. User opens socket
2. User independently connects to website and collects `key`
3. User sends `key` through the socket
4. The socket session asserts the `key` through a website client connection
5. Assert login

For machines:

+ user open
+ user website get key
+ user socket send key
+ session assert key in website


## User Key Drop; [ID] Socket > [ID] website [KEY] > [ID] socket ...

A user provides an ID to the socket. The session connects to the website and drops a `key` given the (authorised) ID credentials. The  user independently reads the new `key` from the website and sends it back to the socket.

1. User opens socket
2. User sends ID credential through the socket
3. Session connects to the website and stores a `key` against the user (ID credential)
4. User independently reads the `key`
5. User sends `key` through socket session
6. Asset login

For machines:

+ user open
+ user socket send id
+ session (website using id) send key
+ user website get key
+ user socket send key
+ session assert key


## Key Swap; [ID] website [KEY] > [KEY] socket [KEY] > [KEY] website [SEC] > [SEC] socket ...

The user must log into the website and keep a key and give it to the session through the socket. The session socket will store a value with the website for the user to provide through the socket.

1. User logs into the website and keeps a `key`
2. User opens a socket
3. User sends the `key`
4. socket session connects to the website and drops a secret for the `key` user.
5. User independently reads the secret
6. User sends `key` through socket session
7. Asset login

For machines:

+ user website get key
+ user open
+ user socket send key
+ session (website using key) send secret
+ user website get secret
+ user socket send secret
+ session assert secret
