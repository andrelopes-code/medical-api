from loguru import logger
from rich import print
from app.core import settings

LOG_LEVEL = settings.log_level

logger.remove(0)
logger.add(
    print,
    level=LOG_LEVEL,
    format='[bold yellow]{time:YYYY-MM-DD at HH:mm:ss}[/bold yellow] ~ [bold cyan]{level}[/bold cyan] ~ {message}',
    catch=True,
    backtrace=False,
    diagnose=False,
)
