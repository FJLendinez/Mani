from .environ import env

CACHES = {
    "default": env.cache_url('DJANGO_CACHE_URL', 'filecache://')
}
