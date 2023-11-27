# -*- coding: utf-8 -*-


class DownloadError (Exception):
    """下载错误"""


class DownloadModeError (Exception):
    """下载模式错误"""


class StatusCodeError (DownloadError):
    """状态码错误"""


class AnalyzeError (DownloadError):
    """解析错误"""


class SHA1VerifyError (Exception):
    """文件散列值校验错误"""


class OperationAborted (Exception):
    """操作中止"""


class OperationInterrupted (Exception):
    """操作中断"""

