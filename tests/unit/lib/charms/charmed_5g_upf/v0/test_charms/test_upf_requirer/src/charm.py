# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

import logging

from charms.charmed_5g_upf_interface.v0.upf import UPFRequires
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class WhateverCharm(CharmBase):
    def __init__(self, *args):
        """Creates a new instance of this object for each event."""
        super().__init__(*args)
        self.upf = UPFRequires(self, "upf")

        self.framework.observe(self.upf.on.upf_available, self._on_upf_available)

    def _on_upf_available(self, event):
        self.model.unit.status = ActiveStatus(event.upf_ip_address)


if __name__ == "__main__":
    main(WhateverCharm)
