# Skill实现原理分析报告 - huawei-cloud-business-support-query

## 0. Skill基本信息

| 属性 | 值 |
| --- | --- |
| Skill名称 | huawei-cloud-business-support-query |
| 实现方式 | SDK |
| 业务目标 | Queries Huawei Cloud billing and pricing. Covers balances, bills, coupons, cash coupons, stored-value cards, orders, refunds, costs, free resources, resource usage, enterprise accounts, and on-demand/period/ELB/NAT/DCS pricing. No write operations. Use this skill when the user needs to check fees... |
| 分析状态 | completed |
| 分析时间 | 2026-06-10T09:03:54.814476+00:00 |

## Skill依赖工具

| 依赖项 | 版本/说明 | 功能描述 | 是否必须 |
| --- | --- | --- | --- |

| Python | 3.14 | Skill实现语言及运行时环境 | 必须 |

| SDK: huaweicloudsdkbms | >=3.1.0 | 裸金属服务器(BMS)服务SDK | 必须 |

| SDK: huaweicloudsdkbss | >=3.1.0 | 运营能力(BSS)服务SDK | 必须 |

| SDK: huaweicloudsdkcore | >=3.1.0 | 华为云SDK核心库，提供认证、HTTP请求等基础能力 | 必须 |

| SDK: huaweicloudsdkecs | >=3.1.0 | 云服务器(ECS)服务SDK，用于创建、查询和管理云服务器 | 必须 |

| SDK: huaweicloudsdkelb | >=3.1.0 | 弹性负载均衡(ELB)服务SDK，用于管理负载均衡器 | 必须 |

| SDK: huaweicloudsdkiam | >=3.1.0 | 身份与访问管理(IAM)服务SDK，用于用户和权限管理 | 必须 |

| SDK: huaweicloudsdknat | >=3.1.0 | NAT网关服务SDK | 必须 |

| SDK: huaweicloudsdksfsturbo | >=3.1.0 | sfsturbo服务SDK，用于调用华为云sfsturbo相关API | 必须 |

| KooCLI (hcloud) | 已确认 | 华为云命令行工具，用于通过CLI调用云服务API | 必须 |

| config | 已确认 | 第三方库: config | 必须 |

| decimal | 已确认 | 第三方库: decimal | 必须 |

| platform | 已确认 | 第三方库: platform | 必须 |

| urllib3 | 已确认 | 第三方库: urllib3 | 必须 |


## 第一阶段：目标Skill使用的华为云Open API接口

### 阶段结论

共识别43个Open API接口。
| 序号 | 服务 | Open API接口 | HTTP方法 | API路径 | 来源SDK调用 | 实际使用参数 | 业务作用 | 是否必须 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

| 1 | Iam | KeystoneListProjects | GET | /v3/projects | IamClient.keystone_list_projects (scripts\ensure_env.py:113) | - | 通过Iam服务执行list操作，作用对象为projects | mandatory |

| 2 | Bms | ListBaremetalFlavorDetailExtends | GET | /v1/{project_id}/baremetalservers/flavors | BmsClient.list_baremetal_flavor_detail_extends (scripts\bms\list_baremetal_flavor_detail_extends.py:104) | - | 通过Bms服务执行list操作，作用对象为flavors | mandatory |

| 3 | Nat | ListNatGatewaySpecs | GET | /v2/{project_id}/nat_gateway_specs | NatClient.list_nat_gateway_specs (scripts\bss\inquiry_nat.py:77) | - | 通过Nat服务执行list操作，作用对象为nat_gateway_specs | mandatory |

| 4 | Nat | ListSpecs | GET | /v3/{project_id}/private-nat/specs | NatClient.list_specs (scripts\bss\inquiry_nat.py:97) | - | 通过Nat服务执行list操作，作用对象为specs | mandatory |

| 5 | Bss | ListCities | GET | /v2/systems/configs/cities | BssClient.list_cities (scripts\bss\list_cities.py:40) | - | 通过Bss服务执行list操作，作用对象为cities | mandatory |

| 6 | Bss | ListConversions | GET | /v2/bases/conversions | BssClient.list_conversions (scripts\bss\list_conversions.py:36) | - | 通过Bss服务执行list操作，作用对象为conversions | mandatory |

