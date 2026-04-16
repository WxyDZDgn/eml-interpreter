# NOTE

1. 不期望有加减等运算符, 所有都指望 EML 嵌套

# TODO

1. 解析注释
1. 偏导

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

# 多元函数

```eml-interpreter
fun(x, y) = eml(x, eml(y, eml(3, x)))
```

# 求导（偏导）?
