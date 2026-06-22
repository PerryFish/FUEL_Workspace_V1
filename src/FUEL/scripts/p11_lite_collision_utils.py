#!/usr/bin/env python3
import heapq
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


Point3 = Tuple[float, float, float]
GridKey = Tuple[int, int]


@dataclass
class CollisionCheckResult:
    collision_free: bool
    min_clearance: float
    first_collision_point: Optional[Point3] = None
    collision_segment_index: int = -1


class OccupancyGrid2D:
    def __init__(self, bounds: Dict[str, float], grid_resolution: float = 0.25, inflation_radius: float = 0.45):
        self.bounds = bounds
        self.grid_resolution = max(1e-3, float(grid_resolution))
        self.inflation_radius = max(0.0, float(inflation_radius))
        self.occupied_raw: Set[GridKey] = set()
        self.occupied_inflated: Set[GridKey] = set()

    def key(self, point: Point3) -> GridKey:
        x, y, _z = point
        return (
            int(round((x - self.bounds["min_x"]) / self.grid_resolution)),
            int(round((y - self.bounds["min_y"]) / self.grid_resolution)),
        )

    def point(self, key: GridKey, z: float = 1.2) -> Point3:
        return (
            self.bounds["min_x"] + key[0] * self.grid_resolution,
            self.bounds["min_y"] + key[1] * self.grid_resolution,
            z,
        )

    def in_bounds_key(self, key: GridKey) -> bool:
        x, y, _z = self.point(key)
        return self.bounds["min_x"] <= x <= self.bounds["max_x"] and self.bounds["min_y"] <= y <= self.bounds["max_y"]

    def update_from_points(self, points: Iterable[Point3]) -> None:
        self.occupied_raw = {self.key(point) for point in points if self._point_in_bounds(point)}
        self.occupied_inflated = set(self.occupied_raw)
        cells = int(math.ceil(self.inflation_radius / self.grid_resolution))
        for key in self.occupied_raw:
            ox, oy, _ = self.point(key)
            for dx in range(-cells, cells + 1):
                for dy in range(-cells, cells + 1):
                    inflated = (key[0] + dx, key[1] + dy)
                    ix, iy, _ = self.point(inflated)
                    if self.in_bounds_key(inflated) and math.hypot(ix - ox, iy - oy) <= self.inflation_radius + 1e-6:
                        self.occupied_inflated.add(inflated)

    def _point_in_bounds(self, point: Point3) -> bool:
        x, y, _ = point
        return self.bounds["min_x"] <= x <= self.bounds["max_x"] and self.bounds["min_y"] <= y <= self.bounds["max_y"]

    def is_occupied(self, point: Point3) -> bool:
        return self.key(point) in self.occupied_inflated

    def clearance(self, point: Point3, max_search_cells: int = 40) -> float:
        key = self.key(point)
        if key in self.occupied_inflated:
            return 0.0
        best = float("inf")
        for occ in self.occupied_raw:
            dx = (occ[0] - key[0]) * self.grid_resolution
            dy = (occ[1] - key[1]) * self.grid_resolution
            d = math.hypot(dx, dy)
            if d < best:
                best = d
            if best <= self.grid_resolution:
                break
        if best == float("inf"):
            return max_search_cells * self.grid_resolution
        return best

    def check_segment(self, p0: Point3, p1: Point3, segment_index: int = 0) -> CollisionCheckResult:
        length = math.dist(p0, p1)
        steps = max(1, int(math.ceil(length / max(self.grid_resolution * 0.5, 1e-3))))
        min_clearance = float("inf")
        for i in range(steps + 1):
            r = i / steps
            point = (p0[0] + (p1[0] - p0[0]) * r, p0[1] + (p1[1] - p0[1]) * r, p0[2] + (p1[2] - p0[2]) * r)
            clearance = self.clearance(point)
            min_clearance = min(min_clearance, clearance)
            if self.is_occupied(point):
                return CollisionCheckResult(False, min_clearance, point, segment_index)
        return CollisionCheckResult(True, min_clearance if min_clearance != float("inf") else 999.0, None, -1)

    def check_path(self, path: Sequence[Point3]) -> CollisionCheckResult:
        if len(path) < 2:
            return CollisionCheckResult(False, 0.0, None, -1)
        min_clearance = float("inf")
        for idx, (p0, p1) in enumerate(zip(path, path[1:])):
            result = self.check_segment(p0, p1, idx)
            min_clearance = min(min_clearance, result.min_clearance)
            if not result.collision_free:
                return CollisionCheckResult(False, min_clearance, result.first_collision_point, idx)
        return CollisionCheckResult(True, min_clearance if min_clearance != float("inf") else 999.0, None, -1)

    def is_segment_collision_free(self, p0: Point3, p1: Point3) -> bool:
        return self.check_segment(p0, p1).collision_free

    def is_path_collision_free(self, path: Sequence[Point3]) -> bool:
        return self.check_path(path).collision_free


