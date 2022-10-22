import traceback
from time import sleep

from core.log_helper import log


def run_catching(function, retry=0, fail=True, on_error=None):
    # log(f'Follows execution of {function.__name__}')
    retry_count = 0
    while True:
        try:
            return function()
        except Exception as ex:
            log('EXCEPTION runCatching\n\n' + traceback.format_exc())
            if on_error is not None:
                on_error(ex)
            if retry_count >= retry:
                if fail:
                    raise Exception('Retry exhausted') from ex
                else:
                    return
            retry_count += 1
            secs = 0.2 * pow(2, retry_count)
            log(f'Retry again ({retry_count}/{retry}) in {secs} seconds')
            sleep(secs)
