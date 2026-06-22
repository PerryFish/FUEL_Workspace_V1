#!/usr/bin/env python3
import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class Collision:
    collides: bool
    obstacle: str = "none"
    point: Tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class Obstacle:
    name: str
    kind: str
    center: Tuple[float, float, float]
    size: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    radius: float = 0.0
    height: float = 0.0

    def contains(self, x: float, y: float, z: float, clearance: float) -> bool:
        cx, cy, cz = self.center
        if self.kind == "box":
            sx, sy, sz = self.size
            return (
                abs(x - cx) <= sx * 0.5 + clearance
                and abs(y - cy) <= sy * 0.5 + clearance
                and abs(z - cz) <= sz * 0.5 + clearance
            )
        if self.kind == "cylinder":
            return (
                math.hypot(x - cx, y - cy) <= self.radius + clearance
                and abs(z - cz) <= self.height * 0.5 + clearance
            )
        return False


OBSTACLE_RE = re.compile(r"-\s*\{([^}]+)\}")


def parse_value_map(body: str):
    result = {}
    parts = re.split(r",\s*(?=[A-Za-z_]+:)", body)
    for part in parts:
        if ":" not in part:
            continue
        key, value = part.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def parse_vec(text: str) -> Tuple[float, float, float]:
    nums = [float(v) for v in re.findall(r"[-0-9.]+", text)]
    if len(nums) != 3:
        raise ValueError(f"expected 3-vector, got {text}")
    return nums[0], nums[1], nums[2]


def load_obstacles(world_config: Path) -> List[Obstacle]:
    text = world_config.read_text(errors="replace")
    obstacles: List[Obstacle] = []
    for match in OBSTACLE_RE.finditer(text):
        values = parse_value_map(match.group(1))
        name = values.get("name", f"obstacle_{len(obstacles)}")
        kind = values.get("type", "box")
        center = parse_vec(values.get("center", "[0,0,0]"))
        if kind == "box":
            obstacles.append(Obstacle(name=name, kind=kind, center=center, size=parse_vec(values.get("size", "[0,0,0]"))))
        elif kind == "cylinder":
            obstacles.append(
                Obstacle(
                    name=name,
                    kind=kind,
                    center=center,
                    radius=float(values.get("radius", "0")),
                    height=float(values.get("height", "0")),
                )
            )
    return obstacles


def point_collision(obstacles: List[Obstacle], p, clearance: float) -> Collision:
    x, y, z = p
    for obstacle in obstacles:
        if obstacle.contains(x, y, z, clearance):
            return Collision(True, obstacle.name, (x, y, z))
    return Collision(False)


def segment_collision(obstacles: List[Obstacle], p1, p2, clearance: float, resolution: float) -> Collision:
    length = math.dist(p1, p2)
    steps = max(1, int(math.ceil(length / max(1e-6, resolution))))
    for i in range(steps + 1):
        r = i / steps
        p = tuple(p1[j] + (p2[j] - p1[j]) * r for j in range(3))
        hit = point_collision(obstacles, p, clearance)
        if hit.collides:
            return hit
    return Collision(False)


def path_collision(obstacles: List[Obstacle], points, clearance: float, resolution: float) -> Collision:
    if not points:
        return Collision(False)
    for p in points:
        hit = point_collision(obstacles, p, clearance)
        if hit.collides:
            return hit
    for a, b in zip(points, points[1:]):
        hit = segment_collision(obstacles, a, b, clearance, resolution)
        if hit.collides:
            return hit
    return Collision(False)


def parse_point(values, offset: int):
    return (float(values[offset]), float(values[offset + 1]), float(values[offset + 2]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world-config", required=True)
    parser.add_argument("--clearance", type=float, default=0.35)
    parser.add_argument("--resolution", type=float, default=0.1)
    parser.add_argument("--point", nargs=3)
    parser.add_argument("--segment", nargs=6)
    parser.add_argument("--path", nargs="+")
    args = parser.parse_args()

    obstacles = load_obstacles(Path(args.world_config))
    if args.point:
        result = point_collision(obstacles, parse_point(args.point, 0), args.clearance)
    elif args.segment:
        result = segment_collision(
            obstacles,
            parse_point(args.segment, 0),
            parse_point(args.segment, 3),
            args.clearance,
            args.resolution,
        )
    elif args.path:
        vals = [float(v) for v in args.path]
        if len(vals) % 3:
            raise SystemExit("--path expects xyz triples")
        points = [parse_point(vals, i) for i in range(0, len(vals), 3)]
        result = path_collision(obstacles, points, args.clearance, args.resolution)
    else:
        raise SystemExit("provide --point, --segment, or --path")

    x, y, z = result.point
    print(f"collision={'true' if result.collides else 'false'}")
    print(f"collision_obstacle={result.obstacle}")
    print(f"collision_point=({x:.3f},{y:.3f},{z:.3f})")
    if result.collides:
        print(f"PATH_COLLISION_REJECTED collision_obstacle={result.obstacle} collision_point=({x:.3f},{y:.3f},{z:.3f})")


if __name__ == "__main__":
    main()
