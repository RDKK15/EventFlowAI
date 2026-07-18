from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.enums.requirement import (
    RequirementCollectionStage,
    RequirementValueType,
)


class RequirementOptionCreate(BaseModel):
    value: str = Field(min_length=1)
    label: str = Field(min_length=1)
    display_order: int = 0


class RequirementOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    requirement_definition_id: int
    value: str
    label: str
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class RequirementDefinitionCreate(BaseModel):
    key: str = Field(min_length=1)
    label: str = Field(min_length=1)
    description: str | None = None
    value_type: RequirementValueType
    unit: str | None = None
    is_required: bool = False
    ask_customer: bool = True
    collection_stage: RequirementCollectionStage = (
        RequirementCollectionStage.ENQUIRY
    )
    display_order: int = 0
    ai_hint: str | None = None
    options: list[RequirementOptionCreate] = Field(
        default_factory=list,
    )


class RequirementDefinitionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    service_type_id: int
    key: str
    label: str
    description: str | None
    value_type: RequirementValueType
    unit: str | None
    is_required: bool
    ask_customer: bool
    collection_stage: RequirementCollectionStage
    display_order: int
    ai_hint: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    options: list[RequirementOptionResponse]



class ServiceTypeCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Service type name cannot be empty.")
        return v


class ServiceTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if not v:
            raise ValueError("Service type name cannot be empty.")
        return v


class ServiceTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    business_id: int
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    requirement_definitions: list[
        RequirementDefinitionResponse
    ]