# KooCLI OBS命令支持指南

> 来源: https://support.huaweicloud.com/usermanual-hcli/hcli_04_009.html
> 更新时间: 2025-08-04

## 概述

KooCLI已集成obsutil功能，通过 `hcloud obs` 命令管理OBS数据。OBS服务**不使用**标准的 `hcloud OBS <ApiName>` 格式，而是使用obsutil风格的子命令。

## 命令结构

```
hcloud obs <command> [parameters...] [options...]
```

## OBS Open API接口到KooCLI命令映射

### 桶相关操作

| OBS Open API接口 | HTTP方法 | KooCLI命令 | 功能说明 |
|-------------------|----------|------------|----------|
| CreateBucket | PUT | `hcloud obs mb obs://bucket` | 创建桶 |
| DeleteBucket | DELETE | `hcloud obs rm obs://bucket` | 删除桶 |
| ListAllMyBuckets | GET | `hcloud obs ls` | 列举桶 |
| GetBucketMetadata | GET | `hcloud obs stat obs://bucket` | 查询桶属性 |
| SetBucketMetadata | PUT | `hcloud obs chattri obs://bucket` | 设置桶属性 |
| GetBucketPolicy | GET | `hcloud obs bucketpolicy obs://bucket -method=get` | 获取桶策略 |
| SetBucketPolicy | PUT | `hcloud obs bucketpolicy obs://bucket -method=put` | 设置桶策略 |
| DeleteBucketPolicy | DELETE | `hcloud obs bucketpolicy obs://bucket -method=delete` | 删除桶策略 |
| GetBucketStoragePolicy | GET | `hcloud obs stat obs://bucket` | 查询桶存储策略 |
| SetBucketStoragePolicy | PUT | `hcloud obs chattri obs://bucket -sc=xxx` | 设置桶存储策略 |
| GetBucketLocation | GET | `hcloud obs stat obs://bucket` | 查询桶区域 |
| GetBucketVersioning | GET | `hcloud obs stat obs://bucket` | 查询桶版本控制 |
| SetBucketVersioning | PUT | `hcloud obs chattri obs://bucket` | 设置桶版本控制 |
| GetBucketAcl | GET | `hcloud obs stat obs://bucket -acl` | 查询桶ACL |
| SetBucketAcl | PUT | `hcloud obs chattri obs://bucket -acl=xxx` | 设置桶ACL |
| GetBucketCors | GET | `hcloud obs stat obs://bucket` | 查询桶CORS |
| SetBucketCors | PUT | `hcloud obs chattri obs://bucket` | 设置桶CORS |
| GetBucketLogging | GET | `hcloud obs stat obs://bucket` | 查询桶日志 |
| SetBucketLogging | PUT | `hcloud obs chattri obs://bucket` | 设置桶日志 |
| GetBucketWebsite | GET | `hcloud obs stat obs://bucket` | 查询桶静态网站 |
| SetBucketWebsite | PUT | `hcloud obs chattri obs://bucket` | 设置桶静态网站 |
| DeleteBucketWebsite | DELETE | `hcloud obs chattri obs://bucket` | 删除桶静态网站 |
| GetBucketTagging | GET | `hcloud obs stat obs://bucket` | 查询桶标签 |
| SetBucketTagging | PUT | `hcloud obs chattri obs://bucket` | 设置桶标签 |
| DeleteBucketTagging | DELETE | `hcloud obs chattri obs://bucket` | 删除桶标签 |
| GetBucketNotification | GET | `hcloud obs stat obs://bucket` | 查询桶事件通知 |
| SetBucketNotification | PUT | `hcloud obs chattri obs://bucket` | 设置桶事件通知 |
| GetBucketRequestPayment | GET | `hcloud obs stat obs://bucket` | 查询桶请求者付费 |
| SetBucketRequestPayment | PUT | `hcloud obs chattri obs://bucket` | 设置桶请求者付费 |
| ListMultipartUploads | GET | `hcloud obs ls obs://bucket -m` | 列举分段上传任务 |
| GetBucketStorageInfo | GET | `hcloud obs stat obs://bucket` | 查询桶存储信息 |
| GetBucketQuota | GET | `hcloud obs stat obs://bucket` | 查询桶配额 |
| SetBucketQuota | PUT | `hcloud obs chattri obs://bucket` | 设置桶配额 |
| GetBucketEncryption | GET | `hcloud obs stat obs://bucket` | 查询桶加密 |
| SetBucketEncryption | PUT | `hcloud obs chattri obs://bucket` | 设置桶加密 |
| DeleteBucketEncryption | DELETE | `hcloud obs chattri obs://bucket` | 删除桶加密 |
| GetBucketReplication | GET | `hcloud obs stat obs://bucket` | 查询桶跨区域复制 |
| SetBucketReplication | PUT | `hcloud obs chattri obs://bucket` | 设置桶跨区域复制 |
| DeleteBucketReplication | DELETE | `hcloud obs chattri obs://bucket` | 删除桶跨区域复制 |
| HeadBucket | HEAD | `hcloud obs stat obs://bucket` | 判断桶是否存在 |

