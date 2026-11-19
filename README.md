# 级联阴影：分割、偏移与级联混合

远近阴影一边糊一边闪：级联分割没有按对数分布，深度偏移不随坡度，PCF 半径按像素而非纹素，级联索引越界，级联之间没有混合，视锥裁剪漏掉包围球，高分辨率级联没降采样，法线偏移不足产生阴影痤疮，深度范围算错，批量灯光只提交一半。

## 目录结构

```
README.md
conftest.py
.gitignore
render/__init__.py
render/shadows.py
tests/test_shadows.py
```

## 当前状态

`render/shadows.py` 中所有函数只保留签名与文档字符串，函数体统一
`raise NotImplementedError`。`tests/test_shadows.py` 有 15 个参数化用例，
初始全部失败。

## 需要修复的 10 个问题

1. 级联按对数与均匀混合分割
2. 深度偏移随坡度变化
3. PCF 半径按纹素计算
4. 级联索引夹到有效范围
5. 级联边界混合
6. 包围球与视锥求交
7. 级联分辨率逐级降低
8. 沿法线偏移避免痤疮
9. 深度范围正确计算
10. 批量灯光统一提交

## 验收

```bash
python -m pytest -q
```

初始应得到 `15 failed`，且没有 collection error。实现 `render/shadows.py`
后 15 条用例应全部通过。
