from assessments.models import Assessment, Question, Choice

def seed_stai():
    # Retrieve the STAI assessment
    stai_test = Assessment.objects.get(short_name='stai')

    # Clear existing questions to avoid duplicates
    stai_test.questions.all().delete()

    # GROUP 1: STATE ANXIETY
    state_questions = [
        "Я спокійний", "Мені ніщо не загрожує", "Я перебуваю в напруженні",
        "Я внутрішньо скутий", "Я відчуваю себе вільно", "Я розчарований",
        "Мене хвилюють можливі невдачі", "Я відчуваю душевний спокій",
        "Я стурбований", "Я відчуваю внутрішнє задоволення", "Я впевнений у собі",
        "Я нервуюсь", "Я не знаходжу собі місця", "Я напружений",
        "Я не відчуваю скутості, напруження", "Я задоволений", "Я стурбований",
        "Я надто збуджений і мені не по собі", "Мені радісно", "Мені приємно"
    ]
    state_reverse = [1, 2, 5, 8, 10, 11, 15, 16, 19, 20]

    # GROUP 2: TRAIT ANXIETY
    trait_questions = [
        "У мене буває піднесений настрій", "Я буваю дратівливим",
        "Я легко впадаю в розпач", "Я хотів би бути таким же щасливим, як і інші",
        "Я тяжко переживаю неприємності та довго не можу про них забути",
        "Я відчуваю приплив сил і бажання працювати", "Я спокійний, врівноважений та зібраний",
        "Мене турбують можливі труднощі", "Я дуже переживаю через дрібниці",
        "Я буваю цілком щасливим", "Я все приймаю близько до серця",
        "Мені бракує впевненості в собі", "Я відчуваю себе беззахисним",
        "Намагаюся уникати критичних ситуацій та труднощів", "У мене буває хандра",
        "Я буваю задоволений", "Усілякі дрібниці відволікають і хвилюють мене",
        "Буває, що відчуваю себе невдахою", "Я врівноважена людина",
        "Іноді мене охоплює занепокоєння, коли я думаю про свої справи і турботи"
    ]
    trait_reverse = [1, 6, 7, 10, 16, 19]

    options_text = ["Ніколи", "Майже ніколи", "Часто", "Майже завжди"]

    def generate_stai(q_list, reverse_keys, scale_name, start_order):
        for i, text in enumerate(q_list):
            q_num = i + 1
            q = Question.objects.create(
                assessment=stai_test,
                text=text,
                order=start_order + i,
                scale=scale_name
            )

            is_reverse = q_num in reverse_keys

            for j, opt in enumerate(options_text):
                # Reverse scoring: 4, 3, 2, 1. Direct scoring: 1, 2, 3, 4
                val = (4 - j) if is_reverse else (j + 1)
                Choice.objects.create(question=q, value=val, text=opt)

    generate_stai(state_questions, state_reverse, 'state', 1)
    generate_stai(trait_questions, trait_reverse, 'trait', 21)

    print("Successfully created 40 STAI questions! Scales and reverse scoring applied.")

if __name__ == "__main__":
    seed_stai()