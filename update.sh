#!/bin/sh
set -e

blender --background meshes/ship.blend --python meshes/update_meshes.py
