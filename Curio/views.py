from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render

# # Create your views here.
# @login_required(login_url="/login/")
# def home(request):
#     user_list = EmployeeLeaveLog.objects.filter(employee_code=request.user.id)
#     data=pagination(request,user_list)[0]
#     page_range=pagination(request,user_list)[1]
#     return render(request,"leavestatus.html",{"data": data,"page_range":page_range},)


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["login_username"], password=request.POST["password"]
        )
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(
                request, "login.html", {"error": "Invalid Username or Password"}
            )

    return render(request, "login.html")


# def logout_view(request):
#     logout(request)
#     return redirect("/login")


# @login_required(login_url="/login/")
# def apply_leave(request):
#     if request.method == "POST":
#         form = ApplyLeaveForm(request.POST,request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             employee_code = request.user
#             instance.employee_code = employee_code
#             db_instance = EmployeeMaster.objects.filter(
#                 employee_code_id=employee_code
#             ).values_list(instance.type_of_leave, flat=True)[0]
#             no_of_days = (instance.to_date - instance.from_date).days + 1
#             if no_of_days < 1:
#                 return render(
#                     request,
#                     "applyleave.html",
#                     {
#                         "form": form,
#                         "error_message": "Please select valid to and from dates.",
#                     },
#                 )
#             if no_of_days > db_instance:
#                 return render(
#                     request,
#                     "applyleave.html",
#                     {
#                         "form": form,
#                         "error_message": f"You do not have enough {instance.type_of_leave} available.",
#                     },
#                 )
#             instance.save()
#             return redirect("/")
#     else:
#         form = ApplyLeaveForm()
#     return render(request, "applyleave.html", {"form": form})


# @login_required(login_url="/login/")
# def leave_approval(request):
#     auth = EmployeeMaster.objects.filter(level1_auth=request.user.id)
#     user_list= EmployeeLeaveLog.objects.filter(
#         employee_code__in=[i.employee_code for i in auth]
#     )

#     if request.method == "POST":
#         form = LeaveApprovalForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             auth_by = request.user
#             instance.authEmpCd = auth_by
#             instance.save()

#             return redirect("/")
#     else:
#         form = LeaveApprovalForm()

#     data=pagination(request,user_list)[0]
#     page_range=pagination(request,user_list)[1]
#     return render(request, "leaveapproval.html", {"data": data,"page_range":page_range, "form": form})


# @login_required(login_url="/login/")
# def credit_leave(request):
#     if request.method == "POST":
#         form = CreditLeaveForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.type = 1
#             instance.type_of_leave = "EL"
#             instance.save()
#     else:
#         form = CreditLeaveForm()

#     user_list = EmployeeLeaveLog.objects.filter(type=1)
#     data=pagination(request,user_list)[0]
#     page_range=pagination(request,user_list)[1]

#     return render(request, "creditLeave.html", {"form": form, "data": data,"page_range":page_range})


# @login_required(login_url="/login/")
# def update_status(request, leavelog_id):
#     pi = EmployeeLeaveLog.objects.get(pk=leavelog_id)
#     form_user = EmployeeMaster.objects.get(employee_code_id=pi.employee_code.id)
#     if request.method == "POST":
#         form = LeaveApprovalForm(request.POST, instance=pi)
#         #leave_form = UpdateLeaveForm(request.POST, instance=form_user)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             auth_by = request.user
#             instance.auth_by = auth_by
#             if instance.status == 1:
#                 db_instance = EmployeeMaster.objects.filter(
#                     employee_code_id=pi.employee_code.id
#                 )
#                 existing_leaves = db_instance.values_list(
#                     instance.type_of_leave, flat=True
#                 )[0]
#                 db_instance.update(
#                     **{instance.type_of_leave: (existing_leaves - instance.days)}
#                 )
#             instance.save()
#             return redirect("lms_approveleave")
#         #if leave_form.is_valid():
#             #leave_form.save()

#     else:
#         form = LeaveApprovalForm(instance=pi)
#         #leave_form = UpdateLeaveForm(instance=form_user)
#     return render(
#         request,
#         "updatestatus.html",
#         {"form": form, "pi": pi, "form_user": form_user
#         #"leave_form": leave_form
#         }
#     )

# @login_required(login_url="/login/")
# def approved_leaves(request):
#     user_list = EmployeeLeaveLog.objects.filter(status=1)
#     data=pagination(request,user_list)[0]
#     page_range=pagination(request,user_list)[1]

#     return render(request, "approvedLeaves.html", {"data": data,"page_range":page_range})

# def pagination(request,user_list):
#     user_list = list(reversed(user_list))
#     page = request.GET.get("page", 1)
#     paginator = Paginator(user_list, 7)
#     page_range = paginator.get_elided_page_range(number=page)
#     try:
#         data = paginator.page(page)
#     except PageNotAnInteger:
#         data = paginator.page(1)
#     except EmptyPage:
#         data = paginator.page(paginator.num_pages)
#     return [data,page_range]