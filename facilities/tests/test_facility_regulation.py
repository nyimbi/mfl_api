import json
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import (
    LoginMixin,
    default
)
from common.models import (
    Ward, UserCounty,
    County,
    Constituency,
    Contact,
    ContactType,
    UserConstituency)

from ..serializers import (
    OwnerSerializer,
    FacilitySerializer,
    FacilityDetailSerializer,
    FacilityStatusSerializer,
    FacilityUnitSerializer,
    FacilityListSerializer,
    FacilityOfficerSerializer,
    RegulatoryBodyUserSerializer,
    FacilityUnitRegulationSerializer,
    FacilityUpdatesSerializer
)
from ..models import (
    OwnerType,
    Owner,
    FacilityStatus,
    Facility,
    FacilityUnit,
    FacilityRegulationStatus,
    FacilityType,
    ServiceCategory,
    Service,
    Option,
    FacilityService,
    FacilityContact,
    FacilityOfficer,
    Officer,
    RegulatingBody,
    RegulatoryBodyUser,
    FacilityUnitRegulation,
    RegulationStatus,
    FacilityApproval,
    FacilityUpdates,
    KephLevel,
    FacilityLevelChangeReason,
    RegulatorSync
)

from django.contrib.auth.models import Group, Permission


class RegulatorMixin(LoginMixin):

    def setUp(self):
        super(RegulatorMixin, self).setUp()
        self.regulator = mommy.make(RegulatingBody)
        self.facility1 = mommy.make(
            Facility, official_name="test facility",
            regulatory_body=self.regulator
        )
        self.facilities = mommy.make(Facility, _quantity=3)
        RegulatoryBodyUser.objects.create(
            user=self.user, regulatory_body=self.regulator
        )


class TestRegulatorSyncView(RegulatorMixin, APITestCase):

    def setUp(self):
        super(TestRegulatorSyncView, self).setUp()
        self.url = reverse("api:facilities:regulator_syncs_list")

    def test_post(self):
        county = mommy.make(County)
        owner = mommy.make(Owner)
        facility_type = mommy.make(FacilityType)
        data = {
            "name": "Jina",
            "registration_number": 100,
            "county": county.code,
            "owner": str(owner.id),
            "facility_type": str(facility_type.id)
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, RegulatorSync.objects.count())
        self.assertEqual(
            str(response.data['regulatory_body']), str(self.regulator.id)
        )

    def test_list(self):
        county = mommy.make(County)
        mommy.make(RegulatorSync, county=county.code)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

    def test_get_single(self):
        county = mommy.make(County)
        sync = mommy.make(RegulatorSync, county=county.code)
        url = self.url + str(sync.id) + "/"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)


class TestRegulatorSyncUpdateView(RegulatorMixin, APITestCase):

    def setUp(self):
        super(TestRegulatorSyncUpdateView, self).setUp()
        self._get_url = lambda pk: reverse(
            "api:facilities:regulator_sync_update", kwargs={"pk": pk}
        )
        self.sync_obj = RegulatorSync.objects.create(
            name=self.facility1.official_name.upper(),
            registration_number=100,
            county=self.facility1.ward.constituency.county.code,
            owner=self.facility1.owner,
            facility_type=self.facility1.facility_type,
            regulatory_body=self.regulator
        )

    def test_update(self):
        response = self.client.post(
            self._get_url(self.sync_obj.id), {"mfl_code": self.facility1.code}
        )
        self.assertEqual(response.status_code, 200)
        s = RegulatorSync.objects.get(pk=self.sync_obj.id)
        f = Facility.objects.get(pk=self.facility1.id)
        self.assertEqual(s.registration_number, f.registration_number)
        self.assertEqual(s.mfl_code, f.code)

    def test_fail_to_update_bad_mfl_code(self):
        response = self.client.post(
            self._get_url(self.sync_obj.id), {"mfl_code": 12345}
        )
        self.assertEqual(response.status_code, 404)
