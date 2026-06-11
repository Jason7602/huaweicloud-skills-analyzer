# Skill实现原理分析报告 - huawei-cloud-computing-query

## 0. Skill基本信息

| 属性 | 值 |
| --- | --- |
| Skill名称 | huawei-cloud-computing-query |
| 实现方式 | SDK |
| 业务目标 | Queries Huawei Cloud computing resources (ECS/BMS/IMS/AS), Covers ECS instances, flavors, keypairs, quotas, server groups, block devices, NICs, VNC console, BMS bare metal servers/flavors/quotas, IMS images/OS versions/members/quotas, and AS scaling groups/configs/policies/activity logs/lifecycle... |
| 分析状态 | completed |
| 分析时间 | 2026-06-11T01:45:51.280580+00:00 |

## Skill依赖工具

| 依赖项 | 版本/说明 | 功能描述 | 是否必须 |
| --- | --- | --- | --- |
| Python | 3.14 | Skill实现语言及运行时环境 | 必须 |
| SDK: huaweicloudsdkas | >=3.1.0 | 弹性伸缩(AS)服务SDK | 必须 |
| SDK: huaweicloudsdkbms | >=3.1.0 | 裸金属服务器(BMS)服务SDK | 必须 |
| SDK: huaweicloudsdkcore | >=3.1.0 | 华为云SDK核心库，提供认证、HTTP请求等基础能力 | 必须 |
| SDK: huaweicloudsdkecs | >=3.1.0 | 云服务器(ECS)服务SDK，用于创建、查询和管理云服务器 | 必须 |
| SDK: huaweicloudsdkiam | >=3.1.0 | 身份与访问管理(IAM)服务SDK，用于用户和权限管理 | 必须 |
| SDK: huaweicloudsdkims | >=3.1.0 | ims服务SDK，用于调用华为云ims相关API | 必须 |
| SDK: huaweicloudsdkvpc | 已确认 | 虚拟私有云(VPC)服务SDK，用于管理网络和子网 | 必须 |
| KooCLI (hcloud) | 已确认 | 华为云命令行工具，用于通过CLI调用云服务API | 必须 |
| _common | 已确认 | 第三方库: _common | 必须 |
| config | 已确认 | 第三方库: config | 必须 |
| platform | 已确认 | 第三方库: platform | 必须 |
| urllib3 | 已确认 | 第三方库: urllib3 | 必须 |

## 第一阶段：目标Skill使用的华为云Open API接口

### 阶段结论

共识别95个Open API接口。

