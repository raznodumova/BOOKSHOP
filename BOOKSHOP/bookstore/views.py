from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from django.db import transaction


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def buy(self, request, pk=None):
        book = self.get_object()
        try:
            with transaction.atomic():
                if book.count > 0:
                    book.count -= 1
                    book.save()
                    return Response({'message': 'Книга куплена :)'})
                else:
                    return Response({'message': 'Книги закончилась, выбери другую :('}, status=status.HTTP_400_BAD_REQUEST) # иногда я развлекаюсь с сообщениями

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
