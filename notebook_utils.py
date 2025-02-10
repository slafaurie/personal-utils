def insert_parent_in_path():
  """
  I like to put notebooks within their own folder "root/notebooks/".
  This functions insert the parent root in the path so I can still
  import code from "root/src/..." and in the notebooks will be
  "from src.package.foo"
  
  """
  import sys
  from pathlib import Path
  # Add the project root directory to Python path
  project_root = Path.cwd().parent
  sys.path.append(str(project_root))
