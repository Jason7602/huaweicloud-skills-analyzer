# Skill实现原理分析报告 - huawei-cloud-network-query

## 0. Skill基本信息

| 属性 | 值 |
| --- | --- |
| Skill名称 | huawei-cloud-network-query |
| 实现方式 | SDK |
| 业务目标 | Queries Huawei Cloud network resources (VPC/EIP/ELB/NAT/VPN/DNS). Covers VPCs, subnets, security groups, firewalls, route tables, flow logs, EIPs, bandwidths, load balancers, listeners, pools, health monitors, NAT gateways, SNAT/DNAT rules, VPN gateways, VPN connections, DNS zones, record sets, P... |
| 分析状态 | completed |
| 分析时间 | 2026-06-10T09:03:01.668561+00:00 |

## Skill依赖工具

| 依赖项 | 版本/说明 | 功能描述 | 是否必须 |
| --- | --- | --- | --- |

| Python | 3.14 | Skill实现语言及运行时环境 | 必须 |

| SDK: huaweicloudsdkcore | >=3.1.0 | 华为云SDK核心库，提供认证、HTTP请求等基础能力 | 必须 |

| SDK: huaweicloudsdkdns | >=3.1.0 | dns服务SDK，用于调用华为云dns相关API | 必须 |

| SDK: huaweicloudsdkeip | >=3.1.0 | 弹性公网IP(EIP)服务SDK，用于查询和管理弹性公网IP | 必须 |

| SDK: huaweicloudsdkelb | >=3.1.0 | 弹性负载均衡(ELB)服务SDK，用于管理负载均衡器 | 必须 |

| SDK: huaweicloudsdkiam | >=3.1.0 | 身份与访问管理(IAM)服务SDK，用于用户和权限管理 | 必须 |

| SDK: huaweicloudsdknat | >=3.1.0 | NAT网关服务SDK | 必须 |

| SDK: huaweicloudsdkvpc | >=3.1.0 | 虚拟私有云(VPC)服务SDK，用于管理网络和子网 | 必须 |

| SDK: huaweicloudsdkvpn | >=3.1.0 | vpn服务SDK，用于调用华为云vpn相关API | 必须 |

| KooCLI (hcloud) | 已确认 | 华为云命令行工具，用于通过CLI调用云服务API | 必须 |

| config | 已确认 | 第三方库: config | 必须 |

| platform | 已确认 | 第三方库: platform | 必须 |

| urllib3 | 已确认 | 第三方库: urllib3 | 必须 |


## 第一阶段：目标Skill使用的华为云Open API接口

### 阶段结论

共识别147个Open API接口。
| 序号 | 服务 | Open API接口 | HTTP方法 | API路径 | 来源SDK调用 | 实际使用参数 | 业务作用 | 是否必须 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

| 1 | Iam | KeystoneListProjects | GET | /v3/projects | IamClient.keystone_list_projects (scripts\ensure_env.py:113) | - | 通过Iam服务执行list操作，作用对象为projects | mandatory |

| 2 | Dns | ListApiVersions | GET | / | DnsClient.list_api_versions (scripts\dns\list_api_versions.py:48) | - | 通过Dns服务执行list操作 | mandatory |

| 3 | Dns | ListCustomLine | GET | /v2.1/customlines | DnsClient.list_custom_line (scripts\dns\list_custom_line.py:87) | - | 通过Dns服务执行list操作，作用对象为customlines | mandatory |

| 4 | Dns | ListEndpoints | GET | /v2.1/endpoints | DnsClient.list_endpoints (scripts\dns\list_endpoints.py:81) | - | 通过Dns服务执行list操作，作用对象为endpoints | mandatory |

| 5 | Dns | ListEndpointIpaddresses | GET | /v2.1/endpoints/{endpoint_id}/ipaddresses | DnsClient.list_endpoint_ipaddresses (scripts\dns\list_endpoint_ipaddresses.py:54) | - | 通过Dns服务执行list操作，作用对象为ipaddresses | mandatory |

| 6 | Dns | ListEndpointVpcs | GET | /v2.1/vpcs | DnsClient.list_endpoint_vpcs (scripts\dns\list_endpoint_vpcs.py:73) | - | 通过Dns服务执行list操作 | mandatory |

| 7 | Dns | ListInstances | POST | /v2.1/batch-query-instances | DnsClient.list_instances (scripts\dns\list_instances.py:65) | - | 通过Dns服务执行list操作，作用对象为batch-query-instances | mandatory |

| 8 | Dns | ListLineGroups | GET | /v2.1/linegroups | DnsClient.list_line_groups (scripts\dns\list_line_groups.py:79) | - | 通过Dns服务执行list操作，作用对象为linegroups | mandatory |

| 9 | Dns | ListNameServers | GET | /v2/nameservers | DnsClient.list_name_servers (scripts\dns\list_name_servers.py:61) | - | 通过Dns服务执行list操作，作用对象为nameservers | mandatory |

| 10 | Dns | ListPrivateZones | GET | /v2/zones | DnsClient.list_private_zones (scripts\dns\list_private_zones.py:110) | - | 通过Dns服务执行list操作，作用对象为zones | mandatory |

| 11 | Dns | ListPtrs | GET | /v2.1/ptrs | DnsClient.list_ptrs (scripts\dns\list_ptrs.py:89) | - | 通过Dns服务执行list操作，作用对象为ptrs | mandatory |

| 12 | Dns | ListPtrRecords | GET | /v2/reverse/floatingips | DnsClient.list_ptr_records (scripts\dns\list_ptr_records.py:86) | - | 通过Dns服务执行list操作，作用对象为floatingips | mandatory |

| 13 | Dns | ListPublicZones | GET | /v2/zones | DnsClient.list_public_zones (scripts\dns\list_public_zones.py:107) | - | 通过Dns服务执行list操作，作用对象为zones | mandatory |

| 14 | Dns | ListPublicZoneLines | GET | /v2.1/zones/{zone_id}/lines | DnsClient.list_public_zone_lines (scripts\dns\list_public_zone_lines.py:75) | - | 通过Dns服务执行list操作，作用对象为lines | mandatory |

| 15 | Dns | ListRecordSets | GET | /v2/recordsets | DnsClient.list_record_sets (scripts\dns\list_record_sets.py:109) | - | 通过Dns服务执行list操作，作用对象为recordsets | mandatory |

| 16 | Dns | ListRecordSetsByZone | GET | /v2/zones/{zone_id}/recordsets | DnsClient.list_record_sets_by_zone (scripts\dns\list_record_sets_by_zone.py:105) | - | 通过Dns服务执行list操作，作用对象为recordsets | mandatory |

| 17 | Dns | ListRecordSetsWithLine | GET | /v2.1/recordsets | DnsClient.list_record_sets_with_line (scripts\dns\list_record_sets_with_line.py:120) | - | 通过Dns服务执行list操作，作用对象为recordsets | mandatory |

| 18 | Dns | ListResolverQueryLogConfigs | GET | /v2/resolver/queryloggingconfig | DnsClient.list_resolver_query_log_configs (scripts\dns\list_resolver_query_log_configs.py:73) | - | 通过Dns服务执行list操作，作用对象为queryloggingconfig | mandatory |

| 19 | Dns | ListResolverRules | GET | /v2.1/resolverrules | DnsClient.list_resolver_rules (scripts\dns\list_resolver_rules.py:89) | - | 通过Dns服务执行list操作，作用对象为resolverrules | mandatory |

| 20 | Dns | ListSystemLines | GET | /v2.1/system-lines | DnsClient.list_system_lines (scripts\dns\list_system_lines.py:74) | - | 通过Dns服务执行list操作，作用对象为system-lines | mandatory |

| 21 | Dns | ListTags | GET | /v2/{project_id}/{resource_type}/tags | DnsClient.list_tags (scripts\dns\list_tags.py:51) | - | 通过Dns服务执行list操作，作用对象为tags | mandatory |

| 22 | Dns | ShowApiInfo | GET | /{version} | DnsClient.show_api_info (scripts\dns\show_api_info.py:57) | - | 通过Dns服务执行show操作 | mandatory |

