from zion.models import ClientIP
from zion.views import trinity_view

class TrinityIPFilterMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        
        if request.get_full_path().split('?')[0] == '/zion-service/':
            matched_ips = ClientIP.objects.filter(ip_address=request.META.get('REMOTE_ADDR'))
        
            if matched_ips.count() == 0:
                return trinity_view(request)

        return None