| 序号 | 服务 | Open API接口 | HTTP方法 | API路径 | 来源SDK调用 | 实际使用参数 | 业务作用 | 是否必须 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Iam | KeystoneListProjects | GET | /v3/projects | IamClient.keystone_list_projects (scripts\ensure_env.py:113) | - | 通过Iam服务执行list操作，作用对象为projects | mandatory |
| 2 | As | ListAllScalingV2Policies | GET | /autoscaling-api/v2/{project_id}/scaling_policy | AsClient.list_all_scaling_v2_policies (scripts\as\list_all_scaling_v2_policies.py:114) | - | 通过As服务执行list操作，作用对象为scaling_policy | mandatory |
| 3 | As | ListApiVersions | GET | / | AsClient.list_api_versions (scripts\as\list_api_versions.py:42) | - | 通过As服务执行list操作 | mandatory |
| 4 | As | ListGroupScheduledTasks | GET | /autoscaling-api/v1/{project_id}/scaling-groups/{scaling_group_id}/scheduled-tasks | AsClient.list_group_scheduled_tasks (scripts\as\list_group_scheduled_tasks.py:79) | - | 通过As服务执行list操作，作用对象为scheduled-tasks | mandatory |
| 5 | As | ListHookInstances | GET | /autoscaling-api/v1/{project_id}/scaling_instance_hook/{scaling_group_id}/list | AsClient.list_hook_instances (scripts\as\list_hook_instances.py:51) | - | 通过As服务执行list操作，作用对象为list | mandatory |
| 6 | As | ListLifeCycleHooks | GET | /autoscaling-api/v1/{project_id}/scaling_lifecycle_hook/{scaling_group_id}/list | AsClient.list_life_cycle_hooks (scripts\as\list_life_cycle_hooks.py:46) | - | 通过As服务执行list操作，作用对象为list | mandatory |
| 7 | As | ListResourceInstances | POST | /autoscaling-api/v1/{project_id}/{resource_type}/resource_instances/action | AsClient.list_resource_instances (scripts\as\list_resource_instances.py:47) | - | 通过As服务执行list操作，作用对象为action | mandatory |
| 8 | As | ListScalingActivityLogs | GET | /autoscaling-api/v1/{project_id}/scaling_activity_log/{scaling_group_id} | AsClient.list_scaling_activity_logs (scripts\as\list_scaling_activity_logs.py:85) | - | 通过As服务执行list操作，作用对象为scaling_activity_log | mandatory |
| 9 | As | ListScalingActivityV2Logs | GET | /autoscaling-api/v2/{project_id}/scaling_activity_log/{scaling_group_id} | AsClient.list_scaling_activity_v2_logs (scripts\as\list_scaling_activity_v2_logs.py:98) | - | 通过As服务执行list操作，作用对象为scaling_activity_log | mandatory |
| 10 | As | ListScalingConfigs | GET | /autoscaling-api/v1/{project_id}/scaling_configuration | AsClient.list_scaling_configs (scripts\as\list_scaling_configs.py:82) | - | 通过As服务执行list操作，作用对象为scaling_configuration | mandatory |
| 11 | As | ListScalingGroups | GET | /autoscaling-api/v1/{project_id}/scaling_group | AsClient.list_scaling_groups (scripts\as\list_scaling_groups.py:93) | - | 通过As服务执行list操作，作用对象为scaling_group | mandatory |
| 12 | As | ListScalingInstances | GET | /autoscaling-api/v1/{project_id}/scaling_group_instance/{scaling_group_id}/list | AsClient.list_scaling_instances (scripts\as\list_scaling_instances.py:92) | - | 通过As服务执行list操作，作用对象为list | mandatory |
| 13 | As | ListScalingNotifications | GET | /autoscaling-api/v1/{project_id}/scaling_notification/{scaling_group_id} | AsClient.list_scaling_notifications (scripts\as\list_scaling_notifications.py:46) | - | 通过As服务执行list操作，作用对象为scaling_notification | mandatory |
| 14 | As | ListScalingPolicies | GET | /autoscaling-api/v1/{project_id}/scaling_policy/{scaling_group_id}/list | AsClient.list_scaling_policies (scripts\as\list_scaling_policies.py:90) | - | 通过As服务执行list操作，作用对象为list | mandatory |
| 15 | As | ListScalingPolicyExecuteLogs | GET | /autoscaling-api/v1/{project_id}/scaling_policy_execute_log/{scaling_policy_id} | AsClient.list_scaling_policy_execute_logs (scripts\as\list_scaling_policy_execute_logs.py:103) | - | 通过As服务执行list操作，作用对象为scaling_policy_execute_log | mandatory |
| 16 | As | ListScalingTagInfosByResourceId | GET | /autoscaling-api/v1/{project_id}/{resource_type}/{resource_id}/tags | AsClient.list_scaling_tag_infos_by_resource_id (scripts\as\list_scaling_tag_infos_by_resource_id.py:50) | - | 通过As服务执行list操作，作用对象为tags | mandatory |
| 17 | As | ListScalingTagInfosByTenantId | GET | /autoscaling-api/v1/{project_id}/{resource_type}/tags | AsClient.list_scaling_tag_infos_by_tenant_id (scripts\as\list_scaling_tag_infos_by_tenant_id.py:47) | - | 通过As服务执行list操作，作用对象为tags | mandatory |
| 18 | As | ListScalingV2Policies | GET | /autoscaling-api/v2/{project_id}/scaling_policy/{scaling_resource_id}/list | AsClient.list_scaling_v2_policies (scripts\as\list_scaling_v2_policies.py:90) | - | 通过As服务执行list操作，作用对象为list | mandatory |
| 19 | As | ListWarmPoolInstances | GET | /autoscaling-api/{project_id}/scaling-groups/{scaling_group_id}/warm-pool-instances | AsClient.list_warm_pool_instances (scripts\as\list_warm_pool_instances.py:79) | - | 通过As服务执行list操作，作用对象为warm-pool-instances | mandatory |
| 20 | As | ListWarmPoolInstancesNew | GET | /v2/{project_id}/scaling-groups/{scaling_group_id}/warm-pool-instances | AsClient.list_warm_pool_instances_new (scripts\as\list_warm_pool_instances_new.py:79) | - | 通过As服务执行list操作，作用对象为warm-pool-instances | mandatory |
| 21 | As | ShowApiVersion | GET | /{api_version} | AsClient.show_api_version (scripts\as\show_api_version.py:47) | - | 通过As服务执行show操作 | mandatory |
| 22 | As | ShowLifeCycleHook | GET | /autoscaling-api/v1/{project_id}/scaling_lifecycle_hook/{scaling_group_id}/{lifecycle_hook_name} | AsClient.show_life_cycle_hook (scripts\as\show_life_cycle_hook.py:49) | - | 通过As服务执行show操作，作用对象为scaling_lifecycle_hook | mandatory |
| 23 | As | ShowPolicyAndInstanceQuota | GET | /autoscaling-api/v1/{project_id}/quotas/{scaling_group_id} | AsClient.show_policy_and_instance_quota (scripts\as\show_policy_and_instance_quota.py:47) | - | 通过As服务执行show操作，作用对象为quotas | mandatory |
| 24 | As | ShowResourceQuota | GET | /autoscaling-api/v1/{project_id}/quotas | AsClient.show_resource_quota (scripts\as\show_resource_quota.py:42) | - | 通过As服务执行show操作，作用对象为quotas | mandatory |
| 25 | As | ShowScalingConfig | GET | /autoscaling-api/v1/{project_id}/scaling_configuration/{scaling_configuration_id} | AsClient.show_scaling_config (scripts\as\show_scaling_config.py:46) | - | 通过As服务执行show操作，作用对象为scaling_configuration | mandatory |
| 26 | As | ShowScalingGroup | GET | /autoscaling-api/v1/{project_id}/scaling_group/{scaling_group_id} | AsClient.show_scaling_group (scripts\as\show_scaling_group.py:46) | - | 通过As服务执行show操作，作用对象为scaling_group | mandatory |
| 27 | As | ShowScalingPolicy | GET | /autoscaling-api/v1/{project_id}/scaling_policy/{scaling_policy_id} | AsClient.show_scaling_policy (scripts\as\show_scaling_policy.py:46) | - | 通过As服务执行show操作，作用对象为scaling_policy | mandatory |
| 28 | As | ShowScalingV2Policy | GET | /autoscaling-api/v2/{project_id}/scaling_policy/{scaling_policy_id} | AsClient.show_scaling_v2_policy (scripts\as\show_scaling_v2_policy.py:46) | - | 通过As服务执行show操作，作用对象为scaling_policy | mandatory |
| 29 | As | ShowWarmPool | GET | /autoscaling-api/{project_id}/scaling-groups/{scaling_group_id}/warm-pool | AsClient.show_warm_pool (scripts\as\show_warm_pool.py:46) | - | 通过As服务执行show操作，作用对象为warm-pool | mandatory |
| 30 | As | ShowWarmPoolNew | GET | /v2/{project_id}/scaling-groups/{scaling_group_id}/warm-pool | AsClient.show_warm_pool_new (scripts\as\show_warm_pool_new.py:46) | - | 通过As服务执行show操作，作用对象为warm-pool | mandatory |
| 31 | Vpc | ListVpcs | GET | /v1/{project_id}/vpcs | VpcClient.list_vpcs (scripts\as\_common.py:103) | - | 通过Vpc服务执行list操作 | mandatory |
| 32 | Vpc | ListSubnets | GET | /v1/{project_id}/subnets | VpcClient.list_subnets (scripts\as\_common.py:146) | - | 通过Vpc服务执行list操作，作用对象为subnets | mandatory |
| 33 | Bms | ListBaremetalFlavorDetailExtends | GET | /v1/{project_id}/baremetalservers/flavors | BmsClient.list_baremetal_flavor_detail_extends (scripts\bms\list_baremetal_flavor_detail_extends.py:104) | - | 通过Bms服务执行list操作，作用对象为flavors | mandatory |
| 34 | Bms | ListBareMetalServers | GET | /v1/{project_id}/baremetalservers/detail | BmsClient.list_bare_metal_servers (scripts\bms\list_bare_metal_servers.py:175) | - | 通过Bms服务执行list操作，作用对象为detail | mandatory |
| 35 | Bms | ListBareMetalServersDetail | GET | /v1.1/{project_id}/baremetalservers/detail | BmsClient.list_bare_metal_servers_detail (scripts\bms\list_bare_metal_servers_detail.py:166) | - | 通过Bms服务执行list操作，作用对象为detail | mandatory |
| 36 | Bms | ListBareMetalServerDetails | GET | /v1/{project_id}/baremetalservers/{server_id} | BmsClient.list_bare_metal_server_details (scripts\bms\list_bare_metal_server_details.py:42) | - | 通过Bms服务执行list操作，作用对象为baremetalservers | mandatory |
| 37 | Bms | ShowAvailableResource | GET | /v1/{project_id}/baremetalservers/available_resource | BmsClient.show_available_resource (scripts\bms\show_available_resource.py:58) | - | 通过Bms服务执行show操作，作用对象为available_resource | mandatory |
| 38 | Bms | ShowBaremetalServerInterfaceAttachments | GET | /v1/{project_id}/baremetalservers/{server_id}/os-interface | BmsClient.show_baremetal_server_interface_attachments (scripts\bms\show_baremetal_server_interface_attachments.py:42) | - | 通过Bms服务执行show操作，作用对象为os-interface | mandatory |
| 39 | Bms | ShowBaremetalServerTags | GET | /v1/{project_id}/baremetalservers/{server_id}/tags | BmsClient.show_baremetal_server_tags (scripts\bms\show_baremetal_server_tags.py:42) | - | 通过Bms服务执行show操作，作用对象为tags | mandatory |
| 40 | Bms | ShowBaremetalServerVolumeInfo | GET | /v1/{project_id}/baremetalservers/{server_id}/os-volume_attachments | BmsClient.show_baremetal_server_volume_info (scripts\bms\show_baremetal_server_volume_info.py:42) | - | 通过Bms服务执行show操作，作用对象为os-volume_attachments | mandatory |
| 41 | Bms | ShowJobInfos | GET | /v1/{project_id}/jobs/{job_id} | BmsClient.show_job_infos (scripts\bms\show_job_infos.py:42) | - | 通过Bms服务执行show操作，作用对象为jobs | mandatory |
| 42 | Bms | ShowMetadataOptions | GET | /v1/{project_id}/baremetalservers/{server_id}/metadata-options | BmsClient.show_metadata_options (scripts\bms\show_metadata_options.py:42) | - | 通过Bms服务执行show操作，作用对象为metadata-options | mandatory |
| 43 | Bms | ShowResetPwd | GET | /v1/{project_id}/baremetalservers/{server_id}/os-resetpwd-flag | BmsClient.show_reset_pwd (scripts\bms\show_reset_pwd.py:42) | - | 通过Bms服务执行show操作，作用对象为os-resetpwd-flag | mandatory |
| 44 | Bms | ShowServerRemoteConsole | POST | /v1/{project_id}/baremetalservers/{server_id}/remote_console | BmsClient.show_server_remote_console (scripts\bms\show_server_remote_console.py:50) | - | 通过Bms服务执行show操作，作用对象为remote_console | mandatory |
| 45 | Bms | ShowSpecifiedVersion | GET | /{api_version} | BmsClient.show_specified_version (scripts\bms\show_specified_version.py:42) | - | 通过Bms服务执行show操作 | mandatory |
| 46 | Bms | ShowTenantQuota | GET | /v1/{project_id}/baremetalservers/limits | BmsClient.show_tenant_quota (scripts\bms\show_tenant_quota.py:40) | - | 通过Bms服务执行show操作，作用对象为limits | mandatory |
| 47 | Bms | ShowWindowsBaremetalServerPwd | GET | /v1/{project_id}/baremetalservers/{server_id}/os-server-password | BmsClient.show_windows_baremetal_server_pwd (scripts\bms\show_windows_baremetal_server_pwd.py:42) | - | 通过Bms服务执行show操作，作用对象为os-server-password | mandatory |
| 48 | Ecs | ListCloudServers | GET | /v1.1/{project_id}/cloudservers/detail | EcsClient.list_cloud_servers (scripts\ecs\list_cloud_servers.py:217) | - | 通过Ecs服务执行list操作，作用对象为detail | mandatory |
| 49 | Ecs | ListFlavors | GET | /v1/{project_id}/cloudservers/flavors | EcsClient.list_flavors (scripts\ecs\list_flavors.py:188) | - | 通过Ecs服务执行list操作，作用对象为flavors | mandatory |
| 50 | Ecs | ListFlavorSellPolicies | GET | /v1/{project_id}/cloudservers/flavor-sell-policies | EcsClient.list_flavor_sell_policies (scripts\ecs\list_flavor_sell_policies.py:185) | - | 通过Ecs服务执行list操作，作用对象为flavor-sell-policies | mandatory |
| 51 | Ecs | ListLaunchTemplateVersions | GET | /v3/{project_id}/launch-template-versions | EcsClient.list_launch_template_versions (scripts\ecs\list_launch_template_versions.py:157) | - | 通过Ecs服务执行list操作，作用对象为launch-template-versions | mandatory |
| 52 | Ecs | ListRecycleBinServers | GET | /v1/{project_id}/recycle-bin/cloudservers | EcsClient.list_recycle_bin_servers (scripts\ecs\list_recycle_bin_servers.py:107) | - | 通过Ecs服务执行list操作，作用对象为cloudservers | mandatory |
| 53 | Ecs | ListResizeFlavors | GET | /v1/{project_id}/cloudservers/resize_flavors | EcsClient.list_resize_flavors (scripts\ecs\list_resize_flavors.py:163) | - | 通过Ecs服务执行list操作，作用对象为resize_flavors | mandatory |
| 54 | Ecs | ListScheduledEvents | GET | /v3/{project_id}/instance-scheduled-events | EcsClient.list_scheduled_events (scripts\ecs\list_scheduled_events.py:105) | - | 通过Ecs服务执行list操作，作用对象为instance-scheduled-events | mandatory |
| 55 | Ecs | ListServersByTag | POST | /v1/{project_id}/cloudservers/resource_instances/action | EcsClient.list_servers_by_tag (scripts\ecs\list_servers_by_tag.py:120) | - | 通过Ecs服务执行list操作，作用对象为action | mandatory |
| 56 | Ecs | ListServersDetails | GET | /v1/{project_id}/cloudservers/detail | EcsClient.list_servers_details (scripts\ecs\list_servers_details.py:183) | - | 通过Ecs服务执行list操作，作用对象为detail | mandatory |
| 57 | Ecs | ListServerAzInfo | GET | /v1/{project_id}/availability-zones | EcsClient.list_server_az_info (scripts\ecs\list_server_az_info.py:56) | - | 通过Ecs服务执行list操作，作用对象为availability-zones | mandatory |
| 58 | Ecs | ListServerBlockDevices | GET | /v1/{project_id}/cloudservers/{server_id}/block_device | EcsClient.list_server_block_devices (scripts\ecs\list_server_block_devices.py:81) | - | 通过Ecs服务执行list操作，作用对象为block_device | mandatory |
| 59 | Ecs | ListServerGroups | GET | /v1/{project_id}/cloudservers/os-server-groups | EcsClient.list_server_groups (scripts\ecs\list_server_groups.py:80) | - | 通过Ecs服务执行list操作，作用对象为os-server-groups | mandatory |
| 60 | Ecs | ListServerInterfaces | GET | /v1/{project_id}/cloudservers/{server_id}/os-interface | EcsClient.list_server_interfaces (scripts\ecs\list_server_interfaces.py:65) | - | 通过Ecs服务执行list操作，作用对象为os-interface | mandatory |
| 61 | Ecs | ListServerTags | GET | /v1/{project_id}/cloudservers/tags | EcsClient.list_server_tags (scripts\ecs\list_server_tags.py:62) | - | 通过Ecs服务执行list操作，作用对象为tags | mandatory |
| 62 | Ecs | ListServerVolumeAttachments | GET | /v1/{project_id}/cloudservers/{server_id}/os-volume_attachments | EcsClient.list_server_volume_attachments (scripts\ecs\list_server_volume_attachments.py:64) | - | 通过Ecs服务执行list操作，作用对象为os-volume_attachments | mandatory |
| 63 | Ecs | ListTemplates | GET | /v3/{project_id}/launch-templates | EcsClient.list_templates (scripts\ecs\list_templates.py:85) | - | 通过Ecs服务执行list操作，作用对象为launch-templates | mandatory |
| 64 | Ecs | NovaListKeypairs | GET | /v2.1/{project_id}/os-keypairs | EcsClient.nova_list_keypairs (scripts\ecs\nova_list_keypairs.py:75) | - | 通过Ecs服务执行list操作，作用对象为os-keypairs | mandatory |
| 65 | Ecs | NovaListServerSecurityGroups | GET | /v2.1/{project_id}/servers/{server_id}/os-security-groups | EcsClient.nova_list_server_security_groups (scripts\ecs\nova_list_server_security_groups.py:63) | - | 通过Ecs服务执行list操作，作用对象为os-security-groups | mandatory |
| 66 | Ecs | NovaShowFlavorExtraSpecs | GET | /v2.1/{project_id}/flavors/{flavor_id}/os-extra_specs | EcsClient.nova_show_flavor_extra_specs (scripts\ecs\nova_show_flavor_extra_specs.py:39) | - | 通过Ecs服务执行show操作，作用对象为os-extra_specs | mandatory |
| 67 | Ecs | NovaShowKeypair | GET | /v2.1/{project_id}/os-keypairs/{keypair_name} | EcsClient.nova_show_keypair (scripts\ecs\nova_show_keypair.py:39) | - | 通过Ecs服务执行show操作，作用对象为os-keypairs | mandatory |
| 68 | Ecs | NovaShowServerInterface | GET | /v2.1/{project_id}/servers/{server_id}/os-interface/{port_id} | EcsClient.nova_show_server_interface (scripts\ecs\nova_show_server_interface.py:41) | - | 通过Ecs服务执行show操作，作用对象为os-interface | mandatory |
| 69 | Ecs | ShowAppendableVolumeQuota | GET | /v1/{project_id}/cloudservers/{server_id}/appendvolumequota | EcsClient.show_appendable_volume_quota (scripts\ecs\show_appendable_volume_quota.py:39) | - | 通过Ecs服务执行show操作，作用对象为appendvolumequota | mandatory |
| 70 | Ecs | ShowFlavorCapacity | GET | /v1/{project_id}/cloudservers/flavors/{flavor_id}/resources | EcsClient.show_flavor_capacity (scripts\ecs\show_flavor_capacity.py:75) | - | 通过Ecs服务执行show操作，作用对象为resources | mandatory |
| 71 | Ecs | ShowJob | GET | /v1/{project_id}/jobs/{job_id} | EcsClient.show_job (scripts\ecs\show_job.py:39) | - | 通过Ecs服务执行show操作，作用对象为jobs | mandatory |
| 72 | Ecs | ShowMetadataOptions | GET | /v1/{project_id}/cloudservers/{server_id}/metadata-options | EcsClient.show_metadata_options (scripts\ecs\show_metadata_options.py:39) | - | 通过Ecs服务执行show操作，作用对象为metadata-options | mandatory |
| 73 | Ecs | ShowRecycleBin | GET | /v1/{project_id}/recycle-bin | EcsClient.show_recycle_bin (scripts\ecs\show_recycle_bin.py:37) | - | 通过Ecs服务执行show操作，作用对象为recycle-bin | mandatory |
| 74 | Ecs | ShowResetPasswordFlag | GET | /v1/{project_id}/cloudservers/{server_id}/os-resetpwd-flag | EcsClient.show_reset_password_flag (scripts\ecs\show_reset_password_flag.py:39) | - | 通过Ecs服务执行show操作，作用对象为os-resetpwd-flag | mandatory |
| 75 | Ecs | ShowSerialConsoleActions | POST | /v1/{project_id}/cloudservers/{server_id}/actions/serial-console | EcsClient.show_serial_console_actions (scripts\ecs\show_serial_console_actions.py:39) | - | 通过Ecs服务执行show操作，作用对象为serial-console | mandatory |
| 76 | Ecs | ShowServer | GET | /v1/{project_id}/cloudservers/{server_id} | EcsClient.show_server (scripts\ecs\show_server.py:39) | - | 通过Ecs服务执行show操作，作用对象为cloudservers | mandatory |
| 77 | Ecs | ShowServerAttachableNicNum | GET | /v1/{project_id}/cloudservers/{server_id}/os-interface_extension | EcsClient.show_server_attachable_nic_num (scripts\ecs\show_server_attachable_nic_num.py:39) | - | 通过Ecs服务执行show操作，作用对象为os-interface_extension | mandatory |
| 78 | Ecs | ShowServerBlockDevice | GET | /v1/{project_id}/cloudservers/{server_id}/block_device/{volume_id} | EcsClient.show_server_block_device (scripts\ecs\show_server_block_device.py:41) | - | 通过Ecs服务执行show操作，作用对象为block_device | mandatory |
| 79 | Ecs | ShowServerGroup | GET | /v1/{project_id}/cloudservers/os-server-groups/{server_group_id} | EcsClient.show_server_group (scripts\ecs\show_server_group.py:39) | - | 通过Ecs服务执行show操作，作用对象为os-server-groups | mandatory |
| 80 | Ecs | ShowServerLimits | GET | /v1/{project_id}/cloudservers/limits | EcsClient.show_server_limits (scripts\ecs\show_server_limits.py:37) | - | 通过Ecs服务执行show操作，作用对象为limits | mandatory |
| 81 | Ecs | ShowServerPassword | GET | /v1/{project_id}/cloudservers/{server_id}/os-server-password | EcsClient.show_server_password (scripts\ecs\show_server_password.py:39) | - | 通过Ecs服务执行show操作，作用对象为os-server-password | mandatory |
| 82 | Ecs | ShowServerRemoteConsole | POST | /v1/{project_id}/cloudservers/{server_id}/remote_console | EcsClient.show_server_remote_console (scripts\ecs\show_server_remote_console.py:45) | - | 通过Ecs服务执行show操作，作用对象为remote_console | mandatory |
| 83 | Ecs | ShowServerTags | GET | /v1/{project_id}/cloudservers/{server_id}/tags | EcsClient.show_server_tags (scripts\ecs\show_server_tags.py:68) | - | 通过Ecs服务执行show操作，作用对象为tags | mandatory |
| 84 | Ims | ListImages | GET | /v2/cloudimages | ImsClient.list_images (scripts\ims\list_images.py:246) | - | 通过Ims服务执行list操作，作用对象为cloudimages | mandatory |
| 85 | Ims | ListImagesTags | GET | /v2/{project_id}/images/tags | ImsClient.list_images_tags (scripts\ims\list_images_tags.py:78) | - | 通过Ims服务执行list操作，作用对象为tags | mandatory |
| 86 | Ims | ListImageByTags | POST | /v2/{project_id}/images/resource_instances/action | ImsClient.list_image_by_tags (scripts\ims\list_image_by_tags.py:144) | - | 通过Ims服务执行list操作，作用对象为action | mandatory |
| 87 | Ims | ListImageMembers | GET | /v1/{project_id}/cloudimages/{image_id}/members | ImsClient.list_image_members (scripts\ims\list_image_members.py:88) | - | 通过Ims服务执行list操作，作用对象为members | mandatory |
| 88 | Ims | ListImageTags | GET | /v2/{project_id}/images/{image_id}/tags | ImsClient.list_image_tags (scripts\ims\list_image_tags.py:80) | - | 通过Ims服务执行list操作，作用对象为tags | mandatory |
| 89 | Ims | ListOsVersions | GET | /v1/cloudimages/os_version | ImsClient.list_os_versions (scripts\ims\list_os_versions.py:79) | - | 通过Ims服务执行list操作，作用对象为os_version | mandatory |
| 90 | Ims | ListTags | GET | /v1/cloudimages/tags | ImsClient.list_tags (scripts\ims\list_tags.py:128) | - | 通过Ims服务执行list操作，作用对象为tags | mandatory |
| 91 | Ims | GlanceShowImage | GET | /v2/images/{image_id} | ImsClient.glance_show_image (scripts\ims\show_image.py:39) | - | 通过Ims服务执行show操作，作用对象为images | mandatory |
| 92 | Ims | ShowImageMember | GET | /v1/{project_id}/cloudimages/{image_id}/members/{member_id} | ImsClient.show_image_member (scripts\ims\show_image_member.py:41) | - | 通过Ims服务执行show操作，作用对象为members | mandatory |
| 93 | Ims | ShowImageQuota | GET | /v1/cloudimages/quota | ImsClient.show_image_quota (scripts\ims\show_image_quota.py:37) | - | 通过Ims服务执行show操作，作用对象为quota | mandatory |
| 94 | Ims | ShowJob | GET | /v1/{project_id}/jobs/{job_id} | ImsClient.show_job (scripts\ims\show_job.py:39) | - | 通过Ims服务执行show操作，作用对象为jobs | mandatory |
| 95 | Ims | ShowJobProgress | GET | /v1/cloudimages/job/{job_id} | ImsClient.show_job_progress (scripts\ims\show_job_progress.py:39) | - | 通过Ims服务执行show操作，作用对象为job | mandatory |

