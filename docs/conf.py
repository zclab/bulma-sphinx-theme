import sys
from os.path import abspath, join, dirname
import bulma_sphinx_theme

sys.path.insert(0, abspath(join(dirname(__file__), "../src")))

project = "A sphinx theme based on bulma"
copyright = "2023"
author = "zclab"
master_doc = "index"
version = bulma_sphinx_theme.__version__
language = "en"  #'zh_CN'
