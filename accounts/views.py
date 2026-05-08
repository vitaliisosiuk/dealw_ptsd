from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from tools.models import TriggerLog, JournalEntry
from assessments.models import TestResult


def register(request):
    """Handle user registration and immediate login."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Authenticate a user and redirect to profile on success."""
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:profile')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Log out the current user and redirect to login."""
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request):
    """Render the main profile dashboard tab."""
    return render(request, 'accounts/profile.html', {'user': request.user, 'active_tab': 'profile'})


@login_required
def profile_journal_view(request):
    """Render journal entries sorted by query parameter."""
    sort = request.GET.get('sort', 'newest')
    ordering = ('-created_at', '-id') if sort != 'oldest' else ('created_at', 'id')
    journal_entries = JournalEntry.objects.filter(user=request.user).order_by(*ordering)
    return render(
        request,
        'accounts/profile_journal.html',
        {
            'user': request.user,
            'active_tab': 'journal',
            'entries': journal_entries,
            'selected_sort': sort,
        },
    )


@login_required
def profile_triggers_view(request):
    """Render trigger logs sorted by date or distress."""
    sort = request.GET.get('sort', 'newest')
    ordering_map = {
        'newest': ('-created_at', '-id'),
        'oldest': ('created_at', 'id'),
        'highest': ('-distress_level', '-created_at', '-id'),
        'lowest': ('distress_level', '-created_at', '-id'),
    }
    trigger_logs = TriggerLog.objects.filter(user=request.user).order_by(*ordering_map.get(sort, ('-created_at', '-id')))
    return render(
        request,
        'accounts/profile_triggers.html',
        {
            'user': request.user,
            'active_tab': 'triggers',
            'trigger_logs': trigger_logs,
            'selected_sort': sort,
        },
    )


@login_required
def profile_tests_view(request):
    """Render test history sorted by date or score."""
    sort = request.GET.get('sort', 'newest')
    ordering_map = {
        'newest': ('-created_at', '-id'),
        'oldest': ('created_at', 'id'),
        'highest': ('-total_score', '-created_at', '-id'),
        'lowest': ('total_score', '-created_at', '-id'),
    }
    test_results = (
        TestResult.objects.filter(user=request.user)
        .select_related("assessment")
        .order_by(*ordering_map.get(sort, ('-created_at', '-id')))
    )
    return render(
        request,
        'accounts/profile_tests.html',
        {
            'user': request.user,
            'active_tab': 'tests',
            'test_results': test_results,
            'selected_sort': sort,
        },
    )


@login_required
def account_details(request):
    """Render account details partial for HTMX requests."""
    return render(request, 'accounts/partials/account_details.html', {'user': request.user})


@login_required
def edit_account_details(request):
    """Render account details edit form partial."""
    form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'accounts/partials/edit_account_details.html', {'user': request.user, 'form': form})


@login_required
def update_account_details(request):
    """Handle account detail updates and return corresponding partial."""
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/partials/account_details.html', {'user': request.user})
        else:
            return render(request, 'accounts/partials/edit_account_details.html', {'user': request.user, 'form': form})

    return render(request, 'accounts/partials/account_details.html', {'user': request.user})