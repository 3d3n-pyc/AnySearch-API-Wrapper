class Utils:

    def combine_url_with_endpoint(base_url: str, endpoint: str) -> str:
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]
        return base_url + "/" + endpoint