def densify_path(points: Sequence[Point3], step: float = 0.3) -> List[Point3]:
    if len(points) < 2:
        return list(points)
    result = [points[0]]
    for a, b in zip(points, points[1:]):
        n = max(1, int(math.ceil(math.dist(a, b) / max(step, 1e-3))))
        for i in range(1, n + 1):
            r = i / n
            result.append((a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r, a[2] + (b[2] - a[2]) * r))
    return result


def astar_detour_path(start: Point3, goal: Point3, grid: OccupancyGrid2D, max_expansions: int = 60000) -> Optional[List[Point3]]:
    start_key = grid.key(start)
    goal_key = grid.key(goal)
    if not grid.in_bounds_key(start_key) or not grid.in_bounds_key(goal_key):
        return None
    if start_key in grid.occupied_inflated or goal_key in grid.occupied_inflated:
        return None

    open_heap: List[Tuple[float, GridKey]] = []
    heapq.heappush(open_heap, (0.0, start_key))
    came: Dict[GridKey, GridKey] = {}
    g_score: Dict[GridKey, float] = {start_key: 0.0}
    visited: Set[GridKey] = set()
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    z = max(0.2, min(start[2], goal[2]))

    expansions = 0
    while open_heap and expansions < max_expansions:
        _score, cur = heapq.heappop(open_heap)
        if cur in visited:
            continue
        visited.add(cur)
        expansions += 1
        if cur == goal_key:
            keys = [cur]
            while cur in came:
                cur = came[cur]
                keys.append(cur)
            keys.reverse()
            raw = [start]
            raw.extend(grid.point(k, z) for k in keys[1:-1])
            raw.append(goal)
            path = densify_path(raw, max(grid.grid_resolution, 0.25))
            return path if len(path) >= 5 and grid.check_path(path).collision_free else None

        cur_point = grid.point(cur, z)
        for dx, dy in neighbors:
            nxt = (cur[0] + dx, cur[1] + dy)
            if nxt in visited or not grid.in_bounds_key(nxt) or nxt in grid.occupied_inflated:
                continue
            nxt_point = grid.point(nxt, z)
            if not grid.check_segment(cur_point, nxt_point).collision_free:
                continue
            tentative = g_score[cur] + math.dist(cur_point, nxt_point)
            if tentative < g_score.get(nxt, float("inf")):
                came[nxt] = cur
                g_score[nxt] = tentative
                h = math.hypot(nxt[0] - goal_key[0], nxt[1] - goal_key[1])
                heapq.heappush(open_heap, (tentative + h, nxt))
    return None


def is_segment_collision_free(grid: OccupancyGrid2D, p0: Point3, p1: Point3) -> bool:
    return grid.is_segment_collision_free(p0, p1)


def is_path_collision_free(grid: OccupancyGrid2D, path: Sequence[Point3]) -> bool:
    return grid.is_path_collision_free(path)
