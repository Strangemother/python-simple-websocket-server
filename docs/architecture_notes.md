# Sockets

Replicating an old project 'bridge' - A central server acts as a broker
for many mini clients. The bridge may send/receive messages but it's main
job consists of client input and management of clients.

Server: Receive admin and client connections, serve pooling and child management
Client: Receive users and delegate to a parent server if required.

Each may live on an independant server, passing the socket through pipes for
each session manager.



A user must:

+ Signup, keeping a secret key, half cipher and a connection path.
+ Connect using connection path ws/023ir20r39ir
+ Provide receive half cipher
+ Send built cipher with secretkey within.

## signup:

1. gives email, username
2. confirms email
3. provides password
4. receives secretkey, provides encrypt-pw


A Server must:

+ Receive on path, test initial entry - kill or proceed
+ push half cipher for new session
+ wait for encrypt
+ decrypt using server encrypt-pw
+ read secretkey - kill or proceed
+ wait for message
