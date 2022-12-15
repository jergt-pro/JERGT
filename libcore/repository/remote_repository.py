#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from libcore.exception.not_support_repository_indexer_exception import NotSupportRepositoryIndexerException
from libcore.repository.index import Index
from libcore.repository.index import App


class RemoteRepository:
    __indexer = None

    def __init__(self, indexer: Index):
        if indexer is None:
            raise NotSupportRepositoryIndexerException
        self.__indexer = indexer

    def get_file_by_app(self, app: App):  # 通过App这个元数据，获取文件实体的路径
        return app.get_file()  # github的下载地址



if __name__ == "__main__":
    pass
