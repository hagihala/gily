# -*- coding: utf-8 -*- vim:set fileencoding=utf-8 ft=python:

import os

from datetime import datetime
from dateutil.tz import tzoffset
from git import *
from gitdb import IStream
from StringIO import StringIO
from pygit2 import (
        Repository, Blob, init_repository
        )


class PageNotFound(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Page (%s) is not found' % (self.name)


class Wiki(object):
    """Wiki site with git backend

    The instance of this class creates/uses a non-bare Git repository
    as backend.
    """
    def __init__(self, repo_path, extension, homepage):
        self.homepage = homepage
        self.extension = extension

        if os.path.isdir(os.path.join(repo_path, '.git')):
            self._repository = Repository(repo_path)
        else:
            if not os.path.isdir(repo_path):
                os.makedirs(repo_path)
            is_bare = False
            self._repository = init_repository(repo_path, is_bare)

    def find_all(self):
        """Nested tree travarsal might not be supported yet"""
        repo = self._repository

        if len(repo.listall_references) == 0:
            return []
        else:
            head = repo.lookup_reference('HEAD').resolve()
            commit = repo[head.oid]
            tree = commit.tree
            pages = []
            for entry in tree:
                obj = entry.to_object()
                if isinstance(obj, Blob):
                    pages.append(Page(obj, repo))
            return pages

    def find(self, name):
        blob = self.find_blob(name)

        if blob is None:
            raise PageNotFound(name)

        return Page(blob, self._repository)

    def find_blob(self, path):
        repo = self._repository

        if len(repo.listall_references()) == 0:
            return None
        else:
            head = repo.lookup_reference('HEAD').resolve()
            commit = repo[head.oid]
            tree = commit.tree
            blob = None

            try:
                path = "%s.%s" % (path, self.extension)
                blob = tree[path].to_object()
            except KeyError, e:
                pass

            return blob

    def find_or_create(self, name, content=''):
        try:
            return self.find(name)
        except PageNotFound, e:
            page = Page(
                    self.create_blob_for(name, data=content),
                    self._repository
                    )
            page.commit('Page (%s) is created.' % (name))
            return page

    def create_blob_for(self, path, data=''):
        repo = self._repository
        istream = IStream('blob', len(data), StringIO(data))

        repo.odb.store(istream)
        blob = Blob(repo, istream.binsha, 0100644,
                "%s.%s" % (path, self.extension))

        return blob


class Page(object):
    def __init__(self, blob, repository):
        self._blob = blob
        self._repository = repository

    def __str__(self):
        # FIXME: support pygit2
        return self.name

    @property
    def name(self):
        """Assume that blob is in the HEAD.
        And nested-tree travarsal might not be supported yet"""
        repo = self._repository
        head = repo.lookup_reference('HEAD').resolve()
        commit = repo[head.oid]
        tree = commit.tree
        entry = [ x for x in tree if x.oid == self._blob.oid ][0]
        return os.path.splitext(entry.name)[0]

    @property
    def content(self):
        try:
            return self._blob.data
        except AttributeError, e:
            return None

    @content.setter
    def content(self, new):
        # FIXME: support pygit2
        if self.content == new:
            return None

        fh = open(self._blob.abspath, 'w')
        fh.write(new)
        fh.close()

        return self.commit('Updated: %s' % (self._blob.name))

    def commit(self, message):
        # FIXME: support pygit2
        index = self._repository.index
        blob = self._blob

        if os.path.isfile(blob.abspath):
            index.add([blob.path])
        else:
            index.add([IndexEntry.from_blob(blob)])

        return index.commit(message)

    def get_histories(self):
        # FIXME: support pygit2
        pages = []
        for i, commit in enumerate(self._repository.iter_commits()):
            pages.extend([
                    Page(x, self._repository, commit) for x in
                        commit.tree.blobs if x.path == self._blob.path
                    ])
        return pages

    @property
    def updated_at(self):
        # FIXME: support pygit2
        if self._commit is not None:
            timestamp = self._commit.committed_date
            offset = self._commit.committer_tz_offset
            dt = datetime.fromtimestamp(timestamp, tzoffset(None, -offset))
            return dt

        else:
            return None
