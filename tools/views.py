from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (
    TriggerOption,
    ReactionOption,
    ContextOption,
    TriggerLog,
    LogReaction,
    Timeframe,
    TriggerCategory,
    InspirationalQuote,
    JournalEntry,
)

# Create your views here.

def tools_home_view(request):
    return render(request, "tools/tools_home.html")

def triggers_view(request):
    return render(request, "tools/triggers.html")

@login_required
def trigger_mapping_view(request):
    if request.method == 'POST':
        distress_level = request.POST.get('distress_level', 0)
        log = TriggerLog.objects.create(
            user=request.user,
            distress_level=distress_level,
            custom_trigger=request.POST.get('custom_trigger', ''),
            custom_context=request.POST.get('custom_context', '')
        )

        log.triggers.add(*request.POST.getlist('triggers'))
        log.contexts.add(*request.POST.getlist('contexts'))

        timeframes = [
            (Timeframe.IMMEDIATE, 'immediate_reactions'),
            (Timeframe.SHORT_TERM, 'short_reactions'),
            (Timeframe.LONG_TERM, 'long_reactions')
        ]

        for time_val, post_key in timeframes:
            reaction_ids = request.POST.getlist(post_key)
            for r_id in reaction_ids:
                LogReaction.objects.create(log=log, reaction_id=r_id, timeframe=time_val)

        return redirect('tools:trigger_summary', log_id=log.id)

    context = {
        'triggers': TriggerOption.objects.filter(user__isnull=True) | TriggerOption.objects.filter(user=request.user),
        'contexts': ContextOption.objects.filter(user__isnull=True) | ContextOption.objects.filter(user=request.user),

        'physical_reactions': ReactionOption.objects.filter(category=TriggerCategory.PHYSICAL),
        'emotional_reactions': ReactionOption.objects.filter(category=TriggerCategory.EMOTIONAL),
        'thinking_reactions': ReactionOption.objects.filter(category=TriggerCategory.THINKING),
        'action_reactions': ReactionOption.objects.filter(category=TriggerCategory.ACTION),
    }
    return render(request, 'tools/trigger_form.html', context)

@login_required
def trigger_summary_view(request, log_id):
    log = get_object_or_404(TriggerLog, id=log_id, user=request.user)

    context = {
        'log': log,
        'immediate_reactions': log.reactions.filter(timeframe=Timeframe.IMMEDIATE).select_related('reaction'),
        'short_term_reactions': log.reactions.filter(timeframe=Timeframe.SHORT_TERM).select_related('reaction'),
        'long_term_reactions': log.reactions.filter(timeframe=Timeframe.LONG_TERM).select_related('reaction'),
    }
    return render(request, 'tools/trigger_summary.html', context)


def inspirational_cards_info_view(request):
    return render(request, "tools/inspirational_cards_info.html")


def inspirational_cards_view(request):
    quotes_qs = InspirationalQuote.objects.filter(is_active=True, language="uk").order_by("sort_order", "id")
    quotes = [{"author": q.author, "text": q.text} for q in quotes_qs]

    if not quotes:
        quotes = [
            {
                "author": "Елен Келлер",
                "text": "Хоча світ сповнений страждань, він також сповнений подолання їх.",
            }
        ]

    return render(request, "tools/inspirational_cards.html", {"quotes": quotes})


def express_with_art_view(request):
    return render(request, "tools/express_with_art.html")


def meditation_view(request):
    return render(request, "tools/meditation.html")


@login_required
def journal_view(request):
    if request.method == "POST":
        text = (request.POST.get("text") or "").strip()
        if text:
            JournalEntry.objects.create(user=request.user, text=text)
        return redirect("accounts:profile")

    return render(request, "tools/journal.html")