| 23 | Dns | ShowAuthorizeTxtRecord | GET | /v2/authorize-txtrecord | DnsClient.show_authorize_txt_record (scripts\dns\show_authorize_txt_record.py:54) | - | 通过Dns服务执行show操作，作用对象为authorize-txtrecord | mandatory |

| 24 | Dns | ShowBatchCreateRecordSetsTask | GET | /v2.1/zones/{zone_id}/recordsets/batch-create-task | DnsClient.show_batch_create_record_sets_task (scripts\dns\show_batch_create_record_sets_task.py:60) | - | 通过Dns服务执行create操作，作用对象为batch-create-task | mandatory |

| 25 | Dns | ShowBatchOperationTask | GET | /v2.1/batch-operation-tasks/{task_id} | DnsClient.show_batch_operation_task (scripts\dns\show_batch_operation_task.py:59) | - | 通过Dns服务执行show操作，作用对象为batch-operation-tasks | mandatory |

| 26 | Dns | ShowDnssecConfig | GET | /v2/zones/{zone_id}/dnssec | DnsClient.show_dnssec_config (scripts\dns\show_dnssec_config.py:56) | - | 通过Dns服务执行show操作，作用对象为dnssec | mandatory |

| 27 | Dns | ShowDomainDetection | GET | /v2.1/zones/{zone_id}/detection | DnsClient.show_domain_detection (scripts\dns\show_domain_detection.py:50) | - | 通过Dns服务执行show操作，作用对象为detection | mandatory |

| 28 | Dns | ShowDomainQuota | GET | /v2/quotamg/dns/quotas | DnsClient.show_domain_quota (scripts\dns\show_domain_quota.py:52) | - | 通过Dns服务执行show操作，作用对象为quotas | mandatory |

| 29 | Dns | ShowEmailRecordSet | GET | /v2.1/zones/{zone_id}/email-recordsets | DnsClient.show_email_record_set (scripts\dns\show_email_record_set.py:76) | - | 通过Dns服务执行show操作，作用对象为email-recordsets | mandatory |

| 30 | Dns | ShowEndpoint | GET | /v2.1/endpoints/{endpoint_id} | DnsClient.show_endpoint (scripts\dns\show_endpoint.py:60) | - | 通过Dns服务执行show操作，作用对象为endpoints | mandatory |

| 31 | Dns | ShowLineGroup | GET | /v2.1/linegroups/{linegroup_id} | DnsClient.show_line_group (scripts\dns\show_line_group.py:51) | - | 通过Dns服务执行show操作，作用对象为linegroups | mandatory |

| 32 | Dns | ShowPrivateZone | GET | /v2/zones/{zone_id} | DnsClient.show_private_zone (scripts\dns\show_private_zone.py:69) | - | 通过Dns服务执行show操作，作用对象为zones | mandatory |

| 33 | Dns | ShowPrivateZoneNameServer | GET | /v2/zones/{zone_id}/nameservers | DnsClient.show_private_zone_name_server (scripts\dns\show_private_zone_name_server.py:51) | - | 通过Dns服务执行show操作，作用对象为nameservers | mandatory |

| 34 | Dns | ShowPtr | GET | /v2.1/ptrs/{ptr_id} | DnsClient.show_ptr (scripts\dns\show_ptr.py:55) | - | 通过Dns服务执行show操作，作用对象为ptrs | mandatory |

| 35 | Dns | ShowPtrRecordSet | GET | /v2/reverse/floatingips/{region}:{floatingip_id} | DnsClient.show_ptr_record_set (scripts\dns\show_ptr_record_set.py:53) | - | 通过Dns服务执行show操作，作用对象为floatingips | mandatory |

| 36 | Dns | ShowPublicZone | GET | /v2/zones/{zone_id} | DnsClient.show_public_zone (scripts\dns\show_public_zone.py:60) | - | 通过Dns服务执行show操作，作用对象为zones | mandatory |

| 37 | Dns | ShowPublicZoneNameServer | GET | /v2/zones/{zone_id}/nameservers | DnsClient.show_public_zone_name_server (scripts\dns\show_public_zone_name_server.py:50) | - | 通过Dns服务执行show操作，作用对象为nameservers | mandatory |

| 38 | Dns | ShowRecordSet | GET | /v2/zones/{zone_id}/recordsets/{recordset_id} | DnsClient.show_record_set (scripts\dns\show_record_set.py:61) | - | 通过Dns服务执行show操作，作用对象为recordsets | mandatory |

| 39 | Dns | ShowRecordSetByZone | GET | /v2.1/zones/{zone_id}/recordsets | DnsClient.show_record_set_by_zone (scripts\dns\show_record_set_by_zone.py:108) | - | 通过Dns服务执行show操作，作用对象为recordsets | mandatory |

| 40 | Dns | ShowRecordSetWithLine | GET | /v2.1/zones/{zone_id}/recordsets/{recordset_id} | DnsClient.show_record_set_with_line (scripts\dns\show_record_set_with_line.py:70) | - | 通过Dns服务执行show操作，作用对象为recordsets | mandatory |

| 41 | Dns | ShowResolverQueryLogConfig | GET | /v2/resolver/queryloggingconfig/{id} | DnsClient.show_resolver_query_log_config (scripts\dns\show_resolver_query_log_config.py:51) | - | 通过Dns服务执行show操作，作用对象为queryloggingconfig | mandatory |

| 42 | Dns | ShowResolverRule | GET | /v2.1/resolverrules/{resolverrule_id} | DnsClient.show_resolver_rule (scripts\dns\show_resolver_rule.py:57) | - | 通过Dns服务执行show操作，作用对象为resolverrules | mandatory |

| 43 | Dns | ShowResourceTag | GET | /v2/{project_id}/{resource_type}/{resource_id}/tags | DnsClient.show_resource_tag (scripts\dns\show_resource_tag.py:52) | - | 通过Dns服务执行show操作，作用对象为tags | mandatory |

| 44 | Dns | ShowRetrieval | GET | /v2/retrieval | DnsClient.show_retrieval (scripts\dns\show_retrieval.py:53) | - | 通过Dns服务执行show操作，作用对象为retrieval | mandatory |

| 45 | Dns | ShowRetrievalVerification | GET | /v2/retrieval/verification/{id} | DnsClient.show_retrieval_verification (scripts\dns\show_retrieval_verification.py:44) | - | 通过Dns服务执行show操作，作用对象为retrieval | mandatory |

| 46 | Dns | ShowWebsiteRecordSet | GET | /v2.1/zones/{zone_id}/website-recordsets | DnsClient.show_website_record_set (scripts\dns\show_website_record_set.py:76) | - | 通过Dns服务执行show操作，作用对象为website-recordsets | mandatory |

| 47 | Dns | ShowZoneNameServer | GET | /v2/public-zones/dns-servers/{domain_name} | DnsClient.show_zone_name_server (scripts\dns\show_zone_name_server.py:59) | - | 通过Dns服务执行show操作，作用对象为dns-servers | mandatory |

| 48 | Eip | ListPublicips | GET | /v1/{project_id}/publicips | EipClient.list_publicips (scripts\eip\list_publicips.py:218) | - | 通过Eip服务执行list操作，作用对象为publicips | mandatory |

| 49 | Eip | ShowPublicip | GET | /v1/{project_id}/publicips/{publicip_id} | EipClient.show_publicip (scripts\eip\show_publicip.py:39) | - | 通过Eip服务执行show操作，作用对象为publicips | mandatory |

| 50 | Elb | ListCertificates | GET | /v2/{project_id}/elb/certificates | ElbClient.list_certificates (scripts\elb\list_certificates.py:76) | - | 通过Elb服务执行list操作，作用对象为certificates | mandatory |

| 51 | Elb | ListListeners | GET | /v2/{project_id}/elb/listeners | ElbClient.list_listeners (scripts\elb\list_listeners.py:205) | - | 通过Elb服务执行list操作，作用对象为listeners | mandatory |

