from algosdk.v2client import algod
from .algorand import Algorand
from algosdk.atomic_transaction_composer import (
    AccountTransactionSigner,
    AtomicTransactionComposer
    )
from algosdk import abi
from django.conf import settings
from algosdk import abi, transaction
from utils.helpers import Helper




class SmartContract:

    console_contract = abi.Contract.from_json(settings.CONSOLE_SMART_JSON)
    tokenization_contract = abi.Contract.from_json(settings.TOKENIZATION_SMART_JSON)
    title_contract = abi.Contract.from_json(settings.TITLE_SMART_JSON)

    console_app_id = settings.CONSOLE_SMART_APP_ID
    tokenization_app_id = settings.TOKENIZATION_SMART_APP_ID
    title_app_id = settings.TITLE_SMART_APP_ID

    client = Algorand.get_algod_client()

    @classmethod
    def __admin_transaction_signer(cls):
        return AccountTransactionSigner(settings.ADMIN_KEY)

    @classmethod
    def act(cls):
        return AtomicTransactionComposer()
    
    @classmethod
    def suggestparams(cls):
        return cls.client.suggested_params()


    @classmethod
    def console_add_method(cls, method_name, title_id):
        act = cls.act()
        act.add_method_call(
        app_id=int(cls.console_app_id),
        method=cls.console_contract.get_method_by_name(method_name),
        sender=settings.ADMIN_ADDRESS,
        sp=cls.suggestparams(),
        signer=cls.__admin_transaction_signer(),
        method_args=[int(title_id)],
        boxes = [[int(cls.console_app_id), int(title_id)]]
        )
        return act
    
    @classmethod
    def console_add_method_reward(cls, method_name, title_id=None):
        act = cls.act()
        act.add_method_call(
        app_id=int(cls.console_app_id),
        method=cls.console_contract.get_method_by_name(method_name),
        sender=settings.ADMIN_ADDRESS,
        sp=cls.suggestparams(),
        signer=cls.__admin_transaction_signer(),
        method_args=[int(title_id), 1000],
        boxes = [[int(cls.console_app_id), int(title_id)]]
        )
        return act
    
    @classmethod
    def console_add_method_read_only(cls, method_name):
        act = cls.act()
        act.add_method_call(
        app_id=int(cls.console_app_id),
        method=cls.console_contract.get_method_by_name(method_name),
        sender=settings.ADMIN_ADDRESS,
        sp=cls.suggestparams(),
        signer=cls.__admin_transaction_signer(),
        )
        return act
    
    @classmethod
    def console_add_method_asset_read(cls, method_name, usdc_id):
        act = cls.act()
        act.add_method_call(
        app_id=int(cls.console_app_id),
        method=cls.console_contract.get_method_by_name(method_name),
        sender=settings.ADMIN_ADDRESS,
        sp=cls.suggestparams(),
        signer=cls.__admin_transaction_signer(),
        method_args = [usdc_id]
        )
        return act
    

    @classmethod 
    def console_add_method_payment(cls, method_name, pay):
        act = cls.act()
        act.add_method_call(
        app_id=int(cls.console_app_id),
        method=cls.console_contract.get_method_by_name(method_name),
        sender=settings.ADMIN_ADDRESS,
        sp=cls.suggestparams(),
        signer=cls.__admin_transaction_signer(),
        method_args=[pay],
        )
        return act
    

    @classmethod 
    def console_add_method_withdraw(cls, method_name, usdc_id, amount):
        act = cls.act()
        act.add_method_call(
        app_id=int(cls.console_app_id),
        method=cls.console_contract.get_method_by_name(method_name),
        sender=settings.ADMIN_ADDRESS,
        sp=cls.suggestparams(),
        signer=cls.__admin_transaction_signer(),
        method_args=[usdc_id, amount],
        )
        return act

    
    @classmethod
    def tokenization_add_method_asset(cls, method_name, asset_id):
        act = cls.act()
        act.add_method_call(
        app_id=int(cls.tokenization_app_id),
        method=cls.tokenization_contract.get_method_by_name(method_name),
        sender=settings.ADMIN_ADDRESS,
        sp=cls.suggestparams(),
        signer=cls.__admin_transaction_signer(),
        method_args=[asset_id],
        )
        return act
    
    @classmethod
    def title_add_method_asset(cls, method_name, asset_id):
        act = cls.act()
        act.add_method_call(
        app_id=int(cls.title_app_id),
        method=cls.title_contract.get_method_by_name(method_name),
        sender=settings.ADMIN_ADDRESS,
        sp=cls.suggestparams(),
        signer=cls.__admin_transaction_signer(),
        method_args=[asset_id],
        )
        return act
    
    @classmethod
    def title_withdraw_add_method(cls, method_name, amount, usdc_id):
        act = cls.act()
        act.add_method_call(
        app_id=int(cls.title_app_id),
        method=cls.title_contract.get_method_by_name(method_name),
        sender=settings.ADMIN_ADDRESS,
        sp=cls.suggestparams(),
        signer=cls.__admin_transaction_signer(),
        method_args=[usdc_id, amount, 1000],
        )
        return act
    


    @classmethod
    def console_check_maintenance(cls, title_id):
        act = cls.console_add_method("read_box_status", title_id)
        return act.execute(cls.client, 4)

    @classmethod
    def console_approve_maintenance_claim(cls, title_id):
        act = cls.console_add_method("approve_claim", title_id)
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.tx_id
    

    @classmethod
    def console_approve_unlock_reward(cls, title_id):
        act = cls.console_add_method("approve_maintain_reward",title_id)
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.tx_id

    @classmethod
    def get_console_balance_smart_contract(cls,addr):
        account_info = cls.client.account_info(address=addr)
        return account_info.get("amount")
        
    @classmethod
    def get_console_usdc_balance(cls, usdc_id):
        act = cls.console_add_method_asset_read("get_usdc_balance", usdc_id)
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.return_value


    @classmethod
    def get_console_usdc_pool(cls):
        act = cls.console_add_method_read_only("get_maintain_pool_total")
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.return_value
        

    @classmethod
    def console_withdraw_fund_usdc(cls, amount, usdc_id):
        act = cls.console_add_method_withdraw("withdraw_fund", usdc_id, amount)
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.tx_id


    @classmethod
    def get_tokenization_algo_balance(cls,addr):
        account_info = cls.client.account_info(address=addr)
        return account_info.get("amount")
        

    @classmethod
    def get_tokenization_unlock_balance(cls, unlock_id):
        act = cls.tokenization_add_method_asset("get_unlock_balance", unlock_id)
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.return_value


    @classmethod
    def title_algo_balance(cls, addr):
        account_info = cls.client.account_info(address=addr)
        return account_info.get("amount")


    @classmethod
    def get_title_usdc_balance(cls, usdc_id):
        act = cls.title_add_method_asset("get_usdc_balance", usdc_id)
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.return_value
        

    @classmethod
    def titles_usdc_withdraw(cls, amount, usdc_id):
        act = cls.title_withdraw_add_method("withdraw_usdc", amount, usdc_id)
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.tx_id

    @classmethod
    def contract_fund(cls, contract_addr, amount):
        unsigned_txn = transaction.PaymentTxn(
            sender=settings.ADMIN_ADDRESS,
            receiver=contract_addr,
            sp=cls.suggestparams(),
            amt=amount,
            note=b"fund",) 
        signed_txn = unsigned_txn.sign(settings.ADMIN_KEY)
        txid = cls.client.send_transaction(signed_txn)
        return txid
        

    @classmethod
    def get_app_algo_balance(cls, app_name, addr):
        if app_name.lower() == "tokenization":
            return cls.get_tokenization_algo_balance(addr)
        elif app_name.lower() == "console":
            return cls.get_console_balance_smart_contract(addr)
        elif app_name.lower() == "title":
            return cls.title_algo_balance(addr)
        

    @classmethod
    def get_app_unlock_balance(cls, app_name, unlock_id):
        if app_name.lower() == "tokenization":
            return cls.get_tokenization_unlock_balance(unlock_id)
        elif app_name.lower() == "console":
            return 0
        elif app_name.lower() == "title":
            return 0
        

    @classmethod
    def get_app_usdc_balance(cls, app_name, usdc_id):
        if app_name.lower() == "tokenization":
            return 0
        elif app_name.lower() == "console":
            return cls.get_console_usdc_balance(usdc_id)
        elif app_name.lower() == "title":
            return cls.get_title_usdc_balance(usdc_id)
        

    @classmethod
    def withdraw_fund_usdc(cls, app_name, amount, usdc_id):
        if app_name.lower() == "tokenization":
            return 0
        elif app_name.lower() == "console":
            return cls.console_withdraw_fund_usdc(amount, usdc_id)
        elif app_name.lower() == "title":
            return cls.titles_usdc_withdraw(amount, usdc_id)
    

    @classmethod
    def get_maintain_pool_total(cls):
        act = cls.console_add_method_read_only("get_maintain_pool_total")
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.return_value
        
    
    @classmethod
    def get_titles_claimed_total(cls):
        act = cls.console_add_method_read_only("get_titles_claimed_total")
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.return_value
        

    @classmethod
    def get_total_active_maintained(cls):
        act = cls.console_add_method_read_only("get_total_active_maintained")
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.return_value


    @classmethod
    def get_maintained_title_total(cls):
        act = cls.console_add_method_read_only("get_maintained_title_total")
        result = act.execute(cls.client, 4)
        for res in result.abi_results:
            return res.return_value
        

    @classmethod
    def console_data(cls):
        maintenance_pool_total = cls.get_maintain_pool_total()
        total_claimed= cls.get_titles_claimed_total()
        titles_in_maintain_total= cls.get_total_active_maintained()
        titles_maintained_total= cls.get_maintained_title_total()
        data = {
            "maintenance_pool_total":Helper.round_asset_count_to_decimal(maintenance_pool_total),
            "total_claimed": total_claimed,
            "titles_in_maintain_total":titles_in_maintain_total,
            "titles_maintained_total": titles_maintained_total
        }
        return data