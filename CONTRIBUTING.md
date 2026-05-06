# 贡献指南

感谢你对 Claude Web UI 项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

通过 [GitHub Issues](https://github.com/BadAppleJuice2/claude-web/issues) 提交，请包含：
- 问题描述和复现步骤
- 预期行为 vs 实际行为
- 环境信息（操作系统、Node.js/Python 版本等）

### 提交代码

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m "feat: 添加新功能"`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 **Pull Request**

### Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

| 前缀 | 说明 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | 修复 bug |
| `docs:` | 文档更新 |
| `style:` | 代码格式 |
| `refactor:` | 重构 |
| `test:` | 测试相关 |
| `chore:` | 构建/工具 |

### 代码规范

- Python 遵循 PEP 8
- Shell 脚本遵循 ShellCheck 规范
- 添加必要的注释和文档字符串

## 开发环境

```bash
git clone https://github.com/BadAppleJuice2/claude-web.git
cd claude-web
pip install -r examples/requirements.txt
```

## 许可证

贡献的代码将采用 MIT 许可证。