| 7 | Bss | ListCosts | POST | /v4/costs/cost-analysed-bills/query | BssClient.list_costs (scripts\bss\list_costs.py:86) | - | 通过Bss服务执行list操作，作用对象为query | mandatory |

| 8 | Bss | ListCounties | GET | /v2/systems/configs/counties | BssClient.list_counties (scripts\bss\list_counties.py:40) | - | 通过Bss服务执行list操作，作用对象为counties | mandatory |

| 9 | Bss | ListCustomerselfResourceRecords | GET | /v2/bills/customer-bills/res-fee-records | BssClient.list_customerself_resource_records (scripts\bss\list_customerself_resource_records.py:84) | - | 通过Bss服务执行list操作，作用对象为res-fee-records | mandatory |

| 10 | Bss | ListCustomerselfResourceRecordDetails | POST | /v2/bills/customer-bills/res-records/query | BssClient.list_customerself_resource_record_details (scripts\bss\list_customerself_resource_record_details.py:97) | - | 通过Bss服务执行list操作，作用对象为query | mandatory |

| 11 | Bss | ListCustomerAccountChangeRecords | GET | /v2/accounts/customer-accounts/account-change-records | BssClient.list_customer_account_change_records (scripts\bss\list_customer_account_change_records.py:59) | - | 通过Bss服务执行list操作，作用对象为account-change-records | mandatory |

| 12 | Bss | ListCustomerBillsFeeRecords | GET | /v2/bills/customer-bills/fee-records | BssClient.list_customer_bills_fee_records (scripts\bss\list_customer_bills_fee_records.py:87) | - | 通过Bss服务执行list操作，作用对象为fee-records | mandatory |

| 13 | Bss | ListCustomerBillsMonthlyBreakDown | GET | /v2/costs/cost-analysed-bills/monthly-breakdown | BssClient.list_customer_bills_monthly_break_down (scripts\bss\list_customer_bills_monthly_break_down.py:72) | - | 通过Bss服务执行list操作，作用对象为monthly-breakdown | mandatory |

| 14 | Bss | ListCustomerCouponChangeRecords | GET | /v2/promotions/benefits/account-change-records | BssClient.list_customer_coupon_change_records (scripts\bss\list_customer_coupon_change_records.py:56) | - | 通过Bss服务执行list操作，作用对象为account-change-records | mandatory |

| 15 | Bss | ListCustomerOrders | GET | /v2/orders/customer-orders | BssClient.list_customer_orders (scripts\bss\list_customer_orders.py:74) | - | 通过Bss服务执行list操作，作用对象为customer-orders | mandatory |

| 16 | Bss | ListEnterpriseMultiAccount | GET | /v2/enterprises/multi-accounts/retrieve-amount | BssClient.list_enterprise_multi_account (scripts\bss\list_enterprise_multi_account.py:42) | - | 通过Bss服务执行list操作，作用对象为retrieve-amount | mandatory |

| 17 | Bss | ListEnterpriseOrganizations | GET | /v2/enterprises/multi-accounts/enterprise-organizations | BssClient.list_enterprise_organizations (scripts\bss\list_enterprise_organizations.py:38) | - | 通过Bss服务执行list操作，作用对象为enterprise-organizations | mandatory |

| 18 | Bss | ListEnterpriseSubCustomers | GET | /v2/enterprises/multi-accounts/sub-customers | BssClient.list_enterprise_sub_customers (scripts\bss\list_enterprise_sub_customers.py:50) | - | 通过Bss服务执行list操作，作用对象为sub-customers | mandatory |

| 19 | Bss | ListFreeResourcesUsageRecords | GET | /v2/bills/customer-bills/free-resources-usage-records | BssClient.list_free_resources_usage_records (scripts\bss\list_free_resources_usage_records.py:51) | - | 通过Bss服务执行list操作，作用对象为free-resources-usage-records | mandatory |

| 20 | Bss | ListFreeResourceInfos | POST | /v3/payments/free-resources/query | BssClient.list_free_resource_infos (scripts\bss\list_free_resource_infos.py:64) | - | 通过Bss服务执行list操作，作用对象为query | mandatory |

| 21 | Bss | ListFreeResourceUsages | POST | /v2/payments/free-resources/usages/details/query | BssClient.list_free_resource_usages (scripts\bss\list_free_resource_usages.py:39) | - | 通过Bss服务执行list操作，作用对象为query | mandatory |

