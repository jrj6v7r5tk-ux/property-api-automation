# 物业管理系统接口自动化测试

这是一个面向软件测试实习岗位的真实接口自动化项目。被测系统为开源的 `Community-Property-Management-System`，测试框架使用 Python、requests 和 pytest，实现公共请求封装、参数化测试、HTTP/业务断言以及可选的 Allure 报告。

## 项目目标

- 对真实运行的 Spring Boot 服务执行接口测试，而不是使用模拟返回。
- 覆盖服务可用性、登录参数校验、接口鉴权和非法 Token 等稳定场景。
- 保持测试可重复执行，不新增、修改或删除业务数据。
- 如实记录执行环境、通过数量和已知阻塞，不虚构测试结果。

## 目录结构

```text
property-api-automation/
├─ src/property_api/
│  └─ client.py                 # 公共 HTTP 客户端
├─ tests/
│  ├─ conftest.py              # 运行前健康检查、公共断言
│  ├─ test_health.py           # 服务可用性和响应结构
│  ├─ test_login_validation.py # 登录必填参数校验
│  └─ test_authorization.py    # 鉴权和非法 Token
├─ pytest.ini
├─ requirements.txt
└─ README.md
```

## 被测接口与范围

| 接口 | 方法 | 场景 |
|---|---|---|
| `/` | GET | 服务可用、统一响应结构 |
| `/login` | POST | 用户名、密码、角色缺失或为空 |
| `/notice/selectAll` | GET | 缺失 Token、非法 Token |
| `/activity/selectAll` | GET | 缺失 Token |
| `/house/selectAll` | GET | 缺失 Token |
| `/parking/selectAll` | GET | 缺失 Token |
| `/complaint/selectAll` | GET | 缺失 Token |
| `/fixed/selectAll` | GET | 缺失 Token |
| `/user/selectPage` | GET | 缺失 Token |

## 运行方式

### 1. 启动被测后端

被测系统来源：[baraberebo/Community-Property-Management-System](https://github.com/baraberebo/Community-Property-Management-System)。本次本地 checkout 的提交为 `0101023dfc97c3026c455dc1cb3ae1c5c262962b`。本仓库只提供独立的自动化测试代码。

本次使用 Java 17 和 Maven 3.9.16。以下示例均使用 Windows PowerShell；首次下载依赖需要联网。在独立目录准备后端：

```powershell
git clone https://github.com/baraberebo/Community-Property-Management-System.git
Set-Location Community-Property-Management-System
git switch --detach 0101023dfc97c3026c455dc1cb3ae1c5c262962b
Set-Location springboot
mvn spring-boot:run
```

保留后端终端运行，访问 `http://localhost:9090/`，预期返回业务码 `200`、数据 `访问成功`。已有后端目录时只需进入其 `springboot` 目录执行启动命令。

数据库相关业务还需要 MySQL、与源码匹配的表结构，以及在后端 `application.yml` 或环境变量中配置的有效连接凭据。当前 17 条用例只覆盖数据库查询之前的校验/鉴权和根接口；根接口可访问不代表数据库连接成功。

### 2. 运行自动化测试

另开终端，进入本测试仓库目录。建议使用已安装的稳定版 Python 3.12 或 3.13；下面以 3.13 为例，直接调用虚拟环境解释器，无需修改 PowerShell 执行策略：

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

如果后端地址不是默认值：

```powershell
$env:BASE_URL = 'http://localhost:9090'
.\.venv\Scripts\python.exe -m pytest -v
```

### 3. 可选 Allure 报告

安装依赖会安装 pytest 的 Allure 插件。下面第一条命令生成原始结果；第二条命令需要另行安装并配置 Allure CLI（`allure-pytest` 不包含 CLI）。本次已记录的 17 条测试使用普通 pytest 执行，尚未生成或验证 Allure 页面。

```powershell
.\.venv\Scripts\python.exe -m pytest --alluredir=allure-results
allure serve allure-results
```

## 真实执行结果

执行日期：2026-09-08

- 被测后端：Spring Boot 2.5.9，Java 17，端口 9090
- 测试环境：Windows 11，Python 3.14.0a1
- 执行命令：`python -m pytest -v`
- 收集用例：17 条
- 执行结果：17 passed，0 failed，1 warning
- 执行耗时：0.13 秒

分组结果和执行摘要保存在 [`docs/test-results-2026-09-08.md`](docs/test-results-2026-09-08.md)。warning 来自当前 Python 3.14 alpha 环境中 requests 缺少可用的字符编码识别依赖，不影响本次 JSON 接口断言。为保证他人复现稳定性，仍建议使用 Python 3.12 或 3.13。

## 已知限制

本机 MySQL 服务已启动，但被测系统源码中的数据库凭据无法连接当前 MySQL 实例。因此，本次先覆盖不依赖数据库的稳定接口场景；登录成功、业务查询、数据库校验等用例不计入当前结果。待提供正确的测试库凭据后，可继续加入登录 Fixture、真实业务查询以及 MySQL 数据一致性断言。

## 后续扩展

- 使用环境变量安全注入测试账号和数据库配置。
- 增加登录成功后的 Token 复用和业务接口正向查询。
- 使用 `allure-pytest` 输出步骤、附件和历史趋势。
- 增加 MySQL 只读校验，验证接口响应与数据库记录一致。

