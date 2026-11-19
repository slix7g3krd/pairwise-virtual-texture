"""第 61 批：角色跑向山脊，远处地表先糊成一块灰，停下来才一页页变清楚，转头又..."""

def page_mip(distance, max_mip):
    """按距离返回页 mip。"""
    raise NotImplementedError("TODO: page_mip")

def feedback_cover(missing, total):
    """反馈覆盖率。"""
    raise NotImplementedError("TODO: feedback_cover")

def request_frame(frame, budget):
    """页请求时机。"""
    raise NotImplementedError("TODO: request_frame")

def async_valid(state):
    """异步上传完成。"""
    raise NotImplementedError("TODO: async_valid")

def compressed_edge(size, block):
    """压缩块边界。"""
    raise NotImplementedError("TODO: compressed_edge")

def camera_share(camera_id, page_id):
    """多相机页共享键。"""
    raise NotImplementedError("TODO: camera_share")

def aniso_page_size(size, aniso):
    """各向异性页尺寸。"""
    raise NotImplementedError("TODO: aniso_page_size")

def lod_uv_offset(lod, tile):
    """LOD UV 偏移。"""
    raise NotImplementedError("TODO: lod_uv_offset")

def byte_budget(pages, bytes_per_page, limit):
    """字节预算。"""
    raise NotImplementedError("TODO: byte_budget")

def evict_age(last_used, current):
    """页淘汰年龄。"""
    raise NotImplementedError("TODO: evict_age")

def border_pad(size, padding):
    """页 border 尺寸。"""
    raise NotImplementedError("TODO: border_pad")

def foot_priority(distance, foot):
    """脚下页优先。"""
    raise NotImplementedError("TODO: foot_priority")

def table_sync(cpu_version, gpu_version):
    """页表同步。"""
    raise NotImplementedError("TODO: table_sync")

def sample_fallback(valid, fallback):
    """未映射页回退。"""
    raise NotImplementedError("TODO: sample_fallback")

def request_latency(frame, latency):
    """请求延迟帧。"""
    raise NotImplementedError("TODO: request_latency")
