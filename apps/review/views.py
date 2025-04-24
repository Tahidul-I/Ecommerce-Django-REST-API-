from django.shortcuts import render
from rest_framework.decorators import api_view,APIView
from rest_framework.response import Response
from ..authentication.utils import get_user
# from .models import *
from .serializers import *
# Create your views here.

@api_view(['POST'])
def save_review(request):
    access_token = request.COOKIES.get('access_token')
    user = get_user(access_token)
    product_id = request.data.get('product_id')
    review_comment = request.data.get('review_comment')
    review_star = int(request.data.get('review_star'))
    review = Review(user=user,product_id=product_id,review_comment=review_comment,review_star=review_star )
    review.save()

    review_images = request.data.get('review_images',None)
    if review_images is not None:
        for image in review_images:
            review_image = ReviewImages(review=review, image_url=image)
            review_image.save()
    
    return Response({'status_code':200,'message':'Thanks for the review'})

@api_view(['GET'])
def get_reviews(request):
    product_id = int(request.GET.get('product_id'))
    print(product_id)
    reviews = Review.objects.filter(product_id=product_id).order_by('-updated_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def delete_review(request):
    review_id = request.data.get('review_id')
    review = Review.objects.get(id = review_id)
    review.delete()
    return Response({'status_code':200,'message':'Your review has been deleted'})