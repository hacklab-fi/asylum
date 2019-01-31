# -*- coding: utf-8 -*-
import holviapi
import holvirc
from django.conf import settings

CONNECTION_SINGLETON = None

def apikey_configured():
    """Check if we have apikey"""
    return bool(settings.HOLVI_POOL) and bool(settings.HOLVI_APIKEY)


def userauth_configured():
    """Check if we have username/password"""
    return bool(settings.HOLVI_POOL) and bool(settings.HOLVI_USER) and bool(settings.HOLVI_PASSWORD)


def api_configured():
    """Check that we have some API config"""
    return apikey_configured() or userauth_configured()


def get_connection():
    """Shorhand connection singleton getter"""
    global CONNECTION_SINGLETON
    if CONNECTION_SINGLETON is not None:
        return CONNECTION_SINGLETON
    if not api_configured():
        raise RuntimeError('Holvi API is not configured')
    if userauth_configured():
        CONNECTION_SINGLETON = holvirc.Connection.singleton(settings.HOLVI_POOL, settings.HOLVI_USER, settings.HOLVI_PASSWORD)
    if apikey_configured():
        CONNECTION_SINGLETON = holviapi.Connection.singleton(settings.HOLVI_POOL, settings.HOLVI_APIKEY)
    return CONNECTION_SINGLETON


def get_invoiceapi():
    """Shorthand API instance creator"""
    return holvirc.InvoiceAPI(get_connection())


def list_invoices(**kwargs):
    """Shorthand accessor for the API method"""
    return get_invoiceapi().list_invoices(**kwargs)


def get_invoice(code):
    """Shorthand accessor for the API method"""
    return get_invoiceapi().get_invoice(code)


def get_checkoutapi():
    """Shorthand API instance creator"""
    cnc = get_connection()
    if isinstance(cnc, (holvirc.Connection, holvirc.connection.Connection)):
        raise RuntimeError("This only works with the old style api keys")
    return holviapi.CheckoutAPI(cnc)


def list_orders(**kwargs):
    """Shorthand accessor for the API method"""
    cnc = get_connection()
    if isinstance(cnc, (holvirc.Connection, holvirc.connection.Connection)):
        # TODO: Log the issue
        return iter([])
    return get_checkoutapi().list_orders(**kwargs)


def get_order(code):
    """Shorthand accessor for the API method"""
    return get_checkoutapi().get_order(code)


def get_categoriesapi():
    """Shorthand API instance creator"""
    cnc = get_connection()
    if isinstance(cnc, (holviapi.Connection, holviapi.connection.Connection)):
        return holviapi.CategoriesAPI(get_connection())
    return holvirc.CategoriesAPI(cnc)


def get_category(code):
    """Shorthand accessor for the API method"""
    return get_categoriesapi().get_category(code)