### 对象相关操作

| OBS Open API接口 | HTTP方法 | KooCLI命令 | 功能说明 |
|-------------------|----------|------------|----------|
| PutObject | PUT | `hcloud obs cp file_url obs://bucket/key` | 上传对象 |
| GetObject | GET | `hcloud obs cp obs://bucket/key file_url` | 下载对象 |
| DeleteObject | DELETE | `hcloud obs rm obs://bucket/key` | 删除对象 |
| ListObjects | GET | `hcloud obs ls obs://bucket` | 列举对象 |
| HeadObject | HEAD | `hcloud obs stat obs://bucket/key` | 查询对象属性 |
| GetObjectMetadata | GET | `hcloud obs stat obs://bucket/key` | 查询对象元数据 |
| SetObjectMetadata | PUT | `hcloud obs chattri obs://bucket/key` | 设置对象元数据 |
| CopyObject | PUT | `hcloud obs cp obs://src/key obs://dst/key` | 复制对象 |
| MoveObject | - | `hcloud obs mv obs://src/key obs://dst/key` | 移动对象 |
| GetObjectAcl | GET | `hcloud obs stat obs://bucket/key -acl` | 查询对象ACL |
| SetObjectAcl | PUT | `hcloud obs chattri obs://bucket/key -acl=xxx` | 设置对象ACL |
| DeleteObjectAcl | DELETE | `hcloud obs chattri obs://bucket/key` | 删除对象ACL |
| InitiateMultipartUpload | POST | `hcloud obs cp file_url obs://bucket/key` | 初始化分段上传 |
| UploadPart | PUT | `hcloud obs cp file_url obs://bucket/key` | 上传分段 |
| CompleteMultipartUpload | POST | `hcloud obs cp file_url obs://bucket/key` | 完成分段上传 |
| AbortMultipartUpload | DELETE | `hcloud obs abort obs://bucket/key -u=xxx` | 取消分段上传 |
| ListParts | GET | `hcloud obs ls obs://bucket -m` | 列举已上传分段 |
| RestoreObject | POST | `hcloud obs restore obs://bucket/key` | 恢复归档对象 |
| GetObjectVersioning | GET | `hcloud obs ls obs://bucket -v` | 列举多版本对象 |
| DeleteObjectVersion | DELETE | `hcloud obs rm obs://bucket/key -versionId=xxx` | 删除指定版本对象 |
| SetObjectTagging | PUT | `hcloud obs chattri obs://bucket/key` | 设置对象标签 |
| GetObjectTagging | GET | `hcloud obs stat obs://bucket/key` | 查询对象标签 |
| DeleteObjectTagging | DELETE | `hcloud obs chattri obs://bucket/key` | 删除对象标签 |

### 辅助命令

| KooCLI命令 | 功能说明 |
|------------|----------|
| `hcloud obs config` | 更新配置文件(endpoint/ak/sk/token) |
| `hcloud obs clear` | 删除断点记录文件 |
| `hcloud obs help` | 查看命令帮助 |
| `hcloud obs version` | 查看obsutil版本号 |
| `hcloud obs archive` | 归档日志文件 |
| `hcloud obs mkdir` | 创建文件夹 |
| `hcloud obs sign` | 生成对象下载链接 |
| `hcloud obs sync` | 增量同步(上传/下载/复制) |
| `hcloud obs create-share` | 创建目录分享授权码 |
| `hcloud obs share-ls` | 授权码列举对象 |
| `hcloud obs share-cp` | 授权码下载对象 |

## 初始化配置

```bash
# 永久AK/SK
hcloud obs config -i=ak -k=sk -e=endpoint

# 临时AK/SK/Token
hcloud obs config -i=ak -k=sk -t=token -e=endpoint
```

## 连通性检查

```bash
hcloud obs ls -s
# 返回 "Bucket number :" 表示配置正确
```

## 注意事项

1. OBS服务**不使用** `hcloud OBS <ApiName>` 格式，必须使用 `hcloud obs <command>` 格式
2. 所有命令参数与obsutil一致，参数详情参考obsutil文档
3. 附加参数必须以 `-` 开头，支持 `-key=value` 和 `-key value` 两种方式
4. Windows系统中特殊字符需用双引号转义
5. 在被委托的ECS中可添加 `-authSource=ecsAgency` 参数自动获取临时认证