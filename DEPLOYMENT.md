# daily-arXiv-ai-enhanced 部署文档

## 第一部分：GitHub 部署（生产使用）

### 1. 准备工作

#### 1.1 Fork 仓库
- 访问 [https://github.com/dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced)
- 点击右上角的 "Fork" 按钮，将仓库复制到你的账户下

#### 1.2 删除原作者信息
- 在你 fork 的仓库中，删除 `buy-me-a-coffee/README.md` 中的原作者信息

### 2. 配置 GitHub Actions Secrets

进入你的仓库：`Settings` → `Secrets and variables` → `Actions`

#### 2.1 创建 Secrets（加密变量）
创建以下两个仓库密钥：
- `OPENAI_API_KEY`：你的 OpenAI API 密钥
- `OPENAI_BASE_URL`：OpenAI API 基础 URL（如使用其他兼容 API，填写对应地址）
- `TOKEN_GITHUB`：（可选）GitHub Token，用于访问 GitHub API 获取仓库信息

#### 2.2 设置访问密码（可选）
- `ACCESS_PASSWORD`：设置访问密码，保护你的页面不被他人访问

### 3. 配置 GitHub Actions Variables

进入 `Variables` 选项卡（非加密变量）

创建以下变量：
- `CATEGORIES`：arXiv 分类，用逗号分隔，如 `"cs.CV, cs.CL"`
- `LANGUAGE`：语言设置，如 `"Chinese"` 或 `"English"`
- `MODEL_NAME`：使用的模型名称，如 `"gpt-4o-mini"` 或 `"deepseek-chat"`
- `EMAIL`：你的邮箱，用于 Git 提交
- `NAME`：你的姓名，用于 Git 提交

### 4. 启用 GitHub Actions

进入 `Actions` → `arXiv-daily-ai-enhanced`
- 点击 "Run workflow" 测试是否正常工作
- 默认情况下，该动作每天自动运行一次（cron: "30 1 * * *"）

### 5. 配置 GitHub Pages

进入 `Settings` → `Pages`
- 在 `Build and deployment` 部分
- 设置 `Source` 为 "Deploy from a branch"
- 设置 `Branch` 为 "main"，路径为 "/(root)"
- 等待几分钟，访问 `https://<your-username>.github.io/daily-arXiv-ai-enhanced/`

### 6. 验证部署

- 访问你的 GitHub Pages 地址
- 检查是否能正常显示论文列表
- 验证评分、标签等功能是否正常工作

## 第二部分：本地部署（测试使用）

### 1. 系统要求

- Python 3.12+
- Git
- uv（推荐的包管理工具）

### 2. 环境搭建

#### 2.1 克隆仓库
```bash
git clone https://github.com/<your-username>/daily-arXiv-ai-enhanced.git
cd daily-arXiv-ai-enhanced
```

#### 2.2 创建虚拟环境（推荐）
```bash
# 使用 venv 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows (Command Prompt):
venv\Scripts\activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
```

#### 2.3 安装依赖
```bash
# 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync
```

或者使用 pip（注意：此项目使用 pyproject.toml 而不是 requirements.txt）：
```bash
# 方法1：使用 uv pip（推荐）
uv pip install arxiv "langchain>=0.3.20" "langchain-openai>=0.3.9" scrapy tqdm python-dotenv

# 方法2：如果系统中没有 uv，则使用 pip 安装依赖
pip install arxiv "langchain>=0.3.20" "langchain-openai>=0.3.9" scrapy tqdm python-dotenv
```

### 3. 配置环境变量

创建 `.env` 文件（位于项目根目录）：
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
TOKEN_GITHUB=your_github_token_here  # 可选
LANGUAGE=Chinese
CATEGORIES=cs.CV, cs.CL
MODEL_NAME=gpt-4o-mini
SKIP_SENSITIVITY_CHECK=true  # 可选，跳过敏感性检查，适用于本地测试
```

### 4. 本地测试运行

#### 4.1 运行爬虫测试
```bash
# 确保在项目根目录
cd daily_arxiv
scrapy crawl arxiv -o ../data/test.jsonl
```

#### 4.2 运行 AI 处理测试
```bash
# 确保在项目根目录
cd ai
python enhance.py --data ../data/test.jsonl
```

#### 4.3 转换为 Markdown
```bash
# 确保在项目根目录
cd to_md
python convert.py --data ../data/test_AI_enhanced_Chinese.jsonl
```

#### 4.4 使用本地脚本一键测试
运行项目提供的 `run.sh` 脚本（Linux/Mac）：
```bash
chmod +x run.sh
./run.sh
```

对于 Windows 用户，可以使用 Git Bash 或 WSL 运行上述命令，或参考以下 PowerShell 方式：
```powershell
# 设置环境变量（PowerShell）
$env:OPENAI_API_KEY="your-api-key-here"
$env:OPENAI_BASE_URL="https://api.openai.com/v1"
$env:LANGUAGE="Chinese"
$env:CATEGORIES="cs.CV"
$env:MODEL_NAME="gpt-4o-mini"
$env:SKIP_SENSITIVITY_CHECK="true"  # 跳过敏感性检查，适用于本地测试

# 然后运行 Scrapy 命令进行测试（在项目根目录下）
# 注意：需要在 daily_arxiv 目录下运行 scrapy 命令
cd daily_arxiv
scrapy crawl arxiv -o ../data/test.jsonl
cd ..
```

或者使用 Python 直接运行（需要安装 scrapy 并在 daily_arxiv 目录下）：
```python
# 在 daily_arxiv 目录下运行 Python 脚本
import os
# 设置环境变量以跳过敏感性检查
os.environ['SKIP_SENSITIVITY_CHECK'] = 'true'

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from daily_arxiv.spiders.arxiv import ArxivSpider

process = CrawlerProcess(get_project_settings())
process.crawl(ArxivSpider)
process.start()
```

### 5. 本地开发服务器

#### 5.1 启动简单 HTTP 服务器
```bash
# 在项目根目录启动
python -m http.server 8000
```

然后访问 `http://localhost:8000`

注意：由于此项目依赖 GitHub API 获取数据，本地服务器主要用于前端界面预览，实际数据加载需要在线访问 GitHub API。

#### 5.2 或使用 Live Server（VS Code 插件）
如果你使用 VS Code，可以安装 "Live Server" 插件，右键点击 `index.html` 选择 "Open with Live Server"

### 6. 本地开发注意事项

#### 6.1 数据分支模拟
由于生产环境使用 `data` 分支存储数据，在本地测试时：
- 确保 `data/` 目录存在
- 生成的数据文件会保存在 `data/` 目录下

在 Windows 环境中，请注意：
- 确保文件名和路径符合 Windows 标准
- 某些特殊字符可能在 Windows 文件系统中不被支持

#### 6.2 配置文件调整
在本地开发时，你可能需要修改 `js/data-config.js` 中的仓库信息：
```javascript
repoOwner: 'your-github-username',
repoName: 'daily-arXiv-ai-enhanced',
```

#### 6.3 本地测试环境变量
```bash
export OPENAI_API_KEY="your-test-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export LANGUAGE="Chinese"
export CATEGORIES="cs.CV"
export MODEL_NAME="gpt-4o-mini"
```

### 7. 故障排除

#### 7.1 常见问题
- **API 密钥错误**：检查 `OPENAI_API_KEY` 是否正确设置
- **依赖安装失败**：确保 Python 版本 >= 3.12
- **权限问题**：确保有写入 `data/` 目录的权限
- **Windows PowerShell 执行策略**：如果遇到脚本执行错误，可能需要更改执行策略：
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- **Scrapy 在 Windows 上的问题**：某些情况下可能需要安装额外的依赖：
  ```bash
  pip install twisted pywin32
  ```
- **LangChain 版本兼容性问题**：如果遇到 `No module named 'langchain.prompts'` 错误，可能是 LangChain 版本不兼容导致的。本项目已更新导入语句以适配较新版本的 LangChain。
- **敏感性检查超时问题**：如果遇到连接 `spam.dw-dengwei.workers.dev` 超时的错误，可以在环境变量中设置 `SKIP_SENSITIVITY_CHECK=true` 来跳过敏感性检查，这对于本地测试非常有用。

#### 7.2 调试技巧
- 查看 GitHub Actions 日志以诊断部署问题
- 在本地运行 `./run.sh` 脚本进行完整流程测试
- 检查浏览器开发者工具中的错误信息

### 8. 维护和更新

#### 8.1 更新代码
定期同步上游仓库的更新：
```bash
git remote add upstream https://github.com/dw-dengwei/daily-arXiv-ai-enhanced.git
git fetch upstream
git merge upstream/main
```

#### 8.2 监控
- 定期检查 GitHub Actions 运行状态
- 监控 GitHub Pages 页面是否正常访问
- 检查新论文是否按时更新

通过以上步骤，你可以成功部署和维护 daily-arXiv-ai-enhanced 项目，无论是用于生产环境还是本地测试开发。