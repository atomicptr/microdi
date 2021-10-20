# microDI

Super tiny and minimal dependency injection package for Python.

## Why?

I needed a simple solution for DI that is preferably contained to a single file that I can just drop into projects
where dependency management isn't an option.

## Usage

````python
import microdi

class ClientInterface:
    def request(self, url: str) -> dict:
        raise NotImplementedError()

# You can register an implementation using the "microdi.register" decorator. It has one required argument
# which is a name for the implementation which you'll later need to inject the implementation again.
# There is also an option to make the implementation a singleton which will prevent microdi from creating
# a new instance every time you inject it somewhere and instead have it create only one instance and reuse it
# when its needed.
@microdi.register("example.Client", is_singleton=True)
class Client(ClientInterface):
    def request(self, url: str) -> dict:
        # do some stuff here
        return {"url": "..."}

BASE_URL = "https://domain.com"

# "microdi.inject" will look for an implementation registered under the name "example.Client" and inject it into the
# "client" argument.
@microdi.inject(client="example.Client")
def request_api(endpoint: str, client: ClientInterface) -> dict:
    return client.request(BASE_URL + "/api/something")
````

## License

```
Copyright (C) 2021 Christopher Kaster

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.
 
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
```