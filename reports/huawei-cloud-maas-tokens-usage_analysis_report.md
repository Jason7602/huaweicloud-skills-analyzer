# Skill实现原理分析报告 - huawei-cloud-maas-tokens-usage

## 0. Skill基本信息

| 属性 | 值 |
| --- | --- |
| Skill名称 | huawei-cloud-maas-tokens-usage |
| 实现方式 | SDK |
| 业务目标 | Query Huawei Cloud MaaS (Model as a Service) tokens usage statistics, including total tokens, prompt tokens, completion tokens, total requests, and total errors. Supports preset service, my service, and custom endpoint with time range queries (last 7/14/30 days or custom). Data source is MaaS Sho... |
| 分析状态 | completed |
| 分析时间 | 2026-06-11T08:49:40.662317+00:00 |

## Skill依赖工具

| 依赖项 | 版本/说明 | 功能描述 | 是否必须 |
| --- | --- | --- | --- |
| Python | 3.14 | Skill实现语言及运行时环境 | 必须 |
| SDK: huaweicloudsdkcore | 已确认 | 华为云SDK核心库，提供认证、HTTP请求等基础能力 | 必须 |
| requests | 已确认 | HTTP请求库，用于调用REST API | 必须 |
| urllib3 | 已确认 | 第三方库: urllib3 | 必须 |

## 第一阶段：目标Skill使用的华为云Open API接口

### 阶段结论

共识别2个Open API接口。

| 序号 | 服务 | Open API接口 | HTTP方法 | API路径 | 来源SDK调用 | 实际使用参数 | 业务作用 | 是否必须 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | modelarts | ShowStatistics | GET | /v1/{var}/maas/monitoring/show-statistics | SignerBypass.show_statistics (scripts\maas_rest_usage_stats.py:68) | resource_path, http_method | 通过modelarts服务执行show操作，作用对象为show-statistics | mandatory |
| 2 | iam | KeystoneListProjects | GET | /v3/projects | SignerBypass.keystone_list_projects (scripts\maas_rest_usage_stats.py:90) | resource_path, http_method | 通过iam服务执行list操作，作用对象为projects | mandatory |

## 第二阶段：KooCLI命令一一对应关系与效果完全一致判定

### 阶段结论

共分析2个Open API接口，其中1个存在效果完全一致的KooCLI命令。

| 序号 | Open API接口 | 对应KooCLI命令 | 判定状态 | 差异说明 | 是否可接受 | 信息来源 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ShowStatistics | - | 无对应命令 | 无对应KooCLI命令 | 不可接受 | none |
| 2 | KeystoneListProjects | hcloud IAM KeystoneListProjects | 效果完全一致 | - | 可接受 | local_cli |


### 不完全一致或无对应命令接口清单
- ShowStatistics（[API Explorer查询](https://console.huaweicloud.com/apiexplorer/#/openapi/MODELARTS/cli?api=ShowStatistics)）

通过在本地实际使用KooCLI命令查询，发现ShowStatistics确实没有与之对应的KooCLI命令。


## 第三阶段：全部改用KooCLI后的业务效果等价性结论

| 项目 | 内容 |
| --- | --- |
| 替换结论 | 不能完全替换 |
| 结论原因 | 存在必须接口无对应KooCLI命令。 |

### 关键阻塞点

| 序号 | 关联接口 | 阻塞原因 | 业务影响 | 建议处理方式 |
| --- | --- | --- | --- | --- |
| 1 | ShowStatistics | 无对应KooCLI命令 | 无法完全迁移该接口能力 | 保留SDK实现或人工验证KooCLI组合命令是否可接受 |

## 第四阶段：KooCLI本地验证结论

基于规则分析，存在必须接口无法通过KooCLI实现等效替换（ShowStatistics），结论为不能完全替换。存在必须接口无对应KooCLI命令。建议保留这些接口的SDK实现方式，或探索KooCLI组合命令是否可达到近似业务效果。

## 最终结论


该Skill是否能够全部改用KooCLI并达到与Huawei Cloud SDK实现一致的业务效果：**不能完全替换**。

原因：存在必须接口无对应KooCLI命令。


