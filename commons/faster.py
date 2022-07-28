from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_WORKERS_LIMIT = 50


def do_concurrently(max_workers: int,
                    func_args_list: list):
    """
    Args:
        max_workers: maximum threads to spawn
        func_args_list: list of tuple of (func, [arg1, arg2, arg3])

    Returns:
        dict of response of each function call aggregated as a list
    """

    futures = []
    future_function_map = {}
    function_response_map = defaultdict(list)
    max_workers = min(max(max_workers, 1), MAX_WORKERS_LIMIT)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        for func, params in func_args_list:
            args = []
            kwargs = {}
            if params:
                if 'args' in params:
                    args = params['args']
                if 'kwargs' in params:
                    kwargs = params['kwargs']

            future = executor.submit(func, *args, **kwargs)
            futures.append(future)
            future_function_map[future] = func

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                function_response_map[future_function_map[future]].append(
                    result
                )

    return function_response_map
