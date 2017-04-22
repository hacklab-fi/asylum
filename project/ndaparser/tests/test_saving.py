# -*- coding: utf-8 -*-
import datetime
import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from ndaparser.models import UploadedTransaction


@pytest.mark.django_db
def test_model_can_be_saved(admin_user):
    with open(os.path.join(os.path.dirname(__file__), "testdata.nda"), 'rb') as f:
        ut = UploadedTransaction(
            last_transaction=datetime.datetime.now().date(),
            user=admin_user,
            file=SimpleUploadedFile('pytest.nda', f.read())
        )
    ut.save()
    assert ut.pk > 0
