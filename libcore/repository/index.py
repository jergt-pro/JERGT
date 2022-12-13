#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests

from libcore.config.config import Config
from libcore.exception.config_key_not_exist_exception import ConfigKeyNotExistException
from libcore.exception.indexer_init_failed_exception import IndexerInitFailedException
from libcore.until.string_util import StringUtil




class App:
    __publisher = None
    __version = None
    __os = None
    __arch = None
    __dist = None
    __checksum_algo = None
    __checksum_content = None
    __file = None
    __path = None






    # TODO Getter/Setter
    def get_file(self) -> str:
        return self.__file  # 远端下载地址

    # def get_system_type(self) -> str:
    #     return self.set_system_type
    #
    # def set_system_type(self: os):
    #     index_version = json_response["version"]
    #     self.set_system_type()

class Index:
    """
    用于访问 Github 存储库或者镜像源的 Index 文件 （JSON）。
    """

    __index_json = "/index.json"
    __mirror_url = ""

    def __init__(self, config: Config = None):
        """
         # TODO 根据环境变量配置文件读取镜像源
        :param config:
        """

        try:
            mirror = config.get("mirror")  # 获取的文件路径
            # TODO 处理兼容 http://mirrors.jlab.io:9900 和http://mirrors.jlab.io:9900/
            self.__mirror_url = mirror + self.__index_json
        except ConfigKeyNotExistException as e:
            raise IndexerInitFailedException("Can not read mirror from config file, because :{}".format(e))

    def get_version(self) -> str | None:
        response = requests.get(self.__mirror_url)  # 请求该路径的信息，response是回应
        if response.status_code != 200:
            return None
        json_response = response.json()  # 请求获取json，返回json的内容(也就是App的内容)
        index_version = json_response["version"]  # 获取json（App）中的version内容


        if StringUtil.is_empty(index_version):
            return None

        return index_version.strip()



    def get_name(self) -> str:
        pass

    def get_publisher(self) -> str:
        pass

    def get_update_time(self) -> str:
        pass

    def get_app_versions_by_pulisher(self, publisher: str) -> tuple:
        pass

    def get_app(self, publisher: str, version: str):
        pass


if __name__ == "__main__":
    pass
