# FUEL Unified Run Summary

## Basic Info
- Date: 2026-06-22T12:15:53+0800
- Task name: p2g_final_syntax_check
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: bash -lc python3 -m py_compile scripts/fuel_frontier_reachability_recorder.py scripts/analyze_frontier_scoring_and_reachability.py scripts/generate_unified_summary_log.py scripts/generate_full_run_log.py src/FUEL/scripts/frontier_viewpoint_lite.py src/FUEL/scripts/exploration_manager_lite.py src/FUEL/scripts/p11_lite_goal_to_path_bridge.py && bash -n scripts/run_p2g_frontier_300s_baseline.sh scripts/run_p2g_coverage_300s_after_fix.sh scripts/run_p2g_coverage_600s_after_fix.sh scripts/run_p2g_visual_coverage_300s.sh scripts/export_p2g_debug_package.sh
- Exit code: 0
- Result: PASS
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_121546_p2g_final_syntax_check.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_121548_p2g_final_syntax_check_summary.md

## Environment
- ROS_DISTRO: humble
- ROS_DOMAIN_ID: UNAVAILABLE
- RMW_IMPLEMENTATION: UNAVAILABLE
- ROS_LOCALHOST_ONLY: 0
- FASTDDS_BUILTIN_TRANSPORTS: UNAVAILABLE
- DISPLAY: :0
- FUEL_WS: UNAVAILABLE

## Git / Source State
- current_commit: 3b11fc50c0ab8e84f9093f084ce80f4d1af6088d
- git status short:

```text
?? ./
```
- changed files:

```text
./
```
- latest diff patch if available: reports/p2g_final_code_diff_20260622_121546.patch

## Key Runtime Evidence
### Node List Summary
```text
UNAVAILABLE
```
### Topic List Summary
```text
/parameter_events
/rosout
```
### Important Topics Detected
- /odom: NO_OR_NOT_RUNNING
- /planning/pos_cmd: NO_OR_NOT_RUNNING
- /planning/travel_traj: NO_OR_NOT_RUNNING
- /fuel/p10_lite/active_path: NO_OR_NOT_RUNNING
- /fuel/p10_lite/traj_server_status: NO_OR_NOT_RUNNING
- /fuel/p11_lite/goal_to_path_status: NO_OR_NOT_RUNNING
- /fuel/p11_lite/exploration_goal: NO_OR_NOT_RUNNING
- /fuel/p11_lite/frontier_viewpoints: NO_OR_NOT_RUNNING
- /fuel/p11_lite/frontier_candidates_raw: NO_OR_NOT_RUNNING
- /fuel/p11_lite/visual/all_markers: NO_OR_NOT_RUNNING

