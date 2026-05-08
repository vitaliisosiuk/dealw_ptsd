from django.db import models
from django.conf import settings


class TriggerCategory(models.TextChoices):
    """Supported reaction categories for trigger mapping."""
    PHYSICAL = 'PHYSICAL', 'Physical Reactions'
    EMOTIONAL = 'EMOTIONAL', 'Emotional Reactions'
    THINKING = 'THINKING', 'Thinking Reactions'
    ACTION = 'ACTION', 'Action Reactions'

class Timeframe(models.TextChoices):
    """Time buckets used to classify reactions."""
    IMMEDIATE = 'IMMEDIATE', 'Immediate (First few minutes)'
    SHORT_TERM = 'SHORT_TERM', 'Short-Term (15 mins to few hours)'
    LONG_TERM = 'LONG_TERM', 'Long-Term (Hours to days)'


class TriggerOption(models.Model):
    """Trigger option that can be global or user-specific."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class ReactionOption(models.Model):
    """Reaction option grouped by category."""
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=TriggerCategory.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class ContextOption(models.Model):
    """Context option attached to trigger logs."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class TriggerLog(models.Model):
    """User trigger mapping record with selected contexts and reactions."""
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
    """Reaction selected for a trigger log and timeframe."""
    log = models.ForeignKey(TriggerLog, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.ForeignKey(ReactionOption, on_delete=models.CASCADE)
    timeframe = models.CharField(max_length=15, choices=Timeframe.choices)

    def __str__(self):
        return f"{self.reaction.name} - {self.get_timeframe_display()}"


class InspirationalQuote(models.Model):
    """Inspirational quote displayed in cards tool."""
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
    """Simple journal note written by a user."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="journal_entries")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_id} {self.created_at.strftime('%Y-%m-%d')}: {self.text[:40]}"


class GettingOutOfHouseCard(models.Model):
    """Stores a single 'Getting out of house' suggestion card."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.FileField(upload_to="tools/getting_out_of_house/", blank=True, null=True)
    image_url = models.URLField(blank=True)
    why_it_helps = models.TextField(
        blank=True,
        help_text="Optional detailed explanation shown in a modal.",
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        """Return a readable card title for admin and logs."""
        return self.title

    @property
    def display_image_url(self):
        """Return uploaded image URL first, then fallback URL."""
        if self.image:
            return self.image.url
        return self.image_url