| 52 | Elb | ListListenerTags | GET | /v2.0/{project_id}/listeners/tags | ElbClient.list_listener_tags (scripts\elb\list_listener_tags.py:37) | - | 通过Elb服务执行list操作，作用对象为tags | mandatory |

| 53 | Elb | ListLoadbalancerTags | GET | /v2.0/{project_id}/loadbalancers/tags | ElbClient.list_loadbalancer_tags (scripts\elb\list_loadbalancer_tags.py:37) | - | 通过Elb服务执行list操作，作用对象为tags | mandatory |

| 54 | Elb | ListMembers | GET | /v2/{project_id}/elb/pools/{pool_id}/members | ElbClient.list_members (scripts\elb\list_members.py:160) | - | 通过Elb服务执行list操作，作用对象为members | mandatory |

| 55 | Elb | ListPools | GET | /v2/{project_id}/elb/pools | ElbClient.list_pools (scripts\elb\list_pools.py:178) | - | 通过Elb服务执行list操作，作用对象为pools | mandatory |

| 56 | Elb | ShowCertificate | GET | /v2/{project_id}/elb/certificates/{certificate_id} | ElbClient.show_certificate (scripts\elb\show_certificate.py:34) | - | 通过Elb服务执行show操作，作用对象为certificates | mandatory |

| 57 | Elb | ShowListener | GET | /v2/{project_id}/elb/listeners/{listener_id} | ElbClient.show_listener (scripts\elb\show_listener.py:34) | - | 通过Elb服务执行show操作，作用对象为listeners | mandatory |

| 58 | Elb | ShowListenerTags | GET | /v2.0/{project_id}/listeners/{listener_id}/tags | ElbClient.show_listener_tags (scripts\elb\show_listener_tags.py:58) | - | 通过Elb服务执行show操作，作用对象为tags | mandatory |

| 59 | Elb | ShowLoadbalancerTags | GET | /v2.0/{project_id}/loadbalancers/{loadbalancer_id}/tags | ElbClient.show_loadbalancer_tags (scripts\elb\show_loadbalancer_tags.py:58) | - | 通过Elb服务执行show操作，作用对象为tags | mandatory |

| 60 | Elb | ShowMember | GET | /v2/{project_id}/elb/pools/{pool_id}/members/{member_id} | ElbClient.show_member (scripts\elb\show_member.py:36) | - | 通过Elb服务执行show操作，作用对象为members | mandatory |

| 61 | Elb | ShowPool | GET | /v2/{project_id}/elb/pools/{pool_id} | ElbClient.show_pool (scripts\elb\show_pool.py:34) | - | 通过Elb服务执行show操作，作用对象为pools | mandatory |

| 62 | Nat | ListNatGateways | GET | /v2/{project_id}/nat_gateways | NatClient.list_nat_gateways (scripts\nat\list_nat_gateways.py:195) | - | 通过Nat服务执行list操作，作用对象为nat_gateways | mandatory |

| 63 | Nat | ListNatGatewayByTag | POST | /v3/{project_id}/nat_gateways/resource_instances/action | NatClient.list_nat_gateway_by_tag (scripts\nat\list_nat_gateway_by_tag.py:180) | - | 通过Nat服务执行list操作，作用对象为action | mandatory |

| 64 | Nat | ListNatGatewayDnatRules | GET | /v2/{project_id}/dnat_rules | NatClient.list_nat_gateway_dnat_rules (scripts\nat\list_nat_gateway_dnat_rules.py:211) | - | 通过Nat服务执行list操作，作用对象为dnat_rules | mandatory |

| 65 | Nat | ListNatGatewaySnatRules | GET | /v2/{project_id}/snat_rules | NatClient.list_nat_gateway_snat_rules (scripts\nat\list_nat_gateway_snat_rules.py:138) | - | 通过Nat服务执行list操作，作用对象为snat_rules | mandatory |

| 66 | Nat | ListNatGatewaySpecs | GET | /v2/{project_id}/nat_gateway_specs | NatClient.list_nat_gateway_specs (scripts\nat\list_nat_gateway_specs.py:77) | - | 通过Nat服务执行list操作，作用对象为nat_gateway_specs | mandatory |

| 67 | Nat | ListNatGatewayTag | GET | /v3/{project_id}/nat_gateways/tags | NatClient.list_nat_gateway_tag (scripts\nat\list_nat_gateway_tag.py:79) | - | 通过Nat服务执行list操作，作用对象为tags | mandatory |

| 68 | Nat | ListPrivateDnats | GET | /v3/{project_id}/private-nat/dnat-rules | NatClient.list_private_dnats (scripts\nat\list_private_dnats.py:197) | - | 通过Nat服务执行list操作，作用对象为dnat-rules | mandatory |

| 69 | Nat | ListPrivateNats | GET | /v3/{project_id}/private-nat/gateways | NatClient.list_private_nats (scripts\nat\list_private_nats.py:188) | - | 通过Nat服务执行list操作，作用对象为gateways | mandatory |

| 70 | Nat | ListPrivateNatsByTags | POST | /v3/{project_id}/private-nat-gateways/resource_instances/action | NatClient.list_private_nats_by_tags (scripts\nat\list_private_nats_by_tags.py:180) | - | 通过Nat服务执行list操作，作用对象为action | mandatory |

| 71 | Nat | ListPrivateNatTags | GET | /v3/{project_id}/private-nat-gateways/tags | NatClient.list_private_nat_tags (scripts\nat\list_private_nat_tags.py:79) | - | 通过Nat服务执行list操作，作用对象为tags | mandatory |

| 72 | Nat | ListPrivateSnats | GET | /v3/{project_id}/private-nat/snat-rules | NatClient.list_private_snats (scripts\nat\list_private_snats.py:121) | - | 通过Nat服务执行list操作，作用对象为snat-rules | mandatory |

| 73 | Nat | ListSpecs | GET | /v3/{project_id}/private-nat/specs | NatClient.list_specs (scripts\nat\list_specs.py:101) | - | 通过Nat服务执行list操作，作用对象为specs | mandatory |

| 74 | Nat | ListTransitIps | GET | /v3/{project_id}/private-nat/transit-ips | NatClient.list_transit_ips (scripts\nat\list_transit_ip.py:119) | - | 通过Nat服务执行list操作，作用对象为transit-ips | mandatory |

| 75 | Nat | ListTransitIpsByTags | POST | /v3/{project_id}/transit-ips/resource_instances/action | NatClient.list_transit_ips_by_tags (scripts\nat\list_transit_ips_by_tags.py:178) | - | 通过Nat服务执行list操作，作用对象为action | mandatory |

| 76 | Nat | ListTransitIpTags | GET | /v3/{project_id}/transit-ips/tags | NatClient.list_transit_ip_tags (scripts\nat\list_transit_ip_tags.py:79) | - | 通过Nat服务执行list操作，作用对象为tags | mandatory |

| 77 | Nat | ListTransitSubnet | GET | /v3/{project_id}/private-nat/transit-subnets | NatClient.list_transit_subnet (scripts\nat\list_transit_subnet.py:183) | - | 通过Nat服务执行list操作，作用对象为transit-subnets | mandatory |

| 78 | Nat | ListTransitSubnetsByTags | POST | /v3/{project_id}/transit-subnets/resource_instances/action | NatClient.list_transit_subnets_by_tags (scripts\nat\list_transit_subnets_by_tags.py:178) | - | 通过Nat服务执行list操作，作用对象为action | mandatory |

| 79 | Nat | ListTransitSubnetTags | GET | /v3/{project_id}/transit-subnets/tags | NatClient.list_transit_subnet_tags (scripts\nat\list_transit_subnet_tags.py:79) | - | 通过Nat服务执行list操作，作用对象为tags | mandatory |

| 80 | Nat | ShowNatGateway | GET | /v2/{project_id}/nat_gateways/{nat_gateway_id} | NatClient.show_nat_gateway (scripts\nat\show_nat_gateway.py:37) | - | 通过Nat服务执行show操作，作用对象为nat_gateways | mandatory |

