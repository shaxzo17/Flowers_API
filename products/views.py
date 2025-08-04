from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Flower
from .serializers import FlowerSerializer
from django.db.models import Q

class FlowerListCreateAPIView(APIView):
    def get(self, request):
        flowers = Flower.objects.all()

        name = request.GET.get("name")
        description = request.GET.get("description")
        search = request.GET.get("search")

        if name:
            flowers = flowers.filter(name__iexact=name)
        if description:
            flowers = flowers.filter(description__iexact=description)
        if search:
            flowers = flowers.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        serializer = FlowerSerializer(flowers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FlowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlowerDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Flower.objects.get(pk=pk)
        except Flower.DoesNotExist:
            return None

    def get(self, request, pk):
        flower = self.get_object(pk)
        if not flower:
            return Response({'error': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FlowerSerializer(flower)
        return Response(serializer.data)

    def put(self, request, pk):
        flower = self.get_object(pk)
        if not flower:
            return Response({'error': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FlowerSerializer(flower, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        flower = self.get_object(pk)
        if not flower:
            return Response({'error': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FlowerSerializer(flower, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        flower = self.get_object(pk)
        if not flower:
            return Response({'error': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        flower.delete()
        return Response({'message': 'O‘chirildi'}, status=status.HTTP_204_NO_CONTENT)
