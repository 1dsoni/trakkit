class MyLocal(object):
    """
    meant as a replacement to the threading.local, we want to share the traces
    across the threads
    """
    pass


my_local = MyLocal()


# always use these helper functions

def get_local_attr(attr):
    return getattr(my_local, attr, None)


def set_local_attr(attr, val):
    setattr(my_local, attr, val)


def delete_local_attr(attr):
    try:
        delattr(my_local, attr)
    except AttributeError:
        pass


def set_local_request_trace_id(request_trace_id):
    set_local_attr('request_trace_id', request_trace_id)


def get_local_request_trace_id():
    return get_local_attr('request_trace_id')


def delete_local_request_trace_id():
    delete_local_attr('request_trace_id')
