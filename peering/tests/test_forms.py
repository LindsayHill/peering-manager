from django.test import TestCase

from peering.constants import *
from peering.forms import (
    AutonomousSystemEmailForm,
    AutonomousSystemForm,
    CommunityForm,
    ConfigurationForm,
    DirectPeeringSessionForm,
    EmailForm,
    InternetExchangeForm,
    InternetExchangePeeringSessionForm,
    RouterForm,
    RoutingPolicyForm,
)
from peering.models import AutonomousSystem, Configuration, Email, InternetExchange


class AutonomousSystemTest(TestCase):
    def test_autonomous_system_form(self):
        test = AutonomousSystemForm(data={"asn": 201281, "name": "Guillaume Mazoyer"})
        self.assertTrue(test.is_valid())
        self.assertTrue(test.save())

    def test_autonomous_system_email_form(self):
        email = Email.objects.create(name="E-mail", subject="Hello", template="World")
        test = AutonomousSystemEmailForm(
            data={
                "email": email.pk,
                "recipient": "test@example.net",
                "subject": "Hello",
                "body": "World",
            }
        )
        test.fields["recipient"].choices = [("test@example.net", "Hello")]
        self.assertTrue(test.is_valid())


class CommunityTest(TestCase):
    def test_community_form(self):
        test = CommunityForm(
            data={
                "name": "test",
                "slug": "test",
                "value": "64500:1",
                "type": COMMUNITY_TYPE_EGRESS,
            }
        )
        self.assertTrue(test.is_valid())
        self.assertTrue(test.save())


class ConfigurationTest(TestCase):
    def test_configuration_form(self):
        test = ConfigurationForm(data={"name": "Test", "template": "test_template"})
        self.assertTrue(test.is_valid())
        self.assertTrue(test.save())


class DirectPeeringSessionTest(TestCase):
    def setUp(self):
        super().setUp()

        self.autonomous_system = AutonomousSystem.objects.create(
            asn=201281, name="Guillaume Mazoyer"
        )

    def test_direct_peering_session_form(self):
        test = DirectPeeringSessionForm(
            data={
                "local_asn": 64500,
                "autonomous_system": self.autonomous_system.pk,
                "relationship": BGP_RELATIONSHIP_PRIVATE_PEERING,
                "ip_address": "2001:db8::1",
            }
        )
        self.assertTrue(test.is_valid())
        self.assertTrue(test.save())


class EmailTest(TestCase):
    def test_email_form(self):
        test = EmailForm(
            data={
                "name": "Test",
                "subject": "test_subject",
                "template": "test_template",
            }
        )
        self.assertTrue(test.is_valid())
        self.assertTrue(test.save())


class InternetExchangeTest(TestCase):
    def test_internet_exchange_form(self):
        test = InternetExchangeForm(data={"name": "Test", "slug": "test"})
        self.assertTrue(test.is_valid())
        self.assertTrue(test.save())


class InternetExchangePeeringSessionTest(TestCase):
    def setUp(self):
        super().setUp()

        self.autonomous_system = AutonomousSystem.objects.create(
            asn=201281, name="Guillaume Mazoyer"
        )
        self.internet_exchange = InternetExchange.objects.create(
            name="Test", slug="test"
        )

    def test_internet_exchange_peering_session_form(self):
        test = InternetExchangePeeringSessionForm(
            data={
                "autonomous_system": self.autonomous_system.pk,
                "internet_exchange": self.internet_exchange.pk,
                "ip_address": "2001:db8::1",
            }
        )
        self.assertTrue(test.is_valid())
        self.assertTrue(test.save())


class RouterTest(TestCase):
    def test_router_form(self):
        test = RouterForm(
            data={
                "netbox_device_id": 0,
                "name": "test",
                "hostname": "test.example.com",
                "platform": PLATFORM_JUNOS,
            }
        )
        self.assertTrue(test.is_valid())
        self.assertTrue(test.save())


class RoutingPolicyTest(TestCase):
    def test_routing_policy_form(self):
        test = RoutingPolicyForm(
            data={
                "name": "Test",
                "slug": "test",
                "type": ROUTING_POLICY_TYPE_IMPORT,
                "weight": 0,
                "address_family": 0,
            }
        )
        self.assertTrue(test.is_valid())
        self.assertTrue(test.save())
