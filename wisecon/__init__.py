from importlib.metadata import version, PackageNotFoundError


__all__ = [
    "__version__",
]


try:
    __version__ = version("wisecon")
except PackageNotFoundError:
    __version__ = "unknown"
