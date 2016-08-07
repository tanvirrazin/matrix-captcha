class TrinityIPFilterMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        print request.META.get('REMOTE_ADDR')

