import os
import sys

testdir = os.path.dirname(__file__)
distdir = os.path.join(testdir, '..')

sys.path.insert(0, distdir)

import nose.tools as nstl
import tempfile
import shutil

from wsgi import *
from gily.models import Page, Wiki


def test_wiki():
    repo = tempfile.mkdtemp()

    try:
        ### create new wiki
        wiki = Wiki(repo, 'txt', 'FrontPage')
        nstl.ok_(isinstance(wiki, Wiki))
        nstl.ok_(wiki.repository.working_tree_dir, repo)
        nstl.ok_(wiki.repository.git_dir, os.path.join(repo, '.git'))

        ### already exists wiki
        wiki2 = Wiki(repo, 'txt', 'FrontPage')
        nstl.ok_(isinstance(wiki2, Wiki))
        nstl.ok_(wiki2.repository.working_tree_dir, repo)
        nstl.ok_(wiki2.repository.git_dir, os.path.join(repo, '.git'))

        ### find_all (empty)
        nstl.ok_(wiki.find_all() == [])

        ### find_or_create
        newpage = wiki.find_or_create('NewPage', 'hello world!')
        nstl.ok_(newpage, Page)

        newpage.commit('created NewPage')

        nstl.ok_(wiki.find('NewPage').name, 'NewPage')
        nstl.ok_(wiki.find('NewPage').content, 'hello world!')

        ### update_content
        pageA = wiki.find('NewPage')
        pageA.update_content('hello new world!')

        pageB = wiki.find('NewPage')
        nstl.ok_(pageB.content, 'hello new world!')

    finally:
        shutil.rmtree(repo)
