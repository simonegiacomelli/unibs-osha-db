import traceback
from time import sleep

from core.log_helper import log


def run_catching(function, retry=0, fail=True):
    # log(f'Follows execution of {function.__name__}')
    retry_count = 0
    while True:
        try:
            return function()
        except Exception as ex:
            log('EXCEPTION runCatching\n\n' + traceback.format_exc())
            if retry_count >= retry:
                if fail:
                    raise Exception('Retry exhausted') from ex
                else:
                    return
            retry_count += 1
            log(f'Retry again ({retry_count}/{retry})')
            sleep(0.2 * pow(2, retry))
