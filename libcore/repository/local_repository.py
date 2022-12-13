#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from libcore.exception.not_support_repository_indexer_exception import NotSupportRepositoryIndexerException
from libcore.repository.index import Index, App
from libcore.cache.cache import Cache
from libcore.until.string_util import StringUtil


class LocalRepository:
    __indexer = None

    __file_id_tpl = "{publisher}::{version}::{os}::{arch}::{dist}"  # 文件ID模板

    def __init__(self, indexer: Index):
        if indexer is None:
            raise NotSupportRepositoryIndexerException("Local Repository indexer is null.")
        self.__indexer = indexer

    def get_file_by_app(self, app: App) -> str:  # 通过App这个元数据，获取本地下载JDK文件名
        """
        定义FileID：Publisher::version::os::Arch::Dist
        :param app:
        :return:
        """
        file = Cache.get_file_by_app(self.__file_id_tpl.format(  # 从本地缓存冲获取到的文件路径
            # TODO 传入文件ID:FileID
        ))

        if StringUtil.is_empty(file):
            return ""
        else:
            return file


if __name__ == "__main__":
    pass
