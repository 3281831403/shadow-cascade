import pytest

from render import shadows as mod

CASES = [
    ('cascade_split', [0.1, 100.0, 0.5, 0, 3], 0.1, True),
    ('cascade_split', [0.1, 100.0, 0.5, 1, 3], 17.2, True),
    ('depth_bias', [0.5, 0.001, 0.01], 0.006, True),
    ('pcf_radius', [0.01, 2], 0.02, True),
    ('cascade_index', [5.0, [10.0, 30.0, 100.0]], 0, False),
    ('cascade_index', [50.0, [10.0, 30.0, 100.0]], 2, False),
    ('blend_factor', [9.5, 10.0, 1.0], 0.25, True),
    ('sphere_in_box', [(0, 0, 0), 1, (-1, -1, -1), (1, 1, 1)], True, False),
    ('sphere_in_box', [(5, 0, 0), 1, (-1, -1, -1), (1, 1, 1)], False, False),
    ('shadow_resolution', [1024, 2], 256, False),
    ('normal_offset', [(0, 0, 1), 0.02], [0.0, 0.0, 0.02], True),
    ('depth_range', [0.1, 100.0], 99.9, True),
    ('commit_lights', [[True, True]], True, False),
    ('depth_bias', [0.0, 0.001, 0.01], 0.001, True),
    ('pcf_radius', [0.02, 1], 0.02, True),
]


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_shadows_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert result == pytest.approx(expected)
    else:
        assert result == expected
