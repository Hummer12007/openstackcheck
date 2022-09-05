from environs import Env

env = Env()
env.read_env()

keystone_url = env.str('KEYSTONE_URL')

test_project = env.str('SMOKETEST_DOMAIN', 'smokecheck')
test_domain = env.str('SMOKETEST_DOMAIN', 'smokecheck')
