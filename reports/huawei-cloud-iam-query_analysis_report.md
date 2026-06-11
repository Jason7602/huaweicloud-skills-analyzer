# Skill实现原理分析报告 - huawei-cloud-iam-query

## 0. Skill基本信息

| 属性 | 值 |
| --- | --- |
| Skill名称 | huawei-cloud-iam-query |
| 实现方式 | SDK |
| 业务目标 | Queries Huawei Cloud identity and access management resources (IAM) via read-only Python SDK. Covers users, groups, policies, agencies, AK/SK, MFA devices, login/password/ACL policies, security compliance, and account quotas. No write operations. Use this skill when the user needs to query IAM id... |
| 分析状态 | completed |
| 分析时间 | 2026-06-11T01:43:27.714617+00:00 |

## Skill依赖工具

| 依赖项 | 版本/说明 | 功能描述 | 是否必须 |
| --- | --- | --- | --- |
| Python | 3.14 | Skill实现语言及运行时环境 | 必须 |
| SDK: huaweicloudsdkcore | >=3.1.0 | 华为云SDK核心库，提供认证、HTTP请求等基础能力 | 必须 |
| SDK: huaweicloudsdkiam | >=3.1.0 | 身份与访问管理(IAM)服务SDK，用于用户和权限管理 | 必须 |
| KooCLI (hcloud) | 已确认 | 华为云命令行工具，用于通过CLI调用云服务API | 必须 |
| config | 已确认 | 第三方库: config | 必须 |
| platform | 已确认 | 第三方库: platform | 必须 |
| urllib3 | 已确认 | 第三方库: urllib3 | 必须 |

## 第一阶段：目标Skill使用的华为云Open API接口

### 阶段结论

共识别74个Open API接口。

