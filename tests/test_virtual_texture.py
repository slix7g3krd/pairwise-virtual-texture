import pytest
from render import virtual_texture as mod

CASES = [
    ("mip", 'm.page_mip(7.0, 3) == 3'),
    ("feedback", 'm.feedback_cover(2, 4) == approx(0.5)'),
    ("request", 'm.request_frame(4, 2) is True'),
    ("async", 'm.async_valid("ready") is True'),
    ("compressed", 'm.compressed_edge(64, 16) is True'),
    ("camera", 'm.camera_share(1, 2) == "1:2"'),
    ("aniso", 'm.aniso_page_size(64, 4) == 256'),
    ("lod", 'm.lod_uv_offset(2, 16) == 32'),
    ("budget", 'm.byte_budget(10, 1024, 20480) is True'),
    ("evict", 'm.evict_age(10, 4) == 6'),
    ("border", 'm.border_pad(64, 2) == 68'),
    ("foot", 'm.foot_priority(1.0, 5.0) == approx(5.0)'),
    ("sync", 'm.table_sync(1, 1) is True'),
    ("fallback", 'm.sample_fallback(False, 0.5) == approx(0.5)'),
    ("latency", 'm.request_latency(10, 2) == 8')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
