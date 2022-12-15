#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os.path
import os

from libcore.config.config import Config


@staticmethod
class Cache:
    """
    缓存
    """
    cache_default_path = None
    __cache_windows_path_tpl = "{system_root}\\ProgramData\\jergt\\cache\\"
    __cache_linux_path_tpl = "/usr/local/jergt/cache/"
    __cache_macos_path_tpl = "/usr/local/jergt/Cache/"
    __file_ext = ".store"

    __cache_file_windows = None  # windows版本jdk缓存文件路径

    __curr_system_type = None  # 判断操作系统

    __fileid = "jdk-{version}-{publisher}"
    __cache_name_tpl = "{fileid}-{year}-{month}-{day}{file_ext}"

    def __init__(self):
        self.Config = None

    @staticmethod
    def init__system_type(self):
        system_type = self.Config.__init_system_info()
        if system_type == "Linux":
            self.cache_default_path = self.__cache_linux_path_tpl
            cache_default_path = self.cache_default_path.strip()
            return cache_default_path
        elif system_type == "Darwin":
            self.cache_default_path = self.__cache_macos_path_tpl
            cache_default_path = self.cache_default_path.strip()
            return cache_default_path
        elif system_type == "Windows":
            system_root = os.getenv("SystemDrive", default="C:")
            self.cache_default_path = self.__cache_windows_path_tpl.format(system_root=system_root)
            cache_default_path = self.cache_default_path.strip()
            return cache_default_path

        # cache_filename = os.listdir(cache_default_path)
        # cache_file_absolute_path = cache_default_path + cache_filename

    # @staticmethod
    # def get_path_by_id(file_id: str) -> str:
    #     """
    #     获取文件系统类型，为其设定缓存位置
    #     :param file_id:
    #     :return: 默认的缓存路径
    #     """



    @staticmethod
    def get_file_by_app(file_id: str):  # 获取缓存中的jdk文件的文件路径
        pass

    def get_store_time(name: str) -> str:
        """
        根据缓存文件名称获取存储时间
        :param cache_name:
        :return:
        """
        # file_time = name.split("-")
        # file_time = file_time[-1].split(".")
        # return file_time[0]
        # pass
        pass

    @staticmethod
    def get_file_id(name: str) -> str:
        """
        根据缓存文件名称获取文件ID（FileID）
        :param cache_name:
        :return:
        """
        pass

    @staticmethod
    def scan_caches(path: str) -> tuple:  # 返回文件缓存列表
        """
        跨平台的方式扫描缓存列表
        :return:
        """
        pass

    @staticmethod
    def remove_cache_name(name: str) -> str:
        """
        删除指定的缓存
        :param name:
        :return:
        """
        pass

    @staticmethod
    def auto_remove_cache() -> int:  # 返回删除的的数量
        """
        返回最近30天的缓存文件，并返回删除的数量
        :return:
        """
        pass

    @staticmethod
    def remove_all_caches() -> bool:
        """
        删除全部的缓存。
        :return:
        """
        pass


if __name__ == "__main__":
    pass
