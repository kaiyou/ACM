Agnostic/Acentric Cloud Messaging
=================================

This project aims at providing the simplest possible mean to notify mobile
devices that an interactive application should display a notification and
load the related contents from its server. It is primarily targeting
Android devices for now.

The main goals are:
 - lower the battery usage on mobile devices that run messaging apps
 - remain free of Google Play Services
 - provide very simple, very agnostic APIs
 - provide protection from a malicious notification broker
 - run properly in constrained environments
 - be extensible to as many technologies as possible in the future

Protocol
========

ACM uses a specifically designed protocol described in
[PROTOCOL.md](PROTOCOL.md). The protocol is available both over a
socket-based interface and a REST API.

ACM is acentric, meaning a device can register on any ACM server, simply
by configuring the ACM endpoint. 

General scheme
--------------

Both the device (or individual applications in case the package is not
installed system-wide) and application server MUST be able to register
on the same WAMP broker.

Subscribing uses the following scheme.

1. The client notification package connects to a broker (in socket mode)
2. The app registers a new notification target, specifying the resulting
   callback and topic type
3. The system package generates a channel identifier and stores the relation
   between the intent type and channel
4. The system package generates an encryption key for the notification
5. The system package subscribes to the channel
6. The application communicates the broker, channel and encryption key to the
   application server

Notifying uses the following scheme.

1. The application server generates a notification, potentially
   attached with a structured payload
2. The current timestamp and event unique identifier are attached
   to the payload, which is encoded
3. The notification content is encrypted using an authenticated
   encryption scheme and the key initially passed by the client
4. The notification is published on the broker and channel specified by the
   client
5. The client notification package decodes and decrypts the notification
6. The client notification package checks the timestamp is recent and stores
   the unique id in a short-lived cache to avoid replay attacks by the
   broker
7. The client notification package triggers the callback

Transport and encoding
----------------------

If the client is able to use Websockets, a secure Websocket MUST be used
to connect to the broker.

Otherwise, the client MUST run regular polling using the REST API.

Channels
--------

For every type of notification an application is able to receive, a unique
channel identifier is generated. The channel identifier MUST be unique to
the device, application and type of notification.

Notifications
-------------

The current and only supported notification format is `1`.

A notification is an event published on a channel. It contains a 16 bytes
header as follows:

    0       4       8      12      15
    --------------------------------
    |   timestamp   |  identifier  |
    --------------------------------

 - `timestamp`, containing the current timestamp since epoch
 - `identifier`, containing the event identifier, which MUST be unique
   per channel (e.g. incremental identifier)

The rest of the notification is the body. Body encoding is delegated to the
applicatioN.

The notification encrypted using AES-GCM and the key provided by the client.

Security
========

Trust model
-----------

The current trust model is based on the following statements:
 - the client trusts its broker with metadata related to its IP
   address, application servers and notification count
 - the client does not trust the broker with the metadata related
   to application (except the server IP address) and notification type
 - the client does not trust the broker with the content of notifications
 - the client does not trust the broker in regard to replay attacks
 - the client does not trust the borker in regard to DoS attacks
 - the client does not trust any third party with its notifications

Confidentiality and integrity of notifications
----------------------------------------------

Notification application and type remain confidential as long as
the channel generation process does not provide information about
either the application or the notification type.

Notification final user is confidential to the broker as long as the
channel generation process does not provide information about the device
or its owner. Confidentiality can be diminished if the broker can link the
source IP address to the final user.

Notification content confidentiality and integrity is guaranteed by the
authenticating encryption scheme, as long as the key is unpredictible by
the broker or any other third party.

A broker MUST NOT provide a list of available topics to any party.

Availability of the service
---------------------------

Any client can subscribe to new channels on the broker, as well as any
application server can publish to any channel on the broker. Thus, the
following limits should be applied:

 - client number of subscriptions should be limited
 - number of subscriptions should be limited per channel
 - client rate of subscription/unsubscription should be limited
 - server publication rate should be limited per channel
 - server publication rate should be limited in general

Any client can ask its application server to publish to many notification
targets. Thus, the following limits should be applied:

 - client number of notification targets should be limited
 - client rate of creation/deletion of notification targets should be limited

Any server or the broker can spam a client with notifications. Thus, the
following limits should be applied:

 - notification rate should be limited per channel
 - notification rate should be limited in general

