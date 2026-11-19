"""级联阴影：分割、偏移与级联混合：待实现的核心模块。"""


def cascade_split(near, far, lambda_, index, count):
    """级联分割距离。"""
    raise NotImplementedError

def depth_bias(slope, base_bias, factor):
    """深度偏移随坡度增大。"""
    raise NotImplementedError

def pcf_radius(texel_size, scale):
    """PCF 半径按纹素大小计算。"""
    raise NotImplementedError

def cascade_index(depth, splits):
    """按深度选择级联索引。"""
    raise NotImplementedError

def blend_factor(depth, split, band):
    """级联边界混合系数。"""
    raise NotImplementedError

def sphere_in_box(center, radius, min_corner, max_corner):
    """包围球与轴对齐盒求交。"""
    raise NotImplementedError

def shadow_resolution(base, index):
    """级联越远分辨率越低。"""
    raise NotImplementedError

def normal_offset(normal, bias):
    """沿法线偏移避免阴影痤疮。"""
    raise NotImplementedError

def depth_range(near, far):
    """深度范围。"""
    raise NotImplementedError

def commit_lights(results):
    """批量灯光全部成功才提交。"""
    raise NotImplementedError