### Process Cleanup Status
```text
nuaa           1  0.0  0.0   3676  1436 ?        Ss   12:15   0:00 bwrap --new-session --die-with-parent --ro-bind / / --dev /dev --bind /tmp /tmp --perms 555 --tmpfs /tmp/.git --remount-ro /tmp/.git --perms 555 --tmpfs /tmp/.agents --remount-ro /tmp/.agents --perms 555 --tmpfs /tmp/.codex --remount-ro /tmp/.codex --bind /home/nuaa/ZHY/FUEL_PLANNER_V3 /home/nuaa/ZHY/FUEL_PLANNER_V3 --perms 555 --tmpfs /home/nuaa/ZHY/FUEL_PLANNER_V3/.git --remount-ro /home/nuaa/ZHY/FUEL_PLANNER_V3/.git --perms 555 --tmpfs /home/nuaa/ZHY/FUEL_PLANNER_V3/.agents --remount-ro /home/nuaa/ZHY/FUEL_PLANNER_V3/.agents --perms 555 --tmpfs /home/nuaa/ZHY/FUEL_PLANNER_V3/.codex --remount-ro /home/nuaa/ZHY/FUEL_PLANNER_V3/.codex --unshare-user --unshare-pid --proc /proc -- /home/nuaa/.codex/tmp/arg0/codex-arg0e3ahOo/codex-linux-sandbox --sandbox-policy-cwd /home/nuaa/ZHY/FUEL_PLANNER_V3 --command-cwd /home/nuaa/ZHY/FUEL_PLANNER_V3 --permission-profile {"type":"managed","file_system":{"type":"restricted","entries":[{"path":{"type":"special","value":{"kind":"root"}},"access":"read"},{"path":{"type":"path","path":"/home/nuaa/ZHY/FUEL_PLANNER_V3"},"access":"write"},{"path":{"type":"special","value":{"kind":"slash_tmp"}},"access":"write"},{"path":{"type":"special","value":{"kind":"tmpdir"}},"access":"write"},{"path":{"type":"path","path":"/home/nuaa/ZHY/FUEL_PLANNER_V3/.git"},"access":"read"},{"path":{"type":"path","path":"/home/nuaa/ZHY/FUEL_PLANNER_V3/.agents"},"access":"read"},{"path":{"type":"path","path":"/home/nuaa/ZHY/FUEL_PLANNER_V3/.codex"},"access":"read"}]},"network":"enabled"} --apply-seccomp-then-exec -- /bin/bash -c __CODEX_SNAPSHOT_OVERRIDE_SET_0="${CODEX_THREAD_ID+x}" __CODEX_SNAPSHOT_OVERRIDE_0="${CODEX_THREAD_ID-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_0="${ALL_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_0="${ALL_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_1="${BUNDLE_HTTPS_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_1="${BUNDLE_HTTPS_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_2="${BUNDLE_HTTP_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_2="${BUNDLE_HTTP_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_3="${BUNDLE_NO_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_3="${BUNDLE_NO_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_4="${BUNDLE_SSL_CA_CERT+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_4="${BUNDLE_SSL_CA_CERT-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_5="${CODEX_CA_CERTIFICATE+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_5="${CODEX_CA_CERTIFICATE-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_6="${CODEX_NETWORK_ALLOW_LOCAL_BINDING+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_6="${CODEX_NETWORK_ALLOW_LOCAL_BINDING-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_7="${CODEX_NETWORK_PROXY_ACTIVE+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_7="${CODEX_NETWORK_PROXY_ACTIVE-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_8="${CURL_CA_BUNDLE+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_8="${CURL_CA_BUNDLE-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_9="${DOCKER_HTTPS_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_9="${DOCKER_HTTPS_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_10="${DOCKER_HTTP_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_10="${DOCKER_HTTP_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_11="${ELECTRON_GET_USE_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_11="${ELECTRON_GET_USE_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_12="${FTP_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_12="${FTP_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_13="${GIT_SSL_CAINFO+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_13="${GIT_SSL_CAINFO-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_14="${HTTPS_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_14="${HTTPS_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_15="${HTTP_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_15="${HTTP_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_16="${NODE_EXTRA_CA_CERTS+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_16="${NODE_EXTRA_CA_CERTS-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_17="${NODE_USE_ENV_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_17="${NODE_USE_ENV_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_18="${NO_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_18="${NO_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_19="${NPM_CONFIG_CAFILE+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_19="${NPM_CONFIG_CAFILE-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_20="${NPM_CONFIG_HTTPS_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_20="${NPM_CONFIG_HTTPS_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_21="${NPM_CONFIG_HTTP_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_21="${NPM_CONFIG_HTTP_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_22="${NPM_CONFIG_NOPROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_22="${NPM_CONFIG_NOPROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_23="${NPM_CONFIG_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_23="${NPM_CONFIG_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_24="${PIP_CERT+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_24="${PIP_CERT-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_25="${PIP_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_25="${PIP_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_26="${REQUESTS_CA_BUNDLE+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_26="${REQUESTS_CA_BUNDLE-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_27="${SSL_CERT_FILE+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_27="${SSL_CERT_FILE-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_28="${WSS_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_28="${WSS_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_29="${WS_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_29="${WS_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_30="${YARN_HTTPS_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_30="${YARN_HTTPS_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_31="${YARN_HTTP_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_31="${YARN_HTTP_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_32="${YARN_NO_PROXY+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_32="${YARN_NO_PROXY-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_33="${all_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_33="${all_proxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_34="${ftp_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_34="${ftp_proxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_35="${http_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_35="${http_proxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_36="${https_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_36="${https_proxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_37="${no_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_37="${no_proxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_38="${npm_config_cafile+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_38="${npm_config_cafile-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_39="${npm_config_http_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_39="${npm_config_http_proxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_40="${npm_config_https_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_40="${npm_config_https_proxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_41="${npm_config_noproxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_41="${npm_config_noproxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_42="${npm_config_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_42="${npm_config_proxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_43="${ws_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_43="${ws_proxy-}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_44="${wss_proxy+x}" __CODEX_SNAPSHOT_PROXY_OVERRIDE_44="${wss_proxy-}" __CODEX_SNAPSHOT_PROXY_ENV_SET="${CODEX_NETWORK_PROXY_ACTIVE+x}"  if . '/home/nuaa/.codex/shell_snapshots/019ee8ac-2fc0-7953-a4e3-fc6976f7323a.1782020059098046389.sh' >/dev/null 2>&1; then :; fi  if [ -n "${__CODEX_SNAPSHOT_OVERRIDE_SET_0}" ]; then export CODEX_THREAD_ID="${__CODEX_SNAPSHOT_OVERRIDE_0}"; else unset CODEX_THREAD_ID; fi if [ -n "$__CODEX_SNAPSHOT_PROXY_ENV_SET" ] || [ -n "${CODEX_NETWORK_PROXY_ACTIVE+x}" ]; then if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_0}" ]; then export ALL_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_0}"; else unset ALL_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_1}" ]; then export BUNDLE_HTTPS_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_1}"; else unset BUNDLE_HTTPS_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_2}" ]; then export BUNDLE_HTTP_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_2}"; else unset BUNDLE_HTTP_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_3}" ]; then export BUNDLE_NO_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_3}"; else unset BUNDLE_NO_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_4}" ]; then export BUNDLE_SSL_CA_CERT="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_4}"; else unset BUNDLE_SSL_CA_CERT; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_5}" ]; then export CODEX_CA_CERTIFICATE="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_5}"; else unset CODEX_CA_CERTIFICATE; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_6}" ]; then export CODEX_NETWORK_ALLOW_LOCAL_BINDING="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_6}"; else unset CODEX_NETWORK_ALLOW_LOCAL_BINDING; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_7}" ]; then export CODEX_NETWORK_PROXY_ACTIVE="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_7}"; else unset CODEX_NETWORK_PROXY_ACTIVE; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_8}" ]; then export CURL_CA_BUNDLE="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_8}"; else unset CURL_CA_BUNDLE; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_9}" ]; then export DOCKER_HTTPS_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_9}"; else unset DOCKER_HTTPS_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_10}" ]; then export DOCKER_HTTP_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_10}"; else unset DOCKER_HTTP_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_11}" ]; then export ELECTRON_GET_USE_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_11}"; else unset ELECTRON_GET_USE_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_12}" ]; then export FTP_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_12}"; else unset FTP_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_13}" ]; then export GIT_SSL_CAINFO="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_13}"; else unset GIT_SSL_CAINFO; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_14}" ]; then export HTTPS_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_14}"; else unset HTTPS_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_15}" ]; then export HTTP_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_15}"; else unset HTTP_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_16}" ]; then export NODE_EXTRA_CA_CERTS="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_16}"; else unset NODE_EXTRA_CA_CERTS; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_17}" ]; then export NODE_USE_ENV_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_17}"; else unset NODE_USE_ENV_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_18}" ]; then export NO_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_18}"; else unset NO_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_19}" ]; then export NPM_CONFIG_CAFILE="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_19}"; else unset NPM_CONFIG_CAFILE; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_20}" ]; then export NPM_CONFIG_HTTPS_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_20}"; else unset NPM_CONFIG_HTTPS_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_21}" ]; then export NPM_CONFIG_HTTP_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_21}"; else unset NPM_CONFIG_HTTP_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_22}" ]; then export NPM_CONFIG_NOPROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_22}"; else unset NPM_CONFIG_NOPROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_23}" ]; then export NPM_CONFIG_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_23}"; else unset NPM_CONFIG_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_24}" ]; then export PIP_CERT="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_24}"; else unset PIP_CERT; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_25}" ]; then export PIP_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_25}"; else unset PIP_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_26}" ]; then export REQUESTS_CA_BUNDLE="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_26}"; else unset REQUESTS_CA_BUNDLE; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_27}" ]; then export SSL_CERT_FILE="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_27}"; else unset SSL_CERT_FILE; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_28}" ]; then export WSS_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_28}"; else unset WSS_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_29}" ]; then export WS_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_29}"; else unset WS_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_30}" ]; then export YARN_HTTPS_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_30}"; else unset YARN_HTTPS_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_31}" ]; then export YARN_HTTP_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_31}"; else unset YARN_HTTP_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_32}" ]; then export YARN_NO_PROXY="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_32}"; else unset YARN_NO_PROXY; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_33}" ]; then export all_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_33}"; else unset all_proxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_34}" ]; then export ftp_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_34}"; else unset ftp_proxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_35}" ]; then export http_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_35}"; else unset http_proxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_36}" ]; then export https_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_36}"; else unset https_proxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_37}" ]; then export no_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_37}"; else unset no_proxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_38}" ]; then export npm_config_cafile="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_38}"; else unset npm_config_cafile; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_39}" ]; then export npm_config_http_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_39}"; else unset npm_config_http_proxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_40}" ]; then export npm_config_https_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_40}"; else unset npm_config_https_proxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_41}" ]; then export npm_config_noproxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_41}"; else unset npm_config_noproxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_42}" ]; then export npm_config_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_42}"; else unset npm_config_proxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_43}" ]; then export ws_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_43}"; else unset ws_proxy; fi if [ -n "${__CODEX_SNAPSHOT_PROXY_OVERRIDE_SET_44}" ]; then export wss_proxy="${__CODEX_SNAPSHOT_PROXY_OVERRIDE_44}"; else unset wss_proxy; fi fi if [ -n "${PATH:-}" ]; then export PATH='/home/nuaa/.codex-npmjs-141/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/codex-path':"$PATH"; else export PATH='/home/nuaa/.codex-npmjs-141/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/codex-path'; fi  exec '/bin/bash' -c 'STAMP=$(date +%Y%m%d_%H%M%S) (git diff --no-index /dev/null src/FUEL/scripts/frontier_viewpoint_lite.py || true; git diff --no-index /dev/null scripts/fuel_frontier_reachability_recorder.py || true) > "reports/p2g_final_code_diff_${STAMP}.patch" ./scripts/run_with_log.sh p2g_final_syntax_check bash -lc '"'"'python3 -m py_compile scripts/fuel_frontier_reachability_recorder.py scripts/analyze_frontier_scoring_and_reachability.py scripts/generate_unified_summary_log.py scripts/generate_full_run_log.py src/FUEL/scripts/frontier_viewpoint_lite.py src/FUEL/scripts/exploration_manager_lite.py src/FUEL/scripts/p11_lite_goal_to_path_bridge.py && bash -n scripts/run_p2g_frontier_300s_baseline.sh scripts/run_p2g_coverage_300s_after_fix.sh scripts/run_p2g_coverage_600s_after_fix.sh scripts/run_p2g_visual_coverage_300s.sh scripts/export_p2g_debug_package.sh'"'"''
nuaa           2  0.3  0.0  13516  3744 ?        S    12:15   0:00 bash ./scripts/run_with_log.sh p2g_final_syntax_check bash -lc python3 -m py_compile scripts/fuel_frontier_reachability_recorder.py scripts/analyze_frontier_scoring_and_reachability.py scripts/generate_unified_summary_log.py scripts/generate_full_run_log.py src/FUEL/scripts/frontier_viewpoint_lite.py src/FUEL/scripts/exploration_manager_lite.py src/FUEL/scripts/p11_lite_goal_to_path_bridge.py && bash -n scripts/run_p2g_frontier_300s_baseline.sh scripts/run_p2g_coverage_300s_after_fix.sh scripts/run_p2g_coverage_600s_after_fix.sh scripts/run_p2g_visual_coverage_300s.sh scripts/export_p2g_debug_package.sh
nuaa          34  0.0  0.0  13516  2180 ?        S    12:15   0:00 bash ./scripts/run_with_log.sh p2g_final_syntax_check bash -lc python3 -m py_compile scripts/fuel_frontier_reachability_recorder.py scripts/analyze_frontier_scoring_and_reachability.py scripts/generate_unified_summary_log.py scripts/generate_full_run_log.py src/FUEL/scripts/frontier_viewpoint_lite.py src/FUEL/scripts/exploration_manager_lite.py src/FUEL/scripts/p11_lite_goal_to_path_bridge.py && bash -n scripts/run_p2g_frontier_300s_baseline.sh scripts/run_p2g_coverage_300s_after_fix.sh scripts/run_p2g_coverage_600s_after_fix.sh scripts/run_p2g_visual_coverage_300s.sh scripts/export_p2g_debug_package.sh
nuaa          35  1.0  0.0  27480 14592 ?        S    12:15   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_unified_summary_log.py --task-name p2g_final_syntax_check --command bash -lc python3 -m py_compile scripts/fuel_frontier_reachability_recorder.py scripts/analyze_frontier_scoring_and_reachability.py scripts/generate_unified_summary_log.py scripts/generate_full_run_log.py src/FUEL/scripts/frontier_viewpoint_lite.py src/FUEL/scripts/exploration_manager_lite.py src/FUEL/scripts/p11_lite_goal_to_path_bridge.py && bash -n scripts/run_p2g_frontier_300s_baseline.sh scripts/run_p2g_coverage_300s_after_fix.sh scripts/run_p2g_coverage_600s_after_fix.sh scripts/run_p2g_visual_coverage_300s.sh scripts/export_p2g_debug_package.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_121546_p2g_final_syntax_check.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
```