| 22 | Bss | ListMeasureUnits | GET | /v2/bases/measurements | BssClient.list_measure_units (scripts\bss\list_measure_units.py:34) | - | 通过Bss服务执行list操作，作用对象为measurements | mandatory |

| 23 | Bss | ListMultiAccountRetrieveCoupons | GET | /v2/enterprises/multi-accounts/retrieve-coupons | BssClient.list_multi_account_retrieve_coupons (scripts\bss\list_multi_account_retrieve_coupons.py:40) | - | 通过Bss服务执行list操作，作用对象为retrieve-coupons | mandatory |

| 24 | Bss | ListMultiAccountTransferCoupons | GET | /v2/enterprises/multi-accounts/transfer-coupons | BssClient.list_multi_account_transfer_coupons (scripts\bss\list_multi_account_transfer_coupons.py:38) | - | 通过Bss服务执行list操作，作用对象为transfer-coupons | mandatory |

| 25 | Bss | ListOnDemandResourceRatings | POST | /v2/bills/ratings/on-demand-resources | BssClient.list_on_demand_resource_ratings (scripts\bss\list_on_demand_resource_ratings.py:243) | - | 通过Bss服务执行list操作，作用对象为on-demand-resources | mandatory |

| 26 | Bss | ListPayPerUseCustomerResources | POST | /v2/orders/suscriptions/resources/query | BssClient.list_pay_per_use_customer_resources (scripts\bss\list_pay_per_use_customer_resources.py:65) | - | 通过Bss服务执行list操作，作用对象为query | mandatory |

| 27 | Bss | ListProvinces | GET | /v2/systems/configs/provinces | BssClient.list_provinces (scripts\bss\list_provinces.py:41) | - | 通过Bss服务执行list操作，作用对象为provinces | mandatory |

| 28 | Bss | ListRateOnPeriodDetail | POST | /v2/bills/ratings/period-resources/subscribe-rate | BssClient.list_rate_on_period_detail (scripts\bss\list_rate_on_period_detail.py:238) | - | 通过Bss服务执行list操作，作用对象为subscribe-rate | mandatory |

| 29 | Bss | ListRenewRateOnPeriod | POST | /v2/bills/ratings/period-resources/renew-rate | BssClient.list_renew_rate_on_period (scripts\bss\list_renew_rate_on_period.py:44) | - | 通过Bss服务执行list操作，作用对象为renew-rate | mandatory |

| 30 | Bss | ListResourceTypes | GET | /v2/products/resource-types | BssClient.list_resource_types (scripts\bss\list_resource_types.py:146) | - | 通过Bss服务执行list操作，作用对象为resource-types | mandatory |

| 31 | Bss | ListResourceUsage | GET | /v2/bills/customer-bills/resources/usage/details | BssClient.list_resource_usage (scripts\bss\list_resource_usage.py:55) | - | 通过Bss服务执行list操作，作用对象为details | mandatory |

| 32 | Bss | ListResourceUsageSummary | GET | /v2/bills/customer-bills/resources/usage/summary | BssClient.list_resource_usage_summary (scripts\bss\list_resource_usage_summary.py:52) | - | 通过Bss服务执行list操作，作用对象为summary | mandatory |

| 33 | Bss | ListServiceResources | GET | /v2/products/service-resources | BssClient.list_service_resources (scripts\bss\list_service_resources.py:43) | - | 通过Bss服务执行list操作，作用对象为service-resources | mandatory |

| 34 | Bss | ListServiceTypes | GET | /v2/products/service-types | BssClient.list_service_types (scripts\bss\list_service_types.py:48) | - | 通过Bss服务执行list操作，作用对象为service-types | mandatory |

| 35 | Bss | ListStoredValueCards | GET | /v2/promotions/benefits/stored-value-cards | BssClient.list_stored_value_cards (scripts\bss\list_stored_value_cards.py:46) | - | 通过Bss服务执行list操作，作用对象为stored-value-cards | mandatory |

| 36 | Bss | ListUsageTypes | GET | /v2/products/usage-types | BssClient.list_usage_types (scripts\bss\list_usage_types.py:44) | - | 通过Bss服务执行list操作，作用对象为usage-types | mandatory |

| 37 | Bss | ShowCustomerAccountBalances | GET | /v2/accounts/customer-accounts/balances | BssClient.show_customer_account_balances (scripts\bss\show_customer_account_balances.py:31) | - | 通过Bss服务执行show操作，作用对象为balances | mandatory |

