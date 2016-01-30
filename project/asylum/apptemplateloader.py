# -*- coding: utf-8 -*-
# adaped from https://www.djangosnippets.org/snippets/1376/
from os.path import abspath, dirname, isdir, join

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.template import TemplateDoesNotExist
from django.template.loaders.filesystem import Loader


class NameSpacedLoader(Loader):

    def _get_template_vars(self, template_name):
        app_name, template_name = template_name.split(":", 1)
        try:
            template_dir = abspath(join(apps.get_app_config(app_name).path, 'templates'))
        except ImproperlyConfigured:
            raise TemplateDoesNotExist()

        return template_name, template_dir

    def load_template_from_app(self, template_name, template_dirs=None):
        """ 
        Template loader that only serves templates from specific app's template directory.

        Works for template_names in format app_label:some/template/name.html
        """
        if ":" not in template_name:
            raise TemplateDoesNotExist()

        template_name, template_dir = self._get_template_vars(template_name)

        if not isdir(template_dir):
            raise TemplateDoesNotExist()

        return super().load_template_source(template_name, template_dirs=[template_dir])

    def load_template_source(self, template_name, template_dirs=None):
        return self.load_template_from_app(template_name)
