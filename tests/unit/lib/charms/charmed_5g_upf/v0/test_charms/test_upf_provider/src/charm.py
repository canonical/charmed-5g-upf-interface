# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

import logging

from charms.charmed_5g_upf_interface.v0.upf import UPFProvides
from ops.charm import CharmBase
from ops.main import main

logger = logging.getLogger(__name__)


class WhateverCharm(CharmBase):
    TEST_UPF_IP_ADDRESS = ""

    def __init__(self, *args):
        """Creates a new instance of this object for each event."""
        super().__init__(*args)
        self.upf_provider = UPFProvides(self, "upf")

        self.framework.observe(self.upf_provider.on.upf_request, self._on_upf_request)

    def _on_upf_request(self, event):
        self.upf_provider.publish_upf_information(
            relation_id=event.relation_id,
            upf_ip_address=self.TEST_UPF_IP_ADDRESS,
        )


if __name__ == "__main__":
    main(WhateverCharm)
