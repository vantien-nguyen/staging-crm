import json
import logging

from django.core.management.base import BaseCommand

from home.models import *
from users.models import User

logger = logging.getLogger(__file__)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        data = json.load(open("crm/home/management/data/data.json"))

        for user_data in data["users"]:
            user, _ = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "is_active": user_data["is_active"],
                    "role": user_data["role"],
                },
            )
            user.set_password(user_data["password"])
            user.save()
            print(f"Creating user...: {user.email}")

        for client_data in data["clients"]:
            client, _ = Client.objects.get_or_create(
                name=client_data["name"],
                siren=client_data["siren"],
                defaults={
                    "description": client_data["description"],
                    "turnover": client_data["turnover"],
                    "cash": client_data["cash"],
                    "website": client_data["website"],
                    "typology": client_data["typology"],
                    "status": client_data["status"],
                    "needs": client_data["needs"],
                    "existing_partners": client_data["existing_partners"],
                },
            )
            print(f"Creating client...: {client.name}")

        for partner_data in data["partners"]:
            partner, _ = Partner.objects.get_or_create(
                name=partner_data["name"],
                siren=partner_data["siren"],
                defaults={
                    "description": partner_data["description"],
                    "turnover": partner_data["turnover"],
                    "cash": partner_data["cash"],
                    "website": partner_data["website"],
                    "typology": partner_data["typology"],
                    "iban": partner_data["iban"],
                    "bic": partner_data["bic"],
                },
            )
            print(f"Creating partner...: {partner.name}")

        for contact_data in data["contacts"]:
            contact, _ = Contact.objects.get_or_create(
                email=contact_data["email"],
                defaults={
                    "first_name": contact_data["first_name"],
                    "last_name": contact_data["last_name"],
                    "phone_number": contact_data["phone_number"],
                    "linkedin": contact_data["linkedin"],
                    "job_description": contact_data["job_description"],
                    "account": Account.objects.get(siren=contact_data["account_siren"]),
                    # "file": contact_data["file"],
                },
            )
            print(f"Creating contact...: {contact.email}")

        for interaction_data in data["interactions"]:
            interaction, _ = Interaction.objects.get_or_create(
                date_time=interaction_data["date_time"],
                status=interaction_data["status"],
                type=interaction_data["type"],
                comment=interaction_data["comment"],
                user=User.objects.get(email=interaction_data["user_email"]),
                contact=Contact.objects.get(email=interaction_data["contact_email"]),
            )
            print(f"Creating interaction...: {interaction.id}")

        for kyc_data in data["kycs"]:
            kyc, _ = Kyc.objects.get_or_create(
                name=kyc_data["name"],
                status=kyc_data["status"],
                notes=kyc_data["notes"],
                der=kyc_data["der"],
                qcf=kyc_data["qcf"],
                assignee=User.objects.get(email=kyc_data["assignee_email"]),
            )
            print(f"Creating kyc...: {kyc.name}")

        for product_data in data["products"]:
            product, _ = Product.objects.get_or_create(
                name=product_data["name"],
                description=product_data["description"],
                typology=product_data["typology"],
                partner=Partner.objects.get(siren=product_data["partner_siren"]),
            )
            print(f"Creating product...: {product.name}")

        for opportunity_data in data["opportunities"]:
            opportunity, _ = Opportunity.objects.get_or_create(
                nominal=opportunity_data["nominal"],
                margin=opportunity_data["margin"],
                status=opportunity_data["status"],
                transfer_type=opportunity_data["transfer_type"],
                frequency=opportunity_data["frequency"],
                amount=opportunity_data["amount"],
                sous_jacent=opportunity_data["sous_jacent"],
                coupon_payments=opportunity_data["coupon_payments"],
                rates=opportunity_data["rates"],
                traab=opportunity_data["traab"],
                capital_protection=opportunity_data["capital_protection"],
                coupon_protection=opportunity_data["coupon_protection"],
                start_date=opportunity_data["start_date"],
                end_date=opportunity_data["end_date"],
                created_date=opportunity_data["created_date"],
                contact=Contact.objects.get(email=opportunity_data["contact_email"]),
                product=Product.objects.get(name=opportunity_data["product_name"]),
                user=User.objects.get(email=opportunity_data["user_email"]),
            )
            print(f"Creating opportunity...: {opportunity.id}")

        for billing_data in data["billings"]:
            billing, _ = Billing.objects.get_or_create(
                reason=billing_data["reason"],
                amount=billing_data["amount"],
                billing_date=billing_data["billing_date"],
                opportunity=Opportunity.objects.get(pk=billing_data["opportunity_id"]),
                partner=Partner.objects.get(siren=billing_data["partner_siren"]),
            )
            print(f"Creating billing...: {billing.id}")
