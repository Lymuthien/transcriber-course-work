from .domain_interfaces import *
from .ifile_manager import *
from .iserializer import *
from .istorage_service import *
from .repositories_interfaces import *


__all__ = [
    "IDictable",
    "IUser",
    "IRestorable",
    "IStorage",
    "IUserRepository",
    "IAudioRepository",
    "IAudioRecord",
    "ISerializer",
    "IFileManager",
    "IStorageService",
    "IStorageRepository",
]
