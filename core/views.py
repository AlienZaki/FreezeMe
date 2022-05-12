from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import reverse, redirect
from .models import Client, Website, Requirement, Submission, Settings
from state.models import State
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import *
from django.http import HttpResponse
from django.views import generic
#from .tasks import scrape_async


def client_list(request):
    if request.method == 'POST':
        pass
    else:
        page_num = request.GET.get('page', default=1)
        query = request.GET.get('q', default=None)

        clients = Client.objects.filter(ssn__contains=query) if query else Client.objects.all()
        paginator = Paginator(clients, per_page=10)
        try:
            page_items = paginator.page(page_num)
        except PageNotAnInteger:
            page_items = paginator.page(1)
        except EmptyPage:
            page_items = paginator.page(paginator.num_pages)


        context = {
            'clients': page_items,
        }
        return render(request, 'clients_list.html', context=context)


def add_client(request):
    if request.method == 'POST':
        form = clientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client_list')
        else:
            states = State.objects.all()
            context = {
                'states': states,
                'form': form
            }
            return render(request, 'add_client.html', context=context)
    else:
        states = State.objects.all()
        #websites = Website.objects.filter(ready=True).all()
        context = {
            'states': states,
        }
        return render(request, 'add_client.html', context=context)


def edit_client(request, pk):
    if request.method == 'POST':
        pass
    else:
        client = Client.objects.get(pk=id)
        form = clientForm(instance=client)
        form = clientForm(request.POST, instance=client)

        states = State.objects.all()
        context = {
            'states': states,
        }
        return render(request, 'add_client.html', context=context)


class UpdateClientView(generic.UpdateView):
    model = Client
    template_name = 'add_client.html'
    form_class = clientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        states = State.objects.all()
        context['states'] = states
        return context




def submission_list(request):
    if request.method == 'POST':
        pass
    else:
        page_num = request.GET.get('page', default=1)

        submissions = Submission.objects.all().order_by('-timestamp')
        paginator = Paginator(submissions, per_page=10)
        try:
            page_items = paginator.page(page_num)
        except PageNotAnInteger:
            page_items = paginator.page(1)
        except EmptyPage:
            page_items = paginator.page(paginator.num_pages)

        processing = Submission.objects.filter(finished=False).count()
        finished = Submission.objects.filter(finished=True).count()
        succeed = Submission.objects.filter(succeed=True).count()
        failed = Submission.objects.filter(finished=True, succeed=False).count()

        context = {
            "submissions": page_items,
            'processing': processing,
            'finished': finished,
            'succeed': succeed,
            'failed': failed

        }
        return render(request, 'submissions_history.html', context=context)


def setting_list(request):
    if request.method == 'POST':
        captcha_key = request.POST.get('captcha_key')
        settings = Settings.objects.first()
        settings.captcha_key = captcha_key
        settings.save()
        messages.success(request, 'Changes has been saved successfully!')
        return redirect('setting_list')
    else:
        settings = Settings.objects.first()
        context = {
            'settings': settings
        }
        return render(request, 'settings.html', context=context)
