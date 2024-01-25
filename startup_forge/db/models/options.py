from enum import Enum


class Role(str, Enum):
    """
    Options for roles
    """

    MENTOR = "MENTOR"
    MENTEE = "MENTEE"


class Industry(str, Enum):
    """
    Options for industries
    """

    FINTECH = "FINTECH"
    AI = "AI"
    ECOMMERCE = "ECOMMERCE"
    HEALTHCARE = "HEALTHCARE"
    EDTECH = "EDTECH"
    HEALTHTECH = "HEALTHTECH"
    CYBERSECURITY = "CYBERSECURITY"
    LOGISTICS = "LOGISTICS"
    MUSIC_ENTERTAINMENT = "MUSIC_ENTERTAINMENT"
    REAL_ESTATE = "REAL_ESTATE"
    SAAS = "SAAS"
    CONSUMER = "CONSUMER"
    BLOCKCHAIN = "BLOCKCHAIN"
    DIGITAL_MEDIA = "DIGITAL_MEDIA"


# Options for related industries
RelatedIndustry = {
    "FINTECH": [
        Industry.AI,
        Industry.ECOMMERCE,
        Industry.HEALTHCARE,
        Industry.LOGISTICS,
        Industry.SAAS,
        Industry.BLOCKCHAIN,
    ],
    "AI": [
        Industry.FINTECH,
        Industry.ECOMMERCE,
        Industry.HEALTHCARE,
        Industry.EDTECH,
        Industry.HEALTHTECH,
        Industry.CYBERSECURITY,
        Industry.LOGISTICS,
        Industry.MUSIC_ENTERTAINMENT,
        Industry.REAL_ESTATE,
        Industry.SAAS,
        Industry.CONSUMER,
        Industry.BLOCKCHAIN,
        Industry.DIGITAL_MEDIA,
    ],
    "ECOMMERCE": [
        Industry.FINTECH,
        Industry.AI,
        Industry.HEALTHCARE,
        Industry.LOGISTICS,
        Industry.REAL_ESTATE,
        Industry.SAAS,
        Industry.CONSUMER,
        Industry.DIGITAL_MEDIA,
    ],
    "HEALTHCARE": [
        Industry.FINTECH,
        Industry.AI,
        Industry.ECOMMERCE,
        Industry.EDTECH,
        Industry.HEALTHTECH,
        Industry.CYBERSECURITY,
        Industry.LOGISTICS,
        Industry.REAL_ESTATE,
        Industry.CONSUMER,
        Industry.BLOCKCHAIN,
        Industry.DIGITAL_MEDIA,
    ],
    "EDTECH": [Industry.AI, Industry.HEALTHCARE, Industry.DIGITAL_MEDIA],
    "HEALTHTECH": [
        Industry.AI,
        Industry.HEALTHCARE,
        Industry.LOGISTICS,
        Industry.BLOCKCHAIN,
        Industry.DIGITAL_MEDIA,
    ],
    "CYBERSECURITY": [
        Industry.AI,
        Industry.HEALTHCARE,
        Industry.LOGISTICS,
        Industry.BLOCKCHAIN,
    ],
    "LOGISTICS": [
        Industry.FINTECH,
        Industry.AI,
        Industry.HEALTHCARE,
        Industry.CYBERSECURITY,
        Industry.ECOMMERCE,
        Industry.REAL_ESTATE,
        Industry.BLOCKCHAIN,
    ],
    "MUSIC_ENTERTAINMENT": [Industry.AI, Industry.DIGITAL_MEDIA],
    "REAL_ESTATE": [
        Industry.FINTECH,
        Industry.ECOMMERCE,
        Industry.HEALTHCARE,
        Industry.LOGISTICS,
        Industry.SAAS,
        Industry.DIGITAL_MEDIA,
    ],
    "SAAS": [
        Industry.FINTECH,
        Industry.AI,
        Industry.ECOMMERCE,
        Industry.LOGISTICS,
        Industry.REAL_ESTATE,
        Industry.DIGITAL_MEDIA,
    ],
    "CONSUMER": [
        Industry.AI,
        Industry.ECOMMERCE,
        Industry.REAL_ESTATE,
        Industry.DIGITAL_MEDIA,
    ],
    "BLOCKCHAIN": [
        Industry.FINTECH,
        Industry.AI,
        Industry.HEALTHTECH,
        Industry.CYBERSECURITY,
        Industry.LOGISTICS,
    ],
    "DIGITAL_MEDIA": [
        Industry.AI,
        Industry.ECOMMERCE,
        Industry.HEALTHTECH,
        Industry.MUSIC_ENTERTAINMENT,
        Industry.REAL_ESTATE,
        Industry.SAAS,
        Industry.CONSUMER,
        Industry.BLOCKCHAIN,
    ],
}


class Day(str, Enum):
    """
    Options for days
    """

    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"