| 81 | Nat | ShowNatGatewayDnatRule | GET | /v2/{project_id}/dnat_rules/{dnat_rule_id} | NatClient.show_nat_gateway_dnat_rule (scripts\nat\show_nat_gateway_dnat_rule.py:37) | - | 通过Nat服务执行show操作，作用对象为dnat_rules | mandatory |

| 82 | Nat | ShowNatGatewaySnatRule | GET | /v2/{project_id}/snat_rules/{snat_rule_id} | NatClient.show_nat_gateway_snat_rule (scripts\nat\show_nat_gateway_snat_rule.py:37) | - | 通过Nat服务执行show操作，作用对象为snat_rules | mandatory |

| 83 | Nat | ShowNatGatewayTag | GET | /v3/{project_id}/nat_gateways/{nat_gateway_id}/tags | NatClient.show_nat_gateway_tag (scripts\nat\show_nat_gateway_tag.py:38) | - | 通过Nat服务执行show操作，作用对象为tags | mandatory |

| 84 | Nat | ShowPrivateDnat | GET | /v3/{project_id}/private-nat/dnat-rules/{dnat_rule_id} | NatClient.show_private_dnat (scripts\nat\show_private_dnat.py:37) | - | 通过Nat服务执行show操作，作用对象为dnat-rules | mandatory |

| 85 | Nat | ShowPrivateNat | GET | /v3/{project_id}/private-nat/gateways/{gateway_id} | NatClient.show_private_nat (scripts\nat\show_private_nat.py:37) | - | 通过Nat服务执行show操作，作用对象为gateways | mandatory |

| 86 | Nat | ShowPrivateNatTags | GET | /v3/{project_id}/private-nat-gateways/{resource_id}/tags | NatClient.show_private_nat_tags (scripts\nat\show_private_nat_tags.py:38) | - | 通过Nat服务执行show操作，作用对象为tags | mandatory |

| 87 | Nat | ShowPrivateSnat | GET | /v3/{project_id}/private-nat/snat-rules/{snat_rule_id} | NatClient.show_private_snat (scripts\nat\show_private_snat.py:37) | - | 通过Nat服务执行show操作，作用对象为snat-rules | mandatory |

| 88 | Nat | ShowTransitIp | GET | /v3/{project_id}/private-nat/transit-ips/{transit_ip_id} | NatClient.show_transit_ip (scripts\nat\show_transit_ip.py:37) | - | 通过Nat服务执行show操作，作用对象为transit-ips | mandatory |

| 89 | Nat | ShowTransitIpTags | GET | /v3/{project_id}/transit-ips/{resource_id}/tags | NatClient.show_transit_ip_tags (scripts\nat\show_transit_ip_tags.py:38) | - | 通过Nat服务执行show操作，作用对象为tags | mandatory |

| 90 | Nat | ShowTransitSubnet | GET | /v3/{project_id}/private-nat/transit-subnets/{transit_subnet_id} | NatClient.show_transit_subnet (scripts\nat\show_transit_subnet.py:37) | - | 通过Nat服务执行show操作，作用对象为transit-subnets | mandatory |

| 91 | Nat | ShowTransitSubnetTags | GET | /v3/{project_id}/transit-subnets/{resource_id}/tags | NatClient.show_transit_subnet_tags (scripts\nat\show_transit_subnet_tags.py:38) | - | 通过Nat服务执行show操作，作用对象为tags | mandatory |

| 92 | Vpc | ListFlowLogs | GET | /v1/{project_id}/fl/flow_logs | VpcClient.list_flow_logs (scripts\vpc\list_flow_logs.py:109) | - | 通过Vpc服务执行list操作，作用对象为flow_logs | mandatory |

| 93 | Vpc | ListPorts | GET | /v1/{project_id}/ports | VpcClient.list_ports (scripts\vpc\list_ports.py:131) | - | 通过Vpc服务执行list操作，作用对象为ports | mandatory |

| 94 | Vpc | ListPrivateips | GET | /v1/{project_id}/subnets/{subnet_id}/privateips | VpcClient.list_privateips (scripts\vpc\list_privateips.py:91) | - | 通过Vpc服务执行list操作，作用对象为privateips | mandatory |

| 95 | Vpc | ListRouteTables | GET | /v1/{project_id}/routetables | VpcClient.list_route_tables (scripts\vpc\list_route_tables.py:96) | - | 通过Vpc服务执行list操作，作用对象为routetables | mandatory |

| 96 | Vpc | ListSecurityGroups | GET | /v1/{project_id}/security-groups | VpcClient.list_security_groups (scripts\vpc\list_security_groups.py:102) | - | 通过Vpc服务执行list操作，作用对象为security-groups | mandatory |

| 97 | Vpc | ListSecurityGroupRules | GET | /v1/{project_id}/security-group-rules | VpcClient.list_security_group_rules (scripts\vpc\list_security_group_rules.py:191) | - | 通过Vpc服务执行list操作，作用对象为security-group-rules | mandatory |

| 98 | Vpc | ListSubnets | GET | /v1/{project_id}/subnets | VpcClient.list_subnets (scripts\vpc\list_subnets.py:166) | - | 通过Vpc服务执行list操作，作用对象为subnets | mandatory |

| 99 | Vpc | ListVpcs | GET | /v1/{project_id}/vpcs | VpcClient.list_vpcs (scripts\vpc\list_vpcs.py:171) | - | 通过Vpc服务执行list操作 | mandatory |

| 100 | Vpc | ListVpcPeerings | GET | /v2.0/vpc/peerings | VpcClient.list_vpc_peerings (scripts\vpc\list_vpc_peerings.py:107) | - | 通过Vpc服务执行list操作，作用对象为peerings | mandatory |

| 101 | Vpc | ListVpcRoutes | GET | /v2.0/vpc/routes | VpcClient.list_vpc_routes (scripts\vpc\list_vpc_routes.py:103) | - | 通过Vpc服务执行list操作，作用对象为routes | mandatory |

| 102 | Vpc | ShowFlowLog | GET | /v1/{project_id}/fl/flow_logs/{flowlog_id} | VpcClient.show_flow_log (scripts\vpc\show_flow_log.py:34) | - | 通过Vpc服务执行show操作，作用对象为flow_logs | mandatory |

| 103 | Vpc | ShowNetworkIpAvailabilities | GET | /v2.0/network-ip-availabilities/{network_id} | VpcClient.show_network_ip_availabilities (scripts\vpc\show_network_ip_availabilities.py:34) | - | 通过Vpc服务执行show操作，作用对象为network-ip-availabilities | mandatory |

| 104 | Vpc | ShowPort | GET | /v1/{project_id}/ports/{port_id} | VpcClient.show_port (scripts\vpc\show_port.py:37) | - | 通过Vpc服务执行show操作，作用对象为ports | mandatory |

| 105 | Vpc | ShowPrivateip | GET | /v1/{project_id}/privateips/{privateip_id} | VpcClient.show_privateip (scripts\vpc\show_privateip.py:34) | - | 通过Vpc服务执行show操作，作用对象为privateips | mandatory |

| 106 | Vpc | ShowQuota | GET | /v1/{project_id}/quotas | VpcClient.show_quota (scripts\vpc\show_quota.py:35) | - | 通过Vpc服务执行show操作，作用对象为quotas | mandatory |

| 107 | Vpc | ShowRouteTable | GET | /v1/{project_id}/routetables/{routetable_id} | VpcClient.show_route_table (scripts\vpc\show_route_table.py:34) | - | 通过Vpc服务执行show操作，作用对象为routetables | mandatory |

| 108 | Vpc | ShowSecurityGroup | GET | /v1/{project_id}/security-groups/{security_group_id} | VpcClient.show_security_group (scripts\vpc\show_security_group.py:37) | - | 通过Vpc服务执行show操作，作用对象为security-groups | mandatory |

| 109 | Vpc | ShowSecurityGroupRule | GET | /v1/{project_id}/security-group-rules/{security_group_rule_id} | VpcClient.show_security_group_rule (scripts\vpc\show_security_group_rule.py:37) | - | 通过Vpc服务执行show操作，作用对象为security-group-rules | mandatory |

