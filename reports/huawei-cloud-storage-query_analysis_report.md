# Skill实现原理分析报告 - huawei-cloud-storage-query

## 0. Skill基本信息

| 属性 | 值 |
| --- | --- |
| Skill名称 | huawei-cloud-storage-query |
| 实现方式 | SDK |
| 业务目标 | Queries Huawei Cloud storage resources (EVS/OBS/SFS/CBR). Covers cloud disks (volumes/snapshots/types/quotas/recycle bin), OBS buckets (ACL/metadata/notifications/policies/objects), SFS Turbo file systems (shares/perm rules/backend targets/quotas/LDAP/AD), and CBR backups (vaults/policies/backups... |
| 分析状态 | completed |
| 分析时间 | 2026-06-10T09:02:23.338491+00:00 |

## Skill依赖工具

| 依赖项 | 版本/说明 | 功能描述 | 是否必须 |
| --- | --- | --- | --- |

| Python | 3.14 | Skill实现语言及运行时环境 | 必须 |

| SDK: huaweicloudsdkcbr | >=3.1.0 | cbr服务SDK，用于调用华为云cbr相关API | 必须 |

| SDK: huaweicloudsdkcore | >=3.1.0 | 华为云SDK核心库，提供认证、HTTP请求等基础能力 | 必须 |

| SDK: huaweicloudsdkevs | >=3.1.0 | 云硬盘(EVS)服务SDK，用于管理云硬盘和卷 | 必须 |

| SDK: huaweicloudsdkiam | >=3.1.0 | 身份与访问管理(IAM)服务SDK，用于用户和权限管理 | 必须 |

| SDK: huaweicloudsdkobs | >=3.1.0 | 对象存储服务(OBS) SDK，用于对象存储操作 | 必须 |

| SDK: huaweicloudsdksfsturbo | >=3.1.0 | sfsturbo服务SDK，用于调用华为云sfsturbo相关API | 必须 |

| KooCLI (hcloud) | 已确认 | 华为云命令行工具，用于通过CLI调用云服务API | 必须 |

| config | 已确认 | 第三方库: config | 必须 |

| platform | 已确认 | 第三方库: platform | 必须 |

| urllib3 | 已确认 | 第三方库: urllib3 | 必须 |


## 第一阶段：目标Skill使用的华为云Open API接口

### 阶段结论

共识别86个Open API接口。
| 序号 | 服务 | Open API接口 | HTTP方法 | API路径 | 来源SDK调用 | 实际使用参数 | 业务作用 | 是否必须 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

| 1 | Iam | KeystoneListProjects | GET | /v3/projects | IamClient.keystone_list_projects (scripts\ensure_env.py:113) | - | 通过Iam服务执行list操作，作用对象为projects | mandatory |

| 2 | Cbr | CheckAgent | POST | /v3/{project_id}/agent/check | CbrClient.check_agent (scripts\cbr\check_agent.py:59) | - | 通过Cbr服务执行check操作，作用对象为check | mandatory |

| 3 | Cbr | ListAgent | GET | /v3/{project_id}/agents | CbrClient.list_agent (scripts\cbr\list_agent.py:78) | - | 通过Cbr服务执行list操作，作用对象为agents | mandatory |

| 4 | Cbr | ListBackups | GET | /v3/{project_id}/backups | CbrClient.list_backups (scripts\cbr\list_backups.py:136) | - | 通过Cbr服务执行list操作，作用对象为backups | mandatory |

| 5 | Cbr | ListDomainProjects | GET | /v3/domain/{domain_name}/projects | CbrClient.list_domain_projects (scripts\cbr\list_domain_projects.py:35) | - | 通过Cbr服务执行list操作，作用对象为projects | mandatory |

| 6 | Cbr | ListExternalVault | GET | /v3/{project_id}/vaults/external | CbrClient.list_external_vault (scripts\cbr\list_external_vault.py:98) | - | 通过Cbr服务执行list操作，作用对象为external | mandatory |

| 7 | Cbr | ListFeatures | GET | /v3/{project_id}/cbr-features | CbrClient.list_features (scripts\cbr\list_features.py:40) | - | 通过Cbr服务执行list操作，作用对象为cbr-features | mandatory |

| 8 | Cbr | ListOpLogs | GET | /v3/{project_id}/operation-logs | CbrClient.list_op_logs (scripts\cbr\list_op_logs.py:100) | - | 通过Cbr服务执行list操作，作用对象为operation-logs | mandatory |

| 9 | Cbr | ListOrganizationPolicies | GET | /v3/{project_id}/organization-policies | CbrClient.list_organization_policies (scripts\cbr\list_organization_policies.py:72) | - | 通过Cbr服务执行list操作，作用对象为organization-policies | mandatory |

| 10 | Cbr | ListOrganizationPolicyDetail | GET | /v3/{project_id}/organization-policies/{organization_policy_id}/policy-detail | CbrClient.list_organization_policy_detail (scripts\cbr\list_organization_policy_detail.py:36) | - | 通过Cbr服务执行list操作，作用对象为policy-detail | mandatory |

| 11 | Cbr | ListPolicies | GET | /v3/{project_id}/policies | CbrClient.list_policies (scripts\cbr\list_policies.py:40) | - | 通过Cbr服务执行list操作，作用对象为policies | mandatory |

| 12 | Cbr | ListProjects | GET | /v3/region-projects | CbrClient.list_projects (scripts\cbr\list_projects.py:33) | - | 通过Cbr服务执行list操作，作用对象为region-projects | mandatory |

| 13 | Cbr | ListProtectable | GET | /v3/{project_id}/protectables/{protectable_type}/instances | CbrClient.list_protectable (scripts\cbr\list_protectable.py:85) | - | 通过Cbr服务执行list操作，作用对象为instances | mandatory |

| 14 | Cbr | ListVault | GET | /v3/{project_id}/vaults | CbrClient.list_vault (scripts\cbr\list_vault.py:109) | - | 通过Cbr服务执行list操作 | mandatory |

| 15 | Cbr | ShowAgent | GET | /v3/{project_id}/agents/{agent_id} | CbrClient.show_agent (scripts\cbr\show_agent.py:35) | - | 通过Cbr服务执行show操作，作用对象为agents | mandatory |

| 16 | Cbr | ShowBackup | GET | /v3/{project_id}/backups/{backup_id} | CbrClient.show_backup (scripts\cbr\show_backup.py:35) | - | 通过Cbr服务执行show操作，作用对象为backups | mandatory |

| 17 | Cbr | ShowCheckpoint | GET | /v3/{project_id}/checkpoints/{checkpoint_id} | CbrClient.show_checkpoint (scripts\cbr\show_checkpoint.py:35) | - | 通过Cbr服务执行show操作，作用对象为checkpoints | mandatory |

| 18 | Cbr | ShowDomain | GET | /v3/domain/{source_project_id} | CbrClient.show_domain (scripts\cbr\show_domain.py:35) | - | 通过Cbr服务执行show操作，作用对象为domain | mandatory |

| 19 | Cbr | ShowFeature | GET | /v3/{project_id}/cbr-features/{feature_key} | CbrClient.show_feature (scripts\cbr\show_feature.py:42) | - | 通过Cbr服务执行show操作，作用对象为cbr-features | mandatory |

| 20 | Cbr | ShowMembersDetail | GET | /v3/{project_id}/backups/{backup_id}/members | CbrClient.show_members_detail (scripts\cbr\show_members_detail.py:90) | - | 通过Cbr服务执行show操作，作用对象为members | mandatory |

| 21 | Cbr | ShowMemberDetail | GET | /v3/{project_id}/backups/{backup_id}/members/{member_id} | CbrClient.show_member_detail (scripts\cbr\show_member_detail.py:37) | - | 通过Cbr服务执行show操作，作用对象为members | mandatory |

| 22 | Cbr | ShowMetadata | GET | /v3/{project_id}/backups/{backup_id}/metadata | CbrClient.show_metadata (scripts\cbr\show_metadata.py:35) | - | 通过Cbr服务执行show操作，作用对象为metadata | mandatory |

| 23 | Cbr | ShowMigrateStatus | GET | /v3/migrates | CbrClient.show_migrate_status (scripts\cbr\show_migrate_status.py:36) | - | 通过Cbr服务执行show操作，作用对象为migrates | mandatory |

| 24 | Cbr | ShowOpLog | GET | /v3/{project_id}/operation-logs/{operation_log_id} | CbrClient.show_op_log (scripts\cbr\show_op_log.py:35) | - | 通过Cbr服务执行show操作，作用对象为operation-logs | mandatory |

| 25 | Cbr | ShowOrganizationPolicy | GET | /v3/{project_id}/organization-policies/{organization_policy_id} | CbrClient.show_organization_policy (scripts\cbr\show_organization_policy.py:35) | - | 通过Cbr服务执行show操作，作用对象为organization-policies | mandatory |

| 26 | Cbr | ShowPolicy | GET | /v3/{project_id}/policies/{policy_id} | CbrClient.show_policy (scripts\cbr\show_policy.py:35) | - | 通过Cbr服务执行show操作，作用对象为policies | mandatory |

| 27 | Cbr | ShowProtectable | GET | /v3/{project_id}/protectables/{protectable_type}/instances/{instance_id} | CbrClient.show_protectable (scripts\cbr\show_protectable.py:37) | - | 通过Cbr服务执行show操作，作用对象为instances | mandatory |

| 28 | Cbr | ShowReplicationCapabilities | GET | /v3/{project_id}/replication-capabilities | CbrClient.show_replication_capabilities (scripts\cbr\show_replication_capabilities.py:33) | - | 通过Cbr服务执行show操作，作用对象为replication-capabilities | mandatory |

| 29 | Cbr | ShowStorageUsage | GET | /v3/{project_id}/storage_usage | CbrClient.show_storage_usage (scripts\cbr\show_storage_usage.py:77) | - | 通过Cbr服务执行show操作，作用对象为storage_usage | mandatory |

| 30 | Cbr | ShowSummary | GET | /v3/{project_id}/vaults/summary | CbrClient.show_summary (scripts\cbr\show_summary.py:33) | - | 通过Cbr服务执行show操作，作用对象为summary | mandatory |

| 31 | Cbr | ShowVault | GET | /v3/{project_id}/vaults/{vault_id} | CbrClient.show_vault (scripts\cbr\show_vault.py:35) | - | 通过Cbr服务执行show操作 | mandatory |

| 32 | Cbr | ShowVaultProjectTag | GET | /v3/{project_id}/vault/tags | CbrClient.show_vault_project_tag (scripts\cbr\show_vault_project_tag.py:33) | - | 通过Cbr服务执行show操作，作用对象为tags | mandatory |

| 33 | Cbr | ShowVaultResourceInstances | POST | /v3/{project_id}/vault/resource_instances/action | CbrClient.show_vault_resource_instances (scripts\cbr\show_vault_resource_instances.py:135) | - | 通过Cbr服务执行show操作，作用对象为action | mandatory |

| 34 | Cbr | ShowVaultTag | GET | /v3/{project_id}/vault/{vault_id}/tags | CbrClient.show_vault_tag (scripts\cbr\show_vault_tag.py:35) | - | 通过Cbr服务执行show操作，作用对象为tags | mandatory |

| 35 | Evs | CinderListAvailabilityZones | GET | /v2/{project_id}/os-availability-zone | EvsClient.cinder_list_availability_zones (scripts\evs\cinder_list_availability_zones.py:33) | - | 通过Evs服务执行list操作，作用对象为os-availability-zone | mandatory |

| 36 | Evs | CinderListQuotas | GET | /v2/{project_id}/os-quota-sets/{target_project_id} | EvsClient.cinder_list_quotas (scripts\evs\cinder_list_quotas.py:37) | - | 通过Evs服务执行list操作，作用对象为os-quota-sets | mandatory |

| 37 | Evs | CinderListVolumeTransfers | GET | /v2/{project_id}/os-volume-transfer | EvsClient.cinder_list_volume_transfers (scripts\evs\cinder_list_volume_transfers.py:39) | - | 通过Evs服务执行list操作，作用对象为os-volume-transfer | mandatory |

| 38 | Evs | CinderListVolumeTypes | GET | /v2/{project_id}/types | EvsClient.cinder_list_volume_types (scripts\evs\cinder_list_volume_types.py:33) | - | 通过Evs服务执行list操作，作用对象为types | mandatory |

| 39 | Evs | CinderShowVolumeTransfer | GET | /v2/{project_id}/os-volume-transfer/{transfer_id} | EvsClient.cinder_show_volume_transfer (scripts\evs\cinder_show_volume_transfer.py:35) | - | 通过Evs服务执行show操作，作用对象为os-volume-transfer | mandatory |

| 40 | Evs | ListSnapshots | GET | /v2/{project_id}/cloudsnapshots/detail | EvsClient.list_snapshots (scripts\evs\list_snapshots.py:48) | - | 通过Evs服务执行list操作，作用对象为detail | mandatory |

| 41 | Evs | ListVersions | GET | / | EvsClient.list_versions (scripts\evs\list_versions.py:33) | - | 通过Evs服务执行list操作 | mandatory |

| 42 | Evs | ListVolumes | GET | /v2/{project_id}/cloudvolumes/detail | EvsClient.list_volumes (scripts\evs\list_volumes.py:57) | - | 通过Evs服务执行list操作，作用对象为detail | mandatory |

| 43 | Evs | ListVolumesInRecycle | GET | /v3/{project_id}/recycle-bin-volumes/detail | EvsClient.list_volumes_in_recycle (scripts\evs\list_volumes_in_recycle.py:51) | - | 通过Evs服务执行list操作，作用对象为detail | mandatory |

| 44 | Evs | ListVolumeTags | GET | /v2/{project_id}/cloudvolumes/tags | EvsClient.list_volume_tags (scripts\evs\list_volume_tags.py:33) | - | 通过Evs服务执行list操作，作用对象为tags | mandatory |

| 45 | Evs | ShowRecyclePolicy | GET | /v3/{project_id}/recycle-bin-volumes/policy | EvsClient.show_recycle_policy (scripts\evs\show_recycle_policy.py:33) | - | 通过Evs服务执行show操作，作用对象为policy | mandatory |

| 46 | Evs | ShowSnapshot | GET | /v2/{project_id}/cloudsnapshots/{snapshot_id} | EvsClient.show_snapshot (scripts\evs\show_snapshot.py:35) | - | 通过Evs服务执行show操作，作用对象为cloudsnapshots | mandatory |

| 47 | Evs | ShowVersion | GET | /{version} | EvsClient.show_version (scripts\evs\show_version.py:35) | - | 通过Evs服务执行show操作 | mandatory |

| 48 | Evs | ShowVolume | GET | /v2/{project_id}/cloudvolumes/{volume_id} | EvsClient.show_volume (scripts\evs\show_volume.py:35) | - | 通过Evs服务执行show操作，作用对象为cloudvolumes | mandatory |

| 49 | Evs | ShowVolumeInRecycle | GET | /v3/{project_id}/recycle-bin-volumes/{volume_id} | EvsClient.show_volume_in_recycle (scripts\evs\show_volume_in_recycle.py:35) | - | 通过Evs服务执行show操作，作用对象为recycle-bin-volumes | mandatory |

| 50 | Evs | ShowVolumeTags | GET | /v2/{project_id}/cloudvolumes/{volume_id}/tags | EvsClient.show_volume_tags (scripts\evs\show_volume_tags.py:35) | - | 通过Evs服务执行show操作，作用对象为tags | mandatory |

| 51 | Obs | GetBucketAcl | GET | / | ObsClient.get_bucket_acl (scripts\obs\get_bucket_acl.py:34) | - | 通过Obs服务执行get操作 | mandatory |

| 52 | Obs | GetBucketCustomdomain | GET | / | ObsClient.get_bucket_customdomain (scripts\obs\get_bucket_customdomain.py:34) | - | 通过Obs服务执行get操作 | mandatory |

| 53 | Obs | GetBucketMetadata | POST | / | ObsClient.get_bucket_metadata (scripts\obs\get_bucket_metadata.py:34) | - | 通过Obs服务执行get操作 | mandatory |

| 54 | Obs | GetBucketNotification | GET | / | ObsClient.get_bucket_notification (scripts\obs\get_bucket_notification.py:34) | - | 通过Obs服务执行get操作 | mandatory |

| 55 | Obs | GetBucketObjectLock | GET | / | ObsClient.get_bucket_object_lock (scripts\obs\get_bucket_object_lock.py:34) | - | 通过Obs服务执行get操作 | mandatory |

| 56 | Obs | GetBucketPolicyPublicStatus | GET | / | ObsClient.get_bucket_policy_public_status (scripts\obs\get_bucket_policy_public_status.py:34) | - | 通过Obs服务执行get操作 | mandatory |

| 57 | Obs | GetBucketPublicAccessBlock | GET | / | ObsClient.get_bucket_public_access_block (scripts\obs\get_bucket_public_access_block.py:34) | - | 通过Obs服务执行get操作 | mandatory |

| 58 | Obs | GetBucketPublicStatus | GET | / | ObsClient.get_bucket_public_status (scripts\obs\get_bucket_public_status.py:34) | - | 通过Obs服务执行get操作 | mandatory |

| 59 | Obs | GetDisPolicy | GET | / | ObsClient.get_dis_policy (scripts\obs\get_dis_policy.py:34) | - | 通过Obs服务执行get操作 | mandatory |

| 60 | Obs | GetObject | GET | /{object_key} | ObsClient.get_object (scripts\obs\get_object.py:39) | - | 通过Obs服务执行get操作 | mandatory |

| 61 | Obs | GetObjectTagging | GET | /{object_key} | ObsClient.get_object_tagging (scripts\obs\get_object_tagging.py:40) | - | 通过Obs服务执行get操作 | mandatory |

| 62 | Obs | HeadObject | POST | /{object_key} | ObsClient.head_object (scripts\obs\head_object.py:39) | - | 通过Obs服务执行HeadObject操作 | mandatory |

| 63 | Obs | ListBuckets | GET | / | ObsClient.list_buckets (scripts\obs\list_buckets.py:32) | - | 通过Obs服务执行list操作 | mandatory |

| 64 | Obs | ListObjects | GET | / | ObsClient.list_objects (scripts\obs\list_objects.py:45) | - | 通过Obs服务执行list操作 | mandatory |

| 65 | SFSTurbo | ListBackendTargets | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/targets | SFSTurboClient.list_backend_targets (scripts\sfs\list_backend_targets.py:41) | - | 通过SFSTurbo服务执行get操作，作用对象为targets | mandatory |

| 66 | SFSTurbo | ListFsTasks | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/fs/{feature}/tasks | SFSTurboClient.list_fs_tasks (scripts\sfs\list_fs_tasks.py:46) | - | 通过SFSTurbo服务执行list操作，作用对象为tasks | mandatory |

| 67 | SFSTurbo | ListHpcCacheTasks | GET | /v1/{project_id}/sfs-turbo/{share_id}/hpc-cache/tasks | SFSTurboClient.list_hpc_cache_tasks (scripts\sfs\list_hpc_cache_tasks.py:53) | - | 通过SFSTurbo服务执行list操作，作用对象为tasks | mandatory |

| 68 | SFSTurbo | ListPermRules | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/fs/perm-rules | SFSTurboClient.list_perm_rules (scripts\sfs\list_perm_rules.py:41) | - | 通过SFSTurbo服务执行list操作，作用对象为perm-rules | mandatory |

| 69 | SFSTurbo | ListSharedTags | GET | /v1/{project_id}/sfs-turbo/tags | SFSTurboClient.list_shared_tags (scripts\sfs\list_shared_tags.py:39) | - | 通过SFSTurbo服务执行list操作，作用对象为tags | mandatory |

| 70 | SFSTurbo | ListShares | GET | /v1/{project_id}/sfs-turbo/shares/detail | SFSTurboClient.list_shares (scripts\sfs\list_shares.py:39) | - | 通过SFSTurbo服务执行list操作，作用对象为detail | mandatory |

| 71 | SFSTurbo | ListSharesByTag | POST | /v1/{project_id}/sfs-turbo/resource_instances/action | SFSTurboClient.list_shares_by_tag (scripts\sfs\list_shares_by_tag.py:47) | - | 通过SFSTurbo服务执行list操作，作用对象为action | mandatory |

| 72 | SFSTurbo | ListShareTypes | GET | /v1/{project_id}/sfs-turbo/share-types | SFSTurboClient.list_share_types (scripts\sfs\list_share_types.py:39) | - | 通过SFSTurbo服务执行list操作，作用对象为share-types | mandatory |

| 73 | SFSTurbo | ShowActiveDirectoryDomain | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/fs/active-directory-domain | SFSTurboClient.show_active_directory_domain (scripts\sfs\show_active_directory_domain.py:35) | - | 通过SFSTurbo服务执行show操作，作用对象为active-directory-domain | mandatory |

| 74 | SFSTurbo | ShowBackendTargetInfo | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/targets/{target_id} | SFSTurboClient.show_backend_target_info (scripts\sfs\show_backend_target_info.py:37) | - | 通过SFSTurbo服务执行show操作，作用对象为targets | mandatory |

| 75 | SFSTurbo | ShowClientIpInfo | POST | /v1/{project_id}/sfs-turbo/shares/{share_id}/action | SFSTurboClient.show_client_ip_info (scripts\sfs\show_client_ip_info.py:40) | - | 通过SFSTurbo服务执行show操作，作用对象为action | mandatory |

| 76 | SFSTurbo | ShowFsDir | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/fs/dir | SFSTurboClient.show_fs_dir (scripts\sfs\show_fs_dir.py:37) | - | 通过SFSTurbo服务执行show操作，作用对象为dir | mandatory |

| 77 | SFSTurbo | ShowFsDirQuota | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/fs/dir-quota | SFSTurboClient.show_fs_dir_quota (scripts\sfs\show_fs_dir_quota.py:37) | - | 通过SFSTurbo服务执行show操作，作用对象为dir-quota | mandatory |

| 78 | SFSTurbo | ShowFsDirUsage | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/fs/dir-usage | SFSTurboClient.show_fs_dir_usage (scripts\sfs\show_fs_dir_usage.py:37) | - | 通过SFSTurbo服务执行show操作，作用对象为dir-usage | mandatory |

| 79 | SFSTurbo | ShowFsTask | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/fs/{feature}/tasks/{task_id} | SFSTurboClient.show_fs_task (scripts\sfs\show_fs_task.py:39) | - | 通过SFSTurbo服务执行show操作，作用对象为tasks | mandatory |

| 80 | SFSTurbo | ShowHpcCacheTask | GET | /v1/{project_id}/sfs-turbo/{share_id}/hpc-cache/task/{task_id} | SFSTurboClient.show_hpc_cache_task (scripts\sfs\show_hpc_cache_task.py:37) | - | 通过SFSTurbo服务执行show操作，作用对象为task | mandatory |

| 81 | SFSTurbo | ShowJobDetail | GET | /v1/{project_id}/sfs-turbo/jobs/{job_id} | SFSTurboClient.show_job_detail (scripts\sfs\show_job_detail.py:35) | - | 通过SFSTurbo服务执行show操作，作用对象为jobs | mandatory |

| 82 | SFSTurbo | ShowLdapConfig | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/fs/ldap | SFSTurboClient.show_ldap_config (scripts\sfs\show_ldap_config.py:35) | - | 通过SFSTurbo服务执行show操作，作用对象为ldap | mandatory |

| 83 | SFSTurbo | ShowPermRule | GET | /v1/{project_id}/sfs-turbo/shares/{share_id}/fs/perm-rules/{rule_id} | SFSTurboClient.show_perm_rule (scripts\sfs\show_perm_rule.py:37) | - | 通过SFSTurbo服务执行show操作，作用对象为perm-rules | mandatory |

| 84 | SFSTurbo | ShowQuota | GET | /v1/{project_id}/sfs-turbo/quotas | SFSTurboClient.show_quota (scripts\sfs\show_quota.py:33) | - | 通过SFSTurbo服务执行show操作，作用对象为quotas | mandatory |

| 85 | SFSTurbo | ShowShare | GET | /v1/{project_id}/sfs-turbo/shares/{share_id} | SFSTurboClient.show_share (scripts\sfs\show_share.py:35) | - | 通过SFSTurbo服务执行show操作，作用对象为shares | mandatory |

| 86 | SFSTurbo | ShowSharedTags | GET | /v1/{project_id}/sfs-turbo/{share_id}/tags | SFSTurboClient.show_shared_tags (scripts\sfs\show_shared_tags.py:35) | - | 通过SFSTurbo服务执行show操作，作用对象为tags | mandatory |



## 第二阶段：KooCLI命令一一对应关系与效果完全一致判定

### 阶段结论

共分析86个Open API接口，其中86个存在效果完全一致的KooCLI命令。


| 序号 | Open API接口 | 对应KooCLI命令 | 判定状态 | 差异说明 | 是否可接受 | 信息来源 |
| --- | --- | --- | --- | --- | --- | --- |

| 1 | KeystoneListProjects | hcloud IAM KeystoneListProjects | 效果完全一致 | - | 可接受 | local_cli |

| 2 | CheckAgent | hcloud CBR CheckAgent | 效果完全一致 | - | 可接受 | local_cli |

| 3 | ListAgent | hcloud CBR ListAgent | 效果完全一致 | - | 可接受 | local_cli |

| 4 | ListBackups | hcloud CBR ListBackups | 效果完全一致 | - | 可接受 | local_cli |

| 5 | ListDomainProjects | hcloud CBR ListDomainProjects | 效果完全一致 | - | 可接受 | local_cli |

| 6 | ListExternalVault | hcloud CBR ListExternalVault | 效果完全一致 | - | 可接受 | local_cli |

| 7 | ListFeatures | hcloud CBR ListFeatures | 效果完全一致 | - | 可接受 | local_cli |

| 8 | ListOpLogs | hcloud CBR ListOpLogs | 效果完全一致 | - | 可接受 | local_cli |

| 9 | ListOrganizationPolicies | hcloud CBR ListOrganizationPolicies | 效果完全一致 | - | 可接受 | local_cli |

| 10 | ListOrganizationPolicyDetail | hcloud CBR ListOrganizationPolicyDetail | 效果完全一致 | - | 可接受 | local_cli |

| 11 | ListPolicies | hcloud CBR ListPolicies | 效果完全一致 | - | 可接受 | local_cli |

| 12 | ListProjects | hcloud CBR ListProjects | 效果完全一致 | - | 可接受 | local_cli |

| 13 | ListProtectable | hcloud CBR ListProtectable | 效果完全一致 | - | 可接受 | local_cli |

| 14 | ListVault | hcloud CBR ListVault | 效果完全一致 | - | 可接受 | local_cli |

| 15 | ShowAgent | hcloud CBR ShowAgent | 效果完全一致 | - | 可接受 | local_cli |

| 16 | ShowBackup | hcloud CBR ShowBackup | 效果完全一致 | - | 可接受 | local_cli |

| 17 | ShowCheckpoint | hcloud CBR ShowCheckpoint | 效果完全一致 | - | 可接受 | local_cli |

| 18 | ShowDomain | hcloud CBR ShowDomain | 效果完全一致 | - | 可接受 | local_cli |

| 19 | ShowFeature | hcloud CBR ShowFeature | 效果完全一致 | - | 可接受 | local_cli |

| 20 | ShowMembersDetail | hcloud CBR ShowMembersDetail | 效果完全一致 | - | 可接受 | local_cli |

| 21 | ShowMemberDetail | hcloud CBR ShowMemberDetail | 效果完全一致 | - | 可接受 | local_cli |

| 22 | ShowMetadata | hcloud CBR ShowMetadata | 效果完全一致 | - | 可接受 | local_cli |

| 23 | ShowMigrateStatus | hcloud CBR ShowMigrateStatus | 效果完全一致 | - | 可接受 | local_cli |

| 24 | ShowOpLog | hcloud CBR ShowOpLog | 效果完全一致 | - | 可接受 | local_cli |

| 25 | ShowOrganizationPolicy | hcloud CBR ShowOrganizationPolicy | 效果完全一致 | - | 可接受 | local_cli |

| 26 | ShowPolicy | hcloud CBR ShowPolicy | 效果完全一致 | - | 可接受 | local_cli |

| 27 | ShowProtectable | hcloud CBR ShowProtectable | 效果完全一致 | - | 可接受 | local_cli |

| 28 | ShowReplicationCapabilities | hcloud CBR ShowReplicationCapabilities | 效果完全一致 | - | 可接受 | local_cli |

| 29 | ShowStorageUsage | hcloud CBR ShowStorageUsage | 效果完全一致 | - | 可接受 | local_cli |

| 30 | ShowSummary | hcloud CBR ShowSummary | 效果完全一致 | - | 可接受 | local_cli |

| 31 | ShowVault | hcloud CBR ShowVault | 效果完全一致 | - | 可接受 | local_cli |

| 32 | ShowVaultProjectTag | hcloud CBR ShowVaultProjectTag | 效果完全一致 | - | 可接受 | local_cli |

| 33 | ShowVaultResourceInstances | hcloud CBR ShowVaultResourceInstances | 效果完全一致 | - | 可接受 | local_cli |

| 34 | ShowVaultTag | hcloud CBR ShowVaultTag | 效果完全一致 | - | 可接受 | local_cli |

| 35 | CinderListAvailabilityZones | hcloud Evs CinderListAvailabilityZones | 效果完全一致 | - | 可接受 | local_cli |

| 36 | CinderListQuotas | hcloud Evs CinderListQuotas | 效果完全一致 | - | 可接受 | local_cli |

| 37 | CinderListVolumeTransfers | hcloud Evs CinderListVolumeTransfers | 效果完全一致 | - | 可接受 | local_cli |

| 38 | CinderListVolumeTypes | hcloud Evs CinderListVolumeTypes | 效果完全一致 | - | 可接受 | local_cli |

| 39 | CinderShowVolumeTransfer | hcloud Evs CinderShowVolumeTransfer | 效果完全一致 | - | 可接受 | local_cli |

| 40 | ListSnapshots | hcloud Evs ListSnapshots | 效果完全一致 | - | 可接受 | local_cli |

| 41 | ListVersions | hcloud Evs ListVersions | 效果完全一致 | - | 可接受 | local_cli |

| 42 | ListVolumes | hcloud Evs ListVolumes | 效果完全一致 | - | 可接受 | local_cli |

| 43 | ListVolumesInRecycle | hcloud Evs ListVolumesInRecycle | 效果完全一致 | - | 可接受 | local_cli |

| 44 | ListVolumeTags | hcloud Evs ListVolumeTags | 效果完全一致 | - | 可接受 | local_cli |

| 45 | ShowRecyclePolicy | hcloud Evs ShowRecyclePolicy | 效果完全一致 | - | 可接受 | local_cli |

| 46 | ShowSnapshot | hcloud Evs ShowSnapshot | 效果完全一致 | - | 可接受 | local_cli |

| 47 | ShowVersion | hcloud Evs ShowVersion | 效果完全一致 | - | 可接受 | local_cli |

| 48 | ShowVolume | hcloud Evs ShowVolume | 效果完全一致 | - | 可接受 | local_cli |

| 49 | ShowVolumeInRecycle | hcloud Evs ShowVolumeInRecycle | 效果完全一致 | - | 可接受 | local_cli |

| 50 | ShowVolumeTags | hcloud Evs ShowVolumeTags | 效果完全一致 | - | 可接受 | local_cli |

| 51 | GetBucketAcl | hcloud obs stat | 效果完全一致 | - | 可接受 | local_cli |

| 52 | GetBucketCustomdomain | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 53 | GetBucketMetadata | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 54 | GetBucketNotification | hcloud obs stat | 效果完全一致 | - | 可接受 | local_cli |

| 55 | GetBucketObjectLock | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 56 | GetBucketPolicyPublicStatus | hcloud obs bucketpolicy | 效果完全一致 | - | 可接受 | local_cli |

| 57 | GetBucketPublicAccessBlock | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 58 | GetBucketPublicStatus | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 59 | GetDisPolicy | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 60 | GetObject | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 61 | GetObjectTagging | hcloud obs stat | 效果完全一致 | - | 可接受 | local_cli |

| 62 | HeadObject | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 63 | ListBuckets | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 64 | ListObjects | hcloud obs ls | 效果完全一致 | - | 可接受 | local_cli |

| 65 | ListBackendTargets | hcloud SFSTurbo ListBackendTargets | 效果完全一致 | - | 可接受 | local_cli |

| 66 | ListFsTasks | hcloud SFSTurbo ListFsTasks | 效果完全一致 | - | 可接受 | local_cli |

| 67 | ListHpcCacheTasks | hcloud SFSTurbo ListHpcCacheTasks | 效果完全一致 | - | 可接受 | local_cli |

| 68 | ListPermRules | hcloud SFSTurbo ListPermRules | 效果完全一致 | - | 可接受 | local_cli |

| 69 | ListSharedTags | hcloud SFSTurbo ListSharedTags | 效果完全一致 | - | 可接受 | local_cli |

| 70 | ListShares | hcloud SFSTurbo ListShares | 效果完全一致 | - | 可接受 | local_cli |

| 71 | ListSharesByTag | hcloud SFSTurbo ListSharesByTag | 效果完全一致 | - | 可接受 | local_cli |

| 72 | ListShareTypes | hcloud SFSTurbo ListShareTypes | 效果完全一致 | - | 可接受 | local_cli |

| 73 | ShowActiveDirectoryDomain | hcloud SFSTurbo ShowActiveDirectoryDomain | 效果完全一致 | - | 可接受 | local_cli |

| 74 | ShowBackendTargetInfo | hcloud SFSTurbo ShowBackendTargetInfo | 效果完全一致 | - | 可接受 | local_cli |

| 75 | ShowClientIpInfo | hcloud SFSTurbo ShowClientIpInfo | 效果完全一致 | - | 可接受 | local_cli |

| 76 | ShowFsDir | hcloud SFSTurbo ShowFsDir | 效果完全一致 | - | 可接受 | local_cli |

| 77 | ShowFsDirQuota | hcloud SFSTurbo ShowFsDirQuota | 效果完全一致 | - | 可接受 | local_cli |

| 78 | ShowFsDirUsage | hcloud SFSTurbo ShowFsDirUsage | 效果完全一致 | - | 可接受 | local_cli |

| 79 | ShowFsTask | hcloud SFSTurbo ShowFsTask | 效果完全一致 | - | 可接受 | local_cli |

| 80 | ShowHpcCacheTask | hcloud SFSTurbo ShowHpcCacheTask | 效果完全一致 | - | 可接受 | local_cli |

| 81 | ShowJobDetail | hcloud SFSTurbo ShowJobDetail | 效果完全一致 | - | 可接受 | local_cli |

| 82 | ShowLdapConfig | hcloud SFSTurbo ShowLdapConfig | 效果完全一致 | - | 可接受 | local_cli |

| 83 | ShowPermRule | hcloud SFSTurbo ShowPermRule | 效果完全一致 | - | 可接受 | local_cli |

| 84 | ShowQuota | hcloud SFSTurbo ShowQuota | 效果完全一致 | - | 可接受 | local_cli |

| 85 | ShowShare | hcloud SFSTurbo ShowShare | 效果完全一致 | - | 可接受 | local_cli |

| 86 | ShowSharedTags | hcloud SFSTurbo ShowSharedTags | 效果完全一致 | - | 可接受 | local_cli |





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


