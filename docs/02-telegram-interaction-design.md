# Telegram 交互设计

## 对话流程设计

### 会话启动

```
用户: /start 或 直接私信
AI: 欢迎来到 AI Code Tutor！

我是你的编程学习伙伴，我们一起通过实战代码重构来提升编程能力。

当前可选课程：
- logic - 代码重构：从混乱到清晰（共 8 课）

输入课程名称开始学习，或输入 /help 查看帮助。
```

### 课程进行流程

```
用户: logic

AI: 开始课程：代码重构：从混乱到清晰

第 1 课 / 共 8 课
主题：识别代码坏味道

场景：订单审批系统

当前代码如下：

```python
def approve_order(order: Order, user: User) -> str:
    try:
        if user.is_premium:
            if order.amount > 1000:
                if not order.has_discount:
                    # ... 更多嵌套
                    return "approved"
    except Exception:
        return "rejected"
```

观察这段代码，你觉得有什么问题？
```

### 用户自然语言指令处理

#### 场景 1：用户描述问题

```
用户: 嵌套太深了，读起来很费劲

AI: 观察到位！这就是经典的箭头反模式。

6 层嵌套确实让代码难以跟踪。那你知道如何改进吗？

提示思路：
- 能否把一些条件提前返回？
- 哪些检查可以放到函数开头？
```

#### 场景 2：用户直接要求修改

```
用户: 把那些嵌套的 if 改成提前返回

AI: 好想法！卫语句正是解决这个问题的利器。

我来帮你生成修改方案：

```python
def approve_order(order: Order, user: User) -> str:
    if user.is_admin:
        return "approved"

    if not user.is_premium:
        return "rejected"
    if order.amount <= 1000 and order.type != "bulk":
        return "rejected"

    return "approved"
```

这样嵌套层级从 6 层降到 1 层。

你想：
- 【应用】将这个修改应用到代码
- 【修改】告诉我你的调整
- 【解释】为什么这样改更好？
```

#### 场景 3：用户想查看提示

```
用户: /hint

AI: 当前提示（1/3）：

关注那个 try...except 块，它包裹了整个函数体。

想想：
- 这里的异常处理真的有必要吗？
- 什么情况下会抛出异常？
- 如果移除它，行为会改变吗？
```

### 一课结束流程

```
AI: 第 1 课完成！

学习总结：
- 你识别了深层嵌套问题
- 你理解了箭头反模式的可读性成本
- 你学会了用卫语句扁平化条件分支

准备进入下一课吗？
```

## 命令设计

- `/start` - 开始学习
- `/help` - 查看帮助
- `/status` - 查看当前状态
- `/hint` - 获取提示
- `/solution` - 查看参考解法
- `/skip` - 跳过当前环节
- `/reset` - 重置当前课程
