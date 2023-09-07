from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import CompareList
from .serializers import CompareListSerializer, CompareListDetailSerializer


class CompareListCreate(ModelViewSet):
    queryset = CompareList.objects.all()
    serializer_class = CompareListSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.generics import ListAPIView, RetrieveAPIView


class CompareListDetail(ListAPIView):
    queryset = CompareList.objects.all()
    serializer_class = CompareListDetailSerializer


class CompareListRetrieve(RetrieveAPIView):
    queryset = CompareList.objects.all()
    serializer_class = CompareListDetailSerializer
