#!/usr/bin/env python3
import heapq
import math
import struct
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path as NavPath
from sensor_msgs.msg import PointCloud2, PointField

from world_collision_checker import load_obstacles, point_collision, segment_collision


Point3 = Tuple[float, float, float]
GridKey = Tuple[int, int]


DEFAULT_WORLD = Path(__file__).resolve().parents[1] / "config" / "fuel_visual_world_exploration.yaml"


def world_config_path(value: str = "") -> Path:
    return Path(value or DEFAULT_WORLD)


def parse_bounds(world_config: Path) -> Dict[str, float]:
    text = world_config.read_text(errors="replace")
    bounds: Dict[str, float] = {
        "min_x": -15.0,
        "max_x": 15.0,
        "min_y": -15.0,
        "max_y": 15.0,
        "min_z": 0.0,
        "max_z": 4.0,
    }
    in_bounds = False
    for raw in text.splitlines():
        line = raw.strip()
        if line == "bounds:":
            in_bounds = True
            continue
        if in_bounds and line and not line.startswith(("min_", "max_")):
            if not raw.startswith("        "):
                break
        if in_bounds and ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            if key in bounds:
                bounds[key] = float(val.strip())
    return bounds


def make_cloud(points: Sequence[Point3], frame_id: str = "map") -> PointCloud2:
    msg = PointCloud2()
    msg.header.frame_id = frame_id
    msg.height = 1
    msg.width = len(points)
    msg.fields = [
        PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
    ]
    msg.is_bigendian = False
    msg.point_step = 12
    msg.row_step = msg.point_step * msg.width
    msg.is_dense = True
    msg.data = b"".join(struct.pack("<fff", float(x), float(y), float(z)) for x, y, z in points)
    return msg


def read_cloud(msg: PointCloud2) -> List[Point3]:
    points: List[Point3] = []
    if msg.point_step < 12:
        return points
    for offset in range(0, len(msg.data), msg.point_step):
        if offset + 12 <= len(msg.data):
            points.append(struct.unpack_from("<fff", msg.data, offset))
    return points


def make_pose(x: float, y: float, z: float, frame_id: str = "map") -> PoseStamped:
    msg = PoseStamped()
    msg.header.frame_id = frame_id
    msg.pose.position.x = float(x)
    msg.pose.position.y = float(y)
    msg.pose.position.z = float(z)
    msg.pose.orientation.w = 1.0
    return msg


def make_path(points: Sequence[Point3], frame_id: str = "map") -> NavPath:
    path = NavPath()
    path.header.frame_id = frame_id
    for x, y, z in points:
        path.poses.append(make_pose(x, y, z, frame_id))
    return path


def densify(points: Sequence[Point3], step: float = 0.5) -> List[Point3]:
    if len(points) < 2:
        return list(points)
    result: List[Point3] = [points[0]]
    for a, b in zip(points, points[1:]):
        dist = math.dist(a, b)
        n = max(1, int(math.ceil(dist / max(step, 1e-3))))
        for i in range(1, n + 1):
            r = i / n
            result.append((a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r, a[2] + (b[2] - a[2]) * r))
    return result


def is_free(point: Point3, obstacles, bounds: Dict[str, float], clearance: float) -> bool:
    x, y, z = point
    if x < bounds["min_x"] or x > bounds["max_x"] or y < bounds["min_y"] or y > bounds["max_y"]:
        return False
    if z < bounds["min_z"] or z > bounds["max_z"]:
        return False
    return not point_collision(obstacles, point, clearance).collides


def path_collision_free(points: Sequence[Point3], obstacles, clearance: float = 0.35, resolution: float = 0.1) -> bool:
    if len(points) < 2:
        return False
    for a, b in zip(points, points[1:]):
        if segment_collision(obstacles, a, b, clearance, resolution).collides:
            return False
    return True


def astar_path(
    start: Point3,
    goal: Point3,
    world_config: Path,
    resolution: float = 0.5,
    clearance: float = 0.35,
    max_expansions: int = 20000,
) -> Optional[List[Point3]]:
    obstacles = load_obstacles(world_config)
    bounds = parse_bounds(world_config)
    z = max(bounds["min_z"] + 0.2, min(bounds["max_z"] - 0.2, goal[2]))

    def key(p: Point3) -> GridKey:
        return (int(round((p[0] - bounds["min_x"]) / resolution)), int(round((p[1] - bounds["min_y"]) / resolution)))

    def pos(k: GridKey) -> Point3:
        return (bounds["min_x"] + k[0] * resolution, bounds["min_y"] + k[1] * resolution, z)

    start_key = key((start[0], start[1], z))
    goal_key = key((goal[0], goal[1], z))
    if not is_free(pos(start_key), obstacles, bounds, clearance):
        return None
    if not is_free(pos(goal_key), obstacles, bounds, clearance):
        return None

    open_heap: List[Tuple[float, GridKey]] = []
    heapq.heappush(open_heap, (0.0, start_key))
    came: Dict[GridKey, GridKey] = {}
    g_score: Dict[GridKey, float] = {start_key: 0.0}
    visited = 0
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while open_heap and visited < max_expansions:
        _, cur = heapq.heappop(open_heap)
        visited += 1
        if cur == goal_key:
            keys = [cur]
            while cur in came:
                cur = came[cur]
                keys.append(cur)
            keys.reverse()
            points = [(start[0], start[1], start[2])]
            points.extend(pos(k) for k in keys[1:-1])
            points.append((goal[0], goal[1], goal[2]))
            points = densify(points, 0.5)
            if len(points) >= 5 and path_collision_free(points, obstacles, clearance):
                return points
            return None

        for dx, dy in neighbors:
            nxt = (cur[0] + dx, cur[1] + dy)
            nxt_pos = pos(nxt)
            cur_pos = pos(cur)
            if not is_free(nxt_pos, obstacles, bounds, clearance):
                continue
            if segment_collision(obstacles, cur_pos, nxt_pos, clearance, 0.15).collides:
                continue
            tentative = g_score[cur] + math.dist(cur_pos, nxt_pos)
            if tentative < g_score.get(nxt, float("inf")):
                came[nxt] = cur
                g_score[nxt] = tentative
                h = math.hypot(nxt[0] - goal_key[0], nxt[1] - goal_key[1])
                heapq.heappush(open_heap, (tentative + h, nxt))
    return None


def sample_circle(center: Point3, radius: float, step: float, z_values: Iterable[float]) -> List[Point3]:
    cx, cy, _ = center
    points: List[Point3] = []
    cells = int(math.ceil(radius / step))
    for ix in range(-cells, cells + 1):
        for iy in range(-cells, cells + 1):
            x = cx + ix * step
            y = cy + iy * step
            if math.hypot(x - cx, y - cy) <= radius:
                for z in z_values:
                    points.append((x, y, z))
    return points
