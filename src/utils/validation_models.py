from pydantic import BaseModel, Field, field_validator, ValidationInfo
from datetime import datetime
from typing import Optional
import re

# Predefined lists for validation
VALID_REGIONS = ["North", "South", "East", "West"]
VALID_INTERACTION_TYPES = ["Call", "Email", "Meeting", "Follow-up"]
VALID_CATEGORIES = ["Electronics", "Outdoor", "Home", "Apparel", "Sports"]
VALID_OUTCOMES = {"Success", "Pending", "Failure"}
VALID_GENDERS = {"Male", "Female"}
VALID_CHANNELS = {"Retail", "Wholesale", "Online"}
VALID_GEO_LOCATIONS = {"Urban", "Rural", "Suburban"}

# -----------------------------------------------
# Define Pydantic Models for Validation
# -----------------------------------------------
class SalesData(BaseModel):
    order_id: int
    date: datetime
    region: str
    sales_representative: str
    customer: str
    product: str
    channel: str
    geo_location: str
    quantity: int = Field(..., ge=0)  # Non-negative validation
    sales_amount: float = Field(..., ge=0.0)  # Non-negative validation

    class Config:
        extra = 'allow'  # Ignore additional columns

    # Field Validators
    @field_validator("order_id")
    def validate_order_id(cls, value):
        if value < 0:
            raise ValueError("Order-ID must be a non-negative integer")
        return value


    @field_validator("region")
    def validate_region(cls, value):
        if value not in VALID_REGIONS:
            raise ValueError(f"Region '{value}' is invalid. Must be one of {VALID_REGIONS}")
        return value

    @field_validator("sales_representative")
    def validate_sales_rep(cls, value):
        if not value.startswith("Rep ") or not value[4:].isalpha():
            raise ValueError("Sales Representative must start with 'Rep ' followed by alphabets")
        return value

    @field_validator("customer")
    def validate_customer(cls, value):
        if not re.match(r"^Customer \d+$", value):
            raise ValueError("Customer must be in the format 'Customer X', where X is a number")
        return value

    @field_validator("product")
    def validate_product(cls, value):
        if not re.match(r"^Product [A-Z]$", value):
            raise ValueError("Product must be in the format 'Product X', where X is an uppercase letter")
        return value

    @field_validator("channel")
    def validate_channel(cls, value):
        if value not in VALID_CHANNELS:
            raise ValueError(f"Channel '{value}' is invalid. Must be one of {VALID_CHANNELS}")
        return value

    @field_validator("geo_location")
    def validate_geo_location(cls, value):
        if value not in VALID_GEO_LOCATIONS:
            raise ValueError(f"Geo Location '{value}' is invalid. Must be one of {VALID_GEO_LOCATIONS}")
        return value

    @field_validator("date")
    def validate_date(cls, value):
        if value > datetime.now():
            raise ValueError("Date cannot be in the future")
        return value


class CustomerInteraction(BaseModel):
    customer_id: str
    interaction_type: str
    date: datetime
    sales_representative: str
    outcome: str
    agent_age: int
    gender: str

    class Config:
        extra = 'allow'  # Ignore additional columns

    # Validations
    @field_validator("customer_id")
    def validate_customer_id(cls, value):
        if not re.match(r"^Customer \d+$", value):
            raise ValueError("Customer ID must be in the format 'Customer X' where X is a number")
        return value

    @field_validator("interaction_type")
    def valid_interaction_type(cls, value):
        if value not in VALID_INTERACTION_TYPES:
            raise ValueError(f"Interaction Type must be one of {VALID_INTERACTION_TYPES}")
        return value

    @field_validator("date")
    def validate_date(cls, value):
        if value > datetime.now():
            raise ValueError("Date cannot be in the future")
        return value

    @field_validator("sales_representative")
    def validate_sales_representative(cls, value):
        if not value.startswith("Rep ") or not value[4:].isalpha():
            raise ValueError("Sales Representative must start with 'Rep ' followed by letters")
        return value

    @field_validator("outcome")
    def validate_outcome(cls, value):
        if value not in VALID_OUTCOMES:
            raise ValueError(f"Outcome must be one of {VALID_OUTCOMES}")
        return value

    @field_validator("agent_age")
    def validate_agent_age(cls, value):
        if not (18 <= value <= 65):
            raise ValueError("Agent Age must be between 18 and 65")
        return value

    @field_validator("gender")
    def validate_gender(cls, value):
        if value not in VALID_GENDERS:
            raise ValueError(f"Gender must be one of {VALID_GENDERS}")
        return value


