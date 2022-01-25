import sys
from loguru import logger

logger.remove()

format = (
    "<red>{level}</> | <green>{time:YYYY-MM-DD  HH:mm:ss}</> | <magenta>{message}</>"
)

logger.add(
    sys.stdout,
    level="INFO",
    format=format,
    colorize=True,
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

# format = '''
# {time:YYYY-MM-DD  HH:mm:ss}
# {level}
# {name}
# {function}
# {line}
# {message}
# '''
