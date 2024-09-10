from .__user import User


class MarketplaceApp(User):
    """# MarketPlaceApp object
    The MarketPlaceApp object is an authentication entity for the SDK that
    represents your MarketPlace Application, being able to access any authorized Workspace.
    All requests to the Stark Bank and Stark Infra API must be authenticated via an SDK user,
    which must have been previously created at the Stark Bank or Stark Infra websites
    [https://web.sandbox.starkbank.com] or [https://web.starkbank.com]
    before you can use it in this SDK. MarketplaceApps may be passed as the user parameter on
    each request or may be defined as the default user at the start (See README).
    If you are accessing a specific MarketplaceAppAuthorization using MarketplaceApp credentials, you should
    specify the authorization ID when building the MarketplaceApp object or by request, using
    the MarketplaceApp.replace(app, authorization_id) function, which creates a copy of the app
    object with the altered authorization ID. If you are listing authorizations, the
    authorization_id should be None.
    ## Parameters (required):
    - id [string]: unique id required to identify the app. ex: "mycompany.myapp"
    - private_key [EllipticCurve.PrivateKey()]: PEM string of the private key linked to the app. ex: "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEyTIHK6jYuik6ktM9FIF3yCEYzpLjO5X/\ntqDioGM+R2RyW0QEo+1DG8BrUf4UXHSvCjtQ0yLppygz23z0yPZYfw==\n-----END PUBLIC KEY-----"
    - environment [string]: environment where the app is being used. ex: "sandbox" or "production"
    - authorization_id [string]: unique id of the accessed MarketplaceAppAuthorization, if any. ex: None or "4848484848484848"
    ## Attributes (return-only):
    - pem [string]: private key in pem format. ex: "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEyTIHK6jYuik6ktM9FIF3yCEYzpLjO5X/\ntqDioGM+R2RyW0QEo+1DG8BrUf4UXHSvCjtQ0yLppygz23z0yPZYfw==\n-----END PUBLIC KEY-----"
    """

    def __init__(self, id, environment, private_key, authorization_id=None):
        self.authorization_id = authorization_id

        User.__init__(
            self,
            id=id,
            private_key=private_key,
            environment=environment,
        )

    def access_id(self):
        if self.authorization_id:
            return "marketplace-app-authorization/{id}".format(id=self.authorization_id)
        return "marketplace-app/{id}".format(id=self.id)

    def replace(app, authorization_id):
        return MarketplaceApp(
            id=app.id,
            environment=app.environment,
            private_key=app.pem,
            authorization_id=authorization_id,
        )
