The connection manager cares and auths for incoming requests.

`get_client` sends a message to a background worker and collects a user object
within the main thread. The `pipe_monitor` maintains a connection to the SessionManager within the process to push Process requests into asyncio