| 38 | Bss | ShowCustomerMonthlySum | GET | /v2/bills/customer-bills/monthly-sum | BssClient.show_customer_monthly_sum (scripts\bss\show_customer_monthly_sum.py:52) | - | 通过Bss服务执行show操作，作用对象为monthly-sum | mandatory |

| 39 | Bss | ShowCustomerOrderDetails | GET | /v2/orders/customer-orders/details/{order_id} | BssClient.show_customer_order_details (scripts\bss\show_customer_order_details.py:43) | - | 通过Bss服务执行show操作，作用对象为details | mandatory |

| 40 | Bss | ShowMultiAccountTransferAmount | GET | /v2/enterprises/multi-accounts/transfer-amount | BssClient.show_multi_account_transfer_amount (scripts\bss\show_multi_account_transfer_amount.py:38) | - | 通过Bss服务执行show操作，作用对象为transfer-amount | mandatory |

| 41 | Bss | ShowRefundOrderDetails | GET | /v2/orders/customer-orders/refund-orders | BssClient.show_refund_order_details (scripts\bss\show_refund_order_details.py:40) | - | 通过Bss服务执行show操作，作用对象为refund-orders | mandatory |

| 42 | Ecs | ListFlavors | GET | /v1/{project_id}/cloudservers/flavors | EcsClient.list_flavors (scripts\ecs\list_flavors.py:189) | - | 通过Ecs服务执行list操作，作用对象为flavors | mandatory |

| 43 | SFSTurbo | ListShareTypes | GET | /v1/{project_id}/sfs-turbo/share-types | SFSTurboClient.list_share_types (scripts\sfs\list_share_types.py:39) | - | 通过SFSTurbo服务执行list操作，作用对象为share-types | mandatory |



## 第二阶段：KooCLI命令一一对应关系与效果完全一致判定

### 阶段结论

共分析43个Open API接口，其中43个存在效果完全一致的KooCLI命令。


| 序号 | Open API接口 | 对应KooCLI命令 | 判定状态 | 差异说明 | 是否可接受 | 信息来源 |
| --- | --- | --- | --- | --- | --- | --- |

| 1 | KeystoneListProjects | hcloud IAM KeystoneListProjects | 效果完全一致 | - | 可接受 | local_cli |

| 2 | ListBaremetalFlavorDetailExtends | hcloud BMS ListBaremetalFlavorDetailExtends | 效果完全一致 | - | 可接受 | local_cli |

| 3 | ListNatGatewaySpecs | hcloud NAT ListNatGatewaySpecs | 效果完全一致 | - | 可接受 | local_cli |

| 4 | ListSpecs | hcloud NAT ListSpecs | 效果完全一致 | - | 可接受 | local_cli |

| 5 | ListCities | hcloud BSS ListCities | 效果完全一致 | - | 可接受 | local_cli |

| 6 | ListConversions | hcloud BSS ListConversions | 效果完全一致 | - | 可接受 | local_cli |

| 7 | ListCosts | hcloud BSS ListCosts | 效果完全一致 | - | 可接受 | local_cli |

| 8 | ListCounties | hcloud BSS ListCounties | 效果完全一致 | - | 可接受 | local_cli |

| 9 | ListCustomerselfResourceRecords | hcloud BSS ListCustomerselfResourceRecords | 效果完全一致 | - | 可接受 | local_cli |

| 10 | ListCustomerselfResourceRecordDetails | hcloud BSS ListCustomerselfResourceRecordDetails | 效果完全一致 | - | 可接受 | local_cli |

| 11 | ListCustomerAccountChangeRecords | hcloud BSS ListCustomerAccountChangeRecords | 效果完全一致 | - | 可接受 | local_cli |

| 12 | ListCustomerBillsFeeRecords | hcloud BSS ListCustomerBillsFeeRecords | 效果完全一致 | - | 可接受 | local_cli |

| 13 | ListCustomerBillsMonthlyBreakDown | hcloud BSS ListCustomerBillsMonthlyBreakDown | 效果完全一致 | - | 可接受 | local_cli |

| 14 | ListCustomerCouponChangeRecords | hcloud BSS ListCustomerAccountChangeRecords | 效果完全一致 | - | 可接受 | local_cli |

