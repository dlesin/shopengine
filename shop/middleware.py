class DisableBrowserCacheMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Pragma'] = 'no-cache'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Expires'] = '0'
        return response
