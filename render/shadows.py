"""级联阴影：分割、偏移与级联混合。"""


def cascade_split(near, far, lambda_, index, count):
    """级联分割距离。

    在第 index 个级联的远端返回对数分割与均匀分割的线性混合：
        split = λ·(near·(far/near)^(i/count)) + (1−λ)·(near + (far−near)·(i/count))
    其中 i = index。index=0 时恰好为 near，index=count 时恰好为 far。
    """
    if count <= 0:
        return float(near)

    i = min(max(index, 0), count)
    ratio = i / count

    uniform = near + (far - near) * ratio
    # near 与 far 同号且非零时对数分割才有定义；否则退化为均匀分割。
    if near > 0.0 and far > 0.0:
        logarithmic = near * (far / near) ** ratio
    else:
        logarithmic = uniform

    return lambda_ * logarithmic + (1.0 - lambda_) * uniform


def depth_bias(slope, base_bias, factor):
    """深度偏移随坡度增大。

    坡度越大，阴影贴图表面与光线的夹角越倾斜，需要更大的深度偏移：
        bias = base_bias + slope·factor
    """
    return base_bias + slope * factor


def pcf_radius(texel_size, scale):
    """PCF 半径按纹素大小计算。

    半径应以纹素为单位，而不是像素：
        radius = texel_size·scale
    """
    return texel_size * scale


def cascade_index(depth, splits):
    """按深度选择级联索引。

    splits 为每个级联的远端深度；返回第一个覆盖 depth 的级联。
    深度落在所有级联之外时夹到最后一个有效索引，避免越界。
    """
    last = max(len(splits) - 1, 0)
    for i, split in enumerate(splits):
        if depth <= split:
            return i
    return last


def blend_factor(depth, split, band):
    """级联边界混合系数。

    在 [split−band, split] 区间内平滑过渡：越靠近 split 混合权重越小，
    使用二次曲线保证边界处一阶连续：
        t = clamp((split−depth)/band, 0, 1);  factor = t²
    """
    if band <= 0.0:
        return 0.0
    t = (split - depth) / band
    t = min(max(t, 0.0), 1.0)
    return t * t


def sphere_in_box(center, radius, min_corner, max_corner):
    """包围球与轴对齐盒求交。

    将球心夹到盒子范围内得到最近点，比较球心到最近点的距离与半径。
    """
    if radius < 0.0:
        return False

    dist_sq = 0.0
    for c, lo, hi in zip(center, min_corner, max_corner):
        closest = min(max(c, lo), hi)
        d = c - closest
        dist_sq += d * d

    return dist_sq <= radius * radius


def shadow_resolution(base, index):
    """级联越远分辨率越低。

    每个级联沿两个轴各降采样一半：
        resolution = base / 2^index
    """
    if base <= 0:
        return 0
    return max(1, base // (1 << max(index, 0)))


def normal_offset(normal, bias):
    """沿法线偏移避免阴影痤疮。

    将采样点沿表面法线推出 bias 距离：
        offset = normalize(normal)·bias
    """
    length_sq = sum(n * n for n in normal)
    if length_sq <= 0.0:
        return [0.0 * bias for _ in normal]

    inv_length = 1.0 / length_sq ** 0.5
    return [n * inv_length * bias for n in normal]


def depth_range(near, far):
    """深度范围。"""
    return far - near


def commit_lights(results):
    """批量灯光全部成功才提交。

    results 为每盏灯的提交结果（布尔值或布尔值序列）。只有全部成功时
    才返回 True；否则返回 False，调用方据此整体回滚，避免只提交一半。
    """
    ok = True
    for result in results:
        if isinstance(result, (list, tuple)):
            ok = ok and all(bool(v) for v in result)
        else:
            ok = ok and bool(result)
    return ok