| 15 | ListCustomerOrders | hcloud BSS ListCustomerOrders | 效果完全一致 | - | 可接受 | local_cli |

| 16 | ListEnterpriseMultiAccount | hcloud BSS ListEnterpriseMultiAccount | 效果完全一致 | - | 可接受 | local_cli |

| 17 | ListEnterpriseOrganizations | hcloud BSS ListEnterpriseOrganizations | 效果完全一致 | - | 可接受 | local_cli |

| 18 | ListEnterpriseSubCustomers | hcloud BSS ListEnterpriseSubCustomers | 效果完全一致 | - | 可接受 | local_cli |

| 19 | ListFreeResourcesUsageRecords | hcloud BSS ListFreeResourcesUsageRecords | 效果完全一致 | - | 可接受 | local_cli |

| 20 | ListFreeResourceInfos | hcloud BSS ListFreeResourceInfos | 效果完全一致 | - | 可接受 | local_cli |

| 21 | ListFreeResourceUsages | hcloud BSS ListFreeResourceUsages | 效果完全一致 | - | 可接受 | local_cli |

| 22 | ListMeasureUnits | hcloud BSS ListMeasureUnits | 效果完全一致 | - | 可接受 | local_cli |

| 23 | ListMultiAccountRetrieveCoupons | hcloud BSS ListMultiAccountRetrieveCoupons | 效果完全一致 | - | 可接受 | local_cli |

| 24 | ListMultiAccountTransferCoupons | hcloud BSS ListMultiAccountTransferCoupons | 效果完全一致 | - | 可接受 | local_cli |

| 25 | ListOnDemandResourceRatings | hcloud BSS ListCustomerOnDemandResources | 效果完全一致 | - | 可接受 | local_cli |

| 26 | ListPayPerUseCustomerResources | hcloud BSS ListPayPerUseCustomerResources | 效果完全一致 | - | 可接受 | local_cli |

| 27 | ListProvinces | hcloud BSS ListProvinces | 效果完全一致 | - | 可接受 | local_cli |

| 28 | ListRateOnPeriodDetail | hcloud BSS ListRateOnPeriodDetail | 效果完全一致 | - | 可接受 | local_cli |

| 29 | ListRenewRateOnPeriod | hcloud BSS ListRenewRateOnPeriod | 效果完全一致 | - | 可接受 | local_cli |

| 30 | ListResourceTypes | hcloud BSS ListResourceTypes | 效果完全一致 | - | 可接受 | local_cli |

| 31 | ListResourceUsage | hcloud BSS ListCustomerselfResourceRecordDetails | 效果完全一致 | - | 可接受 | local_cli |

| 32 | ListResourceUsageSummary | hcloud BSS ListResourceUsageSummary | 效果完全一致 | - | 可接受 | local_cli |

| 33 | ListServiceResources | hcloud BSS ListServiceResources | 效果完全一致 | - | 可接受 | local_cli |

| 34 | ListServiceTypes | hcloud BSS ListServiceTypes | 效果完全一致 | - | 可接受 | local_cli |

| 35 | ListStoredValueCards | hcloud BSS ListStoredValueCards | 效果完全一致 | - | 可接受 | local_cli |

| 36 | ListUsageTypes | hcloud BSS ListUsageTypes | 效果完全一致 | - | 可接受 | local_cli |

| 37 | ShowCustomerAccountBalances | hcloud BSS ShowCustomerAccountBalances | 效果完全一致 | - | 可接受 | local_cli |

| 38 | ShowCustomerMonthlySum | hcloud BSS ShowCustomerMonthlySum | 效果完全一致 | - | 可接受 | local_cli |

| 39 | ShowCustomerOrderDetails | hcloud BSS ShowCustomerOrderDetails | 效果完全一致 | - | 可接受 | local_cli |

| 40 | ShowMultiAccountTransferAmount | hcloud BSS ShowMultiAccountTransferAmount | 效果完全一致 | - | 可接受 | local_cli |

| 41 | ShowRefundOrderDetails | hcloud BSS ShowRefundOrderDetails | 效果完全一致 | - | 可接受 | local_cli |

| 42 | ListFlavors | hcloud Ecs ListFlavors | 效果完全一致 | - | 可接受 | local_cli |

| 43 | ListShareTypes | hcloud SFSTurbo ListShareTypes | 效果完全一致 | - | 可接受 | local_cli |





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