| 序号 | 服务 | Open API接口 | HTTP方法 | API路径 | 来源SDK调用 | 实际使用参数 | 业务作用 | 是否必须 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Iam | KeystoneListProjects | GET | /v3/projects | IamClient.keystone_list_projects (scripts\ensure_env.py:113) | - | 通过Iam服务执行list操作，作用对象为projects | mandatory |
| 2 | Iam | CheckAllProjectsPermissionForAgency | POST | /v3.0/OS-INHERIT/domains/{domain_id}/agencies/{agency_id}/roles/{role_id}/inherited_to_projects | IamClient.check_all_projects_permission_for_agency (scripts\iam\check_all_projects_permission_for_agency.py:38) | - | 通过Iam服务执行check操作，作用对象为inherited_to_projects | mandatory |
| 3 | Iam | CheckDomainPermissionForAgency | POST | /v3.0/OS-AGENCY/domains/{domain_id}/agencies/{agency_id}/roles/{role_id} | IamClient.check_domain_permission_for_agency (scripts\iam\check_domain_permission_for_agency.py:37) | - | 通过Iam服务执行check操作，作用对象为roles | mandatory |
| 4 | Iam | CheckProjectPermissionForAgency | POST | /v3.0/OS-AGENCY/projects/{project_id}/agencies/{agency_id}/roles/{role_id} | IamClient.check_project_permission_for_agency (scripts\iam\check_project_permission_for_agency.py:37) | - | 通过Iam服务执行check操作，作用对象为roles | mandatory |
| 5 | Iam | KeystoneCheckroleForGroup | POST | /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects | IamClient.keystone_checkrole_for_group (scripts\iam\keystone_checkrole_for_group.py:37) | - | 通过Iam服务执行check操作，作用对象为inherited_to_projects | mandatory |
| 6 | Iam | KeystoneCheckDomainPermissionForGroup | POST | /v3/domains/{domain_id}/groups/{group_id}/roles/{role_id} | IamClient.keystone_check_domain_permission_for_group (scripts\iam\keystone_check_domain_permission_for_group.py:37) | - | 通过Iam服务执行check操作，作用对象为roles | mandatory |
| 7 | Iam | KeystoneCheckProjectPermissionForGroup | POST | /v3/projects/{project_id}/groups/{group_id}/roles/{role_id} | IamClient.keystone_check_project_permission_for_group (scripts\iam\keystone_check_project_permission_for_group.py:37) | - | 通过Iam服务执行check操作，作用对象为roles | mandatory |
| 8 | Iam | KeystoneCheckUserInGroup | POST | /v3/groups/{group_id}/users/{user_id} | IamClient.keystone_check_user_in_group (scripts\iam\keystone_check_user_in_group.py:35) | - | 通过Iam服务执行check操作，作用对象为users | mandatory |
| 9 | Iam | KeystoneListAllProjectPermissionsForGroup | GET | /v3/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/inherited_to_projects | IamClient.keystone_list_all_project_permissions_for_group (scripts\iam\keystone_list_all_project_permissions_for_group.py:41) | - | 通过Iam服务执行list操作，作用对象为inherited_to_projects | mandatory |
| 10 | Iam | KeystoneListAuthDomains | GET | /v3/auth/domains | IamClient.keystone_list_auth_domains (scripts\iam\keystone_list_auth_domains.py:39) | - | 通过Iam服务执行list操作，作用对象为domains | mandatory |
| 11 | Iam | KeystoneListAuthProjects | GET | /v3/auth/projects | IamClient.keystone_list_auth_projects (scripts\iam\keystone_list_auth_projects.py:39) | - | 通过Iam服务执行list操作，作用对象为projects | mandatory |
| 12 | Iam | KeystoneListDomainPermissionsForGroup | GET | /v3/domains/{domain_id}/groups/{group_id}/roles | IamClient.keystone_list_domain_permissions_for_group (scripts\iam\keystone_list_domain_permissions_for_group.py:41) | - | 通过Iam服务执行list操作，作用对象为roles | mandatory |
| 13 | Iam | KeystoneListEndpoints | GET | /v3/endpoints | IamClient.keystone_list_endpoints (scripts\iam\keystone_list_endpoints.py:43) | - | 通过Iam服务执行list操作，作用对象为endpoints | mandatory |
| 14 | Iam | KeystoneListFederationDomains | GET | /v3/OS-FEDERATION/domains | IamClient.keystone_list_federation_domains (scripts\iam\keystone_list_federation_domains.py:39) | - | 通过Iam服务执行list操作，作用对象为domains | mandatory |
| 15 | Iam | KeystoneListFederationProjects | GET | /v3/OS-FEDERATION/projects | IamClient.keystone_list_federation_projects (scripts\iam\keystone_list_federation_projects.py:39) | - | 通过Iam服务执行list操作，作用对象为projects | mandatory |
| 16 | Iam | KeystoneListGroups | GET | /v3/groups | IamClient.keystone_list_groups (scripts\iam\keystone_list_groups.py:43) | - | 通过Iam服务执行list操作，作用对象为groups | mandatory |
| 17 | Iam | KeystoneListGroupsForUser | GET | /v3/users/{user_id}/groups | IamClient.keystone_list_groups_for_user (scripts\iam\keystone_list_groups_for_user.py:39) | - | 通过Iam服务执行list操作，作用对象为groups | mandatory |
| 18 | Iam | KeystoneListIdentityProviders | GET | /v3/OS-FEDERATION/identity_providers | IamClient.keystone_list_identity_providers (scripts\iam\keystone_list_identity_providers.py:39) | - | 通过Iam服务执行list操作，作用对象为identity_providers | mandatory |
| 19 | Iam | KeystoneListMappings | GET | /v3/OS-FEDERATION/mappings | IamClient.keystone_list_mappings (scripts\iam\keystone_list_mappings.py:39) | - | 通过Iam服务执行list操作，作用对象为mappings | mandatory |
| 20 | Iam | KeystoneListPermissions | GET | /v3/roles | IamClient.keystone_list_permissions (scripts\iam\keystone_list_permissions.py:67) | - | 通过Iam服务执行list操作，作用对象为roles | mandatory |
| 21 | Iam | KeystoneListProjectsForUser | GET | /v3/users/{user_id}/projects | IamClient.keystone_list_projects_for_user (scripts\iam\keystone_list_projects_for_user.py:39) | - | 通过Iam服务执行list操作，作用对象为projects | mandatory |
| 22 | Iam | KeystoneListProjectPermissionsForGroup | GET | /v3/projects/{project_id}/groups/{group_id}/roles | IamClient.keystone_list_project_permissions_for_group (scripts\iam\keystone_list_project_permissions_for_group.py:41) | - | 通过Iam服务执行list操作，作用对象为roles | mandatory |
| 23 | Iam | KeystoneListProtocols | GET | /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols | IamClient.keystone_list_protocols (scripts\iam\keystone_list_protocols.py:39) | - | 通过Iam服务执行list操作，作用对象为protocols | mandatory |
| 24 | Iam | KeystoneListRegions | GET | /v3/regions | IamClient.keystone_list_regions (scripts\iam\keystone_list_regions.py:39) | - | 通过Iam服务执行list操作，作用对象为regions | mandatory |
| 25 | Iam | KeystoneListServices | GET | /v3/services | IamClient.keystone_list_services (scripts\iam\keystone_list_services.py:40) | - | 通过Iam服务执行list操作，作用对象为services | mandatory |
| 26 | Iam | KeystoneListUsers | GET | /v3/users | IamClient.keystone_list_users (scripts\iam\keystone_list_users.py:49) | - | 通过Iam服务执行list操作，作用对象为users | mandatory |
| 27 | Iam | KeystoneListUsersForGroupByAdmin | GET | /v3/groups/{group_id}/users | IamClient.keystone_list_users_for_group_by_admin (scripts\iam\keystone_list_users_for_group_by_admin.py:39) | - | 通过Iam服务执行list操作，作用对象为users | mandatory |
| 28 | Iam | KeystoneListVersions | GET | / | IamClient.keystone_list_versions (scripts\iam\keystone_list_versions.py:39) | - | 通过Iam服务执行list操作 | mandatory |
| 29 | Iam | KeystoneShowCatalog | GET | /v3/auth/catalog | IamClient.keystone_show_catalog (scripts\iam\keystone_show_catalog.py:33) | - | 通过Iam服务执行show操作，作用对象为catalog | mandatory |
| 30 | Iam | KeystoneShowEndpoint | GET | /v3/endpoints/{endpoint_id} | IamClient.keystone_show_endpoint (scripts\iam\keystone_show_endpoint.py:33) | - | 通过Iam服务执行show操作，作用对象为endpoints | mandatory |
| 31 | Iam | KeystoneShowGroup | GET | /v3/groups/{group_id} | IamClient.keystone_show_group (scripts\iam\keystone_show_group.py:33) | - | 通过Iam服务执行show操作，作用对象为groups | mandatory |
| 32 | Iam | KeystoneShowIdentityProvider | GET | /v3/OS-FEDERATION/identity_providers/{id} | IamClient.keystone_show_identity_provider (scripts\iam\keystone_show_identity_provider.py:33) | - | 通过Iam服务执行show操作，作用对象为identity_providers | mandatory |
| 33 | Iam | KeystoneShowMapping | GET | /v3/OS-FEDERATION/mappings/{id} | IamClient.keystone_show_mapping (scripts\iam\keystone_show_mapping.py:33) | - | 通过Iam服务执行show操作，作用对象为mappings | mandatory |
| 34 | Iam | KeystoneShowPermission | GET | /v3/roles/{role_id} | IamClient.keystone_show_permission (scripts\iam\keystone_show_permission.py:33) | - | 通过Iam服务执行show操作，作用对象为roles | mandatory |
| 35 | Iam | KeystoneShowProject | GET | /v3/projects/{project_id} | IamClient.keystone_show_project (scripts\iam\keystone_show_project.py:33) | - | 通过Iam服务执行show操作，作用对象为projects | mandatory |
| 36 | Iam | KeystoneShowProtocol | GET | /v3/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id} | IamClient.keystone_show_protocol (scripts\iam\keystone_show_protocol.py:35) | - | 通过Iam服务执行show操作，作用对象为protocols | mandatory |
| 37 | Iam | KeystoneShowRegion | GET | /v3/regions/{region_id} | IamClient.keystone_show_region (scripts\iam\keystone_show_region.py:33) | - | 通过Iam服务执行show操作，作用对象为regions | mandatory |
| 38 | Iam | KeystoneShowSecurityCompliance | GET | /v3/domains/{domain_id}/config/security_compliance | IamClient.keystone_show_security_compliance (scripts\iam\keystone_show_security_compliance.py:33) | - | 通过Iam服务执行show操作，作用对象为security_compliance | mandatory |
| 39 | Iam | KeystoneShowSecurityComplianceByOption | GET | /v3/domains/{domain_id}/config/security_compliance/{option} | IamClient.keystone_show_security_compliance_by_option (scripts\iam\keystone_show_security_compliance_by_option.py:35) | - | 通过Iam服务执行show操作，作用对象为security_compliance | mandatory |
| 40 | Iam | KeystoneShowService | GET | /v3/services/{service_id} | IamClient.keystone_show_service (scripts\iam\keystone_show_service.py:33) | - | 通过Iam服务执行show操作，作用对象为services | mandatory |
| 41 | Iam | KeystoneShowUser | GET | /v3/users/{user_id} | IamClient.keystone_show_user (scripts\iam\keystone_show_user.py:33) | - | 通过Iam服务执行show操作，作用对象为users | mandatory |
| 42 | Iam | KeystoneShowVersion | GET | /v3 | IamClient.keystone_show_version (scripts\iam\keystone_show_version.py:33) | - | 通过Iam服务执行show操作 | mandatory |
| 43 | Iam | KeystoneValidateToken | GET | /v3/auth/tokens | IamClient.keystone_validate_token (scripts\iam\keystone_validate_token.py:36) | - | 通过Iam服务执行KeystoneValidateToken操作，作用对象为tokens | mandatory |
| 44 | Iam | ListAgencies | GET | /v3.0/OS-AGENCY/agencies | IamClient.list_agencies (scripts\iam\list_agencies.py:58) | - | 通过Iam服务执行list操作，作用对象为agencies | mandatory |
| 45 | Iam | ListAllProjectsPermissionsForAgency | GET | /v3.0/OS-INHERIT/domains/{domain_id}/agencies/{agency_id}/roles/inherited_to_projects | IamClient.list_all_projects_permissions_for_agency (scripts\iam\list_all_projects_permissions_for_agency.py:42) | - | 通过Iam服务执行list操作，作用对象为inherited_to_projects | mandatory |
| 46 | Iam | ListCustomPolicies | GET | /v3.0/OS-ROLE/roles | IamClient.list_custom_policies (scripts\iam\list_custom_policies.py:85) | - | 通过Iam服务执行list操作，作用对象为roles | mandatory |
| 47 | Iam | ListDomainPermissionsForAgency | GET | /v3.0/OS-AGENCY/domains/{domain_id}/agencies/{agency_id}/roles | IamClient.list_domain_permissions_for_agency (scripts\iam\list_domain_permissions_for_agency.py:85) | - | 通过Iam服务执行list操作，作用对象为roles | mandatory |
| 48 | Iam | ListEnterpriseProjectsForGroup | GET | /v3.0/OS-PERMISSION/groups/{group_id}/enterprise-projects | IamClient.list_enterprise_projects_for_group (scripts\iam\list_enterprise_projects_for_group.py:74) | - | 通过Iam服务执行list操作，作用对象为enterprise-projects | mandatory |
| 49 | Iam | ListEnterpriseProjectsForUser | GET | /v3.0/OS-PERMISSION/users/{user_id}/enterprise-projects | IamClient.list_enterprise_projects_for_user (scripts\iam\list_enterprise_projects_for_user.py:74) | - | 通过Iam服务执行list操作，作用对象为enterprise-projects | mandatory |
| 50 | Iam | ListGroupsForEnterpriseProject | GET | /v3.0/OS-PERMISSION/enterprise-projects/{enterprise_project_id}/groups | IamClient.list_groups_for_enterprise_project (scripts\iam\list_groups_for_enterprise_project.py:78) | - | 通过Iam服务执行list操作，作用对象为groups | mandatory |
| 51 | Iam | ListPermanentAccessKeys | GET | /v3.0/OS-CREDENTIAL/credentials | IamClient.list_permanent_access_keys (scripts\iam\list_permanent_access_keys.py:79) | - | 通过Iam服务执行list操作，作用对象为credentials | mandatory |
| 52 | Iam | ListProjectPermissionsForAgency | GET | /v3.0/OS-AGENCY/projects/{project_id}/agencies/{agency_id}/roles | IamClient.list_project_permissions_for_agency (scripts\iam\list_project_permissions_for_agency.py:85) | - | 通过Iam服务执行list操作，作用对象为roles | mandatory |
| 53 | Iam | ListRolesForGroupOnEnterpriseProject | GET | /v3.0/OS-PERMISSION/enterprise-projects/{enterprise_project_id}/groups/{group_id}/roles | IamClient.list_roles_for_group_on_enterprise_project (scripts\iam\list_roles_for_group_on_enterprise_project.py:82) | - | 通过Iam服务执行list操作，作用对象为roles | mandatory |
| 54 | Iam | ListRolesForUserOnEnterpriseProject | GET | /v3.0/OS-PERMISSION/enterprise-projects/{enterprise_project_id}/users/{user_id}/roles | IamClient.list_roles_for_user_on_enterprise_project (scripts\iam\list_roles_for_user_on_enterprise_project.py:82) | - | 通过Iam服务执行list操作，作用对象为roles | mandatory |
| 55 | Iam | ListUsersForEnterpriseProject | GET | /v3.0/OS-PERMISSION/enterprise-projects/{enterprise_project_id}/users | IamClient.list_users_for_enterprise_project (scripts\iam\list_users_for_enterprise_project.py:99) | - | 通过Iam服务执行list操作，作用对象为users | mandatory |
| 56 | Iam | ListUserLoginProtects | GET | /v3.0/OS-USER/login-protects | IamClient.list_user_login_protects (scripts\iam\list_user_login_protects.py:74) | - | 通过Iam服务执行list操作，作用对象为login-protects | mandatory |
| 57 | Iam | ListUserMfaDevices | GET | /v3.0/OS-MFA/virtual-mfa-devices | IamClient.list_user_mfa_devices (scripts\iam\list_user_mfa_devices.py:73) | - | 通过Iam服务执行list操作，作用对象为OS-MFA | mandatory |
| 58 | Iam | ShowAgency | GET | /v3.0/OS-AGENCY/agencies/{agency_id} | IamClient.show_agency (scripts\iam\show_agency.py:34) | - | 通过Iam服务执行show操作，作用对象为agencies | mandatory |
| 59 | Iam | ShowCustomPolicy | GET | /v3.0/OS-ROLE/roles/{role_id} | IamClient.show_custom_policy (scripts\iam\show_custom_policy.py:34) | - | 通过Iam服务执行show操作，作用对象为roles | mandatory |
| 60 | Iam | ShowDomainApiAclPolicy | GET | /v3.0/OS-SECURITYPOLICY/domains/{domain_id}/api-acl-policy | IamClient.show_domain_api_acl_policy (scripts\iam\show_domain_api_acl_policy.py:34) | - | 通过Iam服务执行show操作，作用对象为api-acl-policy | mandatory |
| 61 | Iam | ShowDomainConsoleAclPolicy | GET | /v3.0/OS-SECURITYPOLICY/domains/{domain_id}/console-acl-policy | IamClient.show_domain_console_acl_policy (scripts\iam\show_domain_console_acl_policy.py:34) | - | 通过Iam服务执行show操作，作用对象为console-acl-policy | mandatory |
| 62 | Iam | ShowDomainLoginPolicy | GET | /v3.0/OS-SECURITYPOLICY/domains/{domain_id}/login-policy | IamClient.show_domain_login_policy (scripts\iam\show_domain_login_policy.py:34) | - | 通过Iam服务执行show操作，作用对象为login-policy | mandatory |
| 63 | Iam | ShowDomainPasswordPolicy | GET | /v3.0/OS-SECURITYPOLICY/domains/{domain_id}/password-policy | IamClient.show_domain_password_policy (scripts\iam\show_domain_password_policy.py:34) | - | 通过Iam服务执行show操作，作用对象为password-policy | mandatory |
| 64 | Iam | ShowDomainProtectPolicy | GET | /v3.0/OS-SECURITYPOLICY/domains/{domain_id}/protect-policy | IamClient.show_domain_protect_policy (scripts\iam\show_domain_protect_policy.py:34) | - | 通过Iam服务执行show操作，作用对象为protect-policy | mandatory |
| 65 | Iam | ShowDomainQuota | GET | /v3.0/OS-QUOTA/domains/{domain_id} | IamClient.show_domain_quota (scripts\iam\show_domain_quota.py:37) | - | 通过Iam服务执行show操作，作用对象为domains | mandatory |
| 66 | Iam | ShowDomainRoleAssignments | GET | /v3.0/OS-PERMISSION/role-assignments | IamClient.show_domain_role_assignments (scripts\iam\show_domain_role_assignments.py:73) | - | 通过Iam服务执行show操作，作用对象为role-assignments | mandatory |
| 67 | Iam | ShowMetadata | GET | /v3-ext/OS-FEDERATION/identity_providers/{idp_id}/protocols/{protocol_id}/metadata | IamClient.show_metadata (scripts\iam\show_metadata.py:35) | - | 通过Iam服务执行show操作，作用对象为metadata | mandatory |
| 68 | Iam | ShowOpenIdConnectConfig | GET | /v3.0/OS-FEDERATION/identity-providers/{idp_id}/openid-connect-config | IamClient.show_open_id_connect_config (scripts\iam\show_open_id_connect_config.py:34) | - | 通过Iam服务执行show操作，作用对象为openid-connect-config | mandatory |
| 69 | Iam | ShowPermanentAccessKey | GET | /v3.0/OS-CREDENTIAL/credentials/{access_key} | IamClient.show_permanent_access_key (scripts\iam\show_permanent_access_key.py:34) | - | 通过Iam服务执行show操作，作用对象为credentials | mandatory |
| 70 | Iam | ShowProjectDetailsAndStatus | GET | /v3-ext/projects/{project_id} | IamClient.show_project_details_and_status (scripts\iam\show_project_details_and_status.py:34) | - | 通过Iam服务执行show操作，作用对象为projects | mandatory |
| 71 | Iam | ShowProjectQuota | GET | /v3.0/OS-QUOTA/projects/{project_id} | IamClient.show_project_quota (scripts\iam\show_project_quota.py:34) | - | 通过Iam服务执行show操作，作用对象为projects | mandatory |
| 72 | Iam | ShowUser | GET | /v3.0/OS-USER/users/{user_id} | IamClient.show_user (scripts\iam\show_user.py:34) | - | 通过Iam服务执行show操作，作用对象为users | mandatory |
| 73 | Iam | ShowUserLoginProtect | GET | /v3.0/OS-USER/users/{user_id}/login-protect | IamClient.show_user_login_protect (scripts\iam\show_user_login_protect.py:33) | - | 通过Iam服务执行show操作，作用对象为login-protect | mandatory |
| 74 | Iam | ShowUserMfaDevice | GET | /v3.0/OS-MFA/users/{user_id}/virtual-mfa-device | IamClient.show_user_mfa_device (scripts\iam\show_user_mfa_device.py:33) | - | 通过Iam服务执行show操作，作用对象为users | mandatory |

