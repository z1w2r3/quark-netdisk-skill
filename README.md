# Quark Netdisk Skill

AI 智能体技能包：让 Claude Code、Cursor、Clawdbot 等 AI 编程助手能够操作夸克网盘进行文件上传、下载和管理。

## 功能特性

- **二维码扫码登录**：安全便捷的认证方式，用夸克 APP 扫描即可
- **文件上传**：支持单文件和文件夹上传，自动分片处理大文件
- **文件下载**：支持断点续传的文件下载
- **文件管理**：创建目录、删除、重命名、移动、搜索
- **分享功能**：创建分享链接、转存他人分享

## 安装方式

### 前置条件

首先安装 quarkpan CLI 工具：

```bash
pip install quarkpan
```

### 方式一：项目级别安装（推荐）

```bash
npx skills add z1w2r3/quark-netdisk-skill
```

### 方式二：全局安装

```bash
npx skills add z1w2r3/quark-netdisk-skill --global
```

### 方式三：Clawdbot / ClawdH 安装

```bash
npx clawdhub@latest install quark-netdisk-skill
```

或手动安装：

```bash
# 克隆到 Clawdbot skills 目录
git clone https://github.com/z1w2r3/quark-netdisk-skill.git ~/.clawdbot/skills/quark-netdisk-skill
```

### 方式四：手动安装到 Claude Code

```bash
# 克隆到 Claude skills 目录
git clone https://github.com/z1w2r3/quark-netdisk-skill.git ~/.claude/skills/quark-netdisk-skill
```

## 首次使用

1. **登录夸克网盘**

   ```bash
   quarkpan auth login
   ```

   终端会显示二维码，使用夸克 APP 扫描即可完成登录。

2. **验证登录状态**

   ```bash
   quarkpan status
   ```

3. **开始使用**

   向 AI 助手说：
   - "帮我把 `/path/to/file` 上传到夸克网盘"
   - "列出我的夸克网盘文件"
   - "从夸克网盘下载 `/文档/报告.pdf`"

## 常用命令

| 功能 | 命令 |
|------|------|
| 登录 | `quarkpan auth login` |
| 检查状态 | `quarkpan status` |
| 列出文件 | `quarkpan ls [路径]` |
| 上传 | `quarkpan upload 本地路径 网盘路径` |
| 下载 | `quarkpan download 网盘路径 本地路径` |
| 创建目录 | `quarkpan mkdir 路径` |
| 删除 | `quarkpan rm 路径` |
| 搜索 | `quarkpan search 关键词` |
| 分享 | `quarkpan share 路径` |
| 转存 | `quarkpan save 分享链接` |

## 技术栈

- **CLI 工具**: [quarkpan](https://pypi.org/project/quarkpan/) - 夸克网盘 Python CLI
- **兼容平台**: Claude Code, Cursor, Clawdbot, Windsurf

## 目录结构

```
quark-netdisk-skill/
├── SKILL.md        # 核心技能文档
└── README.md       # 安装和使用说明
```

## 相关链接

- [quarkpan PyPI](https://pypi.org/project/quarkpan/)
- [quark-auto-save GitHub](https://github.com/Cp0204/quark-auto-save)

## License

MIT
