from django.db import models
from django.conf import settings

class Assessment(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва тесту")
    short_name = models.SlugField(max_length=50, unique=True, verbose_name="Коротка назва (для URL)")
    description = models.TextField(blank=True, verbose_name="Опис тесту (для списку)")
    instruction = models.TextField(blank=True, verbose_name="Інструкція перед проходженням")
    icon = models.CharField(
        max_length=100,
        default='assessments/images/anxiety.png',
        verbose_name="Шлях до іконки",
        help_text="assessments/images/depressed.png"
    )

    time_to_complete = models.CharField(max_length=50, blank=True, verbose_name="Час проходження")
    questions_count = models.PositiveIntegerField(default=0, verbose_name="Кількість питань")
    reliability = models.CharField(max_length=100, blank=True, verbose_name="Надійність")
    about_text = models.TextField(blank=True, verbose_name="Детальний опис (HTML)")

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тести"

    def __str__(self):
        return self.title

class Question(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions', verbose_name="Тест")
    text = models.CharField(max_length=500, verbose_name="Текст запитання")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядковий номер")
    scale = models.CharField(max_length=50, blank=True, verbose_name="Шкала/Субшкала")

    class Meta:
        ordering = ['order']
        verbose_name = "Запитання"
        verbose_name_plural = "Запитання"

    def __str__(self):
        return f"[{self.assessment.short_name}] {self.order}. {self.text}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name="Запитання")
    value = models.PositiveIntegerField(verbose_name="Кількість балів (0, 1, 2...)")
    text = models.CharField(max_length=200, verbose_name="Текст відповіді")

    class Meta:
        ordering = ['value']
        verbose_name = "Варіант відповіді"
        verbose_name_plural = "Варіанти відповідей"

    def __str__(self):
        return f"[{self.question.assessment.short_name}] {self.value} - {self.text}"

class ResultInterpretation(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='interpretations', verbose_name="Тест")
    min_score = models.PositiveIntegerField(verbose_name="Мінімальний бал")
    max_score = models.PositiveIntegerField(verbose_name="Максимальний бал")
    scale = models.CharField(max_length=50, blank=True, verbose_name="Шкала")

    result_title = models.CharField(max_length=200, verbose_name="Заголовок результату")
    result_text = models.TextField(verbose_name="Текст результату")
    recommendation = models.TextField(verbose_name="Рекомендація")

    is_high_risk = models.BooleanField(default=False, verbose_name="Високий ризик (червона іконка)")

    class Meta:
        ordering = ['min_score']
        verbose_name = "Інтерпретація результату"
        verbose_name_plural = "Інтерпретації результатів"

    def __str__(self):
        return f"[{self.assessment.short_name}] {self.min_score}-{self.max_score} балів: {self.result_title}"

class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_results', verbose_name="Користувач")
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='results', verbose_name="Тест")
    total_score = models.PositiveIntegerField(verbose_name="Загальний бал")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата проходження")
    scale_scores = models.JSONField(default=dict, blank=True, verbose_name="Бали по шкалах")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Результат тесту"
        verbose_name_plural = "Результати тестів"

    def __str__(self):
        return f"{self.user.email} - {self.assessment.short_name}: {self.total_score} ({self.created_at.strftime('%d.%m.%Y')})"