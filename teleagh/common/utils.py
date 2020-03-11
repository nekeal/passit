

def setup_view(view, request, *args, **kwargs):
    """
    Initializes generic view or viewset with passed params
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view
