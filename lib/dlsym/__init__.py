import importlib.metadata


try:
    __version__ = importlib.metadata.version("dlsym")
except ImportError:
    __version__ = "0+unknown"
