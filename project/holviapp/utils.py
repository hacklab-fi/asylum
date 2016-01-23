# -*- coding: utf-8 -*-
import holviapi
from django.conf import settings


def api_configured():
    return bool(settings.HOLVI_POOL) and bool(settings.HOLVI_APIKEY)


def get_connection():
    """Shorhand connection singleton getter"""
    if not api_configured():
        raise RuntimeError('Holvi API is not configured')
    return holviapi.Connection.singleton(settings.HOLVI_POOL, settings.HOLVI_APIKEY)


def get_invoiceapi():
    """Shorthand API instance creator"""
    return holviapi.InvoiceAPI(get_connection())


def list_invoices(**kwargs):
    """Shorthand accessor for the API method"""
    return get_invoiceapi().list_invoices(**kwargs)


def get_invoice(code):
    """Shorthand accessor for the API method"""
    return get_invoiceapi().get_invoice(code)


def get_checkoutapi():
    """Shorthand API instance creator"""
    return holviapi.CheckoutAPI(get_connection())


def list_orders(**kwargs):
    """Shorthand accessor for the API method"""
    return get_checkoutapi().list_orders(**kwargs)


def get_order(code):
    """Shorthand accessor for the API method"""
    return get_checkoutapi().get_order(code)


def get_categoriesapi():
    """Shorthand API instance creator"""
    return holviapi.CategoriesAPI(get_connection())


def get_category(code):
    """Shorthand accessor for the API method"""
    return get_categoriesapi().get_category(code)
