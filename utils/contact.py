from apps.account.models import Device, Account
import phonenumbers


class Contact:

    @classmethod
    def get_contacts_with_address(cls, contacts):
        contact_list = []
        for contact in contacts:
            mobile = contact["number"].replace(" ", "")
            if mobile.startswith("+"):
                country_code, mobile = cls.seprate_country_code(mobile)
            contact_list.append(mobile)

        devices = Device.objects.prefetch_related("account_device").filter(
            mobile__in=contact_list, is_wallet=True, is_deleted=False
        )

        for contact in contacts:
            mobile = contact["number"].replace(" ", "")
            country_code, mobile = cls.seprate_country_code(mobile)
            contact["address"] = None
            for device in devices:
                if device.mobile == str(mobile):
                    if account := device.account_device.filter(is_primary=True).first():
                        contact["address"] = getattr(account, "address")

        return contacts

    @classmethod
    def seprate_country_code(cls, contact):
        try:
            contact = phonenumbers.parse(contact)
            return contact.country_code, contact.national_number
        except Exception:
            return None, contact

    @classmethod
    def get_contacts_from_address(cls, address):
        accounts = Account.objects.select_related("device").filter(
            address=address, is_imported=True, is_deleted=False, device__is_deleted=False
        )
        contacts = [
            {"mobile": account.device.mobile, "country_code": account.device.country_code} for account in accounts
        ]
        return contacts
