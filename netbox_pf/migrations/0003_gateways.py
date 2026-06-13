# SPDX-License-Identifier: AGPL-3.0-or-later
# Hand-authored (NetBox disables makemigrations in production). Verify with:
#   python manage.py makemigrations netbox_pf --check --dry-run   (on a dev/ephemeral NetBox)
import django.core.validators
import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dcim", "0001_initial"),
        ("extras", "0001_initial"),
        ("netbox_pf", "0002_natrule"),
    ]
    operations = [
        migrations.CreateModel(
            name="Gateway",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ("name", models.CharField(max_length=64)),
                ("interface", models.CharField(max_length=64)),
                ("address", models.GenericIPAddressField(blank=True, null=True)),
                ("ipprotocol", models.CharField(default="inet", max_length=8)),
                ("monitor_ip", models.GenericIPAddressField(blank=True, null=True)),
                ("weight", models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ("priority", models.PositiveSmallIntegerField(default=255)),
                ("far_gateway", models.BooleanField(default=False)),
                ("default_gateway", models.BooleanField(default=False)),
                ("disabled", models.BooleanField(default=False)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="pf_gateways", to="dcim.device")),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={"verbose_name": "Gateway", "ordering": ["device", "name"], "unique_together": {("device", "name")}},
        ),
        migrations.CreateModel(
            name="GatewayGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ("name", models.CharField(max_length=64)),
                ("trigger", models.CharField(default="down", max_length=20)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="pf_gateway_groups", to="dcim.device")),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={"verbose_name": "Gateway Group", "ordering": ["device", "name"], "unique_together": {("device", "name")}},
        ),
        migrations.CreateModel(
            name="GatewayGroupMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ("tier", models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="members", to="netbox_pf.gatewaygroup")),
                ("gateway", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="group_memberships", to="netbox_pf.gateway")),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={"verbose_name": "Gateway Group Member", "ordering": ["group", "tier"], "unique_together": {("group", "gateway")}},
        ),
    ]
