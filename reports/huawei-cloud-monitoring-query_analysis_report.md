# Skill实现原理分析报告 - huawei-cloud-monitoring-query

## 0. Skill基本信息

| 属性 | 值 |
| --- | --- |
| Skill名称 | huawei-cloud-monitoring-query |
| 实现方式 | SDK |
| 业务目标 | Queries Huawei Cloud monitoring and enterprise project resources (CES/EPS). Covers alarm rules, alarm histories, alarm templates, dashboards, notification masks, resource groups, one-click alarms, and enterprise projects (list/detail/quotas/bound resources/migration records). No write operations.... |
| 分析状态 | completed |
| 分析时间 | 2026-06-10T09:03:08.749856+00:00 |

## Skill依赖工具

| 依赖项 | 版本/说明 | 功能描述 | 是否必须 |
| --- | --- | --- | --- |

| Python | 3.14 | Skill实现语言及运行时环境 | 必须 |

| SDK: huaweicloudsdkces | >=3.1.0 | 云监控(CES)服务SDK，用于监控指标和告警 | 必须 |

| SDK: huaweicloudsdkcore | >=3.1.0 | 华为云SDK核心库，提供认证、HTTP请求等基础能力 | 必须 |

| SDK: huaweicloudsdkeps | >=3.1.0 | eps服务SDK，用于调用华为云eps相关API | 必须 |

| SDK: huaweicloudsdkiam | >=3.1.0 | 身份与访问管理(IAM)服务SDK，用于用户和权限管理 | 必须 |

| KooCLI (hcloud) | 已确认 | 华为云命令行工具，用于通过CLI调用云服务API | 必须 |

| config | 已确认 | 第三方库: config | 必须 |

| platform | 已确认 | 第三方库: platform | 必须 |

| urllib3 | 已确认 | 第三方库: urllib3 | 必须 |


## 第一阶段：目标Skill使用的华为云Open API接口

### 阶段结论

共识别15个Open API接口。
| 序号 | 服务 | Open API接口 | HTTP方法 | API路径 | 来源SDK调用 | 实际使用参数 | 业务作用 | 是否必须 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

| 1 | Iam | KeystoneListProjects | GET | /v3/projects | IamClient.keystone_list_projects (scripts\ensure_env.py:113) | - | 通过Iam服务执行list操作，作用对象为projects | mandatory |

| 2 | Ces | ListAlarmHistories | GET | /V1.0/{project_id}/alarm-histories | CesClient.list_alarm_histories (scripts\ces\list_alarm_histories.py:85) | - | 通过Ces服务执行list操作，作用对象为alarm-histories | mandatory |

| 3 | Ces | ListAlarmTemplates | GET | /V1.0/{project_id}/alarm-template | CesClient.list_alarm_templates (scripts\ces\list_alarm_templates.py:53) | - | 通过Ces服务执行list操作，作用对象为alarm-template | mandatory |

| 4 | Ces | ShowResourceGroup | GET | /V1.0/{project_id}/resource-groups/{group_id} | CesClient.show_resource_group (scripts\ces\show_resource_group.py:34) | - | 通过Ces服务执行show操作，作用对象为resource-groups | mandatory |

| 5 | Eps | ListApiVersions | GET | / | EpsClient.list_api_versions (scripts\eps\list_api_versions.py:79) | - | 通过Eps服务执行list操作 | mandatory |

| 6 | Eps | ListEnterpriseProject | GET | /v1.0/enterprise-projects | EpsClient.list_enterprise_project (scripts\eps\list_enterprise_projects.py:107) | - | 通过Eps服务执行list操作，作用对象为enterprise-projects | mandatory |

| 7 | Eps | ListMigrationRecord | GET | /v1.0/enterprise-projects/migrate-record/list | EpsClient.list_migration_record (scripts\eps\list_migration_records.py:99) | - | 通过Eps服务执行list操作，作用对象为list | mandatory |

| 8 | Eps | ListProviders | GET | /v1.0/enterprise-projects/providers | EpsClient.list_providers (scripts\eps\list_providers.py:91) | - | 通过Eps服务执行list操作，作用对象为providers | mandatory |

| 9 | Eps | ListResourceMapping | GET | /v1.0/enterprise-projects/resources-mapping | EpsClient.list_resource_mapping (scripts\eps\list_resource_mapping.py:76) | - | 通过Eps服务执行list操作，作用对象为resources-mapping | mandatory |

