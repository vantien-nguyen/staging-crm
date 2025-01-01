from typing import Dict

from django.apps import apps

from home.extensions.sendinblue.mailing import Mailing

m = Mailing("https://api.sendinblue.com/v3", apps.get_app_config("home").SENDINBLUE_API_KEY)


def send_email(data: Dict):
    return m.send_email(data)
