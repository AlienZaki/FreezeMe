from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import reverse, redirect
from .models import Client, Website, Requirement, Submission, Settings
from state.models import State
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import *
from django.http import HttpResponse
from django.views import generic
from core.automation import task_manager, resubmit_task
import traceback


def test(request):
    res = 'sss'
    return HttpResponse(res)


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


class ClientListView(generic.ListView):
    model = Client
    template_name = 'clients_list.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        ssn = self.request.GET.get('q') or ''
        qs = super().get_queryset().filter(ssn__contains=ssn)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context


def add_client(request):
    if request.method == 'POST':
        form = clientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save()

            if 'auto_submit' in form.data:
                # send to automation task manager
                print('=> Auto Submit')
                task_manager(client=client)

            return redirect('client_list')
        else:
            states = State.objects.all()
            context = {
                'states': states,
                'form': form
            }
            return render(request, 'client_form.html', context=context)
    else:
        states = State.objects.all()
        #websites = Website.objects.filter(ready=True).all()
        context = {
            'states': states,
        }
        return render(request, 'client_form.html', context=context)


class UpdateClientView(generic.UpdateView):
    model = Client
    template_name = 'client_form.html'
    form_class = clientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        states = State.objects.all()
        context['states'] = states
        return context

    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #
    #     #success_message = 'Success! We just sent you an email to confirm'
    #     #messages.success(self.request, success_message)
    #     return super().form_valid(form)



def resubmit(request, pk):
    submission = Submission.objects.get(pk=pk)
    # resubmit
    resubmit_task(submission)
    return redirect('submission_list')



def submission_list(request):
    if request.method == 'POST':
        pass
    else:
        page_num = request.GET.get('page', default=1)

        submissions = Submission.objects.all().order_by('-timestamp')
        paginator = Paginator(submissions, per_page=20)
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
        return render(request, 'submissions_list.html', context=context)


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
