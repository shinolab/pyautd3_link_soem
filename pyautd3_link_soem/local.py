import ctypes
from collections.abc import Callable
from typing import Self

from pyautd3.derive import builder
from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import HandlePtr, LinkBuilderPtr, LinkPtr, SyncMode
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr
from pyautd3.utils import Duration

from pyautd3_link_soem.adapter import EtherCATAdapter
from pyautd3_link_soem.native_methods.autd3capi_link_soem import NativeMethods as LinkSOEM
from pyautd3_link_soem.native_methods.autd3capi_link_soem import ProcessPriority, ThreadPriorityPtr, TimerStrategy
from pyautd3_link_soem.native_methods.autd3capi_link_soem import Status as _Status
from pyautd3_link_soem.status import Status
from pyautd3_link_soem.thread_priority import ThreadPriority

ErrHandlerFunc = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint8)  # type: ignore[arg-type]


@builder
class _SOEMBuilder(LinkBuilder["SOEM"]):
    _param_ifname: str
    _param_buf_size: int
    _param_send_cycle: Duration
    _param_sync0_cycle: Duration
    _param_err_handler: Callable[[int, Status], None] | None
    _param_timer_strategy: TimerStrategy
    _param_sync_mode: SyncMode
    _param_sync_tolerance: Duration
    _param_sync_timeout: Duration
    _param_state_check_interval: Duration
    _param_process_priority: ProcessPriority
    _param_thread_priority: ThreadPriorityPtr

    def __init__(self: Self) -> None:
        self._param_ifname = ""
        self._param_buf_size = 32
        self._param_send_cycle = Duration.from_millis(1)
        self._param_sync0_cycle = Duration.from_millis(1)
        self._param_err_handler = None
        self._param_timer_strategy = TimerStrategy.SpinSleep
        self._param_sync_mode = SyncMode.DC
        self._param_sync_tolerance = Duration.from_micros(1)
        self._param_sync_timeout = Duration.from_secs(10)
        self._param_state_check_interval = Duration.from_millis(100)
        self._param_process_priority = ProcessPriority.High
        self._param_thread_priority = ThreadPriority.Max

    def _link_builder_ptr(self: Self) -> LinkBuilderPtr:
        def callback_native(_context: ctypes.c_void_p, slave: ctypes.c_uint32, status: ctypes.c_uint8) -> None:  # pragma: no cover
            err = ctypes.create_string_buffer(128)  # pragma: no cover
            status_ = _Status(int(status))  # pragma: no cover
            LinkSOEM().link_soem_status_get_msg(status_, err)  # pragma: no cover
            self._param_err_handler(int(slave), Status.__private_new__(status_, err.value.decode("utf-8")))  # type: ignore[misc]  # pragma: no cover

        self._err_handler = ErrHandlerFunc(callback_native)  # pragma: no cover

        return _validate_ptr(  # pragma: no cover
            LinkSOEM().link_soem(
                _to_null_terminated_utf8(self._param_ifname),
                self._param_buf_size,
                self._param_send_cycle._inner,
                self._param_sync0_cycle._inner,
                None if self._param_err_handler is None else self._err_handler,  # type: ignore[arg-type]
                None,
                self._param_sync_mode,
                self._param_process_priority,
                self._param_thread_priority,
                self._param_state_check_interval._inner,
                self._param_timer_strategy,
                self._param_sync_tolerance._inner,
                self._param_sync_timeout._inner,
            ),
        )

    def _resolve_link(self: Self, handle: HandlePtr, ptr: ControllerPtr) -> "SOEM":
        return SOEM(handle, Base().link_get(ptr), self._err_handler)  # pragma: no cover


class SOEM(Link):
    @staticmethod
    def enumerate_adapters() -> list[EtherCATAdapter]:
        handle = LinkSOEM().adapter_pointer()
        size = LinkSOEM().adapter_get_size(handle)

        def get_adapter(i: int) -> EtherCATAdapter:
            sb_desc = ctypes.create_string_buffer(128)
            sb_name = ctypes.create_string_buffer(128)
            LinkSOEM().adapter_get_adapter(handle, i, sb_desc, sb_name)
            return EtherCATAdapter(sb_name.value.decode("utf-8"), sb_desc.value.decode("utf-8"))

        res = list(map(get_adapter, range(int(size))))

        LinkSOEM().adapter_pointer_delete(handle)

        return res

    def __init__(self: Self, handle: HandlePtr, ptr: LinkPtr, err_handler) -> None:  # noqa: ANN001
        super().__init__(handle, ptr)  # pragma: no cover
        self._err_handler = err_handler  # pragma: no cover

    @staticmethod
    def builder() -> _SOEMBuilder:
        return _SOEMBuilder()
