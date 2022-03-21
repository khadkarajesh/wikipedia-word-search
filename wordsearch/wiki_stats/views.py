from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import get_summary


@api_view()
def search(request):
    return Response(get_summary(request.query_params.get('title', 'wikipedia')))
