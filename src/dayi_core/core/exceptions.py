class DayiCoreError(Exception):
    """Base exception for dayi core."""


class NuxtStateNotFoundError(DayiCoreError):
    """Raised when window.__NUXT__ script block is missing."""