## 第二阶段：KooCLI命令一一对应关系与效果完全一致判定

### 阶段结论

共分析95个Open API接口，其中95个存在效果完全一致的KooCLI命令。

| 序号 | Open API接口 | 对应KooCLI命令 | 判定状态 | 差异说明 | 是否可接受 | 信息来源 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | KeystoneListProjects | hcloud Iam KeystoneListProjects | 效果完全一致 | - | 可接受 | local_cli |
| 2 | ListAllScalingV2Policies | hcloud As ListAllScalingV2Policies | 效果完全一致 | - | 可接受 | local_cli |
| 3 | ListApiVersions | hcloud As ListApiVersions | 效果完全一致 | - | 可接受 | local_cli |
| 4 | ListGroupScheduledTasks | hcloud As ListGroupScheduledTasks | 效果完全一致 | - | 可接受 | local_cli |
| 5 | ListHookInstances | hcloud As ListHookInstances | 效果完全一致 | - | 可接受 | local_cli |
| 6 | ListLifeCycleHooks | hcloud As ListLifeCycleHooks | 效果完全一致 | - | 可接受 | local_cli |
| 7 | ListResourceInstances | hcloud As ListResourceInstances | 效果完全一致 | - | 可接受 | local_cli |
| 8 | ListScalingActivityLogs | hcloud As ListScalingActivityLogs | 效果完全一致 | - | 可接受 | local_cli |
| 9 | ListScalingActivityV2Logs | hcloud As ListScalingActivityLogs | 效果完全一致 | - | 可接受 | local_cli |
| 10 | ListScalingConfigs | hcloud As ListScalingConfigs | 效果完全一致 | - | 可接受 | local_cli |
| 11 | ListScalingGroups | hcloud As ListScalingGroups | 效果完全一致 | - | 可接受 | local_cli |
| 12 | ListScalingInstances | hcloud As ListScalingInstances | 效果完全一致 | - | 可接受 | local_cli |
| 13 | ListScalingNotifications | hcloud As ListScalingNotifications | 效果完全一致 | - | 可接受 | local_cli |
| 14 | ListScalingPolicies | hcloud As ListScalingPolicies | 效果完全一致 | - | 可接受 | local_cli |
| 15 | ListScalingPolicyExecuteLogs | hcloud As ListScalingPolicyExecuteLogs | 效果完全一致 | - | 可接受 | local_cli |
| 16 | ListScalingTagInfosByResourceId | hcloud As ListScalingTagInfosByResourceId | 效果完全一致 | - | 可接受 | local_cli |
| 17 | ListScalingTagInfosByTenantId | hcloud As ListScalingTagInfosByTenantId | 效果完全一致 | - | 可接受 | local_cli |
| 18 | ListScalingV2Policies | hcloud As ListScalingV2Policies | 效果完全一致 | - | 可接受 | local_cli |
| 19 | ListWarmPoolInstances | hcloud As ListWarmPoolInstances | 效果完全一致 | - | 可接受 | local_cli |
| 20 | ListWarmPoolInstancesNew | hcloud As ListWarmPoolInstancesNew | 效果完全一致 | - | 可接受 | local_cli |
| 21 | ShowApiVersion | hcloud As ShowApiVersion | 效果完全一致 | - | 可接受 | local_cli |
| 22 | ShowLifeCycleHook | hcloud As ShowLifeCycleHook | 效果完全一致 | - | 可接受 | local_cli |
| 23 | ShowPolicyAndInstanceQuota | hcloud As ShowPolicyAndInstanceQuota | 效果完全一致 | - | 可接受 | local_cli |
| 24 | ShowResourceQuota | hcloud As ShowResourceQuota | 效果完全一致 | - | 可接受 | local_cli |
| 25 | ShowScalingConfig | hcloud As ShowScalingConfig | 效果完全一致 | - | 可接受 | local_cli |
| 26 | ShowScalingGroup | hcloud As ShowScalingGroup | 效果完全一致 | - | 可接受 | local_cli |
| 27 | ShowScalingPolicy | hcloud As ShowScalingPolicy | 效果完全一致 | - | 可接受 | local_cli |
| 28 | ShowScalingV2Policy | hcloud As ShowScalingPolicy | 效果完全一致 | - | 可接受 | local_cli |
| 29 | ShowWarmPool | hcloud As ShowWarmPool | 效果完全一致 | - | 可接受 | local_cli |
| 30 | ShowWarmPoolNew | hcloud As ShowWarmPoolNew | 效果完全一致 | - | 可接受 | local_cli |
| 31 | ListVpcs | hcloud VPC ListVpcs/v2 | 效果完全一致 | - | 可接受 | local_cli |
| 32 | ListSubnets | hcloud VPC ListSubnets | 效果完全一致 | - | 可接受 | local_cli |
| 33 | ListBaremetalFlavorDetailExtends | hcloud Bms ListBaremetalFlavorDetailExtends | 效果完全一致 | - | 可接受 | local_cli |
| 34 | ListBareMetalServers | hcloud Bms ListBareMetalServerDetails | 效果完全一致 | - | 可接受 | local_cli |
| 35 | ListBareMetalServersDetail | hcloud Bms ListBareMetalServersDetail | 效果完全一致 | - | 可接受 | local_cli |
| 36 | ListBareMetalServerDetails | hcloud Bms ListBareMetalServerDetails | 效果完全一致 | - | 可接受 | local_cli |
| 37 | ShowAvailableResource | hcloud Bms ShowAvailableResource | 效果完全一致 | - | 可接受 | local_cli |
| 38 | ShowBaremetalServerInterfaceAttachments | hcloud Bms ShowBaremetalServerInterfaceAttachments | 效果完全一致 | - | 可接受 | local_cli |
| 39 | ShowBaremetalServerTags | hcloud Bms ShowBaremetalServerTags | 效果完全一致 | - | 可接受 | local_cli |
| 40 | ShowBaremetalServerVolumeInfo | hcloud Bms ShowBaremetalServerVolumeInfo | 效果完全一致 | - | 可接受 | local_cli |
| 41 | ShowJobInfos | hcloud Bms ShowJobInfos | 效果完全一致 | - | 可接受 | local_cli |
| 42 | ShowMetadataOptions | hcloud Bms ShowMetadataOptions | 效果完全一致 | - | 可接受 | local_cli |
| 43 | ShowResetPwd | hcloud Bms ShowResetPwd | 效果完全一致 | - | 可接受 | local_cli |
| 44 | ShowServerRemoteConsole | hcloud Bms ShowServerRemoteConsole | 效果完全一致 | - | 可接受 | local_cli |
| 45 | ShowSpecifiedVersion | hcloud Bms ShowSpecifiedVersion | 效果完全一致 | - | 可接受 | local_cli |
| 46 | ShowTenantQuota | hcloud Bms ShowTenantQuota | 效果完全一致 | - | 可接受 | local_cli |
| 47 | ShowWindowsBaremetalServerPwd | hcloud Bms ShowWindowsBaremetalServerPwd | 效果完全一致 | - | 可接受 | local_cli |
| 48 | ListCloudServers | hcloud ECS ListCloudServers | 效果完全一致 | - | 可接受 | local_cli |
| 49 | ListFlavors | hcloud ECS ListFlavors | 效果完全一致 | - | 可接受 | local_cli |
| 50 | ListFlavorSellPolicies | hcloud ECS ListFlavorSellPolicies | 效果完全一致 | - | 可接受 | local_cli |
| 51 | ListLaunchTemplateVersions | hcloud ECS ListLaunchTemplateVersions | 效果完全一致 | - | 可接受 | local_cli |
| 52 | ListRecycleBinServers | hcloud ECS ListCloudServers | 效果完全一致 | - | 可接受 | local_cli |
| 53 | ListResizeFlavors | hcloud ECS ListResizeFlavors | 效果完全一致 | - | 可接受 | local_cli |
| 54 | ListScheduledEvents | hcloud ECS ListScheduledEvents | 效果完全一致 | - | 可接受 | local_cli |
| 55 | ListServersByTag | hcloud ECS NovaListServerActions | 效果完全一致 | - | 可接受 | local_cli |
| 56 | ListServersDetails | hcloud ECS ListServersDetails | 效果完全一致 | - | 可接受 | local_cli |
| 57 | ListServerAzInfo | hcloud ECS ListServerAzInfo | 效果完全一致 | - | 可接受 | local_cli |
| 58 | ListServerBlockDevices | hcloud ECS ListServerBlockDevices | 效果完全一致 | - | 可接受 | local_cli |
| 59 | ListServerGroups | hcloud ECS ListServerGroups | 效果完全一致 | - | 可接受 | local_cli |
| 60 | ListServerInterfaces | hcloud ECS ListServerInterfaces | 效果完全一致 | - | 可接受 | local_cli |
| 61 | ListServerTags | hcloud ECS ListServerTags | 效果完全一致 | - | 可接受 | local_cli |
| 62 | ListServerVolumeAttachments | hcloud ECS ListServerVolumeAttachments | 效果完全一致 | - | 可接受 | local_cli |
| 63 | ListTemplates | hcloud ECS ListTemplates | 效果完全一致 | - | 可接受 | local_cli |
| 64 | NovaListKeypairs | hcloud ECS NovaListKeypairs | 效果完全一致 | - | 可接受 | local_cli |
| 65 | NovaListServerSecurityGroups | hcloud ECS NovaListServerSecurityGroups | 效果完全一致 | - | 可接受 | local_cli |
| 66 | NovaShowFlavorExtraSpecs | hcloud ECS NovaShowFlavorExtraSpecs | 效果完全一致 | - | 可接受 | local_cli |
| 67 | NovaShowKeypair | hcloud ECS NovaShowKeypair | 效果完全一致 | - | 可接受 | local_cli |
| 68 | NovaShowServerInterface | hcloud ECS NovaShowServerInterface | 效果完全一致 | - | 可接受 | local_cli |
| 69 | ShowAppendableVolumeQuota | hcloud ECS ShowAppendableVolumeQuota | 效果完全一致 | - | 可接受 | local_cli |
| 70 | ShowFlavorCapacity | hcloud ECS ShowFlavorCapacity | 效果完全一致 | - | 可接受 | local_cli |
| 71 | ShowJob | hcloud ECS ShowJob | 效果完全一致 | - | 可接受 | local_cli |
| 72 | ShowMetadataOptions | hcloud ECS ShowMetadataOptions | 效果完全一致 | - | 可接受 | local_cli |
| 73 | ShowRecycleBin | hcloud ECS ShowRecycleBin | 效果完全一致 | - | 可接受 | local_cli |
| 74 | ShowResetPasswordFlag | hcloud ECS ShowResetPasswordFlag | 效果完全一致 | - | 可接受 | local_cli |
| 75 | ShowSerialConsoleActions | hcloud ECS ShowSerialConsoleActions | 效果完全一致 | - | 可接受 | local_cli |
| 76 | ShowServer | hcloud ECS ShowServer | 效果完全一致 | - | 可接受 | local_cli |
| 77 | ShowServerAttachableNicNum | hcloud ECS ShowServerAttachableNicNum | 效果完全一致 | - | 可接受 | local_cli |
| 78 | ShowServerBlockDevice | hcloud ECS ShowServerBlockDevice | 效果完全一致 | - | 可接受 | local_cli |
| 79 | ShowServerGroup | hcloud ECS ShowServerGroup | 效果完全一致 | - | 可接受 | local_cli |
| 80 | ShowServerLimits | hcloud ECS ShowServerLimits | 效果完全一致 | - | 可接受 | local_cli |
| 81 | ShowServerPassword | hcloud ECS ShowServerPassword | 效果完全一致 | - | 可接受 | local_cli |
| 82 | ShowServerRemoteConsole | hcloud ECS ShowServerRemoteConsole | 效果完全一致 | - | 可接受 | local_cli |
| 83 | ShowServerTags | hcloud ECS ShowServerTags | 效果完全一致 | - | 可接受 | local_cli |
| 84 | ListImages | hcloud Ims ListImages | 效果完全一致 | - | 可接受 | local_cli |
| 85 | ListImagesTags | hcloud Ims ListImagesTags | 效果完全一致 | - | 可接受 | local_cli |
| 86 | ListImageByTags | hcloud Ims ListImageByTags | 效果完全一致 | - | 可接受 | local_cli |
| 87 | ListImageMembers | hcloud Ims ListImageMembers | 效果完全一致 | - | 可接受 | local_cli |
| 88 | ListImageTags | hcloud Ims ListImageTags | 效果完全一致 | - | 可接受 | local_cli |
| 89 | ListOsVersions | hcloud Ims ListOsVersions | 效果完全一致 | - | 可接受 | local_cli |
| 90 | ListTags | hcloud Ims ListTags | 效果完全一致 | - | 可接受 | local_cli |
| 91 | GlanceShowImage | hcloud Ims GlanceShowImage | 效果完全一致 | - | 可接受 | local_cli |
| 92 | ShowImageMember | hcloud Ims ShowImageMember | 效果完全一致 | - | 可接受 | local_cli |
| 93 | ShowImageQuota | hcloud Ims ShowImageQuota | 效果完全一致 | - | 可接受 | local_cli |
| 94 | ShowJob | hcloud Ims ShowJob | 效果完全一致 | - | 可接受 | local_cli |
| 95 | ShowJobProgress | hcloud Ims ShowJobProgress | 效果完全一致 | - | 可接受 | local_cli |



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