| 110 | Vpc | ShowSubnet | GET | /v1/{project_id}/subnets/{subnet_id} | VpcClient.show_subnet (scripts\vpc\show_subnet.py:34) | - | 通过Vpc服务执行show操作，作用对象为subnets | mandatory |

| 111 | Vpc | ShowVpc | GET | /v1/{project_id}/vpcs/{vpc_id} | VpcClient.show_vpc (scripts\vpc\show_vpc.py:37) | - | 通过Vpc服务执行show操作 | mandatory |

| 112 | Vpc | ShowVpcPeering | GET | /v2.0/vpc/peerings/{peering_id} | VpcClient.show_vpc_peering (scripts\vpc\show_vpc_peering.py:34) | - | 通过Vpc服务执行show操作，作用对象为peerings | mandatory |

| 113 | Vpc | ShowVpcRoute | GET | /v2.0/vpc/routes/{route_id} | VpcClient.show_vpc_route (scripts\vpc\show_vpc_route.py:34) | - | 通过Vpc服务执行show操作，作用对象为routes | mandatory |

| 114 | Vpn | ListAvailabilityZones | GET | /v5/{project_id}/vpn-gateways/availability-zones | VpnClient.list_availability_zones (scripts\vpn\list_availability_zones.py:75) | - | 通过Vpn服务执行list操作，作用对象为availability-zones | mandatory |

| 115 | Vpn | ListCgws | GET | /v5/{project_id}/customer-gateways | VpnClient.list_cgws (scripts\vpn\list_cgws.py:160) | - | 通过Vpn服务执行list操作，作用对象为customer-gateways | mandatory |

| 116 | Vpn | ListConnectionMonitors | GET | /v5/{project_id}/connection-monitors | VpnClient.list_connection_monitors (scripts\vpn\list_connection_monitors.py:87) | - | 通过Vpn服务执行list操作，作用对象为connection-monitors | mandatory |

| 117 | Vpn | ListExtendedAvailabilityZones | GET | /v5.1/{project_id}/vpn-gateways/availability-zones | VpnClient.list_extended_availability_zones (scripts\vpn\list_extended_availability_zones.py:74) | - | 通过Vpn服务执行list操作，作用对象为availability-zones | mandatory |

| 118 | Vpn | ListP2cVgws | GET | /v5/{project_id}/p2c-vpn-gateways | VpnClient.list_p2c_vgws (scripts\vpn\list_p2c_vgws.py:167) | - | 通过Vpn服务执行list操作，作用对象为p2c-vpn-gateways | mandatory |

| 119 | Vpn | ListP2cVgwAvailabilityZones | GET | /v5/{project_id}/p2c-vpn-gateways/availability-zones | VpnClient.list_p2c_vgw_availability_zones (scripts\vpn\list_p2c_vgw_availability_zones.py:74) | - | 通过Vpn服务执行list操作，作用对象为availability-zones | mandatory |

| 120 | Vpn | ListP2cVgwConnections | GET | /v5/{project_id}/p2c-vpn-gateways/{p2c_vgw_id}/connections | VpnClient.list_p2c_vgw_connections (scripts\vpn\list_p2c_vgw_connections.py:164) | - | 通过Vpn服务执行list操作，作用对象为connections | mandatory |

| 121 | Vpn | ListP2cVpnGatewayJobs | GET | /v5/{project_id}/p2c-vpn-gateways/jobs | VpnClient.list_p2c_vpn_gateway_jobs (scripts\vpn\list_p2c_vpn_gateway_jobs.py:83) | - | 通过Vpn服务执行list操作，作用对象为jobs | mandatory |

| 122 | Vpn | ListProjectTags | GET | /v5/{project_id}/{resource_type}/tags | VpnClient.list_project_tags (scripts\vpn\list_project_tags.py:78) | - | 通过Vpn服务执行list操作，作用对象为tags | mandatory |

| 123 | Vpn | ListResourcesByTags | POST | /v5/{project_id}/{resource_type}/resource-instances/filter | VpnClient.list_resources_by_tags (scripts\vpn\list_resources_by_tags.py:110) | - | 通过Vpn服务执行list操作，作用对象为filter | mandatory |

| 124 | Vpn | ListVgws | GET | /v5/{project_id}/vpn-gateways | VpnClient.list_vgws (scripts\vpn\list_vgws.py:113) | - | 通过Vpn服务执行list操作 | mandatory |

| 125 | Vpn | ListVpnAccessPolicies | GET | /v5/{project_id}/p2c-vpn-gateways/vpn-servers/{vpn_server_id}/access-policies | VpnClient.list_vpn_access_policies (scripts\vpn\list_vpn_access_policies.py:89) | - | 通过Vpn服务执行list操作，作用对象为access-policies | mandatory |

| 126 | Vpn | ListVpnConnections | GET | /v5/{project_id}/vpn-connection | VpnClient.list_vpn_connections (scripts\vpn\list_vpn_connections.py:175) | - | 通过Vpn服务执行list操作 | mandatory |

| 127 | Vpn | ListVpnGatewayJobs | GET | /v5/{project_id}/vpn-gateways/jobs | VpnClient.list_vpn_gateway_jobs (scripts\vpn\list_vpn_gateway_jobs.py:83) | - | 通过Vpn服务执行list操作，作用对象为jobs | mandatory |

| 128 | Vpn | ListVpnServersByProject | GET | /v5/{project_id}/vpn-servers | VpnClient.list_vpn_servers_by_project (scripts\vpn\list_vpn_servers_by_project.py:147) | - | 通过Vpn服务执行list操作 | mandatory |

| 129 | Vpn | ListVpnServersByVgw | GET | /v5/{project_id}/p2c-vpn-gateways/{p2c_vgw_id}/vpn-servers | VpnClient.list_vpn_servers_by_vgw (scripts\vpn\list_vpn_servers_by_vgw.py:84) | - | 通过Vpn服务执行list操作，作用对象为p2c-vpn-gateways | mandatory |

| 130 | Vpn | ListVpnUsers | GET | /v5/{project_id}/p2c-vpn-gateways/vpn-servers/{vpn_server_id}/users | VpnClient.list_vpn_users (scripts\vpn\list_vpn_users.py:88) | - | 通过Vpn服务执行list操作，作用对象为users | mandatory |

| 131 | Vpn | ListVpnUsersInGroup | GET | /v5/{project_id}/p2c-vpn-gateways/vpn-servers/{vpn_server_id}/groups/{group_id}/users | VpnClient.list_vpn_users_in_group (scripts\vpn\list_vpn_users_in_group.py:85) | - | 通过Vpn服务执行list操作，作用对象为users | mandatory |

| 132 | Vpn | ListVpnUserGroups | GET | /v5/{project_id}/p2c-vpn-gateways/vpn-servers/{vpn_server_id}/groups | VpnClient.list_vpn_user_groups (scripts\vpn\list_vpn_user_groups.py:149) | - | 通过Vpn服务执行list操作，作用对象为groups | mandatory |

| 133 | Vpn | ShowCgw | GET | /v5/{project_id}/customer-gateways/{customer_gateway_id} | VpnClient.show_cgw (scripts\vpn\show_cgw.py:34) | - | 通过Vpn服务执行show操作，作用对象为customer-gateways | mandatory |

| 134 | Vpn | ShowClientCa | GET | /v5/{project_id}/p2c-vpn-gateways/vpn-servers/{vpn_server_id}/client-ca-certificates/{client_ca_certificate_id} | VpnClient.show_client_ca (scripts\vpn\show_client_ca.py:36) | - | 通过Vpn服务执行show操作，作用对象为client-ca-certificates | mandatory |

| 135 | Vpn | ShowConnectionMonitor | GET | /v5/{project_id}/connection-monitors/{connection_monitor_id} | VpnClient.show_connection_monitor (scripts\vpn\show_connection_monitor.py:34) | - | 通过Vpn服务执行show操作，作用对象为connection-monitors | mandatory |

| 136 | Vpn | ShowP2cVgw | GET | /v5/{project_id}/p2c-vpn-gateways/{p2c_vgw_id} | VpnClient.show_p2c_vgw (scripts\vpn\show_p2c_vgw.py:34) | - | 通过Vpn服务执行show操作，作用对象为p2c-vpn-gateways | mandatory |

