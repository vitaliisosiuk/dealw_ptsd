from assessments.models import Assessment, Question, Choice

def seed_ais():
    # Retrieve the AIS assessment
    ais_test = Assessment.objects.get(short_name='ais')

    # Clear existing questions to avoid duplicates
    ais_test.questions.all().delete()

    # AIS Questions and their specific options
    ais_data = [
        {
            "question": "Час засинання: Як швидко Ви засинаєте після того, як вимкнете світло?",
            "options": [
                "дуже швидко",
                "з невеликою затримкою",
                "з помітною затримкою",
                "з тривалою затримкою або не сплю взагалі"
            ]
        },
        {
            "question": "Пробудження вночі: Чи прокидаєтеся Ви протягом ночі?",
            "options": [
                "ні",
                "рідко",
                "доволі часто",
                "часто або взагалі не сплю"
            ]
        },
        {
            "question": "Остаточне пробудження раніше бажаного часу: Чи прокидаєтеся ви раніше, ніж хотіли б?",
            "options": [
                "ні",
                "дещо раніше",
                "істотно раніше",
                "набагато раніше або взагалі не сплю"
            ]
        },
        {
            "question": "Загальна тривалість сну: Як довго ви спите?",
            "options": [
                "достатня",
                "недостатня",
                "помітно недостатня",
                "дуже недостатня або не спав взагалі"
            ]
        },
        {
            "question": "Якість сну: Як ви оцінюєте якість свого сну?",
            "options": [
                "задовільна",
                "трохи незадовільна",
                "погана",
                "дуже погана або не спав узагалі"
            ]
        },
        {
            "question": "Самопочуття наступного дня: Як ви себе відчуваєте наступного дня?",
            "options": [
                "нормальний",
                "трохи знижений",
                "помітно знижений",
                "дуже знижений"
            ]
        },
        {
            "question": "Фізична та розумова працездатність наступного дня: Як ви оцінюєте свою працездатність наступного дня?",
            "options": [
                "нормальна",
                "трохи знижена",
                "помітно знижена",
                "дуже знижена"
            ]
        },
        {
            "question": "Денна сонливість: Чи відчуваєте ви сонливість протягом дня?",
            "options": [
                "ні",
                "мало виражена",
                "суттєво виражена",
                "дуже сильно виражена"
            ]
        }
    ]

    for i, item in enumerate(ais_data):
        q = Question.objects.create(
            assessment=ais_test,
            text=item["question"],
            order=i + 1
        )

        for val, opt_text in enumerate(item["options"]):
            Choice.objects.create(question=q, value=val, text=opt_text)

    print("Successfully created 8 AIS questions and their specific choices!")

if __name__ == "__main__":
    seed_ais()