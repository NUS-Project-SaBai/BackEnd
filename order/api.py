import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


from rest_framework.views import APIView
from clinicmodels.models import Order
from order.forms import OrderForm
from sabaibiometrics.serializers.order_serializer import OrderSerializer


"""
Handles all operations regarding the retrieval, update of order models.
"""


class OrderView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        try:
            order_name = request.GET.get('name', '')
            order_status = request.GET.get('order_status', '')
            orders = Order.objects.all()

            if order_name:
                orders = orders.filter(name__icontains=order_name)
            if order_status:
                orders = orders.filter(order_status=order_status)

            serializer = OrderSerializer(orders, many=True)
            return HttpResponse(json.dumps(serializer.data), content_type='application/json')
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            order = order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return HttpResponse(json.dumps(serializer.data), content_type='application/json')
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def post(self, request):
        '''
        POST request with multipart form to create a new order
        :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
        :return: Http Response with corresponding status code
        '''
        try:
            form = OrderForm(json.loads(request.body
                                        or None))
            if form.is_valid():
                order = form.save()
                serializer = OrderSerializer(order)
                return HttpResponse(json.dumps(serializer.data), content_type="application/json")
            else:
                return JsonResponse(form.errors, status=400)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def patch(self, request, pk):
        '''
        Update order data based on the parameters
        :param request: POST with data
        :return: JSON Response with new data, or error
        '''
        try:
            order = Order.objects.get(pk=pk)
            form = OrderSerializer(order, data=request.data, partial=True)

            print(form.is_valid())
            if form.is_valid():
                form.save()
                return HttpResponse(form.data, content_type="application/json")

            else:
                return JsonResponse(form.errors, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)

# @api_view(['GET'])
# def get_order_image_by_id(request):
#     '''
#     GET image of order by id
#     :param request: GET with parameter id of order you want the image of
#     :return: FileResponse if image is found, 404 if not
#     '''
#     try:
#         if 'id' not in request.GET:
#             return JsonResponse({"message": "GET: parameter 'id' not found"}, status=400)
#         order_id = request.GET['id']
#         order = order.objects.get(pk=order_id)
#         image = order.picture
#         if "jpeg" in image.name.lower() or "jpg" in image.name.lower():
#             return HttpResponse(image.file.read(), content_type="image/jpeg")
#         elif "png" in image.name.lower():
#             return HttpResponse(image.file.read(), content_type="image/png")
#         else:
#             return JsonResponse({"message": "order image is in the wrong format"}, status=400)
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message": str(e)}, status=404)
#     except ValueError as e:
#         return JsonResponse({"message": str(e)}, status=400)


# @api_view(['POST'])