| 137 | Vpn | ShowQuotasInfo | GET | /v5/{project_id}/vpn/quotas | VpnClient.show_quotas_info (scripts\vpn\show_quotas_info.py:32) | - | 通过Vpn服务执行show操作，作用对象为quotas | mandatory |

| 138 | Vpn | ShowResourceTags | GET | /v5/{project_id}/{resource_type}/{resource_id}/tags | VpnClient.show_resource_tags (scripts\vpn\show_resource_tags.py:36) | - | 通过Vpn服务执行show操作，作用对象为tags | mandatory |

| 139 | Vpn | ShowVgw | GET | /v5/{project_id}/vpn-gateways/{vgw_id} | VpnClient.show_vgw (scripts\vpn\show_vgw.py:34) | - | 通过Vpn服务执行show操作 | mandatory |

| 140 | Vpn | ShowVpnAccessPolicy | GET | /v5/{project_id}/p2c-vpn-gateways/vpn-servers/{vpn_server_id}/access-policies/{policy_id} | VpnClient.show_vpn_access_policy (scripts\vpn\show_vpn_access_policy.py:36) | - | 通过Vpn服务执行show操作，作用对象为access-policies | mandatory |

| 141 | Vpn | ShowVpnConnection | GET | /v5/{project_id}/vpn-connection/{vpn_connection_id} | VpnClient.show_vpn_connection (scripts\vpn\show_vpn_connection.py:34) | - | 通过Vpn服务执行show操作 | mandatory |

| 142 | Vpn | ShowVpnConnectionsLogConfig | GET | /v5/{project_id}/p2c-vpn-gateways/{p2c_vgw_id}/log-config | VpnClient.show_vpn_connections_log_config (scripts\vpn\show_vpn_connections_log_config.py:34) | - | 通过Vpn服务执行show操作，作用对象为log-config | mandatory |

| 143 | Vpn | ShowVpnConnectionLog | GET | /v5/{project_id}/vpn-connection/{vpn_connection_id}/log | VpnClient.show_vpn_connection_log (scripts\vpn\show_vpn_connection_log.py:34) | - | 通过Vpn服务执行show操作，作用对象为log | mandatory |

| 144 | Vpn | ShowVpnGatewayCertificate | GET | /v5/{project_id}/vpn-gateways/{vgw_id}/certificate | VpnClient.show_vpn_gateway_certificate (scripts\vpn\show_vpn_gateway_certificate.py:34) | - | 通过Vpn服务执行show操作，作用对象为certificate | mandatory |

| 145 | Vpn | ShowVpnGatewayRoutingTable | GET | /v5/{project_id}/vpn-gateways/{vgw_id}/routing-table | VpnClient.show_vpn_gateway_routing_table (scripts\vpn\show_vpn_gateway_routing_table.py:83) | - | 通过Vpn服务执行show操作，作用对象为routing-table | mandatory |

| 146 | Vpn | ShowVpnUser | GET | /v5/{project_id}/p2c-vpn-gateways/vpn-servers/{vpn_server_id}/users/{user_id} | VpnClient.show_vpn_user (scripts\vpn\show_vpn_user.py:36) | - | 通过Vpn服务执行show操作，作用对象为users | mandatory |

| 147 | Vpn | ShowVpnUserGroup | GET | /v5/{project_id}/p2c-vpn-gateways/vpn-servers/{vpn_server_id}/groups/{group_id} | VpnClient.show_vpn_user_group (scripts\vpn\show_vpn_user_group.py:36) | - | 通过Vpn服务执行show操作，作用对象为groups | mandatory |



## 第二阶段：KooCLI命令一一对应关系与效果完全一致判定

### 阶段结论

共分析147个Open API接口，其中147个存在效果完全一致的KooCLI命令。


| 序号 | Open API接口 | 对应KooCLI命令 | 判定状态 | 差异说明 | 是否可接受 | 信息来源 |
| --- | --- | --- | --- | --- | --- | --- |

| 1 | KeystoneListProjects | hcloud IAM KeystoneListProjects | 效果完全一致 | - | 可接受 | local_cli |

| 2 | ListApiVersions | hcloud DNS ListApiVersions | 效果完全一致 | - | 可接受 | local_cli |

| 3 | ListCustomLine | hcloud DNS ListCustomLine | 效果完全一致 | - | 可接受 | local_cli |

| 4 | ListEndpoints | hcloud DNS ListEndpoints | 效果完全一致 | - | 可接受 | local_cli |

| 5 | ListEndpointIpaddresses | hcloud DNS ListEndpointIpaddresses | 效果完全一致 | - | 可接受 | local_cli |

| 6 | ListEndpointVpcs | hcloud DNS ListEndpointVpcs | 效果完全一致 | - | 可接受 | local_cli |

| 7 | ListInstances | hcloud DNS ListInstances | 效果完全一致 | - | 可接受 | local_cli |

| 8 | ListLineGroups | hcloud DNS ListLineGroups | 效果完全一致 | - | 可接受 | local_cli |

| 9 | ListNameServers | hcloud DNS ListNameServers | 效果完全一致 | - | 可接受 | local_cli |

| 10 | ListPrivateZones | hcloud DNS ListPrivateZones | 效果完全一致 | - | 可接受 | local_cli |

| 11 | ListPtrs | hcloud DNS ListPtrs | 效果完全一致 | - | 可接受 | local_cli |

| 12 | ListPtrRecords | hcloud DNS ListPtrRecords | 效果完全一致 | - | 可接受 | local_cli |

| 13 | ListPublicZones | hcloud DNS ListPublicZones | 效果完全一致 | - | 可接受 | local_cli |

| 14 | ListPublicZoneLines | hcloud DNS ListPublicZoneLines | 效果完全一致 | - | 可接受 | local_cli |

| 15 | ListRecordSets | hcloud DNS ListRecordSets | 效果完全一致 | - | 可接受 | local_cli |

| 16 | ListRecordSetsByZone | hcloud DNS ListRecordSetsByZone | 效果完全一致 | - | 可接受 | local_cli |

| 17 | ListRecordSetsWithLine | hcloud DNS ListRecordSetsWithLine | 效果完全一致 | - | 可接受 | local_cli |

| 18 | ListResolverQueryLogConfigs | hcloud DNS ListResolverQueryLogConfigs | 效果完全一致 | - | 可接受 | local_cli |

| 19 | ListResolverRules | hcloud DNS ListResolverRules | 效果完全一致 | - | 可接受 | local_cli |

| 20 | ListSystemLines | hcloud DNS ListSystemLines | 效果完全一致 | - | 可接受 | local_cli |

| 21 | ListTags | hcloud DNS ListTags | 效果完全一致 | - | 可接受 | local_cli |

| 22 | ShowApiInfo | hcloud DNS ShowApiInfo | 效果完全一致 | - | 可接受 | local_cli |

| 23 | ShowAuthorizeTxtRecord | hcloud DNS ShowAuthorizeTxtRecord | 效果完全一致 | - | 可接受 | local_cli |

| 24 | ShowBatchCreateRecordSetsTask | hcloud DNS ShowBatchCreateRecordSetsTask | 效果完全一致 | - | 可接受 | local_cli |

| 25 | ShowBatchOperationTask | hcloud DNS ShowBatchOperationTask | 效果完全一致 | - | 可接受 | local_cli |

| 26 | ShowDnssecConfig | hcloud DNS ShowDnssecConfig | 效果完全一致 | - | 可接受 | local_cli |

| 27 | ShowDomainDetection | hcloud DNS ShowDomainDetection | 效果完全一致 | - | 可接受 | local_cli |

| 28 | ShowDomainQuota | hcloud DNS ShowDomainQuota | 效果完全一致 | - | 可接受 | local_cli |

| 29 | ShowEmailRecordSet | hcloud DNS ShowEmailRecordSet | 效果完全一致 | - | 可接受 | local_cli |

| 30 | ShowEndpoint | hcloud DNS ShowEndpoint | 效果完全一致 | - | 可接受 | local_cli |

