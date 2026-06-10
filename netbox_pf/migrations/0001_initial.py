# SPDX-License-Identifier: AGPL-3.0-or-later
# Hand-authored initial migration. Verify against the target NetBox before deploy:
#   python manage.py makemigrations netbox_pf --check --dry-run
import django.core.validators
import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("dcim", "0001_initial"),
        ("extras", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Alias",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ("name", models.CharField(max_length=128, unique=True)),
                ("type", models.CharField(max_length=16)),
                ("content", models.TextField(blank=True)),
                ("detail", models.TextField(blank=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("advanced", models.JSONField(blank=True, default=dict)),
            ],
            options={"verbose_name": "Firewall Alias", "verbose_name_plural": "Firewall Aliases", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="FirewallRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, blank=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ("sequence", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ("action", models.CharField(max_length=8)),
                ("disabled", models.BooleanField(default=False)),
                ("quick", models.BooleanField(default=True)),
                ("interface", models.CharField(blank=True, max_length=512)),
                ("floating", models.BooleanField(default=False)),
                ("direction", models.CharField(default="in", max_length=4)),
                ("ipprotocol", models.CharField(default="inet", max_length=8)),
                ("protocol", models.CharField(blank=True, max_length=32)),
                ("source_type", models.CharField(default="any", max_length=16)),
                ("source", models.CharField(blank=True, max_length=255)),
                ("source_invert", models.BooleanField(default=False)),
                ("source_port", models.CharField(blank=True, max_length=128)),
                ("destination_type", models.CharField(default="any", max_length=16)),
                ("destination", models.CharField(blank=True, max_length=255)),
                ("destination_invert", models.BooleanField(default=False)),
                ("destination_port", models.CharField(blank=True, max_length=128)),
                ("gateway", models.CharField(blank=True, max_length=128)),
                ("log", models.BooleanField(default=False)),
                ("statetype", models.CharField(blank=True, max_length=32)),
                ("sched", models.CharField(blank=True, max_length=128)),
                ("tcpflags", models.CharField(blank=True, max_length=64)),
                ("icmptype", models.CharField(blank=True, max_length=255)),
                ("reply_to", models.CharField(blank=True, max_length=128)),
                ("tag", models.CharField(blank=True, max_length=128)),
                ("tagged", models.CharField(blank=True, max_length=128)),
                ("os", models.CharField(blank=True, max_length=64)),
                ("description", models.CharField(blank=True, max_length=255)),
                ("tracker", models.CharField(blank=True, max_length=64)),
                ("uuid", models.CharField(blank=True, max_length=64)),
                ("associated_rule_id", models.CharField(blank=True, max_length=64)),
                ("advanced", models.JSONField(blank=True, default=dict)),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="pf_firewall_rules", to="dcim.device")),
                ("source_alias", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="+", to="netbox_pf.alias")),
                ("destination_alias", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="+", to="netbox_pf.alias")),
            ],
            options={"verbose_name": "Firewall Rule", "ordering": ["device", "sequence"], "unique_together": {("device", "sequence")}},
        ),
        migrations.AddField(
            model_name="alias", name="tags",
            field=taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AddField(
            model_name="firewallrule", name="tags",
            field=taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
        ),
    ]
