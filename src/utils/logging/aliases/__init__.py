from . import user_aliases
from .user_aliases import *  # noqa

__all__ = ["_hostname_alias"]


_hostname_alias = {}
for m in user_aliases.__all__:
    mod = getattr(user_aliases, m)
    if hasattr(mod, "_hostname_alias"):
        _hostname_alias.update(mod._hostname_alias)
