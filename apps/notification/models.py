from django.db import models
from utils.constants import Constant
from utils.firebase import FCM
from utils.helpers import Helper


class NotificationManager(models.Manager):
    
    def create_and_notify(self, devices, code, data):
        if not devices: return
        fcm_tokens = []
        notifications = []
        description = eval(Constant.push_notifications[code])
        for device in devices:
            fcm_tokens.append(device.fcm_token)
            notifications.append(Notification(
                device=device, 
                data=Helper.get_txn_in_short(data), 
                net=data["net_type"]
            ))
        self.bulk_create(notifications)
        if data["net_type"] == 3:
            description = f"[Testnet] {description}" 
        FCM.bulk_send(fcm_tokens, description, data)
        
    def notify(self, devices, code, data):
        if not devices: return
        description = eval(Constant.push_notifications[code])
        fcm_tokens = [device.fcm_token for device in devices]
        FCM.bulk_send(fcm_tokens, description, data)
        
    def get_all(self, fcm_token, net):
        return self.filter(device__fcm_token=fcm_token, net=net).order_by("-id")
    
    def update_seen(self):
        return self.filter(is_seen=False).update(is_seen=True)
    
    def get_availability(self, fcm_token, net):
        if instance := self.filter(device__fcm_token=fcm_token, net=net).order_by("-id").first():
            return not instance.is_seen
        return False
        
        
            

class Notification(models.Model):
    device = models.ForeignKey("account.Device", on_delete=models.CASCADE, related_name="device_notifications")
    net = models.CharField(max_length=15, choices=Constant.NET_TYPES)
    is_seen = models.BooleanField(default=False)
    data = models.JSONField(default=dict, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = NotificationManager()
    
    class Meta:
        db_table = 'notifications'