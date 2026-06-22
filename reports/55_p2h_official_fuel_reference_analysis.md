# P2H Official FUEL Reference Analysis

Official FUEL references:

- https://github.com/HKUST-Aerial-Robotics/FUEL#exploring-different-environments
- https://github.com/HKUST-Aerial-Robotics/FUEL#creating-a-pcd-environment

## Relevant Official Ideas

- Frontier Information Structure (FIS): maintain frontier information incrementally instead of treating every frontier point independently.
- Hierarchical planning: choose a coarse frontier coverage direction first, then refine local viewpoints and trajectory.
- Frontier coverage path: favor a path that covers frontier regions efficiently, not just a single isolated point.
- Local viewpoint refinement: improve the exact viewpoint around a frontier before committing to trajectory generation.
- Minimum-time trajectory generation: downstream motion should optimize execution time after the target/path is chosen.
- Environment and bounding box discipline: official examples rely on `.pcd` maps and exploration bounds, which helps keep candidate generation meaningful.

## ROS2 Lite Gap

The current ROS2 lite version does not implement the full FIS or hierarchical planner. It uses lightweight frontier clusters, a best viewpoint publisher, an exploration manager, a goal-to-path bridge, and a simple trajectory server. The observed route issue was not a trajectory generation failure; it was upstream target scoring that underweighted path/distance cost.

## Minimal Transfer

The safe P2H transfer is path-aware frontier scoring and light local viewpoint refinement behavior:

- keep the existing topics and nodes;
- keep the existing office map and local sensing;
- increase path/distance cost in viewpoint scoring;
- add small bonuses for nearby useful frontiers and new regions;
- reduce active-region stickiness;
- leave full FIS, global TSP-style coverage ordering, and minimum-time trajectory optimization for later phases.
