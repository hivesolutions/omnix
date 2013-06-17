# Omni (x)Extensions

Simple web application consuming the omni api.

## Usage

One must define a series of configuration values in order to correctly use the automated
part of the omni extension (supervisor).

* `OMNIX_USERNAME` - The username to be used for authentication on the omni service
* `OMNIX_PASSWORD` - The password value used in the authentication on the omni service, notice that
this value will be sent in plain text (using an SSL encrypted connection)
* `REMOTE` - If the remove mode should be used (production url creation)
* `REDIRECT_URL` - The url that will be used for outh based callbacks
