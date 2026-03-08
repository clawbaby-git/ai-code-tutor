# AI Code Tutor (MVP M1)

## 运行

在项目根目录执行：

```bash
PYTHONPATH=src python3 -m tutor.cli
```

CLI 会扫描 `./courses/` 和 `./my-courses/`，列出课程后进入当前 lesson 展示。

## 测试

在项目根目录执行：

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## 命名兼容

lesson 文件同时兼容以下命名：

- `01_xxx.py`
- `1_xxx.py`

排序规则按数字前缀升序（例如 `01_`、`1_`、`2_`、`10_`）。
