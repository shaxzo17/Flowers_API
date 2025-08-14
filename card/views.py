from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Flower
from .serializers import CardItemSerializer, CardSerializer
from .models import Card, CardItem


class CardCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        card, created = Card.objects.get_or_create(user=request.user)
        serializer = CardSerializer(card)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED if card else status.HTTP_200_OK)


class AddToCard(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        product_id = request.data["product_id"]
        amount = int(request.data["amount"])
        if not Flower.objects.filter(id=product_id).exists():
            data = {
                'error': "Siz mavjud bomagan gul tanladiz",
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        if amount < 0:
            data = {
                "error": "Siz xato malumot kiritdiz",
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(data)
        card, _ = Card.objects.get_or_create(user=request.user)
        gul = Flower.objects.get(id=product_id)
        if not CardItem.objects.filter(product=gul).exists():
            gul = CardItem.objects.create(
                card=card,
                product=gul,
                amount=amount
            )
        else:
            gul = CardItem.objects.get(product=gul)
            gul.amount += amount

        gul.save()
        serializer = CardItemSerializer(gul)
        data = {
            "data": serializer.data,
            'status': status.HTTP_201_CREATED
        }
        return Response(data)


class CardItemUpdate(APIView):
    def post(self, request, pk):
        count = request.data.get('count', None)
        mtd = request.data.get('mtd', None)

        product = CardItem.objects.get(card__user=request.user, id=pk)
        if count:
            product.amount = int(count)
            product.save()

        elif mtd:
            if mtd == "+":
                product.amount += 1
                product.save()
            elif mtd == "-":
                if product.amount == 1:
                    product.delete()
                else:
                    product.amount -= 1
                    product.save()


        else:
            return Response({"error": "Error", 'status': status.HTTP_400_BAD_REQUEST})

        serializer = CardItemSerializer(product)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK, 'msg': "O'zgartirldi"})