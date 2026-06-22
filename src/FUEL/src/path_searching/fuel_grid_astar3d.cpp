#include "fuel_ros2/path_searching/fuel_grid_astar3d.hpp"

#include <algorithm>
#include <cmath>
#include <limits>
#include <queue>
#include <unordered_map>
#include <unordered_set>

namespace fuel_ros2
{

std::size_t FuelGridAstar3D::GridIndexHash::operator()(const GridIndex & idx) const
{
  const std::size_t x = static_cast<std::size_t>(idx.x) * 73856093u;
  const std::size_t y = static_cast<std::size_t>(idx.y) * 19349663u;
  const std::size_t z = static_cast<std::size_t>(idx.z) * 83492791u;
  return x ^ y ^ z;
}

bool FuelGridAstar3D::GridIndexEq::operator()(const GridIndex & a, const GridIndex & b) const
{
  return a.x == b.x && a.y == b.y && a.z == b.z;
}

bool FuelGridAstar3D::QueueCompare::operator()(const QueueNode & a, const QueueNode & b) const
{
  return a.f_score > b.f_score;
}

void FuelGridAstar3D::configure(const Config & config)
{
  config_ = config;
  if (config_.resolution <= 0.0) {
    config_.resolution = 0.2;
  }
  if (config_.neighbor_mode != 6 && config_.neighbor_mode != 26) {
    config_.neighbor_mode = 26;
  }
  if (config_.max_search_nodes <= 0) {
    config_.max_search_nodes = 80000;
  }
}

FuelGridAstar3D::SearchResult FuelGridAstar3D::search(
  const Eigen::Vector3d & start,
  const Eigen::Vector3d & goal,
  const TraversableFn & traversable) const
{
  SearchResult result;
  if (!isInside(start)) {
    result.reason = "start_outside_map";
    return result;
  }
  if (!isInside(goal)) {
    result.reason = "goal_outside_map";
    return result;
  }
  if (!traversable(start)) {
    result.reason = "start_not_traversable";
    return result;
  }
  if (!traversable(goal)) {
    result.reason = "goal_not_traversable";
    return result;
  }

  const GridIndex start_idx = pointToIndex(start);
  const GridIndex goal_idx = pointToIndex(goal);
  std::priority_queue<QueueNode, std::vector<QueueNode>, QueueCompare> open;
  std::unordered_map<GridIndex, double, GridIndexHash, GridIndexEq> g_score;
  std::unordered_map<GridIndex, GridIndex, GridIndexHash, GridIndexEq> parent;
  std::unordered_set<GridIndex, GridIndexHash, GridIndexEq> closed;

  g_score[start_idx] = 0.0;
  open.push(QueueNode{start_idx, heuristic(start_idx, goal_idx), 0.0});

  while (!open.empty()) {
    const QueueNode current = open.top();
    open.pop();
    if (closed.find(current.index) != closed.end()) {
      continue;
    }
    closed.insert(current.index);
    result.visited.push_back(indexToPoint(current.index));
    result.expanded_nodes = static_cast<int>(closed.size());

    if (GridIndexEq{}(current.index, goal_idx)) {
      std::vector<Eigen::Vector3d> reverse_path;
      GridIndex cursor = current.index;
      reverse_path.push_back(goal);
      while (!GridIndexEq{}(cursor, start_idx)) {
        const auto it = parent.find(cursor);
        if (it == parent.end()) {
          result.reason = "broken_parent_chain";
          return result;
        }
        cursor = it->second;
        reverse_path.push_back(indexToPoint(cursor));
      }
      reverse_path.back() = start;
      std::reverse(reverse_path.begin(), reverse_path.end());
      result.path = simplify(reverse_path, traversable);
      result.path_length = pathLength(result.path);
      result.success = true;
      result.reason = "success";
      return result;
    }

    if (result.expanded_nodes >= config_.max_search_nodes) {
      result.reason = "max_search_nodes";
      return result;
    }

    for (const auto & next : neighbors(current.index)) {
      const Eigen::Vector3d next_pos = indexToPoint(next);
      if (!isInside(next_pos) || !traversable(next_pos) || closed.find(next) != closed.end()) {
        continue;
      }
      if (!hasLineOfSight(indexToPoint(current.index), next_pos, traversable)) {
        continue;
      }
      const double tentative_g = current.g_score + stepCost(current.index, next);
      const auto existing = g_score.find(next);
      if (existing != g_score.end() && tentative_g >= existing->second) {
        continue;
      }
      parent[next] = current.index;
      g_score[next] = tentative_g;
      open.push(QueueNode{next, tentative_g + heuristic(next, goal_idx), tentative_g});
    }
  }

  result.reason = "open_set_empty";
  return result;
}

const FuelGridAstar3D::Config & FuelGridAstar3D::config() const
{
  return config_;
}

bool FuelGridAstar3D::isInside(const Eigen::Vector3d & p) const
{
  return p.x() >= config_.min.x() && p.y() >= config_.min.y() && p.z() >= config_.min.z() &&
    p.x() <= config_.max.x() && p.y() <= config_.max.y() && p.z() <= config_.max.z();
}

FuelGridAstar3D::GridIndex FuelGridAstar3D::pointToIndex(const Eigen::Vector3d & p) const
{
  return GridIndex{
    static_cast<int>(std::floor((p.x() - config_.min.x()) / config_.resolution)),
    static_cast<int>(std::floor((p.y() - config_.min.y()) / config_.resolution)),
    static_cast<int>(std::floor((p.z() - config_.min.z()) / config_.resolution))};
}

Eigen::Vector3d FuelGridAstar3D::indexToPoint(const GridIndex & idx) const
{
  return Eigen::Vector3d(
    config_.min.x() + (static_cast<double>(idx.x) + 0.5) * config_.resolution,
    config_.min.y() + (static_cast<double>(idx.y) + 0.5) * config_.resolution,
    config_.min.z() + (static_cast<double>(idx.z) + 0.5) * config_.resolution);
}

double FuelGridAstar3D::heuristic(const GridIndex & a, const GridIndex & b) const
{
  const double dx = static_cast<double>(a.x - b.x);
  const double dy = static_cast<double>(a.y - b.y);
  const double dz = static_cast<double>(a.z - b.z);
  return std::sqrt(dx * dx + dy * dy + dz * dz) * config_.resolution;
}

double FuelGridAstar3D::stepCost(const GridIndex & a, const GridIndex & b) const
{
  return heuristic(a, b);
}

std::vector<FuelGridAstar3D::GridIndex> FuelGridAstar3D::neighbors(const GridIndex & idx) const
{
  std::vector<GridIndex> out;
  out.reserve(config_.neighbor_mode == 6 ? 6 : 26);
  for (int dx = -1; dx <= 1; ++dx) {
    for (int dy = -1; dy <= 1; ++dy) {
      for (int dz = -1; dz <= 1; ++dz) {
        const int manhattan = std::abs(dx) + std::abs(dy) + std::abs(dz);
        if (manhattan == 0) {
          continue;
        }
        if (config_.neighbor_mode == 6 && manhattan != 1) {
          continue;
        }
        out.push_back(GridIndex{idx.x + dx, idx.y + dy, idx.z + dz});
      }
    }
  }
  return out;
}

bool FuelGridAstar3D::hasLineOfSight(
  const Eigen::Vector3d & a,
  const Eigen::Vector3d & b,
  const TraversableFn & traversable) const
{
  const Eigen::Vector3d delta = b - a;
  const double length = delta.norm();
  if (length < 1e-9) {
    return true;
  }
  const int samples = std::max(1, static_cast<int>(std::ceil(length / (0.5 * config_.resolution))));
  for (int i = 1; i <= samples; ++i) {
    const Eigen::Vector3d p = a + delta * (static_cast<double>(i) / static_cast<double>(samples));
    if (!traversable(p)) {
      return false;
    }
  }
  return true;
}

std::vector<Eigen::Vector3d> FuelGridAstar3D::simplify(
  const std::vector<Eigen::Vector3d> & path,
  const TraversableFn & traversable) const
{
  if (!config_.simplify_path || path.size() <= 2) {
    return path;
  }
  std::vector<Eigen::Vector3d> simplified;
  simplified.push_back(path.front());
  std::size_t anchor = 0;
  while (anchor + 1 < path.size()) {
    std::size_t best = anchor + 1;
    if (config_.simplify_line_of_sight) {
      for (std::size_t candidate = path.size() - 1; candidate > anchor + 1; --candidate) {
        if (hasLineOfSight(path[anchor], path[candidate], traversable)) {
          best = candidate;
          break;
        }
      }
    }
    simplified.push_back(path[best]);
    anchor = best;
  }
  return simplified;
}

double FuelGridAstar3D::pathLength(const std::vector<Eigen::Vector3d> & path)
{
  double length = 0.0;
  for (std::size_t i = 1; i < path.size(); ++i) {
    length += (path[i] - path[i - 1]).norm();
  }
  return length;
}

}  // namespace fuel_ros2
