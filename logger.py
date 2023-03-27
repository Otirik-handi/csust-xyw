## 简易日志设置
# import logging
# level = logging.DEBUG
# format = '%(asctime)s [%(levelname)s] - %(message)s'
# logging.basicConfig(level=level, format=format)

## 高级日志设置
import sys
import logging
import coloredlogs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name="Logger")
coloredlogs.install(logger=logger)
logger.propagate = False
coloredFormatter = coloredlogs.ColoredFormatter(
    fmt=
    '[%(name)s] %(asctime)s [%(levelname)s] [%(filename)s %(funcName)s@lineno:%(lineno)-d] - %(message)s',
    level_styles=dict(
        debug=dict(color='white'),
        info=dict(color='green'),
        warning=dict(color='yellow', bright=True),
        error=dict(color='red', bold=True, bright=True),
        critical=dict(color='black', bold=True, background='red'),
    ),
    field_styles=dict(name=dict(color='white'),
                      asctime=dict(color='white'),
                      lineno=dict(color='white'),
                      funcName=dict(color='blue'),
                      filename=dict(color="white")))

sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(fmt=coloredFormatter)
logger.addHandler(hdlr=sh)
logger.setLevel(level=logging.INFO)