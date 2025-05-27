import os
try:
    from colorama import Fore, Style
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install colorama")
from typing import Dict, Union, Optional, Callable, Literal
from logging import Logger, FileHandler, Formatter, INFO


__all__ = ["LoggerMixin"]


print_color_mapping = {
    "BLACK".lower(): Fore.BLACK,
    "RED".lower(): Fore.RED,
    "GREEN".lower(): Fore.GREEN,
    "YELLOW".lower(): Fore.YELLOW,
    "BLUE".lower(): Fore.BLUE,
    "CYAN".lower(): Fore.CYAN,
    "MAGENTA".lower(): Fore.MAGENTA,
    "WHITE".lower(): Fore.WHITE,
    "RESET".lower(): Fore.RESET,
}


TypePrintColor = Literal['black', 'red', 'green', 'yellow', 'blue', 'cyan', 'magenta', 'white', 'reset']


class LoggerMixin:
    """"""
    logger: Optional[Union[Logger, Callable]] = None
    verbose: Optional[bool] = False
    log_file: Optional[str] = None
    logger_name: Optional[str] = None

    def __del__(self):
        """对象销毁时自动清理"""
        self.close_handlers()

    def _start_logging(self) -> None:
        """初始化文件日志记录"""
        if not self.log_file:
            return  # 未指定日志文件时跳过

        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 创建文件处理器
        file_handler = FileHandler(self.log_file)
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # 配置日志记录器
        if isinstance(self.logger, Logger):
            # 如果已有logger，添加文件处理器
            self.logger.addHandler(file_handler)
        else:
            # 否则创建新logger
            logger_name = self.logger_name or __name__
            self.logger = Logger(logger_name, level=INFO)
            self.logger.addHandler(file_handler)

    def _logger(
            self,
            msg: str,
            color: Optional[TypePrintColor] = None,
            level: Literal['info', 'debug', 'warning', 'error'] = 'info',
    ) -> None:
        """"""
        if self.logger:
            logger_mapping = {
                "info": self.logger.info,
                "debug": self.logger.debug,
                "warning": self.logger.warning,
                "error": self.logger.error
            }
            logger_mapping.get(level, self.logger.info)(msg)
        if self.verbose:
            if color:
                print(print_color_mapping.get(color) + msg + Style.RESET_ALL, flush=True)
            else:
                print(msg, flush=True)

    def info(self, msg: str, color: Optional[TypePrintColor] = "green"):
        """"""
        self._logger(msg=msg, color=color, level="info")

    def debug(self, msg: str, color: Optional[TypePrintColor] = "blue"):
        """"""
        self._logger(msg=msg, color=color, level="debug")

    def warning(self, msg: str, color: Optional[TypePrintColor] = "yellow"):
        """"""
        self._logger(msg=msg, color=color, level="warning")

    def error(self, msg: str, color: Optional[TypePrintColor] = "red"):
        """"""
        self._logger(msg=msg, color=color, level="error")

    def _logger_base(self, msg: str, color: Optional[TypePrintColor] = None):
        """"""
        if self.logger:
            self.logger.info(msg)
        if self.verbose:
            print(print_color_mapping.get(color) + msg + Style.RESET_ALL, flush=True)

    def _logger_agent_start(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            color: Optional[TypePrintColor] = "green"
    ):
        """"""
        if msg is None: msg = f"[{name}] Start ...\n"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_end(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            color: Optional[TypePrintColor] = "green"
    ):
        """"""
        if msg is None: msg = f"[{name}] End ...\n"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_question(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            content: Optional[str] = None,
            color: Optional[TypePrintColor] = "green"
    ):
        """"""
        if msg is None: msg = f"[{name}] User Question: {content}\n"
        self._logger_base(msg=msg, color=color)

    def _logger_messages_start(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            color: Optional[TypePrintColor] = "red"
    ):
        """"""
        if msg is None: msg = f"{20 * '='} [{name}] Messages Start {20 * '='}\n"
        self._logger_base(msg=msg, color=color)

    def _logger_messages_end(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            color: Optional[TypePrintColor] = "red"
    ):
        """"""
        if msg is None: msg = f"{20 * '='} [{name}] Messages End    {20 * '='}\n"
        self._logger_base(msg=msg, color=color)

    def _logger_messages(
            self,
            msg: Optional[str] = None,
            role: Optional[str] = None,
            content: Optional[str] = None,
            color: Optional[TypePrintColor] = "blue"
    ):
        """"""
        if msg is None: msg = f"{role}: [{content}]\n"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_script(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            script: Optional[str] = None,
            color: Optional[TypePrintColor] = "magenta"
    ):
        """"""
        if msg is None: msg = f"[{name}] Script: ```\n{script}\n```"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_search(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            content: Optional[str] = None,
            color: Optional[TypePrintColor] = "magenta"
    ):
        """"""
        if msg is None: msg = f"[{name}] Script: ```\n{content}\n```"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_warning(self, msg: str, color: Optional[TypePrintColor] = "red"):
        """"""
        self._logger_base(msg=msg, color=color)

    def _logger_agent_final_answer(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            content: Optional[str] = None,
            color: Optional[TypePrintColor] = "yellow"
    ):
        """"""
        if msg is None: msg = f"[{name}] Final Answer: {content}\n"
        self._logger_base(msg=msg, color=color)

    def _logger_dict(self, msg: Dict, color="green"):
        """"""
        for key, val in msg.items():
            if self.logger: self.logger.info(f"{key}: {val}")
            if self.verbose: print(print_color_mapping.get(color) + f"{key}: {val}" + Style.RESET_ALL, flush=True)

    def _logger_color(self, msg: str) -> None:
        """"""
        last_line = msg.split('\n')[-1]

        if self.logger: self.logger.info(msg)
        if self.verbose:
            if last_line.startswith("Answer"):
                print(Fore.YELLOW + msg + Style.RESET_ALL)
            elif last_line.startswith("Action"):
                print(Fore.GREEN + msg + Style.RESET_ALL)
            elif last_line.startswith("No Action"):
                print(Fore.RED + msg + Style.RESET_ALL)
            elif last_line.startswith("Observation"):
                print(Fore.BLUE + msg + Style.RESET_ALL)
            elif last_line.startswith("Running"):
                print(Fore.CYAN + msg + Style.RESET_ALL)
            else:
                print(msg)
            print()

    def close_handlers(self):
        """关闭所有日志处理器"""
        if hasattr(self, 'logger') and isinstance(self.logger, Logger):
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
                handler.close()
            self.logger.handlers.clear()
