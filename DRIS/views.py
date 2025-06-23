# DRIS/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import CustomUser, DisasterReport, AidRequest, Shelter, Volunteer, VolunteerAssignment
from .forms import (
    UserRegisterForm, UserUpdateForm, ProfileUpdateForm,
    DisasterReportForm, AidRequestForm, ShelterForm,
    VolunteerRegisterForm, VolunteerUpdateForm,
    DisasterReportFilterForm
)


def home(request):
    recent_reports = DisasterReport.objects.filter(is_resolved=False).order_by('-timestamp')[:5]
    shelters = Shelter.objects.all()[:5]
    context = {
        'recent_reports': recent_reports,
        'shelters': shelters,
        'latest_disaster': DisasterReport.objects.last()
    }
    return render(request, 'DRIS/home.html', context)


class DisasterReportListView(ListView):
    model = DisasterReport
    template_name = 'DRIS/disaster_reports.html'
    context_object_name = 'reports'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtering logic
        disaster_type = self.request.GET.get('disaster_type')
        severity = self.request.GET.get('severity')
        location = self.request.GET.get('location')

        if disaster_type:
            queryset = queryset.filter(disaster_type=disaster_type)
        if severity:
            queryset = queryset.filter(severity=severity)
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disaster_types'] = DisasterReport.DisasterType.choices
        context['severity_levels'] = DisasterReport.SeverityLevel.choices
        return context


class DisasterReportDetailView(DetailView):
    model = DisasterReport
    template_name = 'DRIS/report_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aid_requests'] = AidRequest.objects.filter(disaster=self.object)
        return context

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class DisasterReportCreateView(LoginRequiredMixin, CreateView):
    model = DisasterReport
    form_class = DisasterReportForm
    template_name = 'DRIS/report_form.html'
    success_url = reverse_lazy('disaster_reports')

    def form_valid(self, form):
        form.instance.reporter = self.request.user  # 自动关联当前用户
        return super().form_valid(form)

class DisasterReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DisasterReport
    form_class = DisasterReportForm
    template_name = 'DRIS/report_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your disaster report has been updated!')
        return super().form_valid(form)

    def test_func(self):
        report = self.get_object()
        return self.request.user == report.reporter or self.request.user.user_type == 'AT'

from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import AidRequest
from .forms import AidRequestForm
class AidRequestCreateView(LoginRequiredMixin, CreateView):
    model = AidRequest
    form_class = AidRequestForm
    template_name = 'DRIS/aid_request_form.html'
    success_url = reverse_lazy('disaster_reports')
    def get_initial(self):
        initial = super().get_initial()
        disaster_id = self.kwargs.get('disaster_id')
        if disaster_id:
            initial['disaster'] = get_object_or_404(DisasterReport, pk=self.kwargs['disaster_id'])
        return initial

    def form_valid(self, form):
        form.instance.requester = self.request.user
        messages.success(self.request, 'Your aid request has been submitted!')
        return super().form_valid(form)


# DRIS/views.py
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'DRIS/register.html', {'form': form})

from .models import Shelter

def shelter_list(request):
    shelters = Shelter.objects.all()
    return render(request, 'DRIS/shelters.html', {'shelters': shelters})
def register_volunteer(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        volunteer_form = VolunteerRegisterForm(request.POST)

        if user_form.is_valid() and volunteer_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'VL'
            user.save()

            volunteer = volunteer_form.save(commit=False)
            volunteer.user = user
            volunteer.save()

            login(request, user)
            messages.success(request, 'Volunteer account created successfully!')
            return redirect('home')
    else:
        user_form = UserRegisterForm()
        volunteer_form = VolunteerRegisterForm()

    context = {
        'user_form': user_form,
        'volunteer_form': volunteer_form,
    }
    return render(request, 'DRIS/volunteer_register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'DRIS/profile.html', context)


@login_required
def volunteer_dashboard(request):
    if request.user.user_type != 'VL':
        return redirect('home')

    volunteer = get_object_or_404(Volunteer, user=request.user)
    assignments = VolunteerAssignment.objects.filter(volunteer=volunteer)

    context = {
        'volunteer': volunteer,
        'assignments': assignments,
    }
    return render(request, 'DRIS/volunteer_dashboard.html', context)


@login_required
def admin_dashboard(request):
    if request.user.user_type != 'AT':
        return redirect('home')

    # Basic stats for admin dashboard
    total_reports = DisasterReport.objects.count()
    active_reports = DisasterReport.objects.filter(is_resolved=False).count()
    total_aid_requests = AidRequest.objects.count()
    pending_requests = AidRequest.objects.filter(is_fulfilled=False).count()
    total_volunteers = Volunteer.objects.count()
    available_volunteers = Volunteer.objects.filter(availability=True).count()

    context = {
        'total_reports': total_reports,
        'active_reports': active_reports,
        'total_aid_requests': total_aid_requests,
        'pending_requests': pending_requests,
        'total_volunteers': total_volunteers,
        'available_volunteers': available_volunteers,
    }
    return render(request, 'DRIS/admin_dashboard.html', context)