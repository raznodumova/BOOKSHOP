from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def buy(self, request, pk=None):
        book = self.get_object()
        if book.count > 0:
            book.count -= 1
            book.save()
            return Response({'message': 'Book purchased successfully!'})
        else:
            return Response({'error': 'Book is out of stock!'}, status=status.HTTP_400_BAD_REQUEST)
