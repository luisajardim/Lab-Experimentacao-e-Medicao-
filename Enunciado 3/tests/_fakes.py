"""Fakes de httpx para testes (executam sem rede)."""


class FakeResponse:
    def __init__(self, status_code=200, json_data=None, headers=None, text=""):
        self.status_code = status_code
        self._json_data = json_data
        self.headers = headers or {}
        self.text = text

    def json(self):
        if self._json_data is None:
            raise ValueError("resposta sem JSON")
        return self._json_data


class FakeSession:
    """Sessão httpx falsa: devolve respostas pré-programadas."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.requests = []

    def request(self, method, url, params=None, json=None):
        self.requests.append(
            {"method": method, "url": url, "params": params, "json": json}
        )
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    def close(self):
        pass
