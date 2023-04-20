# Charmed 5G UPF interface

This library offers a way of providing and consuming an IP address of the Charmed 5G's UPF.

To get started using the library, you just need to fetch the library using `charmcraft`.

```shell
cd some-charm
charmcraft fetch-lib charms.charmed_5g_upf_interface.v0.upf
```

Charms providing UPF should use `UPFProvides`.
Typical usage of this class would look something like:

```python
...
from charms.charmed_5g_upf_interface.v0.upf import UPFProvides
...

class SomeProviderCharm(CharmBase):

    def __init__(self, *args):
        ...
        self.upf_provider = UPFProvides(charm=self, relationship_name="upf")
        ...
        self.framework.observe(self.upf_provider.on.upf_request, self._on_upf_request)

    def _on_upf_request(self, event):
        ...
        self.upf_provider.publish_upf_information(
            relation_id=event.relation_id,
            upf_ip_address=<UPF IP ADDRESS>,
        )
```

And a corresponding section in charm's `metadata.yaml`:
```
provides:
    upf:  # Relation name
        interface: upf  # Relation interface
```

Charms that require UPF should use `UPFRequires`.
Typical usage of this class would look something like:

```python
...
from charms.charmed_5g_upf_interface.v0.upf import UPFRequires
...

class SomeRequirerCharm(CharmBase):

    def __init__(self, *args):
        ...
        self.upf = UPFRequires(charm=self, relationship_name="upf")
        ...
        self.framework.observe(self.upf.on.upf_available, self._on_upf_available)

    def _on_upf_available(self, event):
        upf_ip_address = event.upf_ip_address
        # Do something with the UPF's IP address
```

And a corresponding section in charm's `metadata.yaml`:
```
requires:
    upf:  # Relation name
        interface: upf  # Relation interface
```
