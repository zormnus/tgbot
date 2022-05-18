from environs import Env

env = Env()
env.read_env()

API_TOKEN = env.str('API_TOKEN')
CHROMEDRIVER_PATH = env.str(r'CHROMEDRIVER_PATH')
