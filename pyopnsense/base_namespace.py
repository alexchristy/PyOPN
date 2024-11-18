class BaseNamespace:
    """Base class for OPNsense namespaces to manage common functionality."""

    def __init__(self, wrapper):
        self._wrapper = wrapper
        self._clients = {}

    def _initialize_client(self, name, client_class):
        """Lazy initialization of clients."""
        if name not in self._clients:
            self._clients[name] = client_class(
                self._wrapper.api_key,
                self._wrapper.api_secret,
                self._wrapper.base_url,
                self._wrapper.verify_cert,
                self._wrapper.timeout,
            )
        return self._clients[name]