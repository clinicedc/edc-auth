from .constants import (
    ACCOUNT_MANAGER_ROLE,
    AUDITOR_ROLE,
    CLINICIAN_ROLE,
    CUSTOM_ROLE,
    DATA_EXPORTER_ROLE,
    DATA_MANAGER_ROLE,
    LAB_TECHNICIAN_ROLE,
    NURSE_ROLE,
    PHARMACIST_ROLE,
    RANDO_VIEW_ROLE,
    SITE_COORDINATOR,
    SITE_DATA_MANAGER_ROLE,
    SITE_PHARMACIST_ROLE,
    STAFF_ROLE,
    TMG_ROLE,
)

from .group_names import (
    ACCOUNT_MANAGER,
    ADMINISTRATION,
    AE,
    AE_REVIEW,
    AUDITOR,
    CELERY_MANAGER,
    CLINIC,
    DATA_MANAGER,
    DATA_QUERY,
    DISPENSING,
    ENROLMENT,
    EVERYONE,
    EXPORT,
    LAB,
    LAB_VIEW,
    PHARMACY,
    PII,
    PII_VIEW,
    RANDO,
    REVIEW,
    SCREENING,
    SITE_DATA_MANAGER,
    TMG,
    UNBLINDING_REVIEWERS,
    UNBLINDING_REQUESTORS,
)

role_names = {
    ACCOUNT_MANAGER_ROLE: "Account Manager",
    AUDITOR_ROLE: "Auditor",
    CLINICIAN_ROLE: "Clinician",
    CUSTOM_ROLE: "Custom ...",
    DATA_EXPORTER_ROLE: "Data Exporter",
    DATA_MANAGER_ROLE: "Data Manager",
    LAB_TECHNICIAN_ROLE: "Laboratory Technician",
    NURSE_ROLE: "Research Nurse",
    PHARMACIST_ROLE: "Pharmacist",
    RANDO_VIEW_ROLE: "Randomization view",
    SITE_COORDINATOR: "Site Coordinator",
    SITE_DATA_MANAGER_ROLE: "Site Data Manager",
    SITE_PHARMACIST_ROLE: "Site Pharmacist",
    STAFF_ROLE: "Staff",
    TMG_ROLE: "TMG (External Review",
}

required_role_names = {STAFF_ROLE: "Staff"}

groups_by_role_name = {
    ACCOUNT_MANAGER_ROLE: [ACCOUNT_MANAGER, ADMINISTRATION, EVERYONE],
    AUDITOR_ROLE: [
        ADMINISTRATION,
        AE_REVIEW,
        AUDITOR,
        ENROLMENT,
        EVERYONE,
        LAB_VIEW,
        PII_VIEW,
        REVIEW,
    ],
    CLINICIAN_ROLE: [
        ADMINISTRATION,
        AE,
        CLINIC,
        DATA_QUERY,
        ENROLMENT,
        EVERYONE,
        LAB,
        PII,
        REVIEW,
        SCREENING,
        UNBLINDING_REQUESTORS,
    ],
    CUSTOM_ROLE: [],
    DATA_EXPORTER_ROLE: [ADMINISTRATION, EVERYONE, EXPORT],
    DATA_MANAGER_ROLE: [
        ADMINISTRATION,
        AE,
        CELERY_MANAGER,
        CLINIC,
        DATA_MANAGER,
        ENROLMENT,
        EVERYONE,
        LAB,
        PII,
        REVIEW,
        SCREENING,
        UNBLINDING_REQUESTORS,
    ],
    LAB_TECHNICIAN_ROLE: [ADMINISTRATION, EVERYONE, LAB, PII_VIEW],
    NURSE_ROLE: [
        ADMINISTRATION,
        AE,
        CLINIC,
        DATA_QUERY,
        EVERYONE,
        LAB,
        PII,
        REVIEW,
        SCREENING,
        UNBLINDING_REQUESTORS,
    ],
    PHARMACIST_ROLE: [ADMINISTRATION, EVERYONE, PHARMACY, RANDO],
    RANDO_VIEW_ROLE: [ADMINISTRATION, EVERYONE, RANDO],
    STAFF_ROLE: [ADMINISTRATION, EVERYONE],
    SITE_PHARMACIST_ROLE: [ADMINISTRATION, EVERYONE, DISPENSING, RANDO],
    SITE_COORDINATOR: [ADMINISTRATION, EVERYONE],
    SITE_DATA_MANAGER_ROLE: [ADMINISTRATION, EVERYONE, REVIEW, SITE_DATA_MANAGER],
    TMG_ROLE: [ADMINISTRATION, EVERYONE, REVIEW, TMG, UNBLINDING_REVIEWERS],
}
