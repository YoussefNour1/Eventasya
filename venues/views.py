import base64

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from accounts.permissions import IsVenueOwner, IsNormalUser
from .models import Venue, VenueImages, LegalDocuments, VenueBooking, Review, FavouriteVenues
from .serializers import VenueSerializer, VenueImagesSerializer, VenueBookingSerializer, LegalDocumentsSerializer, \
    ReviewSerializer, FavouriteVenuesSerializer
from rest_framework.views import *
from rest_framework import generics, status

User = get_user_model()


# Create your views here.


class VenueListCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.filter(status='active').order_by('id')
    serializer_class = VenueSerializer
    permission_classes = [AllowAny, ]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filterset_fields = ['category', 'city']
    search_fields = ['name', 'city', 'category', ]
    order_fields = ['price_per_hour', '']

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsVenueOwner()]
        else:
            return []

    def get_queryset(self):
        queryset = super().get_queryset()
        venue_ids = self.request.query_params.get('venues')
        if venue_ids:
            try:
                venue_ids = [int(pk) for pk in venue_ids.split(',')]
                queryset = self.queryset.filter(pk__in=venue_ids)
            except ValueError:
                raise Http404("Invalid venue_ids")

        # Filter venues based on city
        city: str = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)

        # Filter venues based on category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)

        return queryset

    def post(self, request, *args, **kwargs):
        owner = request.user
        data = request.data.copy()
        data['owner'] = owner.pk
        venue_serializer = self.serializer_class(data=data)
        if venue_serializer.is_valid():
            venue = venue_serializer.save()
            images = request.FILES.getlist('images')
            for img in images:
                VenueImages.objects.create(venue=venue, image=img)

            # Upload legal documents
            tax_card = request.FILES.get('tax_card')
            commercial_register = request.FILES.get('commercial_register')
            license_agreement = request.FILES.get('license_agreement')
            rental_contract = request.FILES.get('rental_contract')
            ownership_contract = request.FILES.get('ownership_contract')
            national_id = request.FILES.get('national_id')

            legalDocs = LegalDocuments.objects.create(
                tax_card=tax_card,
                commercial_register=commercial_register,
                license_agreement=license_agreement,
                rental_contract=rental_contract,
                ownership_contract=ownership_contract,
                national_id=national_id,
                venue=venue
            )
            if legalDocs is not None:
                venue.legal_documents = legalDocs
                venue.save()
            return Response(VenueSerializer(venue).data, status=status.HTTP_201_CREATED)
        return Response({"errors": venue_serializer.errors}, status.HTTP_400_BAD_REQUEST)


class LegalDocsCreateView(generics.CreateAPIView):
    model = LegalDocuments
    serializer_class = LegalDocumentsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        venue_id = self.kwargs['venueId']
        owner = request.user
        venue = Venue.objects.get(id=venue_id)

        # Check if the current user is the owner of the venue
        if venue.owner != owner:
            return Response({'detail': 'You are not the owner of this venue.'}, status=status.HTTP_403_FORBIDDEN)

        tax_card = request.FILES.get('tax_card')
        commercial_register = request.FILES.get('commercial_register')
        license_agreement = request.FILES.get('license_agreement')
        rental_contract = request.FILES.get('rental_contract')
        ownership_contract = request.FILES.get('ownership_contract')
        national_id = request.FILES.get('national_id')

        legalDocs = LegalDocuments(
            venue=venue,
            tax_card=tax_card,
            commercial_register=commercial_register,
            license_agreement=license_agreement,
            rental_contract=rental_contract,
            ownership_contract=ownership_contract,
            national_id=national_id
        )
        serializer = LegalDocumentsSerializer(legalDocs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleVenueAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle, ]

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", 'DELETE'):
            return [IsVenueOwner()]

        elif self.request.method == "GET":
            return [AllowAny()]


class VenueImagesListCreateView(generics.ListCreateAPIView):
    serializer_class = VenueImagesSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        venue_id = self.kwargs['venueId']
        try:
            venue = Venue.objects.get(id=venue_id)
            return venue.venue_images.all().order_by('id')
        except Venue.DoesNotExist:
            return VenueImages.objects.none()

    def post(self, request, *args, **kwargs):
        venue_id = self.kwargs['venueId']
        venue = Venue.objects.get(id=venue_id)

        images = request.FILES.getlist('images')
        venue_images = []
        for image in images:
            venue_images.append(VenueImages(venue=venue, image=image))
        VenueImages.objects.bulk_create(venue_images)

        return Response(VenueImagesSerializer(venue.venue_images.all(), many=True).data, status=status.HTTP_201_CREATED)


class VenueImagesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    model = VenueImages
    serializer_class = VenueImagesSerializer


class VenueBookingListCreateView(generics.ListCreateAPIView):
    queryset = VenueBooking.objects.all()
    serializer_class = VenueBookingSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        venue = Venue.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, venue=venue)


class VenueBookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VenueBooking.objects.all()
    serializer_class = VenueBookingSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        try:
            return VenueBooking.objects.filter(user=user)
        except Venue.DoesNotExist:
            return VenueBooking.objects.none()


class VenueOwnerVenueListView(generics.ListAPIView):
    model = Venue
    serializer_class = VenueSerializer

    def get_queryset(self):
        owner = self.request.user
        return Venue.objects.filter(owner=owner).order_by('id')


class VenueOwnerBookingListView(generics.ListAPIView):
    permission_classes = [IsVenueOwner, ]
    serializer_class = VenueBookingSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        owner = self.request.user
        try:
            return VenueBooking.objects.filter(venue__owner=owner)
        except VenueBooking.DoesNotExist:
            return VenueBooking.objects.none()


class UserBookingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    serializer_class = VenueBookingSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            return VenueBooking.objects.filter(user=user)
        except VenueBooking.DoesNotExist:
            return VenueBooking.objects.none()


class VenueImagesUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = VenueImages.objects.all()
    serializer_class = VenueImagesSerializer


class ReviewsListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related('venue').filter(venue_id=self.kwargs['venueId'])

    def perform_create(self, serializer):
        c = serializer.save(user=self.request.user, venue_id=self.kwargs['venueId'])
        print(c)


class FavouriteVenueCreateDestroyView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = FavouriteVenuesSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'venue_id'

    def get_queryset(self):
        user = self.request.user
        return user.favouriteVenues.all()

    def perform_create(self, serializer):
        user = self.request.user
        venue = Venue.objects.get(pk=self.kwargs["venue_id"])
        serializer.save(user=user, venue=venue)

    def perform_destroy(self, instance):
        instance.delete()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serialized_data = FavouriteVenuesSerializer(page, many=True).data
            return self.get_paginated_response(serialized_data)
        serialized_data = FavouriteVenuesSerializer(queryset, many=True).data
        return Response(serialized_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serialized_data = FavouriteVenuesSerializer(page, many=True).data
            return self.get_paginated_response(serialized_data)
        serialized_data = FavouriteVenuesSerializer(queryset, many=True).data
        return Response(serialized_data, status=status.HTTP_204_NO_CONTENT)
