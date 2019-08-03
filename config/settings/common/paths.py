from os.path import abspath, dirname, join

CONFIG_DIR = dirname(dirname(abspath(__file__)))
BASE_DIR = dirname(dirname(CONFIG_DIR))

# TEST PATH
TEST_ASSETS = join(BASE_DIR, "test")
