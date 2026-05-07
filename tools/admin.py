from django.contrib import admin
from .models import TriggerOption, ReactionOption, ContextOption, TriggerLog, LogReaction

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

# Це дозволить бачити реакції прямо всередині запису логу
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