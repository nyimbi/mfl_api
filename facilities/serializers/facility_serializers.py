import json

from django.utils import timezone
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.models import ContactType, Contact

from common.serializers import (
    AbstractFieldsMixin,
    PhysicalAddressSerializer,
    ContactSerializer
)


from ..models import (
    OwnerType,
    Owner,
    JobTitle,
    Officer,
    OfficerContact,
    FacilityStatus,
    FacilityType,
    RegulatingBody,
    RegulationStatus,
    Facility,
    FacilityRegulationStatus,
    FacilityContact,
    FacilityUnit,
    ServiceCategory,
    Option,
    Service,
    FacilityService,
    FacilityServiceRating,
    ServiceOption,
    FacilityApproval,
    FacilityOperationState,
    FacilityUpgrade,
    RegulatingBodyContact,
    FacilityOfficer,
    RegulatoryBodyUser,
    FacilityUnitRegulation,
    FacilityUpdates,
    KephLevel
)


class CreateFacilityOfficerMixin(object):
    """
    A custom view for creating facility officers.
    Make it less painful to create facility officers via the frontend.
    """

    def _validate_required_fields(self, data):
        facility_id = data.get('facility_id', None)
        name = data.get('name', None)
        title = data.get('title', None)
        id_number = data.get('id_no', None)
        if not facility_id or not name or not title or not id_number:
            error_message = "Facility id , name, ID number and"\
                            "job title of the officer are "\
                            "required"
            return error_message

    def _validate_facility(self, data):
        try:
            Facility.objects.get(id=data.get('facility_id', None))
        except Facility.DoesNotExist:
            error_message = {
                "facility": "Facility provided does not exist"
            }
            return error_message

    def _validate_job_titles(self, data):
        try:
            JobTitle.objects.get(id=data['title'])
        except JobTitle.DoesNotExist:
            error_message = {
                "job title": "JobTitle with id {} does not exist".format(
                    data['title'])
            }
            return error_message

    def data_is_valid(self, data):
        errors = [
            self._validate_required_fields(data),
            self._validate_facility(data),
            self._validate_job_titles(data)
        ]
        errors = [error for error in errors if error is not None]
        if errors:
            return errors
        else:
            return True

    def _inject_creating_user(self, attributes_dict):
        attributes_dict['created_by'] = self.user
        attributes_dict['updated_by'] = self.user
        return attributes_dict

    def _create_contacts(self, data):
        contacts = data.get('contacts', None)
        created_contacts = []
        if contacts:
            for contact in contacts:

                contact_type = ContactType.objects.get(
                    id=contact.get('type'))
                contact_dict = {
                    "contact_type": contact_type,
                    "contact": contact.get('contact')
                }
                contact_dict = self._inject_creating_user(contact_dict)
                created_contacts.append(Contact.objects.create(**contact_dict))
        return created_contacts

    def _create_facility_officer(self, data):
        facility = Facility.objects.get(id=data['facility_id'])
        job_title = JobTitle.objects.get(id=data['title'])

        officer_dict = {
            "name": data['name'],
            "job_title": job_title,
        }
        officer_dict = self._inject_creating_user(officer_dict)

        id_no = data.get('id_no', None)
        reg_no = data.get('reg_no', None)
        officer_dict['id_number'] = id_no if id_no else None
        officer_dict['registration_number'] = reg_no if reg_no else None

        officer = Officer.objects.create(**officer_dict)
        facility_officer_dict = {
            "facility": facility,
            "officer": officer
        }
        facility_officer_dict = self._inject_creating_user(
            facility_officer_dict)
        facility_officer = FacilityOfficer.objects.create(
            **facility_officer_dict)

        # link the officer to the contacts
        created_contacts = self._create_contacts(data)
        for contact in created_contacts:
            contact_dict = {
                "officer": officer,
                "contact": contact
            }
            contact_dict = self._inject_creating_user(contact_dict)
            OfficerContact.objects.create(**contact_dict)
        return facility_officer

    def create_officer(self, data):
        valid_data = self.data_is_valid(data)

        if valid_data is not True:

            return {
                "created": False,
                "detail": valid_data
            }
        else:
            facility_officer = self._create_facility_officer(data)
            serialized_officer = FacilityOfficerSerializer(
                facility_officer).data
            return {
                "created": True,
                "detail": serialized_officer
            }


class KephLevelSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = KephLevel


class RegulatoryBodyUserSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    user_name = serializers.ReadOnlyField(source='user.get_full_name')
    regulatory_body_name = serializers.ReadOnlyField(
        source='regulatory_body.name')

    class Meta:
        model = RegulatoryBodyUser


class FacilityOfficerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer,):
    facility_name = serializers.ReadOnlyField(source='facility.name')
    officer_name = serializers.ReadOnlyField(source='officer.name')
    id_number = serializers.ReadOnlyField(source='officer.id_number')
    registration_number = serializers.ReadOnlyField(
        source='officer.registration_number')
    job_title = serializers.ReadOnlyField(source='officer.job_title.name')

    class Meta(object):
        model = FacilityOfficer


class RegulatingBodyContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    contact_text = serializers.ReadOnlyField(source='contact.contact')
    contact_type = serializers.ReadOnlyField(
        source='contact.contact_type.name'

    )

    class Meta(object):
        model = RegulatingBodyContact


class FacilityUpgradeSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityUpgrade


class FacilityOperationStateSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityOperationState


class FacilityApprovalSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    done_by = serializers.ReadOnlyField(source="created_by.get_full_name")

    class Meta(object):
        model = FacilityApproval


class ServiceCategorySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = ServiceCategory


class OptionSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = Option


class ServiceOptionSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    display_text = serializers.ReadOnlyField(source="option.display_text")
    value = serializers.ReadOnlyField(source="option.value")
    is_exclusive_option = serializers.ReadOnlyField(
        source="option.is_exclusive_option"
    )
    option_type = serializers.ReadOnlyField(source="option.option_type")
    service_name = serializers.ReadOnlyField(source="service.name")

    class Meta(object):
        model = ServiceOption


class ServiceSerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True)
    service_options = ServiceOptionSerializer(many=True, required=False)

    class Meta(object):
        model = Service
        read_only_fields = ('code',)


class FacilityServiceSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    service_name = serializers.CharField(read_only=True)
    option_display_value = serializers.CharField(read_only=True)
    average_rating = serializers.ReadOnlyField()
    number_of_ratings = serializers.ReadOnlyField()
    service_has_options = serializers.ReadOnlyField()

    class Meta(object):
        model = FacilityService


class FacilityStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityStatus


class RegulatingBodySerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    regulatory_body_type_name = serializers.ReadOnlyField(
        source='regulatory_body_type.name'
    )

    class Meta(object):
        model = RegulatingBody


class OwnerTypeSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = OwnerType


class FacilityRegulationStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityRegulationStatus


class FacilityTypeSerializer(serializers.ModelSerializer):
    owner_type_name = serializers.ReadOnlyField(source='owner_type.name')

    class Meta(object):
        model = FacilityType


class OfficerContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = OfficerContact


class JobTitleSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = JobTitle


class RegulationStatusSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    next_state_name = serializers.CharField(read_only=True)
    previous_state_name = serializers.CharField(read_only=True)

    class Meta(object):
        model = RegulationStatus


class OfficerSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    job_title_name = serializers.ReadOnlyField(source='job_title.name')

    class Meta(object):
        model = Officer


class OwnerSerializer(AbstractFieldsMixin, serializers.ModelSerializer):

    owner_type_name = serializers.ReadOnlyField(source='owner_type.name')

    class Meta(object):
        model = Owner
        read_only_fields = ('code',)


class FacilityContactSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    contact_type = serializers.ReadOnlyField(
        source="contact.contact_type.name")
    actual_contact = serializers.ReadOnlyField(source="contact.contact")

    class Meta(object):
        model = FacilityContact


class FacilityUnitSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    regulation_status = serializers.ReadOnlyField()
    regulating_body_name = serializers.ReadOnlyField(
        source="regulating_body.name")

    class Meta(object):
        model = FacilityUnit


class FacilitySerializer(AbstractFieldsMixin, serializers.ModelSerializer):
    regulatory_status_name = serializers.CharField(read_only=True)
    facility_type_name = serializers.CharField(read_only=True)
    owner_name = serializers.CharField(read_only=True)
    owner_type_name = serializers.CharField(read_only=True)
    owner_type = serializers.CharField(
        read_only=True, source='owner.owner_type.pk')
    operation_status_name = serializers.CharField(read_only=True)
    county = serializers.CharField(read_only=True)
    constituency = serializers.CharField(read_only=True)
    ward_name = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    facility_services = serializers.ReadOnlyField(
        source="get_facility_services")
    is_approved = serializers.ReadOnlyField()
    has_edits = serializers.ReadOnlyField()
    latest_update = serializers.ReadOnlyField()
    regulatory_body_name = serializers.ReadOnlyField(
        source="regulatory_body.name"
    )
    owner = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Owner.objects.all())

    class Meta(object):
        model = Facility

    @transaction.atomic
    def create(self, validated_data):
        # prepare the audit fields
        context = self.context
        audit_data = {
            "created_by_id": self.context['request'].user.id,
            "updated_by_id": self.context['request'].user.id,
            "created": (
                validated_data['created'] if
                validated_data.get('created') else timezone.now()),
            "updated": (
                validated_data['update'] if
                validated_data.get('updated') else timezone.now())
        }
        inject_audit_fields = lambda dict_a: dict_a.update(audit_data)

        # create new owners
        errors = []

        def create_owner(owner_data):
            inject_audit_fields(owner_data)
            owner = OwnerSerializer(data=owner_data, context=context)
            if owner.is_valid():
                return owner.save()
            else:
                errors.append(json.dumps(owner.errors))

        new_owner = self.initial_data.pop('new_owner', None)
        if new_owner:
            owner = create_owner(new_owner)
            validated_data['owner'] = owner

        # create the physical address
        def create_physical_address(location_data):
            inject_audit_fields(location_data)
            location = PhysicalAddressSerializer(
                data=location_data, context=context)
            return location.save() if location.is_valid() else errors.append(
                "errors in creating physical address")

        location = self.initial_data.pop('location_data', None)
        if location:
            physical_address = create_physical_address(location)
            validated_data['physical_address'] = physical_address
        if errors:
            raise ValidationError(json.dumps({"detail": errors}))
        return super(FacilitySerializer, self).create(validated_data)


