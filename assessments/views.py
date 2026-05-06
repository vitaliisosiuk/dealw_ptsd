from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Assessment, TestResult, Choice, ResultInterpretation

def test_main_view(request):
    assessments = Assessment.objects.all()
    tests_data = []

    for assessment in assessments:
        tests_data.append({
            'url': reverse('assessments:about-test', kwargs={'test_slug': assessment.short_name}),
            'icon': assessment.icon,
            'alt': f'Іконка {assessment.short_name}',
            'title': assessment.title,
            'description': assessment.description
        })

    return render(request, "assessments/assessments_intro.html", context={'tests': tests_data})


def about_test(request, test_slug):
    assessment = get_object_or_404(Assessment, short_name=test_slug)

    context = {
        'assessment': assessment,
    }
    return render(request, "assessments/about_test.html", context)


def take_test(request, test_slug):
    assessment = get_object_or_404(Assessment, short_name=test_slug)
    questions = assessment.questions.all().order_by('order')

    if request.method == 'POST':
        total_score = 0
        scale_scores = {}
        all_answered = True

        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            if answer and answer.isdigit():
                val = int(answer)
                total_score += val

                if question.scale:
                    scale_scores[question.scale] = scale_scores.get(question.scale, 0) + val
            else:
                all_answered = False

        if not all_answered:
            messages.error(request, "Будь ласка, дайте відповідь на всі запитання.")
            return render(request, 'assessments/take_test.html', {
                'assessment': assessment,
                'questions': questions,
                'error_message': 'Ви пропустили деякі питання.'
            })

        if request.user.is_authenticated:
            TestResult.objects.create(
                user=request.user,
                assessment=assessment,
                total_score=total_score,
                scale_scores=scale_scores
            )

        request.session[f'test_score_{assessment.short_name}'] = total_score
        request.session[f'test_scale_scores_{assessment.short_name}'] = scale_scores
        return redirect('assessments:test-result', test_slug=assessment.short_name)

    context = {
        'assessment': assessment,
        'questions': questions
    }
    return render(request, 'assessments/take_test.html', context)


def test_result(request, test_slug):
    assessment = get_object_or_404(Assessment, short_name=test_slug)
    total_score = request.session.get(f'test_score_{assessment.short_name}')
    scale_scores = request.session.get(f'test_scale_scores_{assessment.short_name}', {})

    if total_score is None:
        return redirect('assessments:about-test', test_slug=assessment.short_name)

    has_scales = assessment.questions.exclude(scale='').exists()

    if has_scales and scale_scores:
        interpretations = []
        max_scores = {}

        for question in assessment.questions.prefetch_related('choices').all():
            if question.scale:
                choices = question.choices.all()
                if choices:
                    max_val = max(choice.value for choice in choices)
                    max_scores[question.scale] = max_scores.get(question.scale, 0) + max_val

        for scale_name, score in scale_scores.items():
            interp = assessment.interpretations.filter(
                scale=scale_name,
                min_score__lte=score,
                max_score__gte=score
            ).first()

            if interp:
                interp.actual_score = score
                interp.max_scale_score = max_scores.get(scale_name, 0)
                interpretations.append(interp)

        context = {
            'assessment': assessment,
            'is_multiscale': True,
            'interpretations': interpretations,
        }

    else:
        interpretation = assessment.interpretations.filter(
            min_score__lte=total_score,
            max_score__gte=total_score
        ).first()

        max_possible_score = 0
        for question in assessment.questions.prefetch_related('choices').all():
            choices = question.choices.all()
            if choices:
                max_possible_score += max(choice.value for choice in choices)

        context = {
            'assessment': assessment,
            'is_multiscale': False,
            'score': total_score,
            'max_score': max_possible_score,
            'interpretation': interpretation,
        }

    return render(request, 'assessments/test_result.html', context)