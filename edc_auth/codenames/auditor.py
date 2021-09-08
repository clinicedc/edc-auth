from edc_adverse_event.auth_objects import ae_review, tmg_review

from .action_items import action_items

auditor = [
    "edc_action_item.view_reference",
    "edc_adverse_event.view_aeclassification",
    "edc_adverse_event.view_saereason",
    "edc_appointment.view_appointment",
    "edc_appointment.view_historicalappointment",
    "edc_crf.view_crfstatus",
    "edc_dashboard.view_lab_aliquot_listboard",
    "edc_dashboard.view_lab_box_listboard",
    "edc_dashboard.view_lab_manifest_listboard",
    "edc_dashboard.view_lab_pack_listboard",
    "edc_dashboard.view_lab_process_listboard",
    "edc_dashboard.view_lab_receive_listboard",
    "edc_dashboard.view_lab_requisition_listboard",
    "edc_dashboard.view_lab_result_listboard",
    "edc_dashboard.view_screening_listboard",
    "edc_dashboard.view_subject_listboard",
    "edc_dashboard.view_subject_review_listboard",
    "edc_lab.view_aliquot",
    "edc_lab.view_box",
    "edc_lab.view_boxitem",
    "edc_lab.view_boxtype",
    "edc_lab.view_consignee",
    "edc_lab.view_historicalaliquot",
    "edc_lab.view_historicalbox",
    "edc_lab.view_historicalboxitem",
    "edc_lab.view_historicalconsignee",
    "edc_lab.view_historicalmanifest",
    "edc_lab.view_historicalorder",
    "edc_lab.view_historicalresult",
    "edc_lab.view_historicalresultitem",
    "edc_lab.view_historicalshipper",
    "edc_lab.view_manifest",
    "edc_lab.view_manifestitem",
    "edc_lab.view_order",
    "edc_lab.view_panel",
    "edc_lab.view_result",
    "edc_lab.view_resultitem",
    "edc_lab.view_shipper",
    "edc_navbar.nav_ae_section",
    "edc_navbar.nav_lab_requisition",
    "edc_navbar.nav_lab_section",
    "edc_navbar.nav_screening_section",
    "edc_navbar.nav_subject_section",
    "edc_offstudy.view_historicalsubjectoffstudy",
    "edc_offstudy.view_subjectoffstudy",
]

auditor.extend(
    c for c in action_items if ("view_" in c or "edc_nav" in c or "edc_dashboard" in c)
)
auditor.extend(ae_review)
auditor.extend(tmg_review)
auditor = list(set(auditor))
