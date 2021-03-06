# -*- coding: utf-8 -*- vim:set fileencoding=utf-8 ft=python:

import os

from git import *
from gitdb import IStream
from StringIO import StringIO


class PageNotFound(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Page (%s) is not found' % (self.name)


class Wiki(object):
    def __init__(self, repository, extension, homepage):
        self.homepage = homepage
        self.extension = extension

        if os.path.isdir(os.path.join(repository, '.git')):
            self.repository = Repo(repository, odbt=GitDB)
        else:
            if not os.path.isdir(repository):
                os.makedirs(repository)

            os.chdir(repository)
            self.repository = Repo.init()

    def find_all(self):
        repo = self.repository

        if len(repo.refs) == 0:
            return []
        else:
            pages = []
            for entry in repo.tree().traverse():
                if entry.type == 'blob':
                    pages.append(Page(entry, repo))
            return pages

    def find(self, name):
        blob = self.find_blob(name)

        if blob is None:
            raise PageNotFound(name)

        return Page(blob, self.repository)

    def find_blob(self, path):
        repo = self.repository

        if len(repo.refs) == 0:
            return None
        else:
            tree = repo.tree()
            blob = None

            try:
                blob = tree / ("%s.%s" % (path, self.extension))
            except KeyError, e:
                pass

            return blob

    def find_or_create(self, name, content=''):
        try:
            return self.find(name)
        except PageNotFound, e:
            page = Page(
                    self.create_blob_for(name, data=content),
                    self.repository
                    )
            page.commit('Page (%s) is created.' % (name))
            return page

    def create_blob_for(self, path, data=''):
        repo = self.repository
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
        return self.blob.name

    @property
    def name(self):
        return os.path.splitext(self._blob.name)[0]

    @property
    def content(self):
        try:
            return self._blob.data_stream.read()
        except AttributeError, e:
            return None

    @content.setter
    def content(self, new):
        if self.content == new:
            return None

        fh = open(self._blob.abspath, 'w')
        fh.write(new)
        fh.close()

        return self.commit('Updated: %s' % (self._blob.name))

    def commit(self, message):
        index = self._repository.index
        blob = self._blob

        if os.path.isfile(blob.abspath):
            index.add([blob.path])
        else:
            index.add([IndexEntry.from_blob(blob)])

        return index.commit(message)
