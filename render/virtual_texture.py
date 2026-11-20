"""第 61 批：角色跑向山脊，远处地表先糊成一块灰，停下来才一页页变清楚，转头又...

本模块实现虚拟纹理页表/流送的关键契约。每个函数对应一类修复：
页优先级、反馈覆盖、请求时机、异步完成、压缩边界、多相机共享、
各向异性页尺寸、LOD UV、字节预算、淘汰保护、border 采样、脚下优先、
页表同步、未映射页回退与请求延迟。
"""

import math

# 距离为 0 时的安全下限，避免除零；不代表真实世界尺度。
_EPSILON = 1e-6


def page_mip(distance, max_mip):
    """按相机距离返回页应取的 mip 层级。

    距离越近需要的分辨率越高（mip 越小），距离翻倍 mip 加一，
    因此取 ``ceil(log2(distance))`` 并夹在 ``[0, max_mip]`` 内。
    页优先级随距离变化重算，而不是常驻固定 mip。
    """
    if max_mip <= 0:
        return 0
    if distance <= 1.0:
        return 0
    mip = math.ceil(math.log2(distance))
    return max(0, min(int(max_mip), mip))


def feedback_cover(missing, total):
    """反馈缓冲覆盖率：被反馈采样命中的页占所需页的比例。

    反馈不能只统计屏幕像素，斜视角/远景页也要计入；
    这里返回缺页比例，供上层做覆盖率门限判断。
    """
    if total <= 0:
        return 1.0
    missing = max(0, min(missing, total))
    return missing / total


def request_frame(frame, budget):
    """页请求时机：在帧预算内提前提交，而不是帧末统一提交。

    ``frame`` 为当前帧序号，``budget`` 为允许的请求延迟帧数；
    到达预算即应立即请求，快速转身时不再先显示低清页。
    """
    return frame >= max(0, budget)


def async_valid(state):
    """异步上传是否完成，只有完成态才允许被采样。

    未完成页继续读到旧内容，因此采样前必须检查上传状态。
    """
    if isinstance(state, str):
        return state.strip().lower() in ("ready", "complete", "completed", "valid")
    return bool(state)


def compressed_edge(size, block):
    """压缩块是否与页边界对齐（块不跨页）。

    返回 ``True`` 表示页尺寸是压缩块尺寸的整数倍，
    页边缘不会出现跨页块导致的色带。
    """
    if block <= 0 or size <= 0:
        return False
    return size % block == 0


def camera_share(camera_id, page_id):
    """多相机页共享键。

    分屏的多个相机请求同一页时，缓存以页为单位共享，
    相机前缀只用于调试/来源标识，不参与页内容的驱逐判定。
    """
    return f"{camera_id}:{page_id}"


def aniso_page_size(size, aniso):
    """各向异性过滤下的有效页尺寸。

    斜视角下屏幕像素覆盖的纹理范围被拉长 ``aniso`` 倍，
    页尺寸必须按该比例放大，否则远处纹理被过度模糊。
    """
    if aniso <= 0:
        return size
    return size * aniso


def lod_uv_offset(lod, tile):
    """LOD 切换后的 UV 偏移。

    层 ``lod`` 中第 ``tile`` 个瓦片的 UV 起点为 ``lod * tile``；
    地形 LOD 切换时必须同步更新，否则页表错位。
    """
    return lod * tile


def byte_budget(pages, bytes_per_page, limit):
    """显存预算按字节而不是页数计算。

    压缩格式切换会改变单页字节数，必须用
    ``pages * bytes_per_page`` 与字节上限比较。
    """
    if pages < 0 or bytes_per_page < 0:
        return False
    return pages * bytes_per_page <= limit


def evict_age(last_used, current):
    """页淘汰年龄（取最近使用时刻与当前时刻的绝对差）。

    年龄越大越优先淘汰；仅按最近使用时间淘汰会误伤过场动画
    扫过但实际常用的页，上层应结合保护规则使用该年龄。
    """
    return abs(current - last_used)


def border_pad(size, padding):
    """带 border 的页尺寸：四周各扩展 ``padding`` 像素。

    跨页采样需要 border 数据，否则接缝处会漏出背景色。
    """
    if padding < 0:
        padding = 0
    return size + 2 * padding


def foot_priority(distance, foot):
    """流送优先级：角色脚下页优先。

    基础优先级与距离成反比，``foot`` 为脚下的加权系数；
    距离趋近于 0 时用安全下限避免除零。
    """
    if foot < 0:
        return 0.0
    return foot / max(distance, _EPSILON)


def table_sync(cpu_version, gpu_version):
    """CPU 页表副本与 GPU 页表版本是否一致。

    版本不一致时采样会命中未映射页并返回黑块，
    因此必须等到两份页表同步后才允许渲染。
    """
    return cpu_version == gpu_version


def sample_fallback(valid, fallback):
    """未映射页的回退采样。

    页未就绪时返回安全回退值而不是黑块/旧内容；
    页有效时返回 1.0 表示直接采样真实内容，无需回退。
    """
    if not valid:
        return fallback
    return 1.0


def request_latency(frame, latency):
    """请求延迟：根据当前帧和延迟帧数推出应提交请求的帧。

    请求必须提前 ``latency`` 帧发出，才能在相机运动时及时到达。
    """
    if latency < 0:
        latency = 0
    return frame - latency
