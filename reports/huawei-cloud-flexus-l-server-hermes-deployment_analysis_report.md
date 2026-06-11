# Skill实现原理分析报告 - huawei-cloud-flexus-l-server-hermes-deployment

## 0. Skill基本信息

| 属性 | 值 |
| --- | --- |
| Skill名称 | huawei-cloud-flexus-l-server-hermes-deployment |
| 实现方式 | SDK |
| 业务目标 | One-click deployment tool for Hermes on Huawei Cloud Flexus L instances. Supports one-click deployment, ModelArts large model configuration, and robot channel configuration. This skill provides a complete workflow for deploying and configuring Hermes AI Agent platform. Trigger words: "Deploy Herm... |
| 分析状态 | completed |
| 分析时间 | 2026-06-11T08:49:17.035565+00:00 |

## Skill依赖工具

| 依赖项 | 版本/说明 | 功能描述 | 是否必须 |
| --- | --- | --- | --- |
| Python | 3.14 | Skill实现语言及运行时环境 | 必须 |
| SDK: huaweicloudsdkcoc | 已确认 | coc服务SDK: 1. COC Service Region (--region-id)**: The region where COC API service is located (cn-north-4, ap-southeast-3, eu-west-101) | 必须 |
| SDK: huaweicloudsdkcore | 已确认 | 华为云SDK核心库，提供认证、HTTP请求等基础能力 | 必须 |
| getpass | 已确认 | 第三方库: getpass | 必须 |
| requests | 已确认 | HTTP请求库，用于调用REST API | 必须 |
| scripts | 已确认 | 第三方库: scripts | 必须 |
| unittest | 已确认 | 第三方库: unittest | 必须 |
| uuid | 已确认 | 第三方库: uuid | 必须 |
| warnings | 已确认 | 第三方库: warnings | 必须 |

## 第一阶段：目标Skill使用的华为云Open API接口

### 阶段结论

共识别8个Open API接口。

| 序号 | 服务 | Open API接口 | HTTP方法 | API路径 | 来源SDK调用 | 实际使用参数 | 业务作用 | 是否必须 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | iam | KeystoneListProjects | GET | /v3/projects | SignerBypass.keystone_list_projects (scripts\lib.py:115) | resource_path, http_method | 通过iam服务执行list操作，作用对象为projects | mandatory |
| 2 | hcss | CreateLightInstances | POST | /v1/light-instances | SignerBypass.create_light_instances (scripts\lib.py:251) | resource_path, http_method | 通过hcss服务执行create操作，作用对象为light-instances | mandatory |
| 3 | Coc | CreateScript | POST | /v1/job/scripts | CocClient.create_script (scripts\lib.py:902) | - | 通过Coc服务执行create操作，作用对象为scripts | mandatory |
| 4 | Coc | ExecuteScript | POST | /v1/job/scripts/{script_uuid} | CocClient.execute_script (scripts\lib.py:1035) | - | 通过Coc服务执行ExecuteScript操作，作用对象为scripts | mandatory |
| 5 | Coc | GetScriptJobBatch | GET | /v1/job/script/orders/{execute_uuid}/batches/{batch_index} | CocClient.get_script_job_batch (scripts\lib.py:1219) | - | 通过Coc服务执行get操作，作用对象为batches | mandatory |
| 6 | Coc | GetScript | GET | /v1/job/scripts/{script_uuid} | CocClient.get_script (scripts\lib.py:1322) | - | 通过Coc服务执行get操作，作用对象为scripts | mandatory |
| 7 | Coc | ListScripts | GET | /v1/job/scripts | CocClient.list_scripts (scripts\lib.py:1366) | - | 通过Coc服务执行list操作，作用对象为scripts | mandatory |
| 8 | coc | ListResources | GET | /v1/resources | SignerBypass.list_resources (scripts\lib.py:1770) | resource_path, http_method | 通过coc服务执行list操作，作用对象为resources | mandatory |

## 第二阶段：KooCLI命令一一对应关系与效果完全一致判定

### 阶段结论

共分析8个Open API接口，其中7个存在效果完全一致的KooCLI命令。

| 序号 | Open API接口 | 对应KooCLI命令 | 判定状态 | 差异说明 | 是否可接受 | 信息来源 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | KeystoneListProjects | hcloud iam KeystoneListProjects | 效果完全一致 | - | 可接受 | local_cli |
| 2 | CreateLightInstances | - | 无对应命令 | 无对应KooCLI命令 | 不可接受 | none |
| 3 | CreateScript | hcloud COC CreateScript | 效果完全一致 | - | 可接受 | local_cli |
| 4 | ExecuteScript | hcloud COC ExecuteScript | 效果完全一致 | - | 可接受 | local_cli |
| 5 | GetScriptJobBatch | hcloud COC GetScriptJobBatch | 效果完全一致 | - | 可接受 | local_cli |
| 6 | GetScript | hcloud COC GetScript | 效果完全一致 | - | 可接受 | local_cli |
| 7 | ListScripts | hcloud COC ListScripts | 效果完全一致 | - | 可接受 | local_cli |
| 8 | ListResources | hcloud COC ListResources | 效果完全一致 | - | 可接受 | local_cli |


### 不完全一致或无对应命令接口清单
- CreateLightInstances（[API Explorer查询](https://console.huaweicloud.com/apiexplorer/#/openapi/HCSS/cli?api=CreateLightInstances)）

通过在本地实际使用KooCLI命令查询，发现CreateLightInstances确实没有与之对应的KooCLI命令。


## 第三阶段：全部改用KooCLI后的业务效果等价性结论

| 项目 | 内容 |
| --- | --- |
| 替换结论 | 不能完全替换 |
| 结论原因 | 存在必须接口无对应KooCLI命令。 |

### 关键阻塞点

| 序号 | 关联接口 | 阻塞原因 | 业务影响 | 建议处理方式 |
| --- | --- | --- | --- | --- |
| 1 | CreateLightInstances | 无对应KooCLI命令 | 无法完全迁移该接口能力 | 保留SDK实现或人工验证KooCLI组合命令是否可接受 |

## 第四阶段：KooCLI本地验证结论

基于规则分析，存在必须接口无法通过KooCLI实现等效替换（CreateLightInstances），结论为不能完全替换。存在必须接口无对应KooCLI命令。建议保留这些接口的SDK实现方式，或探索KooCLI组合命令是否可达到近似业务效果。

## 最终结论


该Skill是否能够全部改用KooCLI并达到与Huawei Cloud SDK实现一致的业务效果：**不能完全替换**。

原因：存在必须接口无对应KooCLI命令。


