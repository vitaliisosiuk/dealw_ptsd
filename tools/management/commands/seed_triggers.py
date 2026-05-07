from django.core.management.base import BaseCommand
from tools.models import TriggerOption, ReactionOption, ContextOption, TriggerCategory

class Command(BaseCommand):
    help = 'Populates the database with sample options for trigger analysis'

    def handle(self, *args, **kwargs):
        triggers = [
            "Затори / Трафік", "Нічний кошмар", "Натовп", "Феєрверки / Вибухи", "Я насамоті",
            "Хтось має наді мною владу", "Я застряг(-ла) у черзі",
            "Я не можу заснути", "Річниця важливої події",
            "Сварка з близькою людиною", "Хтось підійшов надто близько",
            "Я сиджу спиною до дверей", "Мене проігнорували",
            "Фільм або телешоу стали тригером", "Новини або поточні події турбують мене",
            "Гучний звук", "Запах гару / диму", "Навколо надто галасливо",
            "Мене хтось налякав / змусив здригнутися", "Хтось спробував мене обійняти чи торкнутися"
        ]

        physical_reactions = [
            "Прискорене серцебиття", "Пітливість", "Запаморочення", "Задишка",
            "М'язова напруга", "Втома", "Провали в пам'яті",
            "Відчуття слабкості / Переднепритомний стан", "Дзвін у вухах",
            "Флешбеки (нав'язливі спогади)", "Виснаження",
            "Відчуття нереальності світу (дереалізація)", "Сплутаність думок / Важко думати"
        ]

        emotional_reactions = [
            "Безпорадність", "Жах", "Страх", "Паніка", "Гнів / Злість", "Сум", "Розчарування",
            "Тривога", "Огида", "Сором", "Зніяковілість", "Провина",
            "Перевантаженість емоціями", "Емоційне оніміння", "Відстороненість",
            "Я взагалі нічого не відчуваю"
        ]

        thinking_reactions = [
            "Зі мною щось не так", "Я в пастці / в глухому куті", "Це моя провина",
            "Я недостатньо хороша/-ий", "Я недостатньо сильна/-ий", "Я слабка/-ий",
            "Мене ніхто не любить", "Мені важко мислити раціонально",
            "Світ небезпечний", "Я собі не довіряю", "Я не довіряю людям",
            "Я зможу це подолати", "Я знаю, що я в безпеці, хоча мій розум каже інше"
        ]

        action_reactions = [
            "Втік(-ла) із ситуації якнайшвидше", "Відгородився(-лася) від усіх",
            "Уникав(-ла) когось або чогось", "Кричав(-ла)", "Плакав(-ла)",
            "Намагався(-лася) про це не думати", "Пішов(-ла) спати", "Зробив(-ла) щось нерозважливе",
            "Вживав(-ла) алкоголь або наркотики, щоб впоратися",
            "Вживання нікотину (куріння)", "Вживання кофеїну",
            "Заподіяв(-ла) собі фізичну шкоду (селфхарм)", "Заїдання стресу",
            "Практикував(-ла) глибоке дихання", "Зайнявся(-лася) хобі",
            "Фізичні вправи / Спорт", "Пішов(-ла) на прогулянку",
            "Зателефонував(-ла) близькій людині", "Робив(-ла) вправи на заземлення",
            "Зробив(-ла) щось приємне для себе"
        ]

        contexts = [
            "Зміна ліків", "Голод", "Втома", "Добре відпочив(-ла)", "Робота", "Стрес",
            "Вживання алкоголю або наркотиків", "Я був(-ла) насамоті",
            "Догляд за кимось", "Зустріч з друзями", "Час із сім'єю",
            "Пропуск прийому ліків", "Проблеми зі здоров'ям"
        ]

        self.stdout.write("Cleaning up old default entries...")
        TriggerOption.objects.filter(user__isnull=True).delete()
        ReactionOption.objects.filter(user__isnull=True).delete()
        ContextOption.objects.filter(user__isnull=True).delete()

        self.stdout.write("Creating triggers...")
        for t in triggers:
            TriggerOption.objects.create(name=t)

        self.stdout.write("Creating reactions...")
        for r in physical_reactions:
            ReactionOption.objects.create(name=r, category=TriggerCategory.PHYSICAL)
        for r in emotional_reactions:
            ReactionOption.objects.create(name=r, category=TriggerCategory.EMOTIONAL)
        for r in thinking_reactions:
            ReactionOption.objects.create(name=r, category=TriggerCategory.THINKING)
        for r in action_reactions:
            ReactionOption.objects.create(name=r, category=TriggerCategory.ACTION)

        self.stdout.write("Creating contexts...")
        for c in contexts:
            ContextOption.objects.create(name=c)

        self.stdout.write(self.style.SUCCESS('Успішно завантажено всі питання та відповіді у БД (українською мовою)!'))