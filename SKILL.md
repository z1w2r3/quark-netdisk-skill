# Quark Netdisk Skill

> AI 智能体技能：通过 quarkpan CLI 操作夸克网盘，实现文件上传、下载、分享和管理。

## 概述

本技能使 AI 编程助手（Claude Code、Cursor、Clawdbot 等）能够操作夸克网盘进行文件管理。基于 [quarkpan](https://pypi.org/project/quarkpan/) CLI 工具实现。

## 核心功能

- **二维码扫码登录**：安全便捷的认证方式
- **文件上传**：支持单文件和文件夹上传，自动分片
- **文件下载**：支持断点续传的文件下载
- **文件管理**：创建目录、删除、重命名、移动、搜索
- **分享功能**：创建分享链接、转存他人分享

## 前置条件

确保已安装 quarkpan：

```bash
pip install quarkpan
```

验证安装：

```bash
quarkpan version
```

## 工作流程

### 1. 首次使用 - 登录认证

```bash
# 显示二维码，用夸克 APP 扫描登录
quarkpan auth login

# 检查登录状态
quarkpan status
```

登录状态会自动保存，无需每次登录。

### 2. 文件列表

```bash
# 列出根目录
quarkpan ls

# 列出指定目录
quarkpan ls /path/to/folder

# 查看目录树结构
quarkpan list-dirs
```

### 3. 上传文件

```bash
# 上传单个文件到指定目录
quarkpan upload /local/file.txt /remote/path/

# 上传整个文件夹
quarkpan upload /local/folder/ /remote/path/
```

**注意事项：**
- 大文件会自动分片上传
- 网盘路径以 `/` 开头

### 4. 下载文件

```bash
# 下载文件到本地
quarkpan download /remote/file.txt /local/path/

# 下载整个文件夹
quarkpan download /remote/folder/ /local/path/
```

**特性：**
- 支持断点续传
- 大文件分片下载

### 5. 文件管理

```bash
# 创建目录
quarkpan mkdir /new/folder

# 删除文件或目录
quarkpan rm /path/to/file

# 重命名
quarkpan rename /old/name /new/name

# 移动文件
quarkpan mv /source/path /target/path
quarkpan move-to /file/path "目标文件夹名"

# 搜索文件
quarkpan search "关键词"

# 获取文件信息
quarkpan fileinfo /path/to/file
```

### 6. 分享功能

```bash
# 创建分享链接
quarkpan share /path/to/file

# 列出我的分享
quarkpan shares

# 批量分享
quarkpan batch-share /path/to/folder

# 转存他人分享
quarkpan save "分享链接"

# 批量转存
quarkpan batch-save links.txt
```

## 命令速查表

| 功能 | 命令 |
|------|------|
| 登录 | `quarkpan auth login` |
| 检查状态 | `quarkpan status` |
| 列出文件 | `quarkpan ls [路径]` |
| 目录树 | `quarkpan list-dirs` |
| 上传 | `quarkpan upload 本地路径 网盘路径` |
| 下载 | `quarkpan download 网盘路径 本地路径` |
| 创建目录 | `quarkpan mkdir 路径` |
| 删除 | `quarkpan rm 路径` |
| 重命名 | `quarkpan rename 旧名 新名` |
| 移动 | `quarkpan mv 源路径 目标路径` |
| 搜索 | `quarkpan search 关键词` |
| 分享 | `quarkpan share 路径` |
| 转存 | `quarkpan save 分享链接` |
| 交互模式 | `quarkpan interactive` |

## 错误处理

### 未登录或登录过期

```
Error: 未登录或登录已过期
```

**解决：** 运行 `quarkpan auth login` 重新扫码登录

### 文件不存在

```
Error: 文件或目录不存在
```

**解决：** 使用 `quarkpan ls` 确认正确路径

### 网络错误

```
Error: 网络连接失败
```

**解决：** 检查网络连接，稍后重试

### 存储空间不足

```
Error: 存储空间不足
```

**解决：** 清理网盘文件或升级会员

## 最佳实践

1. **定期检查登录状态**：长期不使用后运行 `quarkpan status`
2. **使用绝对路径**：网盘路径始终以 `/` 开头
3. **分批处理大量文件**：避免触发 API 频率限制
4. **上传前确认本地文件**：确保文件存在且路径正确
5. **下载后验证文件**：检查文件完整性

## 交互模式

对于复杂操作，可以使用交互模式：

```bash
quarkpan interactive
```

或使用浏览模式：

```bash
quarkpan browse
```

## 技术参考

- [quarkpan PyPI](https://pypi.org/project/quarkpan/)
- [quark-auto-save GitHub](https://github.com/Cp0204/quark-auto-save)
