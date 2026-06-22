# P2B Coverage Metric Report

## Coverage Proxy Definition

Exact volumetric coverage is not available from a single canonical topic in this ROS2 port, so P2B uses a proxy:

```text
coverage_proxy = explored_grid_point_count / max(global_cloud_point_count, 1)
```

`coverage_proxy_is_not_exact_metric=YES`

This proxy is useful for repeatable trend comparison, but it is not a strict FUEL exploration completion percentage. It depends on point cloud density, publish timing, and whether the first recorder sample occurs before both explored and global cloud topics are populated.

## Before Fix: Office 300s

Metrics directory: `reports/p2b_metrics/p2b_office_300s_20260621_162703`

```text
duration_sec=304.609
global_cloud_points_last=13582
explored_grid_start=1034
explored_grid_end=1565
explored_grid_gain=531
occupancy_grid_start=132
occupancy_grid_end=195
coverage_proxy_start=0.000000
coverage_proxy_end=0.115226
coverage_proxy_gain=0.115226
map_cloud_count=600
local_cloud_count=1800
```

The first proxy sample was `0.0` because the recorder started before the first complete global/explored pair was available. The more reliable raw point metric for this run is `explored_grid_gain=531`.

## After Fix: Office 120s

Metrics directory: `reports/p2b_metrics/p2b_office_120s_20260621_163633`

```text
duration_sec=124.600
global_cloud_points_last=13582
explored_grid_start=1359
explored_grid_end=1705
explored_grid_gain=346
occupancy_grid_start=185
occupancy_grid_end=222
coverage_proxy_start=0.000000
coverage_proxy_end=0.125534
coverage_proxy_gain=0.125534
map_cloud_count=240
local_cloud_count=720
```

The post-fix 120s run gained 346 explored-grid points in a shorter run, which is consistent with improved early exploration. It still reached motion stalls, so the result remains `PARTIAL`.

## Interpretation

- Coverage does increase, so sensing, mapping, and visualization are functional.
- Coverage growth stalls later even with nonzero frontier candidates.
- The post-fix run improves early coverage rate, but long-run coverage continuity still needs another goal/frontier policy pass before multi-map benchmarking.
