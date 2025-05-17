TABLE_SPECS = {
    "forms": {
        "columns": [
        "id_uuid",
        "form_name",
        "url",
        "status",
        "created_at",
        "updated_at",
        "service_id"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {        
            "service_id": "service(id_uuid)"
        },
        "notes": "Represents a specific form, referencing a service if needed."
    },
  
    "form_steps": {
        "columns": [
            "id_uuid",         # PK (unique row ID)
            "forms_id",        # Links to forms(id_uuid)
            "step_order",      # Step number (like step_number in JSON)
            "action_type",     # e.g. 'click', 'manual', 'select_date'
            "selector_value",  # XPATH or CSS that identifies the element
            "selector_type",   # e.g. 'xpath' or 'css'
            "element_type",    # (e.g. input, select, textarea, button)
            "selector_title",  # (You’re using this for text_content from JSON)
            "form_fields_id",  # Optional link to form_fields table
            "insert_value",    # The text/variable Selenium might type (was 'value' in JSON)
            "description",     # A user note for the step
            "created_at",      # Timestamp of row creation
            "updated_at",       # Timestamp of last update
            "element_attributes",
            "client_value"
            "condition"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {
            "forms_id": "forms(id_uuid)",
            "form_fields_id": "form_fields(id_uuid)"
        },
        "notes": "Holds each step for a form. References the form and optionally a form_field."
    },
  
    "form_fields": {
        "columns": [
            "id_uuid",
            "field_name",
            "css_selector",
            "field_type",
            "notes",
            "created_at",
            "updated_at"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {},
        "notes": "Defines reusable field definitions (selector, type, etc.) for form steps."
    },


    # // CRM DATA BASE //
    "service": {
        "columns": [
          "id_uuid",
          "visa_validity",
          "visa_stay_duration",
          "visa_entry_type",
          "note",
          "url",
          "password_login",
          "user_name",
          "service_name",
          "t_creation",
          "gov_fee",
          "aid_air_fee",
          "gov_fee_currency_id",
          "aid_air_fee_currency_id",
          "country_id"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {
          "gov_fee_currency_id": "currency(id_uuid)",
          "aid_air_fee_currency_id": "currency(id_uuid)",
          "country_id": "country(id_uuid)"
        },
        "notes": "Defines a service (e.g., visa). References currency for fees and a country."
    },
    
    "country": {
        "columns": [
            "id_uuid",
            "t_creation",
            "name",
            "continent",
            "name_hebrew",
            "phone_code"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {},
        "notes": "Stores country-level information (phone code, continent, Hebrew name, etc.)."
    }, 

    "address": {
        "columns": [
            "id_uuid",
            "country_id",
            "city_id",
            "street_id",
            "postal_code",
            "client_id",
            "t_creation",
            "number"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {
            "country_id": "country(id_uuid)",
            "city_id": "city(id_uuid)",
            "street_id": "street(id_uuid)",
            "client_id": "client(id_uuid)"
        },
        "notes": "Stores address info. Links to country, city, street, and client."
    },

    "city": {
        "columns": [
            "id_uuid",
            "country_id",
            "name",
            "name_hebrew",
            "t_creation"
        ],
            "primary_key": "id_uuid",
            "foreign_keys": {
            "country_id": "country(id_uuid)"
        },
        "notes": "Stores city info, linking to country."
    },


    "contact": {
        "columns": [
            "id_uuid",
            "client_id",
            "email",
            "family_id",
            "phone",
            "t_creation",
            "internal_email",
            "country_id",
            "contact_type"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {
            "client_id": "client(id_uuid)",
            "family_id": "family(id_uuid)",
            "country_id": "country(id_uuid)"
        },
        "notes": "Stores contact details for a client or family, references country for phone codes, etc."
    },

    "country": {
        "columns": [
            "id_uuid",
            "t_creation",
            "name",
            "continent",
            "name_hebrew",
            "phone_code"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {},
        "notes": "Stores country-level information (phone codes, continent)."
    },

    "ids": {
        "columns": [
            "id_uuid",
            "client_id",
            "t_creation",
            "file_path",
            "date_issue",
            "date_valid_until",
            "document_type",
            "city_id",
            "document_number",
            "country_id",
            "file_name",
            "expired"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {
            "client_id": "client(id_uuid)",
            "city_id": "city(id_uuid)",
            "country_id": "country(id_uuid)"
        },
        "notes": "Stores ID documents (passport, license, etc.) with references to client, city, and country."
    },

    "street": {
        "columns": [
            "id_uuid",
            "city_id",
            "name",
            "name_hebrew"
        ],
        "primary_key": "id_uuid",
        "foreign_keys": {
            "city_id": "city(id_uuid)"
        },
        "notes": "Stores street information, referencing the city."
    },
  };
  