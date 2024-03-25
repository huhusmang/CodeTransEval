from django.shortcuts import redirect


def process_request(request):
    password = request.GET["password"]

    if password == "myPa55word":
        redirect("login")

