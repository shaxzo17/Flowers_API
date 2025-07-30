from django.shortcuts import render
from rest_framework import mixins , status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .models import Flower
from .serializers import FlowerSerializer

# # with mixins
# class FlowerListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin,GenericAPIView):
#     queryset = Flower.objects.all()
#     serializer_class = FlowerSerializer
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
# class FlowerDel(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
#     queryset = Flower.objects.all()
#     serializer_class = FlowerSerializer
#
#     def get(self, request, pk):
#         return self.retrieve(request, pk=pk)
#
#     def put(self, request, pk):
#         return self.update(request, pk=pk)
#
#     def patch(self, request, pk):
#         return self.partial_update(request, pk=pk)
#
#     def delete(self, request, pk):
#         return self.destroy(request, pk=pk)


# # without mixins
class FlowerListCreateAPIView(APIView):
    def get(self, request):
        flowers = Flower.objects.all()
        serializer = FlowerSerializer(flowers, many=True)
        return Response(serializer.data)

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
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FlowerSerializer(flower)
        return Response(serializer.data)

    def put(self, request, pk):
        flower = self.get_object(pk)
        if not flower:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FlowerSerializer(flower, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        flower = self.get_object(pk)
        if not flower:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FlowerSerializer(flower, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        flower = self.get_object(pk)
        if not flower:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        flower.delete()
        return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