## Metrics Summary
- metrics_source: NONE
- metrics_source_path: UNAVAILABLE
- metrics_source_reason: no current-run metrics matched task_name/run_id/timestamp
- matched_by: NONE
- duration_sec: UNAVAILABLE
- odom_total_distance: UNAVAILABLE
- uav_total_distance: UNAVAILABLE
- uav_net_displacement: UNAVAILABLE
- odom_net_displacement: UNAVAILABLE
- odom_max_no_motion_duration_sec: UNAVAILABLE
- goal_msg_count: UNAVAILABLE
- goal_switch_count: UNAVAILABLE
- unique_goal_count: UNAVAILABLE
- unique_goal_count_quantized_1p0m: UNAVAILABLE
- same_goal_max_duration_sec: UNAVAILABLE
- goal_reselect_count: UNAVAILABLE
- goal_reselect_after_path_done_count: UNAVAILABLE
- goal_reselect_after_coverage_stall_count: UNAVAILABLE
- goal_reselect_after_no_motion_count: UNAVAILABLE
- active_path_update_count: UNAVAILABLE
- active_path_done_event_count: UNAVAILABLE
- active_path_same_hash_max_duration_sec: UNAVAILABLE
- active_path_endpoint_to_goal_distance_avg: UNAVAILABLE
- active_path_endpoint_to_goal_distance_max: UNAVAILABLE
- travel_traj_update_count: UNAVAILABLE
- travel_traj_same_hash_max_duration_sec: UNAVAILABLE
- position_cmd_update_count: UNAVAILABLE
- position_cmd_total_variation: UNAVAILABLE
- position_cmd_same_pose_max_duration_sec: UNAVAILABLE
- position_cmd_to_odom_distance_avg: UNAVAILABLE
- trajectory_count: UNAVAILABLE
- frontier_count_start: UNAVAILABLE
- frontier_count_end: UNAVAILABLE
- frontier_count_avg: UNAVAILABLE
- explored_grid_start: UNAVAILABLE
- explored_grid_end: UNAVAILABLE
- explored_grid_gain: UNAVAILABLE
- coverage_proxy_start: UNAVAILABLE
- coverage_proxy_end: UNAVAILABLE
- coverage_proxy_gain: UNAVAILABLE
- coverage_proxy_gain_per_min: UNAVAILABLE
- coverage_stall_count: UNAVAILABLE
- coverage_stall_event_count: UNAVAILABLE
- coverage_stall_max_duration_sec: UNAVAILABLE
- stuck_event_count: UNAVAILABLE
- path_done_without_reselect_count: UNAVAILABLE
- coverage_stall_without_reselect_count: UNAVAILABLE
- traj_server_stale_path_hold_count: UNAVAILABLE
- quadrotor_sim_motion_blocked_count: UNAVAILABLE
- main_chain_break: UNAVAILABLE
- main_stuck_cause: UNAVAILABLE
- main_coverage_blocker: UNAVAILABLE

## Generated Files
- test-log/20260622_121546_p2g_final_syntax_check.md
- reports/p2g_final_code_diff_20260622_121546.patch

## Diagnosis
- Result inferred as `PASS` from exit code and raw log.
- Planner output metric: trajectory_count=UNAVAILABLE.
- Odom/motion metric: uav_total_distance=UNAVAILABLE.
- Main chain break: UNAVAILABLE.
- Main stuck cause: UNAVAILABLE.
- RViz visual chain is expected to remain unchanged unless this task explicitly ran a visual check.

## Visual Re-run Commands
Manual persistent visual demo:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh visual_manual ./scripts/run_manual_visual_demo_persistent.sh
```

Coverage visual diagnostic demo:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2g_visual_coverage_300s ./scripts/run_p2g_visual_coverage_300s.sh
```

Clean all FUEL/RViz processes:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/kill_fuel.sh
```

Latest debug package:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
ls -lh reports/latest_p2f_debug_package.tar.gz reports/latest_p2e_debug_package.tar.gz reports/latest_p2d_debug_package.tar.gz reports/latest_p2c_debug_package.tar.gz 2>/dev/null || true
```

## Next Action
- Run the next targeted diagnostic using `scripts/run_with_log.sh` so this summary system captures it.
