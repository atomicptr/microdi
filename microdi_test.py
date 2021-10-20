import microdi
import unittest


class ClientInterface:
    def request(self, url: str) -> dict:
        raise NotImplementedError()

    def is_fancy(self) -> bool:
        raise NotImplementedError()


@microdi.register("microdi.FancyClientImplementation", is_singleton=True)
class FancyClientImplementation(ClientInterface):
    def __init__(self, api_key: str):
        self._api_key = api_key

    def request(self, url: str) -> dict:
        # imagine a really cool API here...
        return {"api_key_length": len(self._api_key), "url_length": len(url)}

    def is_fancy(self) -> bool:
        return True


@microdi.register("microdi.ComplexImplementation", is_singleton=True)
class ComplexImplementation:
    def __init__(self, base_value: int = 0):
        self._base_value = base_value

    def complex_mathematical_operation(self, param1: int, param2: int) -> int:
        return self._base_value + param1 + param2


@microdi.register("microdi.NotSoFancyClientImplementation", is_singleton=True)
class NotSoFancyClientImplementation(ClientInterface):
    def request(self, url: str) -> dict:
        return {}

    def is_fancy(self) -> bool:
        return False


class TestMicroDI(unittest.TestCase):

    @microdi.inject(client=["microdi.FancyClientImplementation", "apikey"])
    def test_inject(self, client: ClientInterface) -> None:
        self.assertIsNotNone(client)
        res = client.request("fancy_url")
        self.assertEqual(res["api_key_length"], len("apikey"))
        self.assertEqual(res["url_length"], len("fancy_url"))

    @microdi.inject(
        fancy_client=["microdi.FancyClientImplementation", "apikey"],
        complex_impl="microdi.ComplexImplementation"
    )
    def test_inject_multiple(self, fancy_client: ClientInterface, complex_impl: ComplexImplementation) -> None:
        self.assertIsNotNone(fancy_client)
        self.assertIsNotNone(complex_impl)

    def test_overwrite_implementation(self):
        @microdi.inject(client=["microdi.FancyClientImplementation", "apikey"])
        def test_func(client: ClientInterface) -> bool:
            return client.is_fancy()
        # test this by creating our own instance
        self.assertFalse(test_func(client=NotSoFancyClientImplementation()))
        # test this by creating an instance via microdi
        self.assertFalse(test_func(client=microdi.get_instance("microdi.NotSoFancyClientImplementation")))

    def test_inject_without_singleton(self):
        @microdi.register("microdi.Counter")
        class Counter:
            def __init__(self):
                self._val = 0

            def get(self) -> int:
                return self._val

            def add(self) -> int:
                self._val += 1
                return self._val

        @microdi.inject(counter="microdi.Counter")
        def test_func(counter: Counter) -> int:
            counter.add()
            return counter.get()

        self.assertEqual(test_func(), 1)
        self.assertEqual(test_func(), 1)

    def test_inject_with_singleton(self):
        @microdi.register("microdi.CounterSingleton", is_singleton=True)
        class Counter:
            def __init__(self, initial_value=0):
                self._val = initial_value

            def get(self) -> int:
                return self._val

            def add(self) -> int:
                self._val += 1
                return self._val

        @microdi.inject(counter="microdi.CounterSingleton")
        def test_func(counter: Counter) -> int:
            counter.add()
            return counter.get()

        self.assertEqual(test_func(), 1)
        self.assertEqual(test_func(), 2)
        self.assertEqual(test_func(), 3)
        self.assertEqual(test_func(), 4)
        self.assertEqual(test_func(), 5)
        self.assertEqual(test_func(), 6)
