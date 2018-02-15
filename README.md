# [Omni (x)Extensions](http://omnix.hive.pt)

Simple web application consuming the Omni API.

This application may be used as a supervisor of the Omni Platform to run tasks in an async
fashion, this way it's possible to remove async tasks from the Omni core.

## Usage

One must define a series of configuration values in order to correctly use the automated
part of the omni extension (supervisor).

* `OMNIX_REMOTE` (`bool`) - If the remote URL should be used as the default one (legacy) (defaults to `False`)
* `OMNIX_USERNAME` (`str`) - The username to be used for authentication on the omni service
* `OMNIX_PASSWORD` (`str`) - The password value used in the authentication on the omni service, notice that
this value will be sent in plain text (using an SSL encrypted connection)
* `OMNIX_CLIENT_ID` (`str`) - The identifier of the Omni API client to be used for authentication
* `OMNIX_CLIENT_SECRET` (`str`) - The secret string to be used by the Omni API client for authentication
* `OMNIX_QUEUE` (`str`) - The name of AMQP queue that is going to be used (defaults to `omnix`)
* `REMOTE` (`bool`) - If the remove mode should be used (production URL creation)
* `OMNIX_REMOTE` (`bool`) - Same as `REMOTE`
* `OMNIX_SCHEDULE` (`bool`) - If the scheduling (background) operations of the Omnix should be enabled (defaults to `True`)
* `REDIRECT_URL` (`str`) - The URL that will be used for OAuth2 based callbacks

Additionally one must also configure the MongoDB and RabbitMQ instances to be able to execute
the proper master and slave supervisors. For that use the `MONGOHQ_URL` and `CLOUDAMQP_URL` variables.
