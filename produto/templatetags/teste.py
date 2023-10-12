import mercadopago
from django.http import HttpRequest, JsonResponse
sdk = mercadopago.SDK("TEST-2239762821884380-101018-24f361cb4176ec9d36b324301548ea02-1280904713")

# payment_data = {
#     "transaction_amount": float(request.POST.get("transaction_amount")),
#     "token": request.POST.get("token"),
#     "description": request.POST.get("description"),
#     "installments": int(request.POST.get("installments")),
#     "payment_method_id": request.POST.get("payment_method_id"),
#     "payer": {
#         "email": request.POST.get("cardholderEmail"),
#         "identification": {
#             "type": request.POST.get("identificationType"),
#             "number": request.POST.get("identificationNumber"),
#         },
#         "first_name": request.POST.get("cardholderName")
#     }
# }

# payment_data = {
#     "transaction_amount": 100.0,
#         "token": '9313229faacd7078199333a75bcd6ba8',
#         "description": "Descrição do item",
#         "installments": 1,
#         "payment_method_id": "visa",
#         "payer": {
#             "email": "TESTUSER831069532@gmail.com",  # substitua pelo e-mail do pagador
#         }
# }

# payment_response = sdk.payment().create(payment_data)
# payment = payment_response["response"]
# print(payment)
