# Copyright (C) 2019-2020  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from swh.lister.core.tests.conftest import *  # noqa


@pytest.fixture
def lister_cran(swh_listers):
    lister = swh_listers['cran']

    # Add the load-deb-package in the scheduler backend
    lister.scheduler.create_task_type({
        'type': 'load-cran',
        'description': 'Load a CRAN package',
        'backend_name': 'swh.loader.package.cran.tasks.LoaderCRAN',
        'default_interval': '1 day',
    })

    return lister