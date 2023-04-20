# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""The UPF charm relation interface.

This library offers a way of providing and consuming an IP address of the Charmed 5G's UPF.

To get started using the library, you just need to fetch the library using `charmcraft`.

```shell
cd some-charm
charmcraft fetch-lib charms.charmed_5g_upf_interface.v0.upf
```

Charms providing the UPF should use `UPFProvides`.
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
                upf_ip_address=ip_address,
            )
    ```

    And a corresponding section in charm's `metadata.yaml`:
    ```
    provides:
        upf:  # Relation name
            interface: upf  # Relation interface
    ```

Charms that require the UPF should use `UPFRequires`.
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
"""

from ops.charm import CharmBase, CharmEvents, RelationChangedEvent, RelationJoinedEvent
from ops.framework import EventBase, EventSource, Object

# The unique Charmhub library identifier, never change it
LIBID = "To be defined"

# Increment this major API version when introducing breaking changes
LIBAPI = 0

# Increment this PATCH version before using `charmcraft publish-lib` or reset
# to 0 if you are raising the major API version
LIBPATCH = 1


class UPFRequestEvent(EventBase):
    """Dataclass for the UPF request event."""

    def __init__(self, handle, relation_id: int):
        """Sets relation id."""
        super().__init__(handle)
        self.relation_id = relation_id

    def snapshot(self) -> dict:
        """Returns event data."""
        return {
            "relation_id": self.relation_id,
        }

    def restore(self, snapshot):
        """Restores event data."""
        self.relation_id = snapshot["relation_id"]


class UPFProviderCharmEvents(CharmEvents):
    """Custom events for the UPFProvider."""

    upf_request = EventSource(UPFRequestEvent)


class UPFProvides(Object):
    """Class to be instantiated by provider of the UPF."""

    on = UPFProviderCharmEvents()

    def __init__(self, charm: CharmBase, relationship_name: str):
        """Observes relation joined event.

        Args:
            charm: Juju charm
            relationship_name (str): Relation name
        """
        self.relationship_name = relationship_name
        self.charm = charm
        super().__init__(charm, relationship_name)
        self.framework.observe(
            charm.on[relationship_name].relation_joined, self._on_relation_joined
        )

    def publish_upf_information(self, relation_id: int, upf_ip_address: str) -> None:
        """Sets private key in relation data.

        Args:
            relation_id (str): Relation ID
            upf_ip_address (str): UPF's IP address
        """
        relation = self.model.get_relation(
            relation_name=self.relationship_name, relation_id=relation_id
        )
        relation.data[self.model.unit]["upf_ip_address"] = upf_ip_address  # type: ignore[union-attr]  # noqa: E501

    def _on_relation_joined(self, event: RelationJoinedEvent) -> None:
        """Triggered whenever a requirer charm joins the relation.

        Args:
            event (RelationJoinedEvent): Juju event
        """
        self.on.upf_request.emit(relation_id=event.relation.id)


class UPFAvailableEvent(EventBase):
    """Dataclass for the UPF available event."""

    def __init__(self, handle, upf_ip_address: str):
        """Sets certificate."""
        super().__init__(handle)
        self.upf_ip_address = upf_ip_address

    def snapshot(self) -> dict:
        """Returns event data."""
        return {"upf_ip_address": self.upf_ip_address}

    def restore(self, snapshot):
        """Restores event data."""
        self.upf_ip_address = snapshot["upf_ip_address"]


class UPFRequirerCharmEvents(CharmEvents):
    """Custom events for the UPFRequirer."""

    upf_available = EventSource(UPFAvailableEvent)


class UPFRequires(Object):
    """Class to be instantiated by requirer of the UPF."""

    on = UPFRequirerCharmEvents()

    def __init__(self, charm: CharmBase, relationship_name: str):
        """Observes relation joined and relation changed events.

        Args:
            charm: Juju charm
            relationship_name (str): Relation name
        """
        self.relationship_name = relationship_name
        self.charm = charm
        super().__init__(charm, relationship_name)
        self.framework.observe(
            charm.on[relationship_name].relation_joined, self._on_relation_changed
        )
        self.framework.observe(
            charm.on[relationship_name].relation_changed, self._on_relation_changed
        )

    def _on_relation_changed(self, event: RelationChangedEvent) -> None:
        """Triggered everytime there's a change in relation data.

        Args:
            event (RelationChangedEvent): Juju event
        """
        relation_data = event.relation.data
        upf_ip_address = relation_data[event.unit].get("upf_ip_address")  # type: ignore[index]
        if upf_ip_address:
            self.on.upf_available.emit(upf_ip_address=upf_ip_address)
