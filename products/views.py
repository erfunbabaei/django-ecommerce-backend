from rest_framework import generics
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from .permissions import IsSellerOrReadOnly
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


# ----------------------------
# Create Product
# ----------------------------

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

# ----------------------------
# View And Edit Product
# ----------------------------

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]

    @action(detail=True, methods=['post'])
    def upload_images(self, request, pk=None):
        product = self.get_object()
        files = request.FILES.getlist('images')

        if not files:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        images = []
        for file in files:
            if not file.content_type.startswith("image/"):
                continue
            img = ProductImage.objects.create(product=product, image=file)
            images.append(img)

        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
