#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libcore.config.config import Config
from libcore.repository.index import Index
from libcore.repository.local_repository import LocalRepository
from libcore.repository.remote_repository import RemoteRepository
from libcore.exception.not_support_repository_indexer_exception import NotSupportRepositoryIndexerException
from libcore.exception.indexer_init_failed_exception import IndexerInitFailedException
from libcore.cache.cache import Cache

def jergt():
    app_config = Config()       # 实例化Config

    try:
        app_indexer = Index(config=app_config)  # 实例化Index ，要求内容填入配置config，config满足实例化后的Config（）
    except IndexerInitFailedException as e:        # 实例化index可能失败
        print(e)
        return

    try:
        app_local_repository = LocalRepository(indexer=app_indexer)    # 实例化本地仓库，满足实例化index
        app_remote_repository = RemoteRepository(indexer=app_indexer)
    except NotSupportRepositoryIndexerException as e:
        print(e)
        return

    auto_remove_num = Cache.auto_remove_cache()
    if auto_remove_num > 0:
        print("Auto Task: {} cache files are cleared".format(auto_remove_num))


if __name__ == '__main__':
    jergt()
