from enum import Enum


class RequirementValueType(str, Enum):
    TEXT = "Text"
    LONG_TEXT = "LongText"
    INTEGER = "Integer"
    DECIMAL = "Decimal"
    BOOLEAN = "Boolean"
    DATE = "Date"
    DATETIME = "DateTime"
    SINGLE_SELECT = "SingleSelect"
    MULTI_SELECT = "MultiSelect"
    MEDIA = "Media"
    REFERENCE_MEDIA = "ReferenceMedia"
    CATALOG_REFERENCE = "CatalogReference"
    STRUCTURED_DESIGN = "StructuredDesign"


class RequirementCollectionStage(str, Enum):
    ENQUIRY = "Enquiry"
    PLANNING = "Planning"
    EXECUTION = "Execution"