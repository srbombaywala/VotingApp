from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm, generateotp, logintovoteform, votingform
from .models import member
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from urllib.parse import urlencode, parse_qs

def index(request):
    return render(request, 'modules_app/index.html', {'message':''})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'modules_app/register.html', {'form':form})        

def generateOTP(request):
    if request.method == 'POST':
        form = generateotp(request.POST)
        if form.is_valid():
            ppan = form.cleaned_data['ppan']
            voter = member.objects.get(ppan=ppan)
            if voter.otp == '' and voter.has_voted == False:
                generated_otp = voter.generate_otp()
                return render(request, 'modules_app/generate_otp.html',{'message':f'The otp generated for {voter.first_name} is {generated_otp}', 'form':form})
            else:
                form = generateotp()
                return render(request, 'modules_app/generate_otp.html',{'message':f'OTP already Generated', 'form':form})
    else:
        form = generateotp()
    return render(request, 'modules_app/generate_otp.html',{'message':'', 'form':form})

def logintovote(request):
    if request.method == 'POST':
        form = logintovoteform(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            password = form.cleaned_data['password']
            voter = member.objects.get(otp = otp)
            # check if the voter.otp_gen_time is valid
            time_difference = timezone.now() - voter.otp_generated_at
            if time_difference > timedelta(minutes=100):
                messages.info(request, 'OTP Expired')
                return redirect('logintovote')
            else:
                if not voter.has_voted and password == '654321':
                    members = member.objects.all()
                    # Set a session flag to indicate successful login
                    request.session['login_flag'] = True
                    return redirect('popup_modal', voter_id = voter.id)
                elif voter.has_voted and password == '654321':
                    messages.info(request, 'You have already voted!')
                    return redirect('logintovote')
                else:
                    messages.info(request, 'Master Password Incorrect')
                    return redirect('logintovote')
    else:
        form = logintovoteform()
        return render(request, 'modules_app/logintovote.html', {'form':form})


@login_required
def popup_modal(request, voter_id):
    if not request.session.get('login_flag'):
        return HttpResponseForbidden("Access denied. You must log in first.")
    voter = get_object_or_404(member, id=voter_id)
    if request.method == "POST":
        form = votingform(request.POST)
        if form.is_valid():
            member1 = form.cleaned_data['field1']
            member2 = form.cleaned_data['field2']
            member3 = form.cleaned_data['field3']
            member4 = form.cleaned_data['field4']
            member5 = form.cleaned_data['field5']
            # save the members.....
            voter.save_vote([member1, member2, member3, member4, member5])
            del request.session['login_flag']
            messages.success(request,"Thank you for voting")
            return redirect('index')
            # return render(request, 'modules_app/index.html', {'message':'Your vote has been registered. Thank you'})
    else:
        form = votingform()
        return render(request, 'modules_app/popup.html',{'form':form, 'voter':voter})

def member_list_popup(request):
    members = member.objects.all()
    return render(request, 'modules_app/member_list_popup.html', {'members': members})

def candidate_votes(request):
    votes_dict = member.get_votes_count()
    sorted_votes = dict(sorted(votes_dict.items(), key=lambda x: x[1], reverse=True))
    return render(request, 'modules_app/candidate_votes.html', {'votes_dict': sorted_votes})

def user_search(request):
    search_query = request.GET.get('search_query', '')
    # print(f"Received search query: {search_query}")
    # Perform the search based on name or department
    if search_query:
        users = member.objects.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(ppan__icontains=search_query)
        )
    else:
        users = member.objects.all()

    return render(request, 'modules_app/search_result.html', {'members': users})

def voted(request,message):
    print(message)
    return render(request, 'modules_app/index.html', {'message': message})
