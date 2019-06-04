# Public exposure

Once an owner has built an active channel, it may be exposed for raw public
consumption for other users and anonymous vistors to access.

For personal application access, a user integrates with a system via an API key.
This is used for development, personal deployment and general application usage.
An owner builds an active unit with specific auth requirements and may continue
into a public domain using the key with their internal app.

Some authentication units require user data - such as a QR Code secret key store.

Within dev or personal deployment the server needs only one set of credentials.
To allow _another user/visitor_ to maintain a persistent record for the deployed
service to digest, the visitor information is seperate to the deplyed service settings.


## Owner setup

An owner may connect to their socket and validate with _builtin_
configurations, but other users should provide their own credentials.

An owner is expected to administer the socket setup through the master interface.

A service setup is logically defined as an object nested within `username -> apikey` - the api key is simply a unique ID for a single socket service.


## User access

A third-party user may gain access to the owners socket service through one of:

+ The master interface: Already a member within the walls - accessing the socket
 via the master ui.
+ third-party validated app: A Owner built app - many users through one api key.
+ an access endpoint: for a third party to access through the many urls (public api keys).


# Public API key

A public api key defines a url path pointing to a single owner and api key.
As the owner and original api key are stored internally they are not given by
the consumer application, therefore presenting less information about a socket
and owner.

A socket connection consists of:

**standard access:** An allowed API path (entries url), an expected incoming host (e.g. 127.0.0.1), and the unique (unchangeable) API key for the created socket service. Then continue with the service.

    wshost.com/entries_url_0ASD9F0AIF/?api_key=api_key_1
    host only: 127.0.0.1, 192.168.0.1
    origin: ws://, file://
    > continue session protocols


**public access:** An incoming publicly defined friendly url, and a knowledge or agreement of the required authentication routine.

With the deployed public url a user/visitor may see only a public URL.
A user may have previously on-boarded to the endpoint - therefore an owner
defined idenity may be applied.

Then continue with the service.

    wshost.com/daves-endpoint/[?user=test2|app_username]
    host only: *, !localhost
    origin: ws://
    > continue session protocols

For public deployed owner apps, this can save public abuse:

    wshost.com/company-football/ # publically visible.
    host only 88.658.11.25
    > server third-party auth wait.
    # push Valid
    > continue session
    < get_results()


upon brute or abuse:

    wshost.com/entries_url_0ASD9F0AIF/?api_key=api_key_1
    host only: *, !localhost
    > continue session protocol


    wshost.com/company-football/
    host != 88.658.11.25
    > cannot server third part wait