| 10 | Eps | ShowApiVersion | GET | /{api_version} | EpsClient.show_api_version (scripts\eps\show_api_version.py:38) | - | 通过Eps服务执行show操作 | mandatory |

| 11 | Eps | ShowAssociatedResources | GET | /v1.0/associated-resources/{resource_id} | EpsClient.show_associated_resources (scripts\eps\show_associated_resources.py:44) | - | 通过Eps服务执行show操作，作用对象为associated-resources | mandatory |

| 12 | Eps | ShowEnterpriseProject | GET | /v1.0/enterprise-projects/{enterprise_project_id} | EpsClient.show_enterprise_project (scripts\eps\show_enterprise_project.py:38) | - | 通过Eps服务执行show操作，作用对象为enterprise-projects | mandatory |

| 13 | Eps | ShowEnterpriseProjectQuota | GET | /v1.0/enterprise-projects/quotas | EpsClient.show_enterprise_project_quota (scripts\eps\show_enterprise_project_quota.py:36) | - | 通过Eps服务执行show操作，作用对象为quotas | mandatory |

| 14 | Eps | ShowEpConfigs | GET | /v1/enterprise-projects/configs | EpsClient.show_ep_configs (scripts\eps\show_ep_configs.py:36) | - | 通过Eps服务执行show操作，作用对象为configs | mandatory |

| 15 | Eps | ShowResourceBindEnterpriseProject | POST | /v1.0/enterprise-projects/{enterprise_project_id}/resources/filter | EpsClient.show_resource_bind_enterprise_project (scripts\eps\show_resource_bind_enterprise_project.py:94) | - | 通过Eps服务执行show操作，作用对象为filter | mandatory |



## 第二阶段：KooCLI命令一一对应关系与效果完全一致判定

### 阶段结论

共分析15个Open API接口，其中15个存在效果完全一致的KooCLI命令。


| 序号 | Open API接口 | 对应KooCLI命令 | 判定状态 | 差异说明 | 是否可接受 | 信息来源 |
| --- | --- | --- | --- | --- | --- | --- |

| 1 | KeystoneListProjects | hcloud IAM KeystoneListProjects | 效果完全一致 | - | 可接受 | local_cli |

| 2 | ListAlarmHistories | hcloud Ces ListAlarmHistories/v1 | 效果完全一致 | - | 可接受 | local_cli |

| 3 | ListAlarmTemplates | hcloud Ces ListAlarmTemplates/v1 | 效果完全一致 | - | 可接受 | local_cli |

| 4 | ShowResourceGroup | hcloud Ces ShowResourceGroup/v1 | 效果完全一致 | - | 可接受 | local_cli |

| 5 | ListApiVersions | hcloud EPS ListApiVersions | 效果完全一致 | - | 可接受 | local_cli |

| 6 | ListEnterpriseProject | hcloud EPS ListEnterpriseProject | 效果完全一致 | - | 可接受 | local_cli |

| 7 | ListMigrationRecord | hcloud EPS ListMigrationRecord | 效果完全一致 | - | 可接受 | local_cli |

| 8 | ListProviders | hcloud EPS ListProviders | 效果完全一致 | - | 可接受 | local_cli |

| 9 | ListResourceMapping | hcloud EPS ListResourceMapping | 效果完全一致 | - | 可接受 | local_cli |

| 10 | ShowApiVersion | hcloud EPS ShowApiVersion | 效果完全一致 | - | 可接受 | local_cli |

| 11 | ShowAssociatedResources | hcloud EPS ShowAssociatedResources | 效果完全一致 | - | 可接受 | local_cli |

| 12 | ShowEnterpriseProject | hcloud EPS ShowEnterpriseProject | 效果完全一致 | - | 可接受 | local_cli |

| 13 | ShowEnterpriseProjectQuota | hcloud EPS ShowEnterpriseProjectQuota | 效果完全一致 | - | 可接受 | local_cli |

| 14 | ShowEpConfigs | hcloud EPS ShowEpConfigs | 效果完全一致 | - | 可接受 | local_cli |

| 15 | ShowResourceBindEnterpriseProject | hcloud EPS ShowResourceBindEnterpriseProject | 效果完全一致 | - | 可接受 | local_cli |





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


