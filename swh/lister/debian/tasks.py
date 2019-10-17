# Copyright (C) 2017-2018 the Software Heritage developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from celery import shared_task

from .lister import DebianLister


@shared_task(name=__name__ + '.DebianListerTask')
def list_debian_distribution(distribution, **lister_args):
    '''List a Debian distribution'''
    DebianLister(**lister_args).run(distribution)


@shared_task(name=__name__ + '.ping')
def _ping():
    return 'OK'
