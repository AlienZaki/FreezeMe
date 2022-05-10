from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import generic
from django.shortcuts import reverse
from .models import Client, Website, Requirement, Settings, Submission
from .forms import submissionForm, settingsForm, clientForm
#from .tasks import scrape_async


class ClientsItemListView(generic.ListView):
    template_name = 'clients_list.html'

    def get_queryset(self):     # returns page_obj
        qs = Client.objects.all()
        q = self.request.GET.get('q', None)
        if q:
            qs = qs.filter(ssn__contains=q)

        return qs   #.order_by("-publish_date")

    def get_context_data(self, **kwargs):
        context = super(ClientsItemListView, self).get_context_data(**kwargs)

        total_count = Client.objects.all().count()
        context.update({
            'total_count': total_count,
        })
        return context


class SubmissionsRecordListView(generic.FormView):
    template_name = 'submissions_history.html'
    form_class = submissionForm

    def get_success_url(self):
        return reverse("submissions-history")

    def form_valid(self, form):
        #scrape_async.delay()
        return super(SubmissionsRecordListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SubmissionsRecordListView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        qs = Submission.objects.all().order_by('-timestamp')
        paginator = Paginator(qs, 20)
        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)

        total_count = Submission.objects.all().count()
        processing = Submission.objects.filter(finished=False).count()
        finished = Submission.objects.filter(finished=True).count()
        succeed = Submission.objects.filter(succeed=True).count()
        failed = Submission.objects.filter(finished=True, succeed=False).count()
        context.update({
            "object_list": qs,
            'total_count': total_count,
            'processing': processing,
            'finished': finished,
            'succeed': succeed,
            'failed': failed
        })
        return context


class SettingsListView(generic.FormView):
    template_name = 'settings.html'
    form_class = settingsForm


class ClientsListView(generic.FormView):
    template_name = 'new-client-form.html'
    form_class = clientForm