#ifndef FUEL_ROS2_PATH_SEARCHING_FUEL_GRID_ASTAR3D_HPP_
#define FUEL_ROS2_PATH_SEARCHING_FUEL_GRID_ASTAR3D_HPP_

#include <functional>
#include <string>
#include <vector>

#include <Eigen/Core>

namespace fuel_ros2
{

class FuelGridAstar3D
{
public:
  struct Config
  {
    double resolution{0.2};
    int neighbor_mode{26};
    int max_search_nodes{80000};
    Eigen::Vector3d min{-10.0, -10.0, 0.5};
    Eigen::Vector3d max{10.0, 10.0, 3.0};
    bool simplify_path{true};
    bool simplify_line_of_sight{true};
  };

  struct SearchResult
  {
    bool success{false};
    std::string reason{"not_started"};
    std::vector<Eigen::Vector3d> path;
    std::vector<Eigen::Vector3d> visited;
    double path_length{0.0};
    int expanded_nodes{0};
  };

  using TraversableFn = std::function<bool(const Eigen::Vector3d &)>;

  void configure(const Config & config);
  SearchResult search(
    const Eigen::Vector3d & start,
    const Eigen::Vector3d & goal,
    const TraversableFn & traversable) const;

  const Config & config() const;

private:
  struct GridIndex
  {
    int x{0};
    int y{0};
    int z{0};
  };

  struct GridIndexHash
  {
    std::size_t operator()(const GridIndex & idx) const;
  };

  struct GridIndexEq
  {
    bool operator()(const GridIndex & a, const GridIndex & b) const;
  };

  struct QueueNode
  {
    GridIndex index;
    double f_score{0.0};
    double g_score{0.0};
  };

  struct QueueCompare
  {
    bool operator()(const QueueNode & a, const QueueNode & b) const;
  };

  bool isInside(const Eigen::Vector3d & p) const;
  GridIndex pointToIndex(const Eigen::Vector3d & p) const;
  Eigen::Vector3d indexToPoint(const GridIndex & idx) const;
  double heuristic(const GridIndex & a, const GridIndex & b) const;
  double stepCost(const GridIndex & a, const GridIndex & b) const;
  std::vector<GridIndex> neighbors(const GridIndex & idx) const;
  bool hasLineOfSight(
    const Eigen::Vector3d & a,
    const Eigen::Vector3d & b,
    const TraversableFn & traversable) const;
  std::vector<Eigen::Vector3d> simplify(
    const std::vector<Eigen::Vector3d> & path,
    const TraversableFn & traversable) const;
  static double pathLength(const std::vector<Eigen::Vector3d> & path);

  Config config_;
};

}  // namespace fuel_ros2

#endif  // FUEL_ROS2_PATH_SEARCHING_FUEL_GRID_ASTAR3D_HPP_
