# Chosen Routines

An owner can choose processes for a server to run upon messages. from basic
counter to pub/sub methods, each unit is optionally applied to a server socket.

## Count

A counting unit for basic example. For each client onnection, repond with a client
count


## Echo / Broadcast

Perform an echo response (of the same message or a byte length) for each message sent. Apply a 'broadbast' routine to send the message to all connected clients


## Direct message

Send a message to individual clients - through name or regex convention. A
message may apply to a person, group or many individual addresses

