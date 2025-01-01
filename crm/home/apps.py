from django.apps import AppConfig
import os

class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SENDINBLUE_API_KEY = os.environ.get("SENDINBLUE_API_KEY")

    
    @classmethod
    def is_local(cls):
        return cls.ENVIRONMENT == "local"

    @classmethod
    def is_staging(cls):
        return cls.ENVIRONMENT == "testing"

    @classmethod
    def is_production(cls):
        return cls.ENVIRONMENT == "production"
