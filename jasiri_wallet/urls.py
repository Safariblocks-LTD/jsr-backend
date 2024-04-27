from django.urls import (
    path, 
    include,
    re_path, 
)
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^v1/(?P<net_type>(?:testnet|mainnet))/", include([  
        path('adminpanel',include("apps.adminpanel.urls")),
        path("accounts", include("apps.account.urls")),
        path("transactions", include("apps.transaction.urls")),
        path("assets", include("apps.asset.urls")),
        path("notifications", include("apps.notification.urls")),
        path("analytics", include("apps.analytics.urls")),
        path('misc', include('miscellaneous.urls')),
    ])),

    re_path(r"^v2/(?P<net_type>(?:testnet|mainnet))/", include([
        path('accounts', include('apps.account.urls_v2')),
        path('assets', include('apps.asset.urls_v2')),
        path('transactions', include('apps.transaction.urls_v2')),
    ])),

    re_path(r"^v2/wallet/(?P<net_type>(?:testnet|mainnet))/", include([
        path('accounts', include('apps.account.urls_v2_wallet')),
        path('assets', include('apps.asset.urls_v2_wallet')),
        path('transactions', include('apps.transaction.urls_v2_wallet')),
        path('analytics', include("apps.analytics.urls_v2_wallet")),
        path('transactions', include('apps.transaction.urls_v2_wallet'))
    ])),
]

handler404 = "jasiri_wallet.exceptions_handlers.hanlder404"