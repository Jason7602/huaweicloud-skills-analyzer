# 华为云命令行工具服务

华为云命令行工具服务（Koo Command Line Interface，简称KooCLI）是基于华为云API建立的命令行管理工具，软件安装完成之后软件的属主为当前用户。您可以通过此工具调用华为云API来管理您的华为云资源。该工具提供的命令与华为云API一一对应，灵活性高且易于扩展。

## 特性

KooCLI基于GO语言开发，以API为元数据驱动命令解析与执行，最终以HTTPS协议与华为云API交互，具备如下特性：
 * 采用单一可执行文件发布，绿色免安装，解压后即可使用
 * 支持多种操作系统，包括Linux、Windows、Mac
 * 易于扩展，您可基于该工具对华为云API进行封装，扩展出您想要的功能

## 使用

命令使用示例：
 * 列出系统级帮助信息                            
    hcloud --help   
 * 列出配置功能帮助信息                            
    hcloud configure --help   
 * 初始化配置项                  
    hcloud configure init   
 * 列出某服务可用API                   
    hcloud ECS --help  
 * 列出具体API参数信息                   
    hcloud ECS NovaListServers --help    
 * 初始化配置项后调用API                            
    hcloud ECS NovaListServers --cli-profile=default 
 * 未初始化配置项时调用API    
    hcloud ECS NovaListServers --cli-region=region --cli-access-key=accessKey --cli-secret-key=secretKey  
    
更多使用帮助请参考华为云命令行工具服务[用户指南](https://support.huaweicloud.com/productdesc-hcli/hcli_01.html)

## 配置参数

按照华为云API使用规范，为保证本工具的正常使用需要配置以下个人数据：
 * cli-profile：配置项的名称，工具支持配置多配置项，按配置项的名称进行区分
 * cli-mode：支持AKSK|ecsAgency认证模式，推荐使用AKSK
 * [cli-project-id](https://support.huaweicloud.com/usermanual-hcli/hcli_09_002.html)：项目ID
 * [cli-region](https://support.huaweicloud.com/usermanual-hcli/hcli_09_003.html)：所属区域
 * [cli-domain-id](https://support.huaweicloud.com/usermanual-hcli/hcli_09_002.html)：IAM用户所属账号ID
 * [cli-access-key](https://support.huaweicloud.com/usermanual-hcli/hcli_09_001.html)：
访问密钥ID（AK），是您在华为云的长期身份凭证，您可以通过访问密钥对华为云API的请求进行签名。华为云通过AK识别访问用户的身份，通过SK对请求数据进行签名验证，用于确保请求的机密性、完整性和请求者身份的正确性
 * [cli-secret-key](https://support.huaweicloud.com/usermanual-hcli/hcli_09_001.html)：
秘密访问密钥（SK），是您在华为云的长期身份凭证。华为云通过AK识别访问用户的身份，通过SK对请求数据进行签名验证，用于确保请求的机密性、完整性和请求者身份的正确性
 * [cli-security-token](https://support.huaweicloud.com/usermanual-hcli/hcli_09_005.html)：用户获取的临时token，必须和临时AK/SK同时使用
 
上述信息仅用于工具在调用API时透传给华为云API网关，是调用云服务API时进行认证的必要数据。您可通过configure命令将上述信息配置后加密保存在您计算机当前用户的家目录下的config.json文件中，默认永久保存除非用户使用configure命令删除或者直接对config.json文件清理。您也可以在调用API的命令中直接输入相关配置而不进行本地保存。

配置信息存放位置：
 * Linux系统：/home/{当前用户名}/.hcloud/config.json
 * Windows系统：C:\Users\{当前用户名}\.hcloud\config.json
 * Mac系统：/Users/{当前用户名}/.hcloud/config.json

## 日志

在使用本工具过程中产生的某些错误日志，会记录在日志文件中，默认日志级别为error，单个日志文件大小为20MB，日志保留个数为3。

您可通过以下参数来修改日志相关配置：
 * level：日志记录级别[info|warning|error]
 * max-file-size：单个日志文件大小(MB),min=1,max=100,默认值20
 * max-file-num：日志文件保留个数(0表示保留所有日志文件),默认值3
 * retention-period：日志文件保留时间(天)(0表示永久保留)

日志存放位置：
 * Linux系统：/home/{当前用户名}/.hcloud/log
 * Windows系统：C:\Users\{当前用户名}\.hcloud\log
 * Mac系统：/Users/{当前用户名}/.hcloud/log

## 用户指南

 * [用户指南](https://support.huaweicloud.com/productdesc-hcli/hcli_01.html)