# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.api.routers import NetBoxRouter
from . import views

app_name = "netbox_pf"

router = NetBoxRouter()
router.register("aliases", views.AliasViewSet)
router.register("firewall-rules", views.FirewallRuleViewSet)
router.register("nat-rules", views.NATRuleViewSet)
router.register("gateways", views.GatewayViewSet)
router.register("gateway-groups", views.GatewayGroupViewSet)
router.register("gateway-group-members", views.GatewayGroupMemberViewSet)

urlpatterns = router.urls
