from django.http import JsonResponse
from django.core.cache import cache

def check_redis(request):
    '''
    Функция для проверки работы Redis
    '''

    try:
        cache.set('test', 'working', 5)
        value = cache.get('test')
        return JsonResponse({'status': 'connected', 'test_value': value})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})