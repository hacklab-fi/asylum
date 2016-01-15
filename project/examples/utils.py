# -*- coding: utf-8 -*-
import environ
env = environ.Env()
HOLVI_CNC = False

def get_holvi_singleton():
    global HOLVI_CNC
    if HOLVI_CNC:
        return HOLVI_CNC
    holvi_pool = env('HOLVI_POOL', default=None)
    holvi_key = env('HOLVI_APIKEY', default=None)
    if not holvi_pool or not holvi_key:
        return False
    import holviapi
    HOLVI_CNC = holviapi.Connection(holvi_pool, holvi_key)
    return HOLVI_CNC
