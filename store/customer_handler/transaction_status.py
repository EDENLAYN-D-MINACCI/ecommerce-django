def set_status(request, status):
    try:
        request.session['transaction_status'] = status
        request.session['show_snackbar'] = True
        print("show snackbar is true")
    except Exception as e:
        print("set_status:",e)

def get_status(request):
    try:
        show    = request.session["show_snackbar"]
        status  = request.session["transaction_status"]

        if show is not None and status is not None:
            request.session['show_snackbar'] = False
            print("get status:",status)

            if show: return status
            else: return 0

    except Exception as e:
        print("get_status error:",e)


    