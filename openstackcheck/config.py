from environs import Env

env = Env()
env.read_env('.env')

keystone_url = env.str('KEYSTONE_URL')

test_project = env.str('SMOKETEST_PROJECT', 'smokecheck')
test_domain = env.str('SMOKETEST_DOMAIN', 'smokecheck')
