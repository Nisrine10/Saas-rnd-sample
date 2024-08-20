import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL

ALLOW_CUSTOM_GROUPS = True

SUBSCRIPTION_PERMISSIONS = [
    ("advanced", "Advanced Perm"),
    ("pro", "Pro Perm"),
    ("basic", "Basic Perm"),
]

class Subscription(models.Model):
    name = models.CharField(max_length=120)
    subtitle = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(
        Permission, limit_choices_to={
            "content_type__app_label": "subscriptions", 
            "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSIONS]
        }
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    user_cancelled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @staticmethod
    def user_sub_post_save(sender, instance, *args, **kwargs):
        user_sub_instance = instance
        user = user_sub_instance.user
        subscription_obj = user_sub_instance.subscription
        groups_ids = []
        if subscription_obj is not None:
            groups = subscription_obj.groups.all()
            groups_ids = groups.values_list('id', flat=True)
        if not ALLOW_CUSTOM_GROUPS:
            user.groups.set(groups_ids)
        else:
            subs_qs = Subscription.objects.filter(active=True)
            if subscription_obj is not None:
                subs_qs = subs_qs.exclude(id=subscription_obj.id)
                
            subs_groups = subs_qs.values_list("groups__id", flat=True)
            subs_groups_set = set(subs_groups)
            current_groups = user.groups.all().values_list('id', flat=True)
            groups_ids_set = set(groups_ids)
            current_groups_set = set(current_groups) - subs_groups_set
            final_group_ids = list(groups_ids_set | current_groups_set)
            user.groups.set(final_group_ids)

# Connect the post_save signal after the model definition is complete
post_save.connect(UserSubscription.user_sub_post_save, sender=UserSubscription)