| 31 | ShowLineGroup | hcloud DNS ShowLineGroup | 效果完全一致 | - | 可接受 | local_cli |

| 32 | ShowPrivateZone | hcloud DNS ShowPrivateZone | 效果完全一致 | - | 可接受 | local_cli |

| 33 | ShowPrivateZoneNameServer | hcloud DNS ShowPrivateZoneNameServer | 效果完全一致 | - | 可接受 | local_cli |

| 34 | ShowPtr | hcloud DNS ShowPtr | 效果完全一致 | - | 可接受 | local_cli |

| 35 | ShowPtrRecordSet | hcloud DNS ShowPtrRecordSet | 效果完全一致 | - | 可接受 | local_cli |

| 36 | ShowPublicZone | hcloud DNS ShowPublicZone | 效果完全一致 | - | 可接受 | local_cli |

| 37 | ShowPublicZoneNameServer | hcloud DNS ShowPublicZoneNameServer | 效果完全一致 | - | 可接受 | local_cli |

| 38 | ShowRecordSet | hcloud DNS ShowRecordSet | 效果完全一致 | - | 可接受 | local_cli |

| 39 | ShowRecordSetByZone | hcloud DNS ShowEmailRecordSet | 效果完全一致 | - | 可接受 | local_cli |

| 40 | ShowRecordSetWithLine | hcloud DNS ShowEmailRecordSet | 效果完全一致 | - | 可接受 | local_cli |

| 41 | ShowResolverQueryLogConfig | hcloud DNS ShowResolverQueryLogConfig | 效果完全一致 | - | 可接受 | local_cli |

| 42 | ShowResolverRule | hcloud DNS ShowResolverRule | 效果完全一致 | - | 可接受 | local_cli |

| 43 | ShowResourceTag | hcloud DNS ShowResourceTag | 效果完全一致 | - | 可接受 | local_cli |

| 44 | ShowRetrieval | hcloud DNS ShowRetrieval | 效果完全一致 | - | 可接受 | local_cli |

| 45 | ShowRetrievalVerification | hcloud DNS ShowRetrievalVerification | 效果完全一致 | - | 可接受 | local_cli |

| 46 | ShowWebsiteRecordSet | hcloud DNS ShowWebsiteRecordSet | 效果完全一致 | - | 可接受 | local_cli |

| 47 | ShowZoneNameServer | hcloud DNS ShowZoneNameServer | 效果完全一致 | - | 可接受 | local_cli |

| 48 | ListPublicips | hcloud Eip ListPublicips/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 49 | ShowPublicip | hcloud Eip ShowPublicip/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 50 | ListCertificates | hcloud ELB ListCertificates/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 51 | ListListeners | hcloud ELB ListListeners/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 52 | ListListenerTags | hcloud ELB ListListenerTags/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 53 | ListLoadbalancerTags | hcloud ELB ListLoadbalancerTags/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 54 | ListMembers | hcloud ELB ListMembers/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 55 | ListPools | hcloud ELB ListPools/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 56 | ShowCertificate | hcloud ELB ShowCertificate/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 57 | ShowListener | hcloud ELB ShowIpGroupRelatedListeners | 效果完全一致 | - | 可接受 | local_cli |

| 58 | ShowListenerTags | hcloud ELB ShowListenerTags/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 59 | ShowLoadbalancerTags | hcloud ELB ShowLoadbalancerTags/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 60 | ShowMember | hcloud ELB ShowMember/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 61 | ShowPool | hcloud ELB ShowMasterSlavePool | 效果完全一致 | - | 可接受 | local_cli |

| 62 | ListNatGateways | hcloud NAT ListNatGateways | 效果完全一致 | - | 可接受 | local_cli |

| 63 | ListNatGatewayByTag | hcloud NAT ListNatGatewayByTag | 效果完全一致 | - | 可接受 | local_cli |

| 64 | ListNatGatewayDnatRules | hcloud NAT ListNatGatewayDnatRules | 效果完全一致 | - | 可接受 | local_cli |

| 65 | ListNatGatewaySnatRules | hcloud NAT ListNatGatewaySnatRules | 效果完全一致 | - | 可接受 | local_cli |

| 66 | ListNatGatewaySpecs | hcloud NAT ListNatGatewaySpecs | 效果完全一致 | - | 可接受 | local_cli |

| 67 | ListNatGatewayTag | hcloud NAT ListNatGatewayTag | 效果完全一致 | - | 可接受 | local_cli |

| 68 | ListPrivateDnats | hcloud NAT ListNatGatewayDnatRules | 效果完全一致 | - | 可接受 | local_cli |

| 69 | ListPrivateNats | hcloud NAT ListNatGatewaySnatRules | 效果完全一致 | - | 可接受 | local_cli |

| 70 | ListPrivateNatsByTags | hcloud NAT ListPrivateNatsByTags | 效果完全一致 | - | 可接受 | local_cli |

| 71 | ListPrivateNatTags | hcloud NAT ListPrivateNatTags | 效果完全一致 | - | 可接受 | local_cli |

| 72 | ListPrivateSnats | hcloud NAT ListNatGatewaySnatRules | 效果完全一致 | - | 可接受 | local_cli |

| 73 | ListSpecs | hcloud NAT ListSpecs | 效果完全一致 | - | 可接受 | local_cli |

| 74 | ListTransitIps | hcloud NAT ListTransitIps | 效果完全一致 | - | 可接受 | local_cli |

| 75 | ListTransitIpsByTags | hcloud NAT ListTransitIpsByTags | 效果完全一致 | - | 可接受 | local_cli |

| 76 | ListTransitIpTags | hcloud NAT ListTransitIpTags | 效果完全一致 | - | 可接受 | local_cli |

| 77 | ListTransitSubnet | hcloud NAT ListTransitSubnet | 效果完全一致 | - | 可接受 | local_cli |

| 78 | ListTransitSubnetsByTags | hcloud NAT ListTransitSubnetsByTags | 效果完全一致 | - | 可接受 | local_cli |

| 79 | ListTransitSubnetTags | hcloud NAT ListTransitSubnetTags | 效果完全一致 | - | 可接受 | local_cli |

| 80 | ShowNatGateway | hcloud NAT ShowNatGateway | 效果完全一致 | - | 可接受 | local_cli |

| 81 | ShowNatGatewayDnatRule | hcloud NAT ShowNatGatewayDnatRule | 效果完全一致 | - | 可接受 | local_cli |

| 82 | ShowNatGatewaySnatRule | hcloud NAT ShowNatGatewaySnatRule | 效果完全一致 | - | 可接受 | local_cli |

| 83 | ShowNatGatewayTag | hcloud NAT ShowNatGatewayTag | 效果完全一致 | - | 可接受 | local_cli |

| 84 | ShowPrivateDnat | hcloud NAT ShowNatGatewayDnatRule | 效果完全一致 | - | 可接受 | local_cli |

| 85 | ShowPrivateNat | hcloud NAT ShowNatGateway | 效果完全一致 | - | 可接受 | local_cli |

| 86 | ShowPrivateNatTags | hcloud NAT ShowPrivateNatTags | 效果完全一致 | - | 可接受 | local_cli |

| 87 | ShowPrivateSnat | hcloud NAT ShowNatGatewaySnatRule | 效果完全一致 | - | 可接受 | local_cli |

| 88 | ShowTransitIp | hcloud NAT ShowTransitIp | 效果完全一致 | - | 可接受 | local_cli |

| 89 | ShowTransitIpTags | hcloud NAT ShowTransitIpTags | 效果完全一致 | - | 可接受 | local_cli |

| 90 | ShowTransitSubnet | hcloud NAT ShowTransitSubnet | 效果完全一致 | - | 可接受 | local_cli |

| 91 | ShowTransitSubnetTags | hcloud NAT ShowTransitSubnetTags | 效果完全一致 | - | 可接受 | local_cli |

| 92 | ListFlowLogs | hcloud VPC ListFlowLogs | 效果完全一致 | - | 可接受 | local_cli |

