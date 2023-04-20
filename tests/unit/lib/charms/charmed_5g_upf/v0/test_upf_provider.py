# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

import unittest
from unittest.mock import PropertyMock, patch

from ops import testing
from test_charms.test_upf_provider.src.charm import WhateverCharm  # type: ignore[import]


class TestUPFProvides(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = testing.Harness(WhateverCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()
        self.relationship_name = "upf"

    @patch(
        "test_charms.test_upf_provider.src.charm.WhateverCharm.TEST_UPF_IP_ADDRESS",
        new_callable=PropertyMock,
    )
    def test_given_upf_relation_when_relation_created_then_upf_ip_address_is_published_in_the_relation_data(  # noqa: E501
        self, patched_test_upf_ip
    ):
        test_upf_ip = "1.2.3.4"
        patched_test_upf_ip.return_value = test_upf_ip
        relation_id = self.harness.add_relation(
            relation_name=self.relationship_name, remote_app="whatever-app"
        )
        self.harness.add_relation_unit(relation_id, "whatever-app/0")

        relation_data = self.harness.get_relation_data(
            relation_id=relation_id, app_or_unit=self.harness.charm.unit.name
        )
        self.assertEqual(test_upf_ip, relation_data["upf_ip_address"])
