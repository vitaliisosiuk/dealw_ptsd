from django.db import models
from django.conf import settings

class TriggerCategory(models.TextChoices):
    PHYSICAL = 'PHYSICAL', 'Physical Reactions'
    EMOTIONAL = 'EMOTIONAL', 'Emotional Reactions'
    THINKING = 'THINKING', 'Thinking Reactions'
    ACTION = 'ACTION', 'Action Reactions'

class Timeframe(models.TextChoices):
    IMMEDIATE = 'IMMEDIATE', 'Immediate (First few minutes)'
    SHORT_TERM = 'SHORT_TERM', 'Short-Term (15 mins to few hours)'
    LONG_TERM = 'LONG_TERM', 'Long-Term (Hours to days)'


class TriggerOption(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class ReactionOption(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=TriggerCategory.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class ContextOption(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class TriggerLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trigger_logs')
    created_at = models.DateTimeField(auto_now_add=True)

    triggers = models.ManyToManyField(TriggerOption, blank=True)
    custom_trigger = models.CharField(max_length=255, blank=True, help_text="Якщо користувач ввів свій варіант")

    distress_level = models.PositiveIntegerField(default=0)

    contexts = models.ManyToManyField(ContextOption, blank=True)
    custom_context = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Log by {self.user} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class LogReaction(models.Model):
    log = models.ForeignKey(TriggerLog, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.ForeignKey(ReactionOption, on_delete=models.CASCADE)
    timeframe = models.CharField(max_length=15, choices=Timeframe.choices)

    def __str__(self):
        return f"{self.reaction.name} - {self.get_timeframe_display()}"


class InspirationalQuote(models.Model):
    author = models.CharField(max_length=255)
    text = models.TextField()
    language = models.CharField(max_length=10, default="uk")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.author}: {self.text[:60]}"


class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="journal_entries")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_id} {self.created_at.strftime('%Y-%m-%d')}: {self.text[:40]}"