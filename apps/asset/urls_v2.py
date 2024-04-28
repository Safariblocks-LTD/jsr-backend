from django.urls import path
from .views import *


urlpatterns = [
    path('/bought-unbought-titles', BoughtUnboughtTitles.as_view()),
    path('/verify-title', SendMailToVerifyTitle.as_view()),
    path('/get-title-details', GetTitleDetails.as_view()),
    path('/get-device-title',GetTitleDevice.as_view()),
    path('/get-maintenance-premium', GetMaintenancePremium.as_view()),
    path('/get-verified-titles', GetVerifiedTitles.as_view()),
    path('/get-secured-assets', GetSecuredAssets.as_view()),
    path('/update-index-token', UpdateIndexToken.as_view()),
    path('/verify-titleid', VerifyTitleId.as_view()),
    path('/file-maintenance-claim', FileMaintenanceClaim.as_view()),
    path('/claim-maintenance-reward', ClaimMaintenanceReward.as_view()),
    path('/update-reward-status', UpdateRewardStatus.as_view()),
    path('/price-calculate', TitleMaintenancePrice.as_view()),
    path('/currency-convert', ConvertUSDCTo.as_view()),
    path('/get-title-detail-from-dynamodb', TitleDetailsDynamoDB.as_view())
]
