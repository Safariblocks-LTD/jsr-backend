from algosdk import constants as algosdk_constants
from django.conf import settings
from enum import Enum


class Constant:

    class NewsTopic(Enum):
        ConsumerElectronics = "Consumer Electronics Industry"
        CapitalGoods = "Capital Goods Smart-Tv Laptop Smart-Watch"
        SmartDevices = "Smart Devices"
        SmartPhone = "Smart Phone"
        BrandDevices = "New Brand Devices"
        ElectronicProduct = "Trending Smart Product"

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)
        

    django_default_codes = {
        "required": 506,
        "blank": 506,
        "null": 506,
        "empty": 506,
    }
    

    response_messages = {
        500: "Server error!",
        501: "Requested api endpoint is not valid!",
        502: "Given data is not a valid JSON format!",
        503: "Requested Content-Type should be 'application/json'!",
        504: "Requested method not allowed!",
        505: "Invalid parameter passed!",
        506: "Required parameter or value missing!",
        507: "Authentication failed, invalid algorand key",
        508: "Given net is not valid",
        509: "Authentication failed, missing algorand key!",
        510: "Sorry, you are not allowed to perform this action!",
        511: "Given mnemonic is not valid",
        512: "Sorry, service is unavailable",
        513: "Authentication failed, User access token expired or invalid",
        514: "Authentication failed, missing JWT Token.",

        100: "Given address is not a valid Algorand address.",
        101: "Your transaction was successfully received by the Algorand network.",
        102: "Transaction amount cannot be negative.",
        103: "Transaction amount should be at least 1 microAlgos",
        104: '''f"You have to maintain minimum {args['min_amount']} AlGO in your account."''',
        105: "Account details found.",
        
        106: "Transactions history found.",
        107: "Given timestamp, 'to' or 'for' is not valid for transaction history.",
        108: "Assets found.",
        109: "No any assets found.",
        110: "No any transactions found.",
        111: "This transaction can not be proceed, please try again.",
        
        112: "Your account registered successfully.",
        113: "Your FCM token is not valid or expired.",
        114: "Successfully logged-out",
        115: "Successfully reset",
        116: "Your offline transaction request received.",
        117: "Sorry we did not found your account!",
        118: "This mobile number is already registered with your account!",
        119: "Your OTP verification limit exceeded, please try after some time.",
        120: "Your mobile number successfully registered!",
        121: "Your mobile number already registered with another account, would you like to add with this account?",
        122: "Sorry, your otp is expired!",
        123: "Sorry, your otp is invalid!",
        124: "Please first request otp for this number!",
        125: "An OTP sent on your requested mobile number please check it.",
        126: "Resend OTP timeout, please try after some time.",
        
        127: "Given mobile number is not valid!",
        128: "Requested Asset does not exist or has been deleted",
        129: "You have already own this asset.",
        130: "You do not have own this asset.",
        131: "To remove this Asset balance must be 0. Please transfer the balance to another account and try again.",
        132: "Transactions failed, insufficient amount for the asset transaction",
        133: '''f"Receiver {args['address']} must optin, asset {args['index']}."''',
        134: '''f"Transaction failed, {args['error']}"''',
        
        135: "Notifications found",
        136: "No any notifications found",
        137: "Notifications status",
        
        138: "Analytics data",
        
        139: "News received successfully.",

        140: "Titles received Successfully.",

        141: "Trending tokenizable products received successfully.",

        142: "Brand not supported yet.",
        143: "A device has already been verified for the given title id.",
        144: "Title verified successfully.",
        145: "Device type not matched.",
        146: "Please scan QR Code.",
        147: "No device found.",
        148: "Verified titles received successfully.",
        149: "Title details received successfully.",
        150: "Maintenance premium calculated successfully.",
        151: "No maintenance record found for given id.",
        152: "Maintenance record updated successfully.",
        153: "This title is already under maintenance.",
        154: "Index token updated successfully.",
        155: "Secured assets received successfully.",
        156: "Title exists.",
        157: "Title does not exist.",
        158: "Asset is not under maintenance.",
        159: "No maintenance record found for the given title id.",
        160: "Maintenance claim is filed. Please wait for its approval.",
        161: "Claim Status Updated Successfully.",
        162: "This title is not eligible for maintenance rewards.",
        163: "Mail for maintenance rewards sent to the user successfully.",
        164: "Claim status updated successfully.",
        165: "Top Tokenized Assets received successfully.",
        166: "The News cache has been deleted",
        167: "Feedback submitted successfully.",
        168: "Invalid format for feedback",
        169: "Locations data are being retrieved successfully",
        170: "No Locations found",
        171: "The email passcode has been verified successfully",
        172: "The email passcode verification failed",
        173: "Title does not exist on dynamodb!",
        174: "Title already verified!",

        175: "Protocol transaction submitted successfully.",
        176: "Protocol transaction submission failed !",
        177: "Protocol transactions are being retrieved successfully",
        178: "Maintenance price calculated successfully",
        179: "Successfully convert USDC to another currency",

        180: "Wallet created successfully.",
        181: "Mobile number is not verified.",
        182: "OTP is sent but mobile number is attached to another device.",

        183: "Account already linked to wallet.",

        184: "Your OTP verification limit exceeded, please request for new one.",

        185: "Reward list found.",
        186: "Can't claim reward, task not completed.",
        187: "Reward claimed successfully.",
        188: "Reward already claimed.",
        189: "Task doesn't exists.",

        190: "Can't set primary account, first import the account.",
        191: "Account is already set to primary.",

        192: "Address found for contacts.",

        193: "Subtask doesn't exists.",
        194: "Successfully marked task completed.",
        195: "Task removed from screen.",

        196: "Receive request submitted successfully.",
        197: "Receive transaction doesn't exists.",
        198: "Receive transaction details updated successfully.",
        199: "Can't update resolved transactions.",
        200: "Transaction history created successfully.",

        201: "Contact found.",
        202: "Contact not found.",

        203: "My titles found.",
        204: "My titles not found.",

        205: "Set a primary account.",

        206: "Address and shared key are different"
    }

    MAINNET_CODE = 1
    BETANET_CODE = 2
    TESTNET_CODE = 3
    
    ALGO_EXPLORER_MAINNET_BASE_URL = "https://mainnet-idx.algonode.cloud/v2"
    ALGO_EXPLORER_TESTNET_BASE_URL = "https://testnet-idx.algonode.cloud/v2"
    ALGO_EXPLORER_ALGO_2_USD_URL = "https://price.algoexplorerapi.io/price/algo-usd"
    
    HEADER_KEYS = "Content-Type User-Agent Host Sec-Ch-Ua Sec-Ch-Ua-Platform Origin"
    
    TXN_CHOICES = [
        ("pay", "Algo Transaction"),
        ("axfer", "Asset Transfer Transaction")
    ]
    
    ASSET_OPTIN_CLOSEOUT_CHOICES = [
        ("optin_axfer", "Asset OptIn Transaction"),
        ("closeout_axfer", "Asset CloseOut Transaction"),
    ]
    
    NET_TYPES = [
        (MAINNET_CODE, "MAIN"),
        (BETANET_CODE, "BETA"),
        (TESTNET_CODE, "TEST"),
    ]
    
    MIN_TXN_FEE = algosdk_constants.MIN_TXN_FEE  # microAlgos
    OFFLINE_TXN_EXPIRE_TIME = 10  # Minutes
    OTP_EXPIRE_TIME = 5  # Minutes
    OTP_RESEND_TIMEOUT = 1  # Minutes
    OTP_MAX_ATTEMPTS = 3  # Attempts count
    OTP_MAX_ATTEMPTS_TIMEOUT = 8*60  # Hours
    
    twilio_messages = {
        100: '''f"Your OTP is: {kwargs.get('otp')}"''',
    }

    push_notifications = {
        100: "Jasiri Algo Wallet",
        101: '''f"Your transaction of {data['amount']} {data['asset_name']} from {Helper.get_address_in_short(data['sender'])} to {Helper.get_address_in_short(data['receiver'])} is complete."''',
        102: '''f"{data['amount']} {data['asset_name']} were sent to {Helper.get_address_in_short(data['receiver'])} by {Helper.get_address_in_short(data['sender'])}."''',
        103: '''f"Your transaction to add asset {data['asset_name']} is complete."''',
        104: '''f"Your transaction to remove asset {data['asset_name']} is complete."''',
    }
    
    TWILIO_DEFAULT_OTP = "123456"
    
    ANALYTICS_EXPIRE_TIME = 60*60*3
    ANALYTICS_BASE_VALUE_INDEX_NAME = "assetValue"
    ANALYTICS_TOTAL_CAPITAL_UNLOCK_RATIO = .7
    
    OFFLINE_TXN_RECEIVER = {
        "+1": settings.TWILIO_NUMBER,
        "+254": settings.AFRICAS_TALKING_NUMBER,
    }
    
    ASSETS_ID_SAME_VALUE_AS_USD = [118346460] # jsrUNLOCK

    userAgents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/107.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/108.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/106.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/105.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/104.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/103.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/102.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/107.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/108.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/106.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/105.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/104.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/103.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/102.0",
    ]

    choices = {
        "VerificationStatus": [
            (0, "Pending"),
            (1, "Verified"),
        ],
        "AssetCategory":[
            (0, "Smartphone"),
            (1, "Laptop"),
            (2, "Tablet"),
            (3, "SmartTV"),
            (4, "Smartwatch"),
        ],
        "PaymentStatus":[
            (0, "Pending"),
            (1, "Approved")
        ],
        "DamageType":[
            (0, "No Damage"),
            (1, "Water Damage"),
            (2, "Screen Damage"),
            (3, "Physical Damage")
        ],
        "ClaimStatus":[
            (0, "Not Claimed"),
            (1, "Rejected"),
            (2, "Approved"),
            (3, "In Progress"),
            (4, "Pre-Approved")
        ],
        "MaintenanceRewardStatus":[
            (0, "Not Claimed"),
            (1, "Claim In Progress"),
            (2, "Approved"),
            (3, "Rejected"),
            (4, "Pre-Approved")
        ]
    }   

    deviceCategories = {
        "smartphone":0,
        "laptop": 1,
        "tablet": 2,
        "smarttv": 3,
        "smartwatch": 4,
    }

    COINGEKO_COIN_ID = {
        "algo": "algorand",
        "usdc": "usd-coin",
        "usdt": "tether"
    }

    TESTNET_VERIFIED_ASSET_ID_LIST = [0, 487086338, 10458941, 180447]
    MAINNET_VERIFIED_ASSET_ID_LIST = [0, 881424020, 31566704, 312769]
