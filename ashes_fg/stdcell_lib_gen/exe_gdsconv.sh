#!/usr/bin/env bash
set -euo pipefail
# Compatibility wrapper: run from your project Tools/lib directory.
exec ashes cells prepare "$@"
