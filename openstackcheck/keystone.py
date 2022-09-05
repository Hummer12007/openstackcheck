import secrets

from contextlib import contextmanager

from keystoneclient import client
from keystoneauth1.identity import v3

import openstackcheck.config as cfg

from openstackcheck.auth import get_admin_auth

def get_keystone():
    admin_auth = get_admin_auth()
    ks = client.Client('3', session=admin_auth)
    return ks

@contextmanager
def get_domain(ctx):
    domain = ctx.ks.domains.create(cfg.test_domain, description='Temporary domain for smoke test')
    yield domain
    ctx.ks.domains.delete(domain)

@contextmanager
def get_project(ctx):
    proj = ctx.ks.projects.create(cfg.test_project, ctx.domain, description='Temporary project for smoke test')
    yield proj
    ctx.ks.projects.delete(proj)

@contextmanager
def get_user(ctx):
    ks = ctx['ks']
    ctx.acquire_res('username', 'test_user')
    ctx.acquire_res('password', secrets.token_urlsafe(16))
    user = ks.users.create(ctx.username, password=ctx.password, domain=ctx.domain, default_project=ctx.project)
    yield user
    ks.users.delete(user)

@contextmanager
def get_auth(ctx):
    auth = v3.Password(auth_url=cfg.keystone_url,
        user_id=ctx.user.id,
        username=ctx.username, password=ctx.password,
        domain_id=ctx.domain.id, project_id=ctx.project.id)
    yield auth
