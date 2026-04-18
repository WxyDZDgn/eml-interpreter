# NOTE

1. 不期望有加减等运算符, 所有都指望 EML 嵌套

# 自定义函数

```eml-interpreter
ex(x) = eml(x, 1);
ln(x) = eml(1, ex(eml(1, x)));
```

# 警告未使用的变量

```eml-interpreter
h(x) = eml(12, 3) // Warning: Unused Variable
```

# 允许常数变量定义

```eml-interpreter
h = eml(12, 4) // ok
```

# 允许重新赋值

```eml-interpreter
h = eml(12, 4)
h = eml(h, h + 1) //怎么又有加减
h = eml(h, 233)
```

```eml-interpreter
fun(x) = eml(x, 1);
fun(x) = eml(fun(x), fun(2));
```

我可不可以定义加减?
```text
add(x, y) = x + y:
```

???怎么有点像Lean, 我是不是可以用Lean写这玩意, 比如构造出只用`eml`的加法运算, 然后用Lean证明）

## !!Lean4??

# 函数名与常数名分离

```eml-interpreter
h = eml(12, 4);
h(x) = eml(h, x) // ok, => h(x) = eml(eml(12, 4), x);
h(y) = eml(h(h), h(y)) // ok, => h(x) = eml(eml(eml(12, 4), eml(12, 4)), h(x) = eml(eml(12, 4), y));
```

# 常数与零元函数等价

```eml-interpreter
h = eml(1, 2)
h() = eml(1, 2) // 二者等价
eml(h, h()) // 等价于 eml(eml(1, 2), eml(1, 2))
```

# 未赋值变量

如果一个参数数量为0（常数）的变量没有被赋值，那么视该名字作为“参数”

```eml-interpreter
eml(x, 1) // x 未被赋值, 是参数, 类似于 _(x) = eml(x, 1)
x = eml(1, 1) // x 被赋值
eml(x, 1) // 实际为 eml(x, 1), x 为 eml(eml(1, 1), 1)
```

# 只有函数名相同且参数数量相同的函数不能同时存在

```eml-interpreter
h() = eml(12, 3)
h = eml(5, 5) // 覆盖 h()

h(x) = eml(x, 1) // ok
h(x, y) = eml(x, y) //ok
h(x, y, z) = eml(h(x), h(y, z)) // ok
h(y, z) = eml(h(y), h(z)) // 覆盖 h(x, y)
```

# !!递归定义??

```eml-interpreter
h(x) = eml(x, 1)
h(x) = h(x) // 没必要, 但是确实有问题
```

## 解决递归定义

默认懒传递, 递归

```eml-interpreter
h(x) = eml(x, 1)
h(x) = !h(x) // 等价于 h(x) = h(x), 此时 !h(x) 为懒传递的 h(x) 而不是 eml(x, 1), 从而导致递归
```

值传递

```eml-interpreter
h(x) = eml(x, 1)
h(x) = ?h(x) // 没必要, 但是确实解决, 此时 ?h(x) 为 eml(x, 1)
```

# 值传递和懒传递标识符

`!`表示直接将其他非当前函数变量替换对应表达式, 后续修改对应变量结果不会影响有`!`所在的表达式, 如:

```eml-interpreter
h = eml(3, 1)
f(x) = eml(x, h)    // f(x) = eml(x, h), h 为 eml(3, 1)
h = eml(5, 5)   // f(x) 为 f(x) = eml(x, h), 但此时 h 改为 eml(5, 5)
f(x)    // 输出: eml(x, eml(5, 5))
```

```eml-interpreter
h = eml(3, 1)
f(x) =! eml(x, h)    // f(x) = eml(x, eml(3, 1)), h 被 eml(3, 1) 替代.
h = eml(5, 5)   // 此时, f(x) 还是原来的不变
f(x)    // 输出: eml(x, eml(3, 1))
```

`?`表示相反的, 默认是`?`

```eml-interpreter
h = eml(3, 1)
g = eml(1, 3)
f = ?eml(h, g) // 等价于 f = eml(h, g)
h = eml(5, 5)
g = eml(9, 9)
f // 此时 f 表示 eml(h, g), 即 eml(eml(5, 5), eml(9, 9))
```

## 修改嵌套内部所有变量的值懒传递

```eml-interpreter
h = eml(3, 1)
g = eml(1, 3)
f = !eml(h, g) // f 变成 eml(eml(3, 1), eml(1, 3))
h = eml(5, 5)
g = eml(9, 9)
f // 此时 f 保持不变, 为 eml(eml(3, 1), eml(1, 3))
```

## 部分修改值懒传递