class FacilityDetailSerializer(CreateFacilityOfficerMixin, FacilitySerializer):
    regulatory_status_name = serializers.CharField(read_only=True)
    facility_services = serializers.ReadOnlyField(
        source="get_facility_services")
    facility_contacts = serializers.ReadOnlyField(
        read_only=True, source="get_facility_contacts")
    facility_physical_address = serializers.DictField(
        read_only=True, required=False)
    coordinates = serializers.ReadOnlyField()
    latest_approval = serializers.ReadOnlyField()
    boundaries = serializers.ReadOnlyField()
    service_catalogue_active = serializers.ReadOnlyField()
    facility_units = FacilityUnitSerializer(many=True, required=False)

    class Meta(object):
        model = Facility
        exclude = ('attributes', )

    @transaction.atomic
    def update(self, instance, validated_data):
        contacts = self.initial_data.pop('contacts', None)
        units = self.initial_data.pop('units', None)
        services = self.initial_data.pop('services', None)
        officer_in_charge = self.initial_data.pop('officer_in_charge', None)
        errors = []
        facility = super(FacilityDetailSerializer, self).update(
            instance, validated_data)
        audit_data = {
            "created_by_id": self.context['request'].user.id,
            "updated_by_id": self.context['request'].user.id,
            "created": (
                validated_data['created'] if
                validated_data.get('created') else timezone.now()),
            "updated": (
                validated_data['update'] if
                validated_data.get('updated') else timezone.now())
        }
        inject_audit_fields = lambda dict_a: dict_a.update(audit_data)

        def create_contact(contact_data):
            contact = ContactSerializer(
                data=contact_data, context=self.context)
            if contact.is_valid():
                return contact.save()
            else:
                errors.append(json.dumps(contact.errors))

        def create_facility_contacts(contact_data):
            contact = create_contact(contact_data)
            facility_contact_data = {
                "contact": contact,
                "facility": instance
            }
            inject_audit_fields(facility_contact_data)
            try:
                FacilityContact.objects.create(**facility_contact_data)
            except:
                error = "The contacts provided did not validate"
                errors.append(error)

        def create_facility_units(unit_data):
            unit_data['facility'] = instance.id
            inject_audit_fields(unit_data)
            unit = FacilityUnitSerializer(data=unit_data, context=self.context)
            if unit.is_valid():
                return unit.save()
            else:
                errors.append((json.dumps(unit.errors)))

        def create_facility_services(service_data):
            service_data['facility'] = instance.id
            inject_audit_fields(service_data)
            f_service = FacilityServiceSerializer(
                data=service_data, context=self.context)
            if f_service.is_valid():
                f_service.save()
            else:
                errors.append(json.dumps(f_service.errors))
        if officer_in_charge:
            self.user = self.context['request'].user
            officer_in_charge['facility_id'] = facility.id
            created_officer = self.create_officer(officer_in_charge)
            if not created_officer.get("created"):
                errors = created_officer.get("detail")

        if contacts:
            map(create_facility_contacts, contacts)
        if units:
            map(create_facility_units, units)
        if services:
            map(create_facility_services, services)
        if errors:
            raise ValidationError(errors)
        return instance


class FacilityListSerializer(FacilitySerializer):

    class Meta(object):
        model = Facility
        fields = [
            'code', 'name', 'id', 'county', 'constituency',
            'facility_type_name', 'owner_name', 'owner_type_name',
            'regulatory_status_name', 'ward', 'operation_status_name',
            'ward_name', 'is_published', "is_approved", "has_edits",
            "rejected"
        ]


class FacilityServiceRatingSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    class Meta(object):
        model = FacilityServiceRating


class FacilityUnitRegulationSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):
    class Meta(object):
        model = FacilityUnitRegulation


class FacilityUpdatesSerializer(
        AbstractFieldsMixin, serializers.ModelSerializer):

    facility_updates = serializers.ReadOnlyField()
    facility_updated_json = serializers.ReadOnlyField()
    facility = FacilityDetailSerializer(required=False)
    created_by_name = serializers.ReadOnlyField(
        source='created_by.get_full_name')

    class Meta:
        model = FacilityUpdates
        exclude = ('facility_updates', )