## 第二阶段：KooCLI命令一一对应关系与效果完全一致判定

### 阶段结论

共分析74个Open API接口，其中74个存在效果完全一致的KooCLI命令。

| 序号 | Open API接口 | 对应KooCLI命令 | 判定状态 | 差异说明 | 是否可接受 | 信息来源 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | KeystoneListProjects | hcloud Iam KeystoneListProjects | 效果完全一致 | - | 可接受 | local_cli |
| 2 | CheckAllProjectsPermissionForAgency | hcloud Iam CheckAllProjectsPermissionForAgency | 效果完全一致 | - | 可接受 | local_cli |
| 3 | CheckDomainPermissionForAgency | hcloud Iam CheckDomainPermissionForAgency | 效果完全一致 | - | 可接受 | local_cli |
| 4 | CheckProjectPermissionForAgency | hcloud Iam CheckProjectPermissionForAgency | 效果完全一致 | - | 可接受 | local_cli |
| 5 | KeystoneCheckroleForGroup | hcloud Iam KeystoneCheckroleForGroup | 效果完全一致 | - | 可接受 | local_cli |
| 6 | KeystoneCheckDomainPermissionForGroup | hcloud Iam KeystoneCheckDomainPermissionForGroup | 效果完全一致 | - | 可接受 | local_cli |
| 7 | KeystoneCheckProjectPermissionForGroup | hcloud Iam KeystoneCheckProjectPermissionForGroup | 效果完全一致 | - | 可接受 | local_cli |
| 8 | KeystoneCheckUserInGroup | hcloud Iam KeystoneCheckUserInGroup | 效果完全一致 | - | 可接受 | local_cli |
| 9 | KeystoneListAllProjectPermissionsForGroup | hcloud Iam KeystoneListAllProjectPermissionsForGroup | 效果完全一致 | - | 可接受 | local_cli |
| 10 | KeystoneListAuthDomains | hcloud Iam KeystoneListAuthDomains | 效果完全一致 | - | 可接受 | local_cli |
| 11 | KeystoneListAuthProjects | hcloud Iam KeystoneListAuthProjects | 效果完全一致 | - | 可接受 | local_cli |
| 12 | KeystoneListDomainPermissionsForGroup | hcloud Iam KeystoneListDomainPermissionsForGroup | 效果完全一致 | - | 可接受 | local_cli |
| 13 | KeystoneListEndpoints | hcloud Iam KeystoneListEndpoints | 效果完全一致 | - | 可接受 | local_cli |
| 14 | KeystoneListFederationDomains | hcloud Iam KeystoneListFederationDomains | 效果完全一致 | - | 可接受 | local_cli |
| 15 | KeystoneListFederationProjects | hcloud Iam KeystoneListFederationProjects | 效果完全一致 | - | 可接受 | local_cli |
| 16 | KeystoneListGroups | hcloud Iam KeystoneListGroups | 效果完全一致 | - | 可接受 | local_cli |
| 17 | KeystoneListGroupsForUser | hcloud Iam KeystoneListGroupsForUser | 效果完全一致 | - | 可接受 | local_cli |
| 18 | KeystoneListIdentityProviders | hcloud Iam KeystoneListIdentityProviders | 效果完全一致 | - | 可接受 | local_cli |
| 19 | KeystoneListMappings | hcloud Iam KeystoneListMappings | 效果完全一致 | - | 可接受 | local_cli |
| 20 | KeystoneListPermissions | hcloud Iam KeystoneListPermissions | 效果完全一致 | - | 可接受 | local_cli |
| 21 | KeystoneListProjectsForUser | hcloud Iam KeystoneListProjectsForUser | 效果完全一致 | - | 可接受 | local_cli |
| 22 | KeystoneListProjectPermissionsForGroup | hcloud Iam KeystoneListProjectPermissionsForGroup | 效果完全一致 | - | 可接受 | local_cli |
| 23 | KeystoneListProtocols | hcloud Iam KeystoneListProtocols | 效果完全一致 | - | 可接受 | local_cli |
| 24 | KeystoneListRegions | hcloud Iam KeystoneListRegions | 效果完全一致 | - | 可接受 | local_cli |
| 25 | KeystoneListServices | hcloud Iam KeystoneListServices | 效果完全一致 | - | 可接受 | local_cli |
| 26 | KeystoneListUsers | hcloud Iam KeystoneListUsers | 效果完全一致 | - | 可接受 | local_cli |
| 27 | KeystoneListUsersForGroupByAdmin | hcloud Iam KeystoneListUsersForGroupByAdmin | 效果完全一致 | - | 可接受 | local_cli |
| 28 | KeystoneListVersions | hcloud Iam KeystoneListVersions | 效果完全一致 | - | 可接受 | local_cli |
| 29 | KeystoneShowCatalog | hcloud Iam KeystoneShowCatalog | 效果完全一致 | - | 可接受 | local_cli |
| 30 | KeystoneShowEndpoint | hcloud Iam KeystoneShowEndpoint | 效果完全一致 | - | 可接受 | local_cli |
| 31 | KeystoneShowGroup | hcloud Iam KeystoneShowGroup | 效果完全一致 | - | 可接受 | local_cli |
| 32 | KeystoneShowIdentityProvider | hcloud Iam KeystoneShowIdentityProvider | 效果完全一致 | - | 可接受 | local_cli |
| 33 | KeystoneShowMapping | hcloud Iam KeystoneShowMapping | 效果完全一致 | - | 可接受 | local_cli |
| 34 | KeystoneShowPermission | hcloud Iam KeystoneShowPermission | 效果完全一致 | - | 可接受 | local_cli |
| 35 | KeystoneShowProject | hcloud Iam KeystoneShowProject | 效果完全一致 | - | 可接受 | local_cli |
| 36 | KeystoneShowProtocol | hcloud Iam KeystoneShowProtocol | 效果完全一致 | - | 可接受 | local_cli |
| 37 | KeystoneShowRegion | hcloud Iam KeystoneShowRegion | 效果完全一致 | - | 可接受 | local_cli |
| 38 | KeystoneShowSecurityCompliance | hcloud Iam KeystoneShowSecurityCompliance | 效果完全一致 | - | 可接受 | local_cli |
| 39 | KeystoneShowSecurityComplianceByOption | hcloud Iam KeystoneShowSecurityComplianceByOption | 效果完全一致 | - | 可接受 | local_cli |
| 40 | KeystoneShowService | hcloud Iam KeystoneShowService | 效果完全一致 | - | 可接受 | local_cli |
| 41 | KeystoneShowUser | hcloud Iam KeystoneShowUser | 效果完全一致 | - | 可接受 | local_cli |
| 42 | KeystoneShowVersion | hcloud Iam KeystoneShowVersion | 效果完全一致 | - | 可接受 | local_cli |
| 43 | KeystoneValidateToken | hcloud Iam KeystoneValidateToken | 效果完全一致 | - | 可接受 | local_cli |
| 44 | ListAgencies | hcloud Iam ListAgencies | 效果完全一致 | - | 可接受 | local_cli |
| 45 | ListAllProjectsPermissionsForAgency | hcloud Iam ListAllProjectsPermissionsForAgency | 效果完全一致 | - | 可接受 | local_cli |
| 46 | ListCustomPolicies | hcloud Iam ListCustomPolicies | 效果完全一致 | - | 可接受 | local_cli |
| 47 | ListDomainPermissionsForAgency | hcloud Iam ListDomainPermissionsForAgency | 效果完全一致 | - | 可接受 | local_cli |
| 48 | ListEnterpriseProjectsForGroup | hcloud Iam ListEnterpriseProjectsForGroup | 效果完全一致 | - | 可接受 | local_cli |
| 49 | ListEnterpriseProjectsForUser | hcloud Iam ListEnterpriseProjectsForUser | 效果完全一致 | - | 可接受 | local_cli |
| 50 | ListGroupsForEnterpriseProject | hcloud Iam ListGroupsForEnterpriseProject | 效果完全一致 | - | 可接受 | local_cli |
| 51 | ListPermanentAccessKeys | hcloud Iam ListPermanentAccessKeys | 效果完全一致 | - | 可接受 | local_cli |
| 52 | ListProjectPermissionsForAgency | hcloud Iam ListProjectPermissionsForAgency | 效果完全一致 | - | 可接受 | local_cli |
| 53 | ListRolesForGroupOnEnterpriseProject | hcloud Iam ListRolesForGroupOnEnterpriseProject | 效果完全一致 | - | 可接受 | local_cli |
| 54 | ListRolesForUserOnEnterpriseProject | hcloud Iam ListRolesForUserOnEnterpriseProject | 效果完全一致 | - | 可接受 | local_cli |
| 55 | ListUsersForEnterpriseProject | hcloud Iam ListUsersForEnterpriseProject | 效果完全一致 | - | 可接受 | local_cli |
| 56 | ListUserLoginProtects | hcloud Iam ListUserLoginProtects | 效果完全一致 | - | 可接受 | local_cli |
| 57 | ListUserMfaDevices | hcloud Iam ListUserMfaDevices | 效果完全一致 | - | 可接受 | local_cli |
| 58 | ShowAgency | hcloud Iam ShowAgency | 效果完全一致 | - | 可接受 | local_cli |
| 59 | ShowCustomPolicy | hcloud Iam ShowCustomPolicy | 效果完全一致 | - | 可接受 | local_cli |
| 60 | ShowDomainApiAclPolicy | hcloud Iam ShowDomainApiAclPolicy | 效果完全一致 | - | 可接受 | local_cli |
| 61 | ShowDomainConsoleAclPolicy | hcloud Iam ShowDomainConsoleAclPolicy | 效果完全一致 | - | 可接受 | local_cli |
| 62 | ShowDomainLoginPolicy | hcloud Iam ShowDomainLoginPolicy | 效果完全一致 | - | 可接受 | local_cli |
| 63 | ShowDomainPasswordPolicy | hcloud Iam ShowDomainPasswordPolicy | 效果完全一致 | - | 可接受 | local_cli |
| 64 | ShowDomainProtectPolicy | hcloud Iam ShowDomainProtectPolicy | 效果完全一致 | - | 可接受 | local_cli |
| 65 | ShowDomainQuota | hcloud Iam ShowDomainQuota | 效果完全一致 | - | 可接受 | local_cli |
| 66 | ShowDomainRoleAssignments | hcloud Iam ShowDomainRoleAssignments | 效果完全一致 | - | 可接受 | local_cli |
| 67 | ShowMetadata | hcloud Iam ShowMetadata | 效果完全一致 | - | 可接受 | local_cli |
| 68 | ShowOpenIdConnectConfig | hcloud Iam ShowOpenIdConnectConfig | 效果完全一致 | - | 可接受 | local_cli |
| 69 | ShowPermanentAccessKey | hcloud Iam ShowPermanentAccessKey | 效果完全一致 | - | 可接受 | local_cli |
| 70 | ShowProjectDetailsAndStatus | hcloud Iam ShowProjectDetailsAndStatus | 效果完全一致 | - | 可接受 | local_cli |
| 71 | ShowProjectQuota | hcloud Iam ShowProjectQuota | 效果完全一致 | - | 可接受 | local_cli |
| 72 | ShowUser | hcloud Iam ShowUser | 效果完全一致 | - | 可接受 | local_cli |
| 73 | ShowUserLoginProtect | hcloud Iam ShowUserLoginProtect | 效果完全一致 | - | 可接受 | local_cli |
| 74 | ShowUserMfaDevice | hcloud Iam ShowUser | 效果完全一致 | - | 可接受 | local_cli |



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