| 93 | ListPorts | hcloud VPC ListPorts/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 94 | ListPrivateips | hcloud VPC ListPrivateips | 效果完全一致 | - | 可接受 | local_cli |

| 95 | ListRouteTables | hcloud VPC ListRouteTables | 效果完全一致 | - | 可接受 | local_cli |

| 96 | ListSecurityGroups | hcloud VPC ListSecurityGroups/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 97 | ListSecurityGroupRules | hcloud VPC ListSecurityGroupRules/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 98 | ListSubnets | hcloud VPC ListSubnets | 效果完全一致 | - | 可接受 | local_cli |

| 99 | ListVpcs | hcloud VPC ListVpcs/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 100 | ListVpcPeerings | hcloud VPC ListVpcPeerings | 效果完全一致 | - | 可接受 | local_cli |

| 101 | ListVpcRoutes | hcloud VPC ListVpcRoutes | 效果完全一致 | - | 可接受 | local_cli |

| 102 | ShowFlowLog | hcloud VPC ShowFlowLog | 效果完全一致 | - | 可接受 | local_cli |

| 103 | ShowNetworkIpAvailabilities | hcloud VPC ShowNetworkIpAvailabilities | 效果完全一致 | - | 可接受 | local_cli |

| 104 | ShowPort | hcloud VPC ShowPort/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 105 | ShowPrivateip | hcloud VPC ShowPrivateip | 效果完全一致 | - | 可接受 | local_cli |

| 106 | ShowQuota | hcloud VPC ShowQuota/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 107 | ShowRouteTable | hcloud VPC ShowRouteTable | 效果完全一致 | - | 可接受 | local_cli |

| 108 | ShowSecurityGroup | hcloud VPC ShowSecurityGroup/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 109 | ShowSecurityGroupRule | hcloud VPC ShowSecurityGroupRule/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 110 | ShowSubnet | hcloud VPC ShowSubnet | 效果完全一致 | - | 可接受 | local_cli |

| 111 | ShowVpc | hcloud VPC ShowVpc/v2 | 效果完全一致 | - | 可接受 | local_cli |

| 112 | ShowVpcPeering | hcloud VPC ShowVpcPeering | 效果完全一致 | - | 可接受 | local_cli |

| 113 | ShowVpcRoute | hcloud VPC ShowVpcRoute | 效果完全一致 | - | 可接受 | local_cli |

| 114 | ListAvailabilityZones | hcloud Vpn ListAvailabilityZones | 效果完全一致 | - | 可接受 | local_cli |

| 115 | ListCgws | hcloud Vpn ListCgws | 效果完全一致 | - | 可接受 | local_cli |

| 116 | ListConnectionMonitors | hcloud Vpn ListConnectionMonitors | 效果完全一致 | - | 可接受 | local_cli |

| 117 | ListExtendedAvailabilityZones | hcloud Vpn ListExtendedAvailabilityZones | 效果完全一致 | - | 可接受 | local_cli |

| 118 | ListP2cVgws | hcloud Vpn ListP2cVgws | 效果完全一致 | - | 可接受 | local_cli |

| 119 | ListP2cVgwAvailabilityZones | hcloud Vpn ListP2cVgwAvailabilityZones | 效果完全一致 | - | 可接受 | local_cli |

| 120 | ListP2cVgwConnections | hcloud Vpn ListP2cVgwConnections | 效果完全一致 | - | 可接受 | local_cli |

| 121 | ListP2cVpnGatewayJobs | hcloud Vpn ListP2cVpnGatewayJobs | 效果完全一致 | - | 可接受 | local_cli |

| 122 | ListProjectTags | hcloud Vpn ListProjectTags | 效果完全一致 | - | 可接受 | local_cli |

| 123 | ListResourcesByTags | hcloud Vpn ListResourcesByTags | 效果完全一致 | - | 可接受 | local_cli |

| 124 | ListVgws | hcloud Vpn ListVgws | 效果完全一致 | - | 可接受 | local_cli |

| 125 | ListVpnAccessPolicies | hcloud Vpn ListVpnAccessPolicies | 效果完全一致 | - | 可接受 | local_cli |

| 126 | ListVpnConnections | hcloud Vpn ListVpnConnections | 效果完全一致 | - | 可接受 | local_cli |

| 127 | ListVpnGatewayJobs | hcloud Vpn ListVpnGatewayJobs | 效果完全一致 | - | 可接受 | local_cli |

| 128 | ListVpnServersByProject | hcloud Vpn ListVpnServersByProject | 效果完全一致 | - | 可接受 | local_cli |

| 129 | ListVpnServersByVgw | hcloud Vpn ListVpnServersByVgw | 效果完全一致 | - | 可接受 | local_cli |

| 130 | ListVpnUsers | hcloud Vpn ListVpnUsers | 效果完全一致 | - | 可接受 | local_cli |

| 131 | ListVpnUsersInGroup | hcloud Vpn ListVpnUsersInGroup | 效果完全一致 | - | 可接受 | local_cli |

| 132 | ListVpnUserGroups | hcloud Vpn ListVpnUserGroups | 效果完全一致 | - | 可接受 | local_cli |

| 133 | ShowCgw | hcloud Vpn ShowCgw | 效果完全一致 | - | 可接受 | local_cli |

| 134 | ShowClientCa | hcloud Vpn ShowClientCa | 效果完全一致 | - | 可接受 | local_cli |

| 135 | ShowConnectionMonitor | hcloud Vpn ShowConnectionMonitor | 效果完全一致 | - | 可接受 | local_cli |

| 136 | ShowP2cVgw | hcloud Vpn ShowP2cVgw | 效果完全一致 | - | 可接受 | local_cli |

| 137 | ShowQuotasInfo | hcloud Vpn ShowQuotasInfo | 效果完全一致 | - | 可接受 | local_cli |

| 138 | ShowResourceTags | hcloud Vpn ShowResourceTags | 效果完全一致 | - | 可接受 | local_cli |

| 139 | ShowVgw | hcloud Vpn ShowVgw | 效果完全一致 | - | 可接受 | local_cli |

| 140 | ShowVpnAccessPolicy | hcloud Vpn ShowVpnAccessPolicy | 效果完全一致 | - | 可接受 | local_cli |

| 141 | ShowVpnConnection | hcloud Vpn ShowVpnConnection | 效果完全一致 | - | 可接受 | local_cli |

| 142 | ShowVpnConnectionsLogConfig | hcloud Vpn ShowVpnConnectionsLogConfig | 效果完全一致 | - | 可接受 | local_cli |

| 143 | ShowVpnConnectionLog | hcloud Vpn ShowVpnConnectionLog | 效果完全一致 | - | 可接受 | local_cli |

| 144 | ShowVpnGatewayCertificate | hcloud Vpn ShowVpnGatewayCertificate | 效果完全一致 | - | 可接受 | local_cli |

| 145 | ShowVpnGatewayRoutingTable | hcloud Vpn ShowVpnGatewayRoutingTable | 效果完全一致 | - | 可接受 | local_cli |

| 146 | ShowVpnUser | hcloud Vpn ShowVpnUser | 效果完全一致 | - | 可接受 | local_cli |

| 147 | ShowVpnUserGroup | hcloud Vpn ShowVpnUserGroup | 效果完全一致 | - | 可接受 | local_cli |





## 第三阶段：全部改用KooCLI后的业务效果等价性结论


| 项目 | 内容 |
| --- | --- |
| 替换结论 | 可以完全替换 |
| 结论原因 | 所有接口均存在对应的KooCLI命令。 |

### 关键阻塞点


无关键阻塞点。



## 第四阶段：KooCLI本地验证结论

基于规则分析，所有必须接口均存在效果完全一致的KooCLI命令，结论为可以完全替换。所有接口均存在对应的KooCLI命令。建议在实际替换前，通过本地KooCLI命令行工具对关键接口进行端到端验证，确认返回结果格式和业务流程无差异。

## 最终结论


该Skill是否能够全部改用KooCLI并达到与Huawei Cloud SDK实现一致的业务效果：**可以完全替换**。

原因：所有接口均存在对应的KooCLI命令。


