import sys
import site

try:
  import _sitecustomize
except ImportError:
  pass

site.addsitedir("/data/projects/SlideCaster/control_center/.dream2nix/python/site")

# addsitedir only supports appending to the path, not prepending.
# As we already include a non-editable instance of each package
# in our pyEnv, those would shadow the editables. So we move
# the editables to the front of sys.path.
for index, path in enumerate(sys.path):
  if path in ['/data/projects/SlideCaster/control_center']:
    sys.path.insert(0, sys.path.pop(index))
        