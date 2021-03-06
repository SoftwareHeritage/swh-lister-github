swh-lister
==========

This component from the Software Heritage stack aims to produce listings
of software origins and their urls hosted on various public developer platforms
or package managers. As these operations are quite similar, it provides a set of
Python modules abstracting common software origins listing behaviors.

It also provides several lister implementations, contained in the
following Python modules:

- `swh.lister.bitbucket`
- `swh.lister.cgit`
- `swh.lister.cran`
- `swh.lister.debian`
- `swh.lister.gitea`
- `swh.lister.github`
- `swh.lister.gitlab`
- `swh.lister.gnu`
- `swh.lister.launchpad`
- `swh.lister.npm`
- `swh.lister.packagist`
- `swh.lister.phabricator`
- `swh.lister.pypi`

Dependencies
------------

All required dependencies can be found in the `requirements*.txt` files located
at the root of the repository.

Local deployment
----------------

## lister configuration

Each lister implemented so far by Software Heritage (`github`, `gitlab`, `debian`, `pypi`, `npm`)
must be configured by following the instructions below (please note that you have to replace
`<lister_name>` by one of the lister name introduced above).

### Preparation steps

1. `mkdir ~/.config/swh/ ~/.cache/swh/lister/<lister_name>/`
2. create configuration file `~/.config/swh/lister_<lister_name>.yml`
3. Bootstrap the db instance schema

```lang=bash
$ createdb lister-<lister_name>
$ python3 -m swh.lister.cli --db-url postgres:///lister-<lister_name> <lister_name>
```

Note: This bootstraps a minimum data set needed for the lister to run.

### Configuration file sample

Minimalistic configuration shared by all listers to add in file `~/.config/swh/lister_<lister_name>.yml`:

```lang=yml
storage:
  cls: 'remote'
  args:
    url: 'http://localhost:5002/'

scheduler:
  cls: 'remote'
  args:
    url: 'http://localhost:5008/'

lister:
  cls: 'local'
  args:
    # see http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls
    db: 'postgresql:///lister-<lister_name>'

credentials: []
cache_responses: True
cache_dir: /home/user/.cache/swh/lister/<lister_name>/
```

Note: This expects storage (5002) and scheduler (5008) services to run locally

## lister-github

Once configured, you can execute a GitHub lister using the following instructions in a `python3` script:

```lang=python
import logging
from swh.lister.github.tasks import range_github_lister

logging.basicConfig(level=logging.DEBUG)
range_github_lister(364, 365)
...
```

## lister-gitlab

Once configured, you can execute a GitLab lister using the instructions detailed in the `python3` scripts below:

```lang=python
import logging
from swh.lister.gitlab.tasks import range_gitlab_lister

logging.basicConfig(level=logging.DEBUG)
range_gitlab_lister(1, 2, {
    'instance': 'debian',
    'api_baseurl': 'https://salsa.debian.org/api/v4',
    'sort': 'asc',
    'per_page': 20
})
```

```lang=python
import logging
from swh.lister.gitlab.tasks import full_gitlab_relister

logging.basicConfig(level=logging.DEBUG)
full_gitlab_relister({
    'instance': '0xacab',
    'api_baseurl': 'https://0xacab.org/api/v4',
    'sort': 'asc',
    'per_page': 20
})
```

```lang=python
import logging
from swh.lister.gitlab.tasks import incremental_gitlab_lister

logging.basicConfig(level=logging.DEBUG)
incremental_gitlab_lister({
    'instance': 'freedesktop.org',
    'api_baseurl': 'https://gitlab.freedesktop.org/api/v4',
    'sort': 'asc',
    'per_page': 20
})
```

## lister-debian

Once configured, you can execute a Debian lister using the following instructions in a `python3` script:

```lang=python
import logging
from swh.lister.debian.tasks import debian_lister

logging.basicConfig(level=logging.DEBUG)
debian_lister('Debian')
```

## lister-pypi

Once configured, you can execute a PyPI lister using the following instructions in a `python3` script:

```lang=python
import logging
from swh.lister.pypi.tasks import pypi_lister

logging.basicConfig(level=logging.DEBUG)
pypi_lister()
```

## lister-npm

Once configured, you can execute a npm lister using the following instructions in a `python3` REPL:

```lang=python
import logging
from swh.lister.npm.tasks import npm_lister

logging.basicConfig(level=logging.DEBUG)
npm_lister()
```

## lister-phabricator

Once configured, you can execute a Phabricator lister using the following instructions in a `python3` script:

```lang=python
import logging
from swh.lister.phabricator.tasks import incremental_phabricator_lister

logging.basicConfig(level=logging.DEBUG)
incremental_phabricator_lister(forge_url='https://forge.softwareheritage.org', api_token='XXXX')
```

## lister-gnu

Once configured, you can execute a PyPI lister using the following instructions in a `python3` script:

```lang=python
import logging
from swh.lister.gnu.tasks import gnu_lister

logging.basicConfig(level=logging.DEBUG)
gnu_lister()
```

## lister-cran

Once configured, you can execute a CRAN lister using the following instructions in a `python3` script:

```lang=python
import logging
from swh.lister.cran.tasks import cran_lister

logging.basicConfig(level=logging.DEBUG)
cran_lister()
```

## lister-cgit

Once configured, you can execute a cgit lister using the following instructions
in a `python3` script:

```lang=python
import logging
from swh.lister.cgit.tasks import cgit_lister

logging.basicConfig(level=logging.DEBUG)
# simple cgit instance
cgit_lister(url='https://git.kernel.org/')
# cgit instance whose listed repositories differ from the base url
cgit_lister(url='https://cgit.kde.org/',
            url_prefix='https://anongit.kde.org/')
```

## lister-packagist

Once configured, you can execute a Packagist lister using the following instructions
in a `python3` script:

```lang=python
import logging
from swh.lister.packagist.tasks import packagist_lister

logging.basicConfig(level=logging.DEBUG)
packagist_lister()
```

Licensing
---------

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

See top-level LICENSE file for the full text of the GNU General Public License
along with this program.