class ProductInventory(BaseModel):
    product_id: str
    product_name: str
    category: str
    stock_level: int = Field(..., ge=0)
    stock_turnover_rate:  float = Field(..., ge=0.0)  # Non-negative
    supplier: str
    reorder_level: Optional[int]

    @field_validator("category")
    def validate_category(cls, value):
        if value not in VALID_CATEGORIES:
            raise ValueError(f"Category '{value}' is invalid. Must be one of {VALID_CATEGORIES}")
        return value


    @field_validator("reorder_level")
    def validate_reorder_level(cls, value, info: ValidationInfo):
        stock_level = info.data.get("stock_level")
        if stock_level and value is not None and value > stock_level:
            raise ValueError("Reorder Threshold cannot be greater than Stock Level")
        return value


class MarketingCampaign(BaseModel):
    campaign_id: str
    start_date: datetime
    end_date: datetime
    channel: str
    total_reach: int = Field(..., ge=0)  # Non-negative total reach
    total_conversions: int = Field(..., ge=0)  # Non-negative total conversions
    conversion_rate_percent: float = Field(..., ge=0.0)  # Non-negative
    revenue_generated: float = Field(..., ge=0.0)  # Non-negative revenue
    
    class Config:
        extra = 'allow'  # Ignore unrecognized fields

    # Validators
    @field_validator("campaign_id")
    def validate_campaign_id(cls, value):
        if not re.match(r"^CAMP\d+$", value):
            raise ValueError("Campaign ID must be in the format 'CAMP<digits>' (e.g., CAMP123)")
        return value

    @field_validator("start_date")
    def validate_start_date(cls, value):
        if value > datetime.now():
            raise ValueError("Start Date cannot be in the future")
        return value

    @field_validator("end_date")
    def validate_end_date(cls, value, info: ValidationInfo):
        start_date = info.data.get("start_date")
        if start_date and value <= start_date:
            raise ValueError("End Date must be strictly after Start Date")
        return value

    @field_validator("channel")
    def validate_channel(cls, value):
        if value not in VALID_CHANNELS:
            raise ValueError(f"Channel '{value}' is invalid. Must be one of {VALID_CHANNELS}")
        return value

    @field_validator("total_reach")
    def validate_total_reach(cls, value):
        if value < 0:
            raise ValueError("Total Reach must be a non-negative integer")
        return value

    @field_validator("total_conversions")
    def validate_total_conversions(cls, value):
        if value < 0:
            raise ValueError("Total Conversions must be a non-negative integer")
        return value

    @field_validator("revenue_generated")
    def validate_revenue_generated(cls, value):
        if value < 0:
            raise ValueError("Revenue Generated must be a non-negative float")
        return value



class RegionalSalesTarget(BaseModel):
    region: str
    quarter_1_target: float = Field(..., ge=0.0)
    quarter_2_target: float = Field(..., ge=0.0)
    quarter_3_target: float = Field(..., ge=0.0)
    quarter_4_target: float = Field(..., ge=0.0)
    yearly_target: float = Field(..., ge=0.0)
    
    class Config:
        extra = 'allow'  # Ignore unrecognized fields

    # Validators
    @field_validator("region")
    def validate_region(cls, value):
        if value not in VALID_REGIONS:
            raise ValueError(f"Region '{value}' is invalid. Must be one of {VALID_REGIONS}")
        return value

    @field_validator("yearly_target")
    def validate_yearly_target(cls, value, info: ValidationInfo):
        data = info.data
        if "quarter_1_target" in data and "quarter_2_target" in data and \
           "quarter_3_target" in data and "quarter_4_target" in data:
            expected_total = (
                data["quarter_1_target"] +
                data["quarter_2_target"] +
                data["quarter_3_target"] +
                data["quarter_4_target"]
            )
            if value != expected_total:
                raise ValueError(f"Yearly Target {value} does not match the sum of quarterly targets {expected_total}")
        return value

def get_pydantic_model_for_table(table_name):
    """
    Return the appropriate Pydantic model for a given table name.
    """
    if table_name == "sales_data":
        return SalesData
    elif table_name == "customer_interactions":
        return CustomerInteraction
    elif table_name == "product_inventory":
        return ProductInventory
    elif table_name == "marketing_campaigns":
        return MarketingCampaign
    elif table_name == "regional_sales_targets":
        return RegionalSalesTarget
    else:
        raise ValueError(f"No Pydantic model defined for table: {table_name}")