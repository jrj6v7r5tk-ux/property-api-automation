# 测试执行记录（2026-09-08）

## 环境

- 被测服务：`Community-Property-Management-System` Spring Boot 后端
- 地址：`http://localhost:9090`
- Java：17.0.12
- Python：3.14.0a1
- pytest：9.1.1
- requests：2.34.2

## 执行命令

```text
E:\python\python.exe -m pytest -v
```

## 结果摘要

```text
collected 17 items
17 passed, 1 warning in 0.13s
```

## 逐组结果

| 测试文件 | 数量 | 结果 | 覆盖内容 |
|---|---:|---|---|
| `test_health.py` | 2 | 2 passed | 服务可用性、统一响应结构 |
| `test_login_validation.py` | 6 | 6 passed | 用户名、密码、角色缺失或为空 |
| `test_authorization.py` | 9 | 9 passed | 7 个受保护接口缺失 Token、2 种非法 Token |
| **合计** | **17** | **17 passed** | **0 failed** |

## 执行边界

本次结果仅统计实际运行的 17 条用例。被测系统连接 MySQL 时返回 `Access denied for user 'root'@'localhost'`，因此依赖数据库的登录成功和业务查询正向场景没有纳入结果，也没有计入通过率。

