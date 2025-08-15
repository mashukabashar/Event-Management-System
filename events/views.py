from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from events.models import Category, Event, Participant
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.utils.timezone import localdate


def home(request):
    events=Event.objects.select_related("category").prefetch_related("participants").all().annotate(total=Count('participants'))

    categories = Category.objects.prefetch_related('event').all()
    selected_category_id = request.GET.get('category') 

    if selected_category_id:
        selected_category_id = int(selected_category_id)  
        selected_category = Category.objects.get(id=selected_category_id)
        events = selected_category.event.all().annotate(total=Count('participants'))

        context={'categories': categories,'events': events,'selected_category_id': selected_category_id}

        return render(request, 'home.html', context)

    query=request.GET.get('q','')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if query:
        events=Event.objects.filter(Q(name__icontains=query)|Q(location__icontains=query)).annotate(total=Count('participants'))
        context={'events':events, 'query':query, 'categories': categories}
        return render(request, "home.html", context)
    
    elif start_date and end_date:
        events = events.filter(date__range=[start_date, end_date]).annotate(total=Count('participants'))
        context = {
        'events': events,
        'start_date': start_date,
        'end_date': end_date,
        'categories': categories
    }
        return render(request, "home.html", context)


    else:
        context={'events':events, 'categories': categories}
        return render(request, "home.html", context)


def event_details(request,id):
    event=Event.objects.get(id=id)
    return render(request, "eventdetails.html",{'event':event})


def dashboard(request):
    type=request.GET.get('type','all')

    events=Event.objects.select_related("category").prefetch_related("participants").all()
    participant=Participant.objects.prefetch_related('events')
    categories = Category.objects.prefetch_related('event')

    counts = Event.objects.aggregate(
        total=Count('id'),
        past_events=Count('id', filter=Q(date__lt=date.today())),
        future_events=Count('id', filter=Q(date__gt=date.today())),
        today_event=Count('id', filter=Q(date=date.today())),
    )

    unique_participant_count = Participant.objects.distinct().aggregate(total=Count('id'))
    total_categories=Category.objects.aggregate(total=Count('id'))

    base_query=Event.objects.select_related("category").prefetch_related("participants")

    if type=='total':
        events=base_query.all()

    elif type=='past_events':
        events=base_query.filter(Q(date__lt=date.today()))

    elif type=='future_events':
        events=base_query.filter(Q(date__gt=date.today()))

    elif type=='all':
        events=base_query.filter(Q(date=date.today()))

    elif type=="total_participants":
        participant=Participant.objects.distinct().annotate(total=Count('events'))
    
    elif type=='category':
        categories=Category.objects.prefetch_related('event')


    context={"events":events, 'participant':participant, "counts":counts, 
             "unique_participant_count":unique_participant_count, "type":type, 
             'categories': categories, 'total_categories':total_categories}

    return render(request, "dashboard.html", context)


def create_event(request):
    
    form = EventModelForm()  

    if request.method == "POST":
        form = EventModelForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request,'Event Created Successfully')
            return redirect('create-event')
        
    context={"form":form}
    return render(request, "event_form.html", context)


def create_category(request):
    
    form = CategoryModelForm()  

    if request.method == "POST":
        form = CategoryModelForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request,'Category Created Successfully')
            return redirect('create-category')
        
    context={"form":form}
    return render(request, "category_form.html", context)


def create_participant(request):
    
    form = ParticipantModelForm()  

    if request.method == "POST":
        form = ParticipantModelForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request,'Participant Created Successfully')
            return redirect('create-participant')
        
    context={"form":form}
    return render(request, "participant_form.html", context)


def update_event(request, id):

    event=Event.objects.get(id=id)

    form = EventModelForm(instance=event)  

    if request.method == "POST":
        form = EventModelForm(request.POST, instance=event) 

        if form.is_valid():

            form.save()
            messages.success(request,'Event Updated Successfully')
            return redirect('update-event', id)
        
    context={"form":form}
    return render(request, "event_form.html", context)


def update_category(request, id):

    category=Category.objects.get(id=id)

    form = CategoryModelForm(instance=category) 

    if request.method == "POST":
        form = CategoryModelForm(request.POST, instance=category) 

        if form.is_valid():

            form.save()
            messages.success(request,'Category Updated Successfully')
            return redirect('update-category', id)
        
    context={"form":form}
    return render(request, "category_form.html", context)


def update_participant(request, id):

    participant=Participant.objects.get(id=id)

    form = ParticipantModelForm(instance=participant)  

    if request.method == "POST":
        form = ParticipantModelForm(request.POST, instance=participant) 

        if form.is_valid():

            form.save()
            messages.success(request,'Participant Updated Successfully')
            return redirect('update-participant', id)
        
    context={"form":form}
    return render(request, "participant_form.html", context)


def delete_event(request, id):

    if request.method == "POST":
        event=Event.objects.get(id=id)
        event.delete()

        messages.success(request,'Event Deleted Successfully')
        return redirect('dashboard')
    else:
        messages.error(request,'Something Went Wrong!')
        return redirect('dashboard')
    

def delete_category(request, id):

    if request.method == "POST":
        category=Category.objects.get(id=id)
        category.delete()

        messages.success(request,'Category Deleted Successfully')
        return redirect('dashboard')
    else:
        messages.error(request,'Something Went Wrong!')
        return redirect('dashboard')


def delete_participant(request, id):

    if request.method == "POST":
        participant=Participant.objects.get(id=id)
        participant.delete()

        messages.success(request,'Participant Deleted Successfully')
        return redirect('dashboard')
    else:
        messages.error(request,'Something Went Wrong!')
        return redirect('dashboard')

