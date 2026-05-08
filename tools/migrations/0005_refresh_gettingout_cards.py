from django.db import migrations


CARDS = [
    ("Прогулянка біля дому", "Вийдіть на 10-15 хвилин і пройдіться знайомим маршрутом.", "https://loremflickr.com/900/1200/walk,street?lock=11"),
    ("Парк поруч", "Завітайте в найближчий парк і звертайте увагу на деталі навколо.", "https://loremflickr.com/900/1200/park,trees?lock=12"),
    ("Кава на свіжому повітрі", "Візьміть напій з собою і посидьте кілька хвилин надворі.", "https://loremflickr.com/900/1200/coffee,outdoor?lock=13"),
    ("Прогулянка з улюбленцем", "Якщо є можливість, прогуляйтеся з собакою у спокійному темпі.", "https://loremflickr.com/900/1200/dog,walk?lock=14"),
    ("Нова вулиця", "Оберіть вулицю, якою давно не ходили, і дослідіть її.", "https://loremflickr.com/900/1200/city,street?lock=15"),
    ("Сонячна пауза", "Проведіть кілька хвилин на сонці, роблячи повільні вдихи.", "https://loremflickr.com/900/1200/sunlight,outdoor?lock=16"),
    ("Невеликий похід у магазин", "Купіть одну корисну дрібницю для себе або дому.", "https://loremflickr.com/900/1200/shop,city?lock=17"),
    ("Маршрут із музикою", "Увімкніть спокійний плейлист і пройдіть короткий маршрут.", "https://loremflickr.com/900/1200/headphones,walk?lock=18"),
    ("Книга на лавці", "Почитайте 10 хвилин у сквері або на лавці біля дому.", "https://loremflickr.com/900/1200/book,bench?lock=19"),
    ("Фото-прогулянка", "Зробіть кілька фото приємних моментів під час виходу.", "https://loremflickr.com/900/1200/camera,street?lock=20"),
    ("Прогулянка біля води", "Якщо поряд є водойма, проведіть там трохи часу.", "https://loremflickr.com/900/1200/lake,walk?lock=21"),
    ("Маленька мандрівка містом", "Проїдьте кілька зупинок і прогуляйтеся новим місцем.", "https://loremflickr.com/900/1200/bus,city?lock=22"),
    ("Відвідати музей", "Оберіть невеликий музей або виставку у вашому місті.", "https://loremflickr.com/900/1200/museum,city?lock=23"),
    ("Місце з видом", "Знайдіть точку з гарним видом і побудьте там декілька хвилин.", "https://loremflickr.com/900/1200/viewpoint,city?lock=24"),
    ("Зустріч у русі", "Запропонуйте знайомому коротку прогулянку замість сидіння вдома.", "https://loremflickr.com/900/1200/friends,walk?lock=25"),
    ("Похід у бібліотеку", "Завітаєте в бібліотеку та оберіть одну цікаву книгу.", "https://loremflickr.com/900/1200/library,books?lock=26"),
    ("Сніданок поза домом", "Поснідайте в затишному місці неподалік.", "https://loremflickr.com/900/1200/breakfast,cafe?lock=27"),
    ("Обід у місті", "Спробуйте пообідати у новому місці в комфортному темпі.", "https://loremflickr.com/900/1200/lunch,restaurant?lock=28"),
    ("Вечірня прогулянка", "Вийдіть увечері на 10 хвилин, щоб змінити обстановку.", "https://loremflickr.com/900/1200/evening,walk?lock=29"),
    ("Ранковий старт", "Почніть день з короткого виходу надвір.", "https://loremflickr.com/900/1200/morning,street?lock=30"),
    ("Купити квіти", "Подаруйте собі маленький букет або рослину.", "https://loremflickr.com/900/1200/flowers,shop?lock=31"),
    ("Міні-екскурсія", "Огляньте знайомі місця так, ніби ви турист у своєму місті.", "https://loremflickr.com/900/1200/tourism,city?lock=32"),
    ("Маршрут вдячності", "Під час прогулянки знайдіть 5 речей, за які вдячні.", "https://loremflickr.com/900/1200/sky,street?lock=33"),
    ("Крок за кроком", "Складіть простий маршрут: одна точка туди і назад.", "https://loremflickr.com/900/1200/road,walk?lock=34"),
    ("Пауза в сквері", "Сядьте в тихому місці і кілька хвилин спостерігайте за навколишнім.", "https://loremflickr.com/900/1200/garden,bench?lock=35"),
    ("Добра справа", "Підтримайте когось добрим словом або маленькою допомогою.", "https://loremflickr.com/900/1200/help,people?lock=36"),
    ("Крок у рутину", "Зробіть одну звичну справу поза домом у своєму темпі.", "https://loremflickr.com/900/1200/routine,city?lock=37"),
    ("Прогулянка з диханням", "Синхронізуйте кроки з диханням: 4 кроки вдих, 4 кроки видих.", "https://loremflickr.com/900/1200/walking,path?lock=38"),
    ("Тиха локація", "Оберіть менш людне місце для комфортного виходу.", "https://loremflickr.com/900/1200/quiet,street?lock=39"),
    ("Відзначте прогрес", "Після повернення запишіть, що саме вам вдалося сьогодні.", "https://loremflickr.com/900/1200/notebook,outdoor?lock=40"),
]

WHY_IT_HELPS = (
    "• Відволікання: приємна активність допомагає переключити увагу з тривожних думок.\n"
    "• Зниження стресу: зміна обстановки та рух підтримують заспокоєння.\n"
    "• Покращення настрою: навіть короткий вихід може підвищити рівень енергії.\n"
    "• Відчуття досягнення: маленькі кроки повертають відчуття контролю.\n"
    "• Соціальний контакт: взаємодія з людьми зменшує відчуття ізоляції."
)


def refresh_cards(apps, schema_editor):
    """Refresh seeded getting-out-of-house cards with stable image links."""
    GettingOutOfHouseCard = apps.get_model("tools", "GettingOutOfHouseCard")
    existing = list(GettingOutOfHouseCard.objects.order_by("id"))

    for idx, (title, description, image_url) in enumerate(CARDS, start=1):
        if idx <= len(existing):
            card = existing[idx - 1]
            card.title = title
            card.description = description
            card.image = None
            card.image_url = image_url
            card.why_it_helps = WHY_IT_HELPS
            card.sort_order = idx
            card.is_active = True
            card.save(
                update_fields=[
                    "title",
                    "description",
                    "image",
                    "image_url",
                    "why_it_helps",
                    "sort_order",
                    "is_active",
                ]
            )
        else:
            GettingOutOfHouseCard.objects.create(
                title=title,
                description=description,
                image_url=image_url,
                why_it_helps=WHY_IT_HELPS,
                sort_order=idx,
                is_active=True,
            )

    if len(existing) > len(CARDS):
        for card in existing[len(CARDS):]:
            card.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tools", "0004_gettingoutofhousecard"),
    ]

    operations = [
        migrations.RunPython(refresh_cards, migrations.RunPython.noop),
    ]
