# NOTE

1. 不期望有加减等运算符, 所有都指望 EML 嵌套

# TODO（更长远的打算）

1. 解析注释
1. 偏导
1. 可以不用`;`结尾`stmt`
1. 直接输出表达式（没有前缀`=`等内容时）
1. 循环???等结构???
1. 我是不是还得写加减……比如简化表达式什么的，呃呃

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

# 只有函数名相同且参数数量相同的函数不能同时存在

```eml-interpreter
h() = eml(12, 3)
h = eml(5, 5) // 覆盖 h()

h(x) = eml(x, 1) // ok
h(x, y) = eml(x, y) //ok
h(x, y, z) = eml(h(x), h(y, z)) // ok
h(y, z) = eml(h(y), h(z)) // 覆盖 h(x, y)
```

# 值传递和引用传递标识符

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

# 多元函数

```eml-interpreter
fun(x, y) = eml(x, eml(y, eml(3, x)))
```