```eml-interpreter
h = eml(3, 1)
g = eml(1, 3)
f = !eml(h, ?g) // 只有 g 是 g, 即 f 为 eml(eml(3, 1), g)
// 等价于 f = eml(!h, g) 或 f = eml(!h, ?g)
h = eml(5, 5)
g = eml(9, 9)
f // f 参数只有 g 受到影响变成 eml(eml(3, 1), g), 即 eml(eml(3, 1), eml(9, 9))
```

## 连续修改值懒传递

```eml-interpreter
h = eml(3, 1)
g = eml(1, 3)
f = !?!?eml(h, g) // 值传递, f 为 eml(eml(3, 1), eml(1, 3))
// f = !(?(!(?(eml(h, g)))))
h = eml(5, 5)
g = eml(9, 9)
f // 结果是 eml(eml(3, 1), eml(1, 3))
```

## 允许连续修改为同一个

```eml-interpreter
h = eml(3, 1)
g = eml(1, 3)
f = !!!!!!!!?????????eml(h, g) // 直接取值, f 为 eml(eml(3, 1), eml(1, 3))
h = eml(5, 5)
g = eml(9, 9)
f // 结果是 eml(eml(3, 1), eml(1, 3))
```

## 字面量和其它一样默认为懒传递

```eml-interpreter
h = eml(3, 1) // 等价于 eml(?3, ?1)
h = eml(!3, !1) // 两者表现相同, 字面量无法被直接修改, 不像变量
```

## 警告连续设置

```eml-interpreter
h = ?????!!!!!eml(3, 1) // 警告 连续的设置
```

```eml-interpreter
h = eml(?3, 1) // 警告 在只有字面量的情况下主动设置值传递或懒传递
h = eml(!3, 1) // 警告 在只有字面量的情况下主动设置值传递或懒传递
h = ?eml(3, 1) // 警告 在只有字面量的情况下主动设置值传递或懒传递
h = !eml(3, 1) // 警告 在只有字面量的情况下主动设置值传递或懒传递
```

# 多元函数

```eml-interpreter
fun(x, y) = eml(x, eml(y, eml(3, x)))
```
# 删除符

```eml-interpreter
// 系统函数不支持删除
.eml(x, y); // 报错
.eml(vdsjnk, abscau); // 等价于上一个语句
```

## 删除符不能在赋值左边
```eml-interpreter
f(a, b, c) = eml(eml(a, b), c)
.f(a, b, c) = eml(a, eml(b, c)) // 报错
.f(a, b, c) // 取值并删除函数f
```

## 重命名函数
```eml-interpreter
f(x, y, z) = eml(x, eml(y, z))
h[3] = .f[3]  // 按顺序取参数, 自动推断, 只有参数数量一致才可以使用
```

## 先取值再删除

```eml-interpreter
h(x) = eml(x, 1)
g(x) = eml(h(x), 2)
f(x) = .h(g(x)) // 默认仅删除h[1]
```
等价于
```eml-interpreter
h(x) = eml(x, 1)
g(x) = eml(h(x), 2)
f(x) = !h(g(x))
.h[1]
```

## 同时删除嵌套

```eml-interpreter
h(x) = eml(x, 1)
g(x) = eml(h(x), 2)
f(x) = .h(.g(x)) // 正确同时删除嵌套函数
```

```eml-interpreter
h(x) = eml(x, 1)
g(x) = eml(h(x), 2)
f(x) = .h(?g(x)) // 报错
```

## 选择性删除

```eml-interpreter
f(x) = eml(x, 1)
g(x) = eml(1, x)
h(x) = eml(.f(x), g(x)) // 只删除 f[1]
```

## 自动删除依赖

```eml-interpreter
g(x) = eml(1, x)
h(x) = eml(g(x), 1)
.g(x) // 删除 g[1], 由于 h[1] 用上了 g[1], h[1] 也会被删除
```

## 不能对常数删除

```eml-interpreter
.1 // 报错
.eml(1, 2) // 报错
h(x) = eml(1, x) // ok
.h(1) // 报错
.h[1] // ok
```

## 有删除符时强制设置为值传递:

```eml-interpreter
f(x) = eml(x, 1)
g(x) = eml(1, x)
h(x) = eml(.f(x), .g(x)) 
// h(x) = eml(eml(x, 1), eml(1, x)), 并随后删除 h[1] 和 g[1]
```

# 中括号语法

函数名 '[' 参数数量 ']'

```eml-interpreter
f(a, b, c) = eml(eml(a, b), c)
h[3] = f[3] // 懒传递复制 f
g[3] = !f[3] // 值传递赋值, 参数为正常顺序
```

自动推断

```eml-interpreter
f(x) = eml(1, x)
g(x) = eml(x, 1)
h[1] = eml(f[1], g[1])
```