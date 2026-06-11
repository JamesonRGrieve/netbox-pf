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
        ("netbox_pf", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="NATRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ("nat_type", models.CharField(max_length=16)),
                ("sequence", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ("disabled", models.BooleanField(default=False)),
                ("interface", models.CharField(blank=True, max_length=128)),
                ("ipprotocol", models.CharField(blank=True, max_length=8)),
                ("protocol", models.CharField(blank=True, max_length=32)),
                ("source", models.CharField(blank=True, max_length=255)),
                ("source_port", models.CharField(blank=True, max_length=128)),
                ("destination", models.CharField(blank=True, max_length=255)),
                ("destination_port", models.CharField(blank=True, max_length=128)),
                ("target", models.CharField(blank=True, max_length=255)),
                ("local_port", models.CharField(blank=True, max_length=128)),
                ("target_subnet", models.CharField(blank=True, max_length=64)),
                ("external", models.CharField(blank=True, max_length=255)),
                ("nat_port", models.CharField(blank=True, max_length=128)),
                ("static_nat_port", models.BooleanField(default=False)),
                ("nonat", models.BooleanField(default=False)),
                ("nordr", models.BooleanField(default=False)),
                ("nosync", models.BooleanField(default=False)),
                ("natreflection", models.CharField(blank=True, max_length=32)),
                ("poolopts", models.CharField(blank=True, max_length=64)),
                ("associated_rule_id", models.CharField(blank=True, max_length=64)),
                ("description", models.CharField(blank=True, max_length=255)),
                ("advanced", models.JSONField(blank=True, default=dict)),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="pf_nat_rules", to="dcim.device")),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={"verbose_name": "NAT Rule", "ordering": ["device", "nat_type", "sequence"], "unique_together": {("device", "nat_type", "sequence")}},
        ),
    ]
