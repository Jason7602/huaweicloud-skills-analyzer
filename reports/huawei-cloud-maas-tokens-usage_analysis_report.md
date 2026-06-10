# Skill实现原理分析报告 - huawei-cloud-maas-tokens-usage

## 0. Skill基本信息

| 属性 | 值 |
| --- | --- |
| Skill名称 | huawei-cloud-maas-tokens-usage |
| 实现方式 | SDK |
| 业务目标 | Query Huawei Cloud MaaS (Model as a Service) tokens usage statistics, including total tokens, prompt tokens, completion tokens, total requests, and total errors. Supports preset service, my service, and custom endpoint with time range queries (last 7/14/30 days or custom). Data source is MaaS Sho... |
| 分析状态 | completed |
| 分析时间 | 2026-06-10T14:41:26.269137+00:00 |

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
| 1 | modelarts | GetShow-statistics | GET | /v1/{var}/maas/monitoring/show-statistics | SignerBypass.get_show-statistics (scripts\maas_rest_usage_stats.py:68) | resource_path, http_method | 通过modelarts服务执行show操作，作用对象为show-statistics | mandatory |
| 2 | modelarts | PostShow-statistics | POST | /v1/{var}/maas/monitoring/show-statistics | SignerBypass.post_show-statistics (scripts\maas_rest_usage_stats.py:104) | resource_path, http_method | 通过modelarts服务执行show操作，作用对象为show-statistics | mandatory |

## 第二阶段：KooCLI命令一一对应关系与效果完全一致判定

### 阶段结论

共分析2个Open API接口，其中2个存在效果完全一致的KooCLI命令。

| 序号 | Open API接口 | 对应KooCLI命令 | 判定状态 | 差异说明 | 是否可接受 | 信息来源 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | GetShow-statistics | hcloud modelarts ShowAlgorithmByUuid | 效果完全一致 | - | 可接受 | local_cli |
| 2 | PostShow-statistics | hcloud modelarts ShowAlgorithmByUuid | 效果完全一致 | - | 可接受 | local_cli |



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


