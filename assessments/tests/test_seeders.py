import pytest
from assessments.models import Assessment, Choice
from assessments.management.commands.seed_stai import seed_stai
from assessments.management.commands.seed_pcl5 import seed_pcl5
from assessments.management.commands.seed_sorensen import seed_sorensen
from assessments.management.commands.seed_ais import seed_ais
from assessments.management.commands.seed_bdi import seed_bdi

@pytest.mark.django_db
def test_seed_stai_creates_correct_data():
    Assessment.objects.create(short_name='stai')

    seed_stai()

    stai_test = Assessment.objects.get(short_name='stai')

    assert stai_test.questions.count() == 40
    assert Choice.objects.filter(question__assessment=stai_test).count() == 160

    state_questions = stai_test.questions.filter(scale='state')
    assert state_questions.count() == 20

    q1 = stai_test.questions.get(order=1)
    assert q1.choices.get(text="Ніколи").value == 4
    assert q1.choices.get(text="Майже завжди").value == 1

    q3 = stai_test.questions.get(order=3)
    assert q3.choices.get(text="Ніколи").value == 1

@pytest.mark.django_db
def test_seed_pcl5_creates_correct_data():
    Assessment.objects.create(short_name='pcl5')

    seed_pcl5()
    pcl5_test = Assessment.objects.get(short_name='pcl5')

    # 20 questions
    assert pcl5_test.questions.count() == 20

    # 5 options to answer
    assert Choice.objects.filter(question__assessment=pcl5_test).count() == 100

    # Checking logic
    q1 = pcl5_test.questions.get(order=1)

    assert q1.choices.get(text="Зовсім ні").value == 0
    assert q1.choices.get(text="Трохи").value == 1
    assert q1.choices.get(text="Помірно").value == 2
    assert q1.choices.get(text="Досить сильно").value == 3
    assert q1.choices.get(text="Дуже сильно").value == 4

@pytest.mark.django_db
def test_seed_sorensen_creates_correct_data():
    Assessment.objects.create(short_name='sorensen')
    seed_sorensen()

    sorensen_test = Assessment.objects.get(short_name='sorensen')

    assert sorensen_test.questions.count() == 50
    # 50 questions * 2 options
    assert Choice.objects.filter(question__assessment=sorensen_test).count() == 100

    q1 = sorensen_test.questions.get(order=1)
    assert q1.choices.get(text="так").value == 1
    assert q1.choices.get(text="ні").value == 0

@pytest.mark.django_db
def test_seed_ais_creates_correct_data():
    Assessment.objects.create(short_name='ais')
    seed_ais()

    ais_test = Assessment.objects.get(short_name='ais')

    assert ais_test.questions.count() == 8
    # 8 questions * 4 options
    assert Choice.objects.filter(question__assessment=ais_test).count() == 32

    q1 = ais_test.questions.get(order=1)
    assert q1.choices.get(value=0).text == "дуже швидко"
    assert q1.choices.get(value=3).text == "з тривалою затримкою або не сплю взагалі"

@pytest.mark.django_db
def test_seed_bdi_creates_correct_data():
    Assessment.objects.create(short_name='bdi')
    seed_bdi()

    bdi_test = Assessment.objects.get(short_name='bdi')

    assert bdi_test.questions.count() == 21
    # 21 questions * 4 options
    assert Choice.objects.filter(question__assessment=bdi_test).count() == 84

    # The first option is also the question text
    q1 = bdi_test.questions.get(order=1)
    assert q1.text == "Мені не сумно."
    assert q1.choices.get(value=0).text == "Мені не сумно."
    assert q1.choices.get(value=3).text == "Я відчуваю нестерпний сум та тугу."