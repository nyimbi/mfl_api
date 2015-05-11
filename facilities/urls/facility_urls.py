from django.conf.urls import url, patterns

from ..views import (
    FacilityStatusListView,
    FacilityStatusDetailView,
    JobTitleListView,
    JobTitleDetailView,
    OfficerListView,
    OfficerDetailView,
    RegulatingBodyListView,
    RegulatingBodyDetailView,
    OwnerTypeListView,
    OwnerTypeDetailView,
    OfficerContactListView,
    OfficerContactDetailView,
    OwnerListView,
    OwnerDetailView,
    FacilityListView,
    FacilityDetailView,
    FacilityContactListView,
    FacilityContactDetailView,
    FacilityRegulationStatusListView,
    FacilityRegulationStatusDetailView,
    FacilityTypeListView,
    FacilityTypeDetailView,
    RegulationStatusListView,
    RegulationStatusDetailView,
    FacilityUnitsListView,
    FacilityUnitDetailView,
    ServiceCategoryListView,
    ServiceCategoryDetailView,
    OptionListView,
    OptionDetailView,
    ServiceListView,
    ServiceDetailView,
    FacilityServiceListView,
    FacilityServiceDetailView,
    ServiceOptionListView,
    ServiceOptionDetailView,
    ServiceRatingListView,
    ServiceRatingDetailView,
    FacilityApprovalListView,
    FacilityApprovalDetailView,
    FacilityOperationStateListView,
    FacilityOperationStateDetailView,
    FacilityUpgradeListView,
    FacilityUpgradeDetailView,
    get_cover_report,
    get_inspection_report,
    RegulatingBodyContactListView,
    RegulatingBodyContactDetailView,
    get_correction_template,
    DashBoard
)
urlpatterns = patterns(
    '',

    url(r'^dashboard/$', DashBoard.as_view(),
        name='dashboard'),

    url(r'^facility_correction_template/(?P<facility_id>[^/]+)/$',
        get_correction_template,
        name='facility_correction_template'),
    url(r'^facility_inspection_report/(?P<facility_id>[^/]+)/$',
        get_inspection_report,
        name='facility_inspection_report'),

    url(r'^facility_cover_report/(?P<facility_id>[^/]+)/$', get_cover_report,
        name='facility_cover_report'),
    url(r'^facility_inspection_report/(?P<facility_id>[^/]+)/$',
        get_inspection_report,
        name='facility_inspection_report'),

    url(r'^regulating_body_contacts/$',
        RegulatingBodyContactListView.as_view(),
        name='regulating_body_contacts_list'),
    url(r'^regulating_body_contacts/(?P<pk>[^/]+)/$',
        RegulatingBodyContactDetailView.as_view(),
        name='regulating_body_contact_detail'),

    url(r'^facility_upgrade/$',
        FacilityUpgradeListView.as_view(),
        name='facility_upgrades_list'),
    url(r'^facility_upgrade/(?P<pk>[^/]+)/$',
        FacilityUpgradeDetailView.as_view(),
        name='facility_upgrade_detail'),

    url(r'^facility_operation_state/$',
        FacilityOperationStateListView.as_view(),
        name='facility_operation_states_list'),
    url(r'^facility_operation_state/(?P<pk>[^/]+)/$',
        FacilityOperationStateDetailView.as_view(),
        name='facility_operation_state_detail'),

    url(r'^facilitiy_approvals/$', FacilityApprovalListView.as_view(),
        name='facility_approvals_list'),
    url(r'^facilitiy_approvals/(?P<pk>[^/]+)/$',
        FacilityApprovalDetailView.as_view(),
        name='facility_approval_detail'),

    url(r'^service_ratings/$', ServiceRatingListView.as_view(),
        name='service_ratings_list'),
    url(r'^service_ratings/(?P<pk>[^/]+)/$',
        ServiceRatingDetailView.as_view(),
        name='service_rating_detail'),

    url(r'^service_categories/$', ServiceCategoryListView.as_view(),
        name='service_categories_list'),
    url(r'^service_categories/(?P<pk>[^/]+)/$',
        ServiceCategoryDetailView.as_view(),
        name='service_category_detail'),

    url(r'^services/$', ServiceListView.as_view(),
        name='services_list'),
    url(r'^services/(?P<pk>[^/]+)/$', ServiceDetailView.as_view(),
        name='service_detail'),

    url(r'^options/$', OptionListView.as_view(),
        name='options_list'),
    url(r'^options/(?P<pk>[^/]+)/$', OptionDetailView.as_view(),
        name='option_detail'),

    url(r'^facility_services/$', FacilityServiceListView.as_view(),
        name='facility_services_list'),
    url(r'^facility_services/(?P<pk>[^/]+)/$',
        FacilityServiceDetailView.as_view(),
        name='facility_service_detail'),

    url(r'^service_options/$', ServiceOptionListView.as_view(),
        name='service_options_list'),
    url(r'^service_options/(?P<pk>[^/]+)/$', ServiceOptionDetailView.as_view(),
        name='service_option_detail'),

    url(r'^facility_units/$', FacilityUnitsListView.as_view(),
        name='facility_units_list'),
    url(r'^facility_units/(?P<pk>[^/]+)/$', FacilityUnitDetailView.as_view(),
        name='facility_unit_detail'),

    url(r'^regulating_bodies/$', RegulatingBodyListView.as_view(),
        name='regulating_bodies_list'),
    url(r'^regulating_bodies/(?P<pk>[^/]+)/$',
        RegulatingBodyDetailView.as_view(),
        name='regulating_body_detail'),

    url(r'^facility_types/$', FacilityTypeListView.as_view(),
        name='facility_types_list'),
    url(r'^facility_types/(?P<pk>[^/]+)/$', FacilityTypeDetailView.as_view(),
        name='facility_type_detail'),

    url(r'^facility_status/$', FacilityStatusListView.as_view(),
        name='facility_statuses_list'),
    url(r'^facility_status/(?P<pk>[^/]+)/$',
        FacilityStatusDetailView.as_view(),
        name='facility_status_detail'),

    url(r'^officer_contacts/$', OfficerContactListView.as_view(),
        name='officer_contacts_list'),
    url(r'^officer_contacts/(?P<pk>[^/]+)/$',
        OfficerContactDetailView.as_view(),
        name='officer_contact_detail'),

    url(r'^job_titles/$', JobTitleListView.as_view(),
        name='job_titles_list'),
    url(r'^job_titles/(?P<pk>[^/]+)/$', JobTitleDetailView.as_view(),
        name='job_title_detail'),

    url(r'^facility_regulation_status/$',
        FacilityRegulationStatusListView.as_view(),
        name='facility_regulation_statuses_list'),
    url(r'^facility_regulation_status/(?P<pk>[^/]+)/$',
        FacilityRegulationStatusDetailView.as_view(),
        name='facility_regulation_status_detail'),

    url(r'^regulation_status/$', RegulationStatusListView.as_view(),
        name='regulation_statuses_list'),
    url(r'^regulation_status/(?P<pk>[^/]+)/$',
        RegulationStatusDetailView.as_view(),
        name='regulation_status_detail'),

    url(r'^officers/$', OfficerListView.as_view(),
        name='officers_in_charge_list'),
    url(r'^officers_incharge/(?P<pk>[^/]+)/$',
        OfficerDetailView.as_view(),
        name='officer_detail'),

    url(r'^owner_types/$', OwnerTypeListView.as_view(),
        name='owner_types_list'),
    url(r'^owner_types/(?P<pk>[^/]+)/$', OwnerTypeDetailView.as_view(),
        name='owner_type_detail'),

    url(r'^owners/$', OwnerListView.as_view(), name='owners_list'),
    url(r'^owners/(?P<pk>[^/]+)/$', OwnerDetailView.as_view(),
        name='owner_detail'),

    url(r'^contacts/$', FacilityContactListView .as_view(),
        name='facility_contacts_list'),
    url(r'^contacts/(?P<pk>[^/]+)/$', FacilityContactDetailView.as_view(),
        name='facility_contact_detail'),

    url(r'^facilities/$', FacilityListView.as_view(), name='facilities_list'),
    url(r'^facilities/(?P<pk>[^/]+)/$', FacilityDetailView.as_view(),
        name='facility_detail'),
)
