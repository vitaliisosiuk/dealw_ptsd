from django.contrib import admin
from .models import TriggerOption, ReactionOption, ContextOption, TriggerLog, LogReaction, InspirationalQuote, JournalEntry

@admin.register(TriggerOption)
class TriggerOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)

@admin.register(ReactionOption)
class ReactionOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'user')
    list_filter = ('category', 'user')
    search_fields = ('name',)

@admin.register(ContextOption)
class ContextOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)

class LogReactionInline(admin.TabularInline):
    model = LogReaction
    extra = 0

@admin.register(TriggerLog)
class TriggerLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'distress_level', 'created_at')
    list_filter = ('created_at', 'distress_level')
    search_fields = ('user__username', 'custom_trigger')
    inlines = [LogReactionInline]
    filter_horizontal = ('triggers', 'contexts')


@admin.register(InspirationalQuote)
class InspirationalQuoteAdmin(admin.ModelAdmin):
    list_display = ("author", "language", "is_active", "sort_order", "created_at")
    list_filter = ("language", "is_active")
    search_fields = ("author", "text")
    ordering = ("sort_order", "id")


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__email", "text")
    ordering = ("-created_at",)