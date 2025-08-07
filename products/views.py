from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Flower
from .serializers import FlowerSerializer
from django.db.models import Q


class ListCreateApiView(APIView):
    def get(self, request):
        flowers = Flower.objects.all()

        name = request.GET.get('name')
        description = request.GET.get('description')
        if name:
            flowers = flowers.filter(name=name)
        if description:
            flowers = flowers.filter(description=description)
        search = request.GET.get('search')
        if search:
            flowers = flowers.filter(Q(name__icontains=search) | Q(description__icontains=search))

        paginator = PageNumberPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(flowers, request)

        serializer = FlowerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
