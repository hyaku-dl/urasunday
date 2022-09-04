try:
    from .cli import cli
except ImportError:
    from cli import cli

cli()
