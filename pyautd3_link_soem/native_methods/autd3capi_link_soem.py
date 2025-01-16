# This file is autogenerated
import threading
import ctypes
import os
from pyautd3.native_methods.structs import Vector3, Quaternion
from pyautd3.native_methods.autd3_core import SamplingConfig, LoopBehavior, GPIOOut, GPIOIn, Segment, Drive
from pyautd3.native_methods.autd3_driver import GainSTMMode, SilencerTarget
from pyautd3_link_soem.native_methods.autd3_link_soem import SyncMode, TimerStrategy, ProcessPriority
from pyautd3.native_methods.autd3capi_driver import Duration, ResultLinkBuilder, ResultStatus

from enum import IntEnum


class Status(IntEnum):
    Error = 0
    StateChanged = 1
    Lost = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class EthernetAdaptersPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class ThreadPriorityPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]



class Singleton(type):
    _instances = {}  # type: ignore
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances: # pragma: no cover
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):

    def init_dll(self, bin_location: str, bin_prefix: str, bin_ext: str):
        self.dll = ctypes.CDLL(os.path.join(bin_location, f'{bin_prefix}autd3capi_link_soem{bin_ext}'))

        self.dll.AUTDAdapterPointer.argtypes = [] 
        self.dll.AUTDAdapterPointer.restype = EthernetAdaptersPtr

        self.dll.AUTDAdapterGetSize.argtypes = [EthernetAdaptersPtr]  # type: ignore 
        self.dll.AUTDAdapterGetSize.restype = ctypes.c_uint32

        self.dll.AUTDAdapterGetAdapter.argtypes = [EthernetAdaptersPtr, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_char_p]  # type: ignore 
        self.dll.AUTDAdapterGetAdapter.restype = None

        self.dll.AUTDAdapterPointerDelete.argtypes = [EthernetAdaptersPtr]  # type: ignore 
        self.dll.AUTDAdapterPointerDelete.restype = None

        self.dll.AUTDLinkSOEMTracingInit.argtypes = [] 
        self.dll.AUTDLinkSOEMTracingInit.restype = None

        self.dll.AUTDLinkSOEMTracingInitWithFile.argtypes = [ctypes.c_char_p] 
        self.dll.AUTDLinkSOEMTracingInitWithFile.restype = ResultStatus

        self.dll.AUTDLinkSOEM.argtypes = [ctypes.c_char_p, ctypes.c_uint32, Duration, Duration, ctypes.c_void_p, ctypes.c_void_p, SyncMode, ProcessPriority, ThreadPriorityPtr, Duration, TimerStrategy, Duration, Duration]  # type: ignore 
        self.dll.AUTDLinkSOEM.restype = ResultLinkBuilder

        self.dll.AUTDLinkSOEMIsDefault.argtypes = [ctypes.c_uint32, Duration, Duration, SyncMode, ProcessPriority, ThreadPriorityPtr, Duration, TimerStrategy, Duration, Duration]  # type: ignore 
        self.dll.AUTDLinkSOEMIsDefault.restype = ctypes.c_bool

        self.dll.AUTDLinkSOEMStatusGetMsg.argtypes = [Status, ctypes.c_char_p]  # type: ignore 
        self.dll.AUTDLinkSOEMStatusGetMsg.restype = ctypes.c_uint32

        self.dll.AUTDLinkRemoteSOEM.argtypes = [ctypes.c_char_p] 
        self.dll.AUTDLinkRemoteSOEM.restype = ResultLinkBuilder

        self.dll.AUTDLinkSOEMThreadPriorityMin.argtypes = [] 
        self.dll.AUTDLinkSOEMThreadPriorityMin.restype = ThreadPriorityPtr

        self.dll.AUTDLinkSOEMThreadPriorityCrossplatform.argtypes = [ctypes.c_uint8] 
        self.dll.AUTDLinkSOEMThreadPriorityCrossplatform.restype = ThreadPriorityPtr

        self.dll.AUTDLinkSOEMThreadPriorityMax.argtypes = [] 
        self.dll.AUTDLinkSOEMThreadPriorityMax.restype = ThreadPriorityPtr

    def adapter_pointer(self) -> EthernetAdaptersPtr:
        return self.dll.AUTDAdapterPointer()

    def adapter_get_size(self, adapters: EthernetAdaptersPtr) -> ctypes.c_uint32:
        return self.dll.AUTDAdapterGetSize(adapters)

    def adapter_get_adapter(self, adapters: EthernetAdaptersPtr, idx: int, desc: ctypes.Array[ctypes.c_char] | None, name: ctypes.Array[ctypes.c_char] | None) -> None:
        return self.dll.AUTDAdapterGetAdapter(adapters, idx, desc, name)

    def adapter_pointer_delete(self, adapters: EthernetAdaptersPtr) -> None:
        return self.dll.AUTDAdapterPointerDelete(adapters)

    def link_soem_tracing_init(self) -> None:
        return self.dll.AUTDLinkSOEMTracingInit()

    def link_soem_tracing_init_with_file(self, path: bytes) -> ResultStatus:
        return self.dll.AUTDLinkSOEMTracingInitWithFile(path)

    def link_soem(self, ifname: bytes, buf_size: int, send_cycle: Duration, sync0_cycle: Duration, err_handler: ctypes.c_void_p | None, err_context: ctypes.c_void_p | None, mode: SyncMode, process_priority: ProcessPriority, thread_priority: ThreadPriorityPtr, state_check_interval: Duration, timer_strategy: TimerStrategy, tolerance: Duration, sync_timeout: Duration) -> ResultLinkBuilder:
        return self.dll.AUTDLinkSOEM(ifname, buf_size, send_cycle, sync0_cycle, err_handler, err_context, mode, process_priority, thread_priority, state_check_interval, timer_strategy, tolerance, sync_timeout)

    def link_soem_is_default(self, buf_size: int, send_cycle: Duration, sync0_cycle: Duration, mode: SyncMode, process_priority: ProcessPriority, thread_priority: ThreadPriorityPtr, state_check_interval: Duration, timer_strategy: TimerStrategy, tolerance: Duration, sync_timeout: Duration) -> ctypes.c_bool:
        return self.dll.AUTDLinkSOEMIsDefault(buf_size, send_cycle, sync0_cycle, mode, process_priority, thread_priority, state_check_interval, timer_strategy, tolerance, sync_timeout)

    def link_soem_status_get_msg(self, src: Status, dst: ctypes.Array[ctypes.c_char] | None) -> ctypes.c_uint32:
        return self.dll.AUTDLinkSOEMStatusGetMsg(src, dst)

    def link_remote_soem(self, addr: bytes) -> ResultLinkBuilder:
        return self.dll.AUTDLinkRemoteSOEM(addr)

    def link_soem_thread_priority_min(self) -> ThreadPriorityPtr:
        return self.dll.AUTDLinkSOEMThreadPriorityMin()

    def link_soem_thread_priority_crossplatform(self, value: int) -> ThreadPriorityPtr:
        return self.dll.AUTDLinkSOEMThreadPriorityCrossplatform(value)

    def link_soem_thread_priority_max(self) -> ThreadPriorityPtr:
        return self.dll.AUTDLinkSOEMThreadPriorityMax()
