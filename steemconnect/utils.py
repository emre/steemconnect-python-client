def requires_access_token(func):
    def _decorated(self, *args, **kwargs):
        if not self.access_token:
            raise ValueError("you need to set your access_token"
                             " property for this method.")

        return func(self, *args, **kwargs)
    return _decorated


def requires_client_id_and_secret(func):
    def _decorated(self, *args, **kwargs):
        if not self.client_id or not self.client_secret:
            raise ValueError("you need to set your client_id and client_secret"
                             " properties for this method.")

        return func(self, *args, **kwargs)
    return _decorated
