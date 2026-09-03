#!/usr/bin/env python3
"""Собирает статический сайт из шаблона + контента страниц.

Запуск:  python3 build.py
Правки:  контент страниц ниже в PAGES, общая обвязка в SHELL.
"""
import pathlib
import re

import os
STAGING = os.environ.get("STAGING") == "1"
SITE = ("https://maximer111.github.io/nadia-photo"
        if STAGING else "https://nadiaphoto.mensreactivation.com")
ROOT = pathlib.Path(__file__).parent

NAV = [
    ("/sessions.html", "Фотосессии"),
    ("/presets.html", "Пресеты"),
    ("/workshop.html", "Воркшоп 1:1"),
    ("/schedule.html", "Расписание"),
]

EMAIL = ""  # почты пока нет, связь через Instagram и телефон
INSTAGRAM = "https://www.instagram.com/nadi_loban/"
PHONE = "+380676903262"
PHONE_HREF = "+380676903262"
BRAND = "Nadiia Loban Photography"

SHELL = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{url}">
<meta name="robots" content="index, follow, max-image-preview:large">

<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="Nadiia Loban Photography">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{url}">
<meta property="og:image" content="{site}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%231A1917'/%3E%3Ctext x='16' y='23' font-family='Georgia,serif' font-size='20' fill='%23F7F5F1' text-anchor='middle'%3E%D0%9D%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="/css/style.css">
{schema}
</head>
<body>
<a class="skip" href="#main">К содержимому</a>

<header class="site-head{headclass}">
  <a class="brand" href="/">Nadiia Loban<small>Photography · Budapest</small></a>
  <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Меню">
    <span></span><span></span>
  </button>
  <nav class="nav" id="nav" aria-label="Основная навигация">
    <ul>{nav}</ul>
  </nav>
</header>

<main id="main">
{body}
</main>

<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <p class="label">Nadiia Loban Photography</p>
        <p class="lede" style="font-size:var(--step-1);max-width:24ch">Individual. Couple.<br>Family. Event.</p>
      </div>
      <div>
        <p class="label">Разделы</p>
        <ul>{footnav}</ul>
      </div>
      <div>
        <p class="label">Связь</p>
        <ul>
          <li><a href="tel:{phone_href}">{phone}</a></li>
          <li><a href="{ig}" rel="me noopener" target="_blank">Instagram &mdash; @nadi_loban</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 Nadiia Loban Photography. Все фотографии защищены авторским правом.</span>
      <span><a href="/terms.html">Условия</a> &nbsp;·&nbsp; <a href="/policy.html">Конфиденциальность</a></span>
    </div>
  </div>
</footer>

<script src="/js/main.js" defer></script>
</body>
</html>
"""


def ld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % obj


# --------------------------------------------------------------------------
# Контент страниц
# --------------------------------------------------------------------------

HOME_BODY = """
  <section class="intro">
    <div class="wrap narrow">
      <h1 class="display intro__title">Photography in Budapest</h1>
      <p class="intro__line">We will never be so young again!<br>Save the moment!</p>
    </div>
  </section>

  <figure class="portrait">
    <img src="img/nadia-hero-1400.jpg"
         srcset="img/nadia-hero-800.jpg 800w, img/nadia-hero-1400.jpg 1400w"
         sizes="(max-width: 760px) 92vw, 720px"
         width="1400" height="2100" fetchpriority="high"
         alt="Чёрно-белый портрет: девушка в клетчатой рубашке на контровом закатном свете, волосы развевает ветер">
  </figure>

  <section class="contacts">
    <div class="wrap narrow">
      <p class="contacts__name display rv">Nadiia Loban Photography</p>
      <p class="contacts__lines rv">
        <a href="tel:+380676903262">+380&nbsp;67&nbsp;690&nbsp;32&nbsp;62</a>
        <a href="__CONTACT__" rel="me noopener" target="_blank">@nadi_loban</a>
      </p>
      <p class="label contacts__services rv">Individual. Couple. Family. Event</p>
      <hr class="rule rv" style="margin:3.5rem 0">
      <p class="contacts__tagline display rv">I create cinematic portraits for those who want to remember themselves alive</p>
    </div>
  </section>

  <section class="band" style="padding-top:0" aria-labelledby="portfolio-h">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:3rem">01 &mdash; Портфолио</p>
      <h2 id="portfolio-h" style="position:absolute;left:-9999px">Портфолио</h2>
      <div class="duo" style="margin-bottom:var(--band)">
        <figure class="plate plate--r34 ph rv" data-ph="Фото 3:4"></figure>
        <figure class="plate plate--r23 ph rv" data-ph="Фото 2:3"></figure>
      </div>
      <div class="trio" style="margin-bottom:var(--band)">
        <figure class="plate plate--r23 ph rv" data-ph="Фото 2:3"></figure>
        <figure class="plate plate--r43 ph rv" data-ph="Фото 4:3"></figure>
        <figure class="plate plate--r34 ph rv" data-ph="Фото 3:4"></figure>
      </div>
    </div>
    <figure class="plate plate--r169 ph bleed rv" data-ph="Фото во всю ширину"></figure>
  </section>

  <section class="band" style="padding-top:0" aria-labelledby="work-h">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:3rem">02 &mdash; Чем я занимаюсь</p>
      <h2 id="work-h" class="display rv" style="font-size:var(--step-2);max-width:18ch;margin-bottom:4rem">
        Съёмки, обучение и мои <em style="font-style:italic">пресеты</em>
      </h2>
      <div class="offers">
        <a class="offer rv" href="sessions.html">
          <div class="offer__name"><span>Съёмка</span>Фотосессии</div>
          <p class="offer__desc">Individual. Couple. Family. Event. Будапешт и выезды по Европе.</p>
          <div class="offer__price">от 000&nbsp;€</div>
        </a>
        <a class="offer rv" href="presets.html">
          <div class="offer__name"><span>Обработка</span>Авторские пресеты</div>
          <p class="offer__desc">Наборы для Lightroom Classic, которыми я обрабатываю собственные съёмки.</p>
          <div class="offer__price">от 00&nbsp;€</div>
        </a>
        <a class="offer rv" href="workshop.html">
          <div class="offer__name"><span>Обучение</span>Воркшоп 1:1</div>
          <p class="offer__desc">Полный день вдвоём: теория, съёмка живой пары, отбор и обработка.</p>
          <div class="offer__price">от 0&nbsp;000&nbsp;€</div>
        </a>
        <a class="offer rv" href="schedule.html">
          <div class="offer__name"><span>Группы</span>Расписание воркшопов</div>
          <p class="offer__desc">Двухдневные групповые воркшопы в европейских городах.</p>
          <div class="offer__price">2026</div>
        </a>
      </div>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Save the moment</h2>
      <p class="rv">Напишите в Instagram или позвоните &mdash; расскажу про свободные даты.</p>
      <a class="btn rv" href="__CONTACT__" rel="noopener" target="_blank"><span>Написать в Instagram</span></a>
    </div>
  </section>
"""

SESSIONS_BODY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label rv">Съёмка</span>
      <h1 class="display rv">Фотосессии<em> в Будапеште</em></h1>
      <p class="lede rv">Два часа, кофе, разговор и камера, о которой вы забудете через десять минут.</p>
    </div>
  </section>

  <figure class="plate plate--r169 ph bleed rv" data-ph="Фото во всю ширину"></figure>

  <section class="band">
    <div class="wrap split">
      <div class="split__media">
        <figure class="plate plate--r34 ph rv" data-ph="Фото 3:4"></figure>
      </div>
      <div class="split__body prose rv">
        <h2>Как это проходит</h2>
        <p>Мы начинаем не со съёмки, а с кофе. Пятнадцать минут разговора делают
          для кадра больше, чем час поз. Когда вы перестаёте следить за камерой,
          начинается то, ради чего я работаю.</p>
        <p>Я не ставлю вас в позы. Я даю простые действия и снимаю то, что
          происходит между ними, — паузы, переглядывания, движение.</p>

        <h2>Что входит</h2>
        <ul>
          <li>Около двух часов съёмки</li>
          <li>Рекомендации по одежде и локации заранее</li>
          <li>150+ обработанных фотографий</li>
          <li>Готово в течение ЧИСЛО недель после съёмки</li>
        </ul>
        <p style="color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
          Ретушь кожи не делаю — это осознанное решение, а не экономия времени.</p>
      </div>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap">
      <div class="trio">
        <figure class="plate plate--r23 ph rv" data-ph="Фото 2:3"></figure>
        <figure class="plate plate--r43 ph rv" data-ph="Фото 4:3"></figure>
        <figure class="plate plate--r34 ph rv" data-ph="Фото 3:4"></figure>
      </div>
    </div>
  </section>

  <section class="band" style="background:var(--paper-deep)">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:3rem">Стоимость</p>
      <div class="offers">
        <div class="offer rv">
          <div class="offer__name"><span>Будапешт</span>Съёмка в городе</div>
          <p class="offer__desc">Пара или семья. Локацию подбираем вместе: Дунай, Буда, дворы Пешта, купальни.</p>
          <div class="offer__price">000&nbsp;€</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Европа</span>Выездная съёмка</div>
          <p class="offer__desc">Вена, Прага, Париж, Лиссабон и далее. Гонорар и дорога считаются под конкретный город.</p>
          <div class="offer__price">по запросу</div>
        </div>
      </div>
      <p style="margin-top:2rem;color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
        Цены указаны без НДС. Дата бронируется предоплатой.</p>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Свободные даты уточняйте письмом</h2>
      <p class="rv">Напишите, когда вы в Будапеште, — отвечу, свободна ли дата, и пришлю всё остальное.</p>
      <a class="btn rv" href="__CONTACT__"><span>Проверить дату</span></a>
    </div>
  </section>
"""

PRESETS_BODY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label rv">Обработка</span>
      <h1 class="display rv">Мои <em>пресеты</em></h1>
      <p class="lede rv">Те же наборы, которыми я обрабатываю собственные съёмки. Lightroom Classic.</p>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap split split--flip">
      <div class="split__media">
        <figure class="plate plate--r43 ph rv" data-ph="До / после"></figure>
      </div>
      <div class="split__body prose rv">
        <h2>Зачем они вам</h2>
        <p>Снимать я люблю, но обработка для меня — не рутина, а вторая половина
          кадра. Пресеты не сделают за вас свет, но дадут отправную точку и
          сэкономят те часы, которые уходят на подгон цвета вручную.</p>
        <p>Все наборы совместимы с Adobe Lightroom Classic. После оплаты файл
          приходит на почту сразу.</p>
      </div>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:3rem">Наборы</p>
      <div class="offers">
        <div class="offer rv">
          <div class="offer__name"><span>Новое</span>Название набора &mdash; 00 цветных пресетов</div>
          <p class="offer__desc">Короткое описание набора: под какой свет, какая плёночная база, для каких съёмок подходит.</p>
          <div class="offer__price">00&nbsp;€</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Классика</span>Название набора &mdash; первый пак</div>
          <p class="offer__desc">Короткое описание: сколько цветных, сколько чёрно-белых, чем отличается от нового.</p>
          <div class="offer__price">00&nbsp;€</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Чёрно-белое</span>Название набора &mdash; ч/б пресеты</div>
          <p class="offer__desc">Короткое описание: контраст, зерно, для каких сюжетов.</p>
          <div class="offer__price">00&nbsp;€</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Всё сразу</span>Полный пак</div>
          <p class="offer__desc">Все наборы одним файлом, включая будущие обновления. Выгоднее, чем покупать по отдельности.</p>
          <div class="offer__price">000&nbsp;€</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Проба</span>Тестовый набор</div>
          <p class="offer__desc">Один цветной и один чёрно-белый пресет — для тех, кто хочет сначала попробовать стиль.</p>
          <div class="offer__price">00&nbsp;€</div>
        </div>
      </div>
      <p style="margin-top:2.5rem;color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
        Оплата и выдача файла подключаются отдельно (Gumroad / Lemon Squeezy).
        Цифровой товар возврату не подлежит.</p>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Не уверены, подойдёт ли стиль?</h2>
      <p class="rv">Возьмите тестовый набор из двух пресетов. Если подойдёт — стоимость зачту в полный пак.</p>
      <a class="btn rv" href="__CONTACT__"><span>Написать мне</span></a>
    </div>
  </section>
"""

WORKSHOP_BODY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label rv">Обучение</span>
      <h1 class="display rv">Воркшоп <em>1:1</em></h1>
      <p class="lede rv">Полный день вдвоём. Не показать, как я снимаю, а объяснить, почему именно так.</p>
    </div>
  </section>

  <figure class="plate plate--r169 ph bleed rv" data-ph="Фото во всю ширину"></figure>

  <section class="band">
    <div class="wrap prose rv">
      <h2>Как устроен день</h2>
      <p>Начинаем с теории: принципы, на которые я опираюсь в работе с парой,
        в выборе локации, в свете, в движении и в том, как из отдельных кадров
        собирается история.</p>
      <p>Дальше практика. Мы вместе снимаем пару, и вы видите работу вживую:
        как я разговариваю с людьми, как направляю вместо того, чтобы ставить
        в позу, как выбираю оптику и точку съёмки, как принимаю решения на ходу.</p>
      <p>После съёмки садимся разбирать материал. Я показываю свой отбор и
        обработку и связываю финальные кадры с теми принципами, с которых мы
        начали утро.</p>

      <h2>Что входит</h2>
      <ul>
        <li>Теоретический блок и мои базовые принципы</li>
        <li>Практическая съёмка с парой</li>
        <li>Разбор и комментарии прямо во время съёмки</li>
        <li>Отбор и обработка кадров</li>
        <li>Финальный разбор результата</li>
        <li>Ваши вопросы в течение всего дня</li>
      </ul>
      <p>Не входят и оплачиваются отдельно: обед, транспорт при необходимости и
        гонорар моделей. Пару для практики вы можете найти и сами.</p>

      <h2>Дополнительный день практики</h2>
      <p>Если хочется больше именно съёмки, на следующий день можно добавить
        ещё одну практическую сессию — в другой локации и с упором на ваши
        конкретные задачи.</p>
    </div>
  </section>

  <section class="band" style="background:var(--paper-deep);padding-top:0">
    <div class="wrap" style="padding-top:var(--band)">
      <div class="offers">
        <div class="offer rv">
          <div class="offer__name"><span>Основной</span>Полный день 1:1</div>
          <p class="offer__desc">Около ЧИСЛО часов: теория, съёмка, отбор, обработка, разбор.</p>
          <div class="offer__price">0&nbsp;000&nbsp;€</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Опция</span>Дополнительный день практики</div>
          <p class="offer__desc">Ещё одна съёмка на следующий день, другая локация, ваши задачи.</p>
          <div class="offer__price">000&nbsp;€</div>
        </div>
      </div>
      <p style="margin-top:2rem;color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
        Цены указаны без НДС.</p>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Забронировать день</h2>
      <p class="rv">Напишите, когда вам удобно и что для вас сейчас самое непонятное в съёмке. Подберём дату.</p>
      <a class="btn rv" href="__CONTACT__"><span>Написать мне</span></a>
    </div>
  </section>
"""

WORKSHOPS_2026 = [
    # (даты, дни недели, язык, мест, город, страна, статус)
    ("00&ndash;00 марта", "ПН&ndash;ВТ", "русский", "12", "Будапешт", "Венгрия", "open"),
    ("00&ndash;00 апреля", "СБ&ndash;ВС", "русский", "12", "Вена", "Австрия", "open"),
    ("00&ndash;00 мая", "ЧТ&ndash;ПТ", "английский", "9", "Париж", "Франция", "open"),
    ("00&ndash;00 сентября", "ВТ&ndash;СР", "русский", "12", "Будапешт", "Венгрия", "full"),
]


def schedule_rows():
    out = []
    for when, days, lang, seats, city, country, status in WORKSHOPS_2026:
        full = status == "full"
        out.append(f"""        <div class="date-row rv{' is-full' if full else ''}">
          <div class="date-row__when">{when}<span>{days}</span></div>
          <div class="date-row__where">{city}, {country}</div>
          <div class="date-row__meta">Язык: {lang} &nbsp;·&nbsp; {seats} мест</div>
          <a class="btn btn--ghost" href="__CONTACT__"><span>{'Мест нет' if full else 'Записаться'}</span></a>
        </div>""")
    return "\n".join(out)


SCHEDULE_BODY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label rv">Группы</span>
      <h1 class="display rv">Воркшопы <em>2026</em></h1>
      <p class="lede rv">Двухдневные групповые воркшопы в городах, в которых мне самой хочется снимать.</p>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap narrow prose rv">
      <p>Обучение всегда было для меня главным двигателем. Курсы, которые я
        прошла, не просто ускорили развитие — они помогли понять, куда мне вообще
        хочется идти.</p>
      <p>Чаще всего фотографы буксуют на технике: пока камера остаётся задачей,
        на человека перед ней не остаётся внимания. Когда настройки уходят в
        автоматизм, освобождается место для главного — света, композиции и той
        связи между людьми, ради которой всё и затевается.</p>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:2.5rem">Расписание</p>
      <div class="dates">
__ROWS__
      </div>
      <p style="margin-top:2rem;color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
        Место в группе закрепляется предоплатой. При отмене за 30 дней предоплата возвращается.</p>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Вашего города нет в списке?</h2>
      <p class="rv">Напишите — если наберётся группа, приеду. Так появилась половина дат в этом расписании.</p>
      <a class="btn rv" href="__CONTACT__"><span>Предложить город</span></a>
    </div>
  </section>
"""

LEGAL_TERMS = """
  <section class="page-head">
    <div class="wrap">
      <span class="label">Документы</span>
      <h1 class="display">Условия</h1>
    </div>
  </section>
  <section class="band" style="padding-top:0">
    <div class="wrap prose">
      <p><strong>Черновик.</strong> Раздел нужно заполнить реальными условиями до
        запуска продаж. Ниже — обязательный минимум для продажи цифровых товаров
        и услуг в ЕС.</p>
      <h2>Кто продавец</h2>
      <p>Юридическое наименование, регистрационный номер, адрес, контактная почта.</p>
      <h2>Что продаётся</h2>
      <p>Фотосессии, воркшопы, цифровые пресеты. Цены, валюта, включён ли НДС.</p>
      <h2>Оплата и доставка</h2>
      <p>Способы оплаты. Цифровой товар отправляется на почту сразу после оплаты.</p>
      <h2>Возврат</h2>
      <p>Порядок возврата предоплаты за съёмки и воркшопы. Для цифровых товаров
        право на отказ утрачивается в момент скачивания файла — покупатель
        подтверждает это при оформлении.</p>
      <h2>Авторские права</h2>
      <p>Права на фотографии и пресеты. Что разрешено покупателю, что запрещено.</p>
    </div>
  </section>
"""

LEGAL_POLICY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label">Документы</span>
      <h1 class="display">Политика конфиденциальности</h1>
    </div>
  </section>
  <section class="band" style="padding-top:0">
    <div class="wrap prose">
      <p><strong>Черновик.</strong> Раздел нужно заполнить до запуска. Ниже —
        минимум под GDPR.</p>
      <h2>Кто обрабатывает данные</h2>
      <p>Наименование контролёра данных и контактная почта.</p>
      <h2>Какие данные собираются</h2>
      <p>Имя и почта при обращении, данные платежа у платёжного провайдера,
        аналитика посещений.</p>
      <h2>Зачем</h2>
      <p>Ответ на обращение, исполнение договора, бухгалтерия.</p>
      <h2>Кому передаются</h2>
      <p>Платёжный провайдер, почтовый сервис, хостинг, аналитика.</p>
      <h2>Ваши права</h2>
      <p>Доступ, исправление, удаление, перенос, отзыв согласия, жалоба в
        надзорный орган.</p>
      <h2>Cookies</h2>
      <p>Какие используются и как отказаться.</p>
    </div>
  </section>
"""

PAGES = [
    dict(
        file="index.html", url="/",
        title="Nadiia Loban Photography — фотограф в Будапеште",
        desc="Nadiia Loban Photography. Individual, couple, family and event photography in Budapest. Кинематографичные портреты, съёмки в Будапеште и по Европе.",
        body=HOME_BODY,
        schema=ld("""{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "%(site)s/#person",
      "name": "Nadiia Loban",
      "jobTitle": "Фотограф",
      "telephone": "+380676903262",
      "sameAs": ["https://www.instagram.com/nadi_loban/"],
      "url": "%(site)s/",
      "address": { "@type": "PostalAddress", "addressLocality": "Будапешт", "addressCountry": "HU" },
      "knowsAbout": ["Портретная фотография", "Семейная фотография", "Съёмка пар"]
    },
    {
      "@type": "ProfessionalService",
      "@id": "%(site)s/#business",
      "name": "Nadiia Loban Photography",
      "image": "%(site)s/img/og.jpg",
      "url": "%(site)s/",
      "founder": { "@id": "%(site)s/#person" },
      "areaServed": [
        { "@type": "City", "name": "Будапешт" },
        { "@type": "Place", "name": "Европа" }
      ],
      "address": { "@type": "PostalAddress", "addressLocality": "Будапешт", "addressCountry": "HU" },
      "priceRange": "€€",
      "telephone": "+380676903262",
      "sameAs": ["https://www.instagram.com/nadi_loban/"]
    },
    {
      "@type": "WebSite",
      "@id": "%(site)s/#website",
      "url": "%(site)s/",
      "name": "Nadiia Loban Photography",
      "inLanguage": "ru",
      "publisher": { "@id": "%(site)s/#person" }
    }
  ]
}""" % {"site": SITE}),
    ),
    dict(
        file="sessions.html", url="/sessions.html",
        title="Фотосессии в Будапеште | Nadiia Loban Photography",
        desc="Съёмка пар, семей и портретов в Будапеште и по Европе. Два часа, живой свет, "
             "150+ обработанных кадров. Стоимость и свободные даты.",
        body=SESSIONS_BODY,
        schema=ld("""{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Фотосессия в Будапеште",
  "serviceType": "Портретная и парная фотосъёмка",
  "provider": { "@type": "Person", "@id": "%(site)s/#person", "name": "Nadiia Loban" },
  "areaServed": [
    { "@type": "City", "name": "Будапешт" },
    { "@type": "Place", "name": "Европа" }
  ],
  "url": "%(site)s/sessions.html"
}""" % {"site": SITE}),
    ),
    dict(
        file="presets.html", url="/presets.html",
        title="Пресеты для Lightroom | Nadiia Loban Photography",
        desc="Наборы пресетов для Adobe Lightroom Classic, которыми я обрабатываю свои съёмки. "
             "Цветные и чёрно-белые пакеты, тестовый набор.",
        body=PRESETS_BODY,
        schema=ld("""{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Пресеты для Lightroom",
  "itemListElement": []
}"""),
    ),
    dict(
        file="workshop.html", url="/workshop.html",
        title="Воркшоп 1:1 для фотографов | Nadiia Loban",
        desc="Полный день индивидуального обучения: теория, практическая съёмка пары, "
             "отбор и обработка кадров, разбор результата.",
        body=WORKSHOP_BODY,
        schema=ld("""{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Индивидуальный воркшоп 1:1 по фотографии",
  "description": "Полный день индивидуального обучения фотографии: теория, практическая съёмка пары, отбор и обработка.",
  "inLanguage": "ru",
  "provider": { "@type": "Person", "@id": "%(site)s/#person", "name": "Nadiia Loban" },
  "url": "%(site)s/workshop.html"
}""" % {"site": SITE}),
    ),
    dict(
        file="schedule.html", url="/schedule.html",
        title="Расписание воркшопов 2026 | Nadiia Loban",
        desc="Даты групповых двухдневных воркшопов по фотографии в 2026 году: город, язык, "
             "количество мест и запись.",
        body=SCHEDULE_BODY.replace("__ROWS__", schedule_rows()),
        schema=ld("""{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Воркшопы по фотографии, 2026",
  "itemListElement": []
}"""),
    ),
    dict(file="terms.html", url="/terms.html", title="Условия | Nadiia Loban Photography",
         desc="Условия оказания услуг и продажи цифровых товаров.",
         body=LEGAL_TERMS, schema="", noindex=True),
    dict(file="policy.html", url="/policy.html", title="Политика конфиденциальности | Nadiia Loban",
         desc="Как обрабатываются персональные данные посетителей сайта.",
         body=LEGAL_POLICY, schema="", noindex=True),
]


def nav_html(current):
    return "".join(
        '<li><a href="%s"%s>%s</a></li>' % (
            href, ' aria-current="page"' if href == current else "", text)
        for href, text in NAV)


def foot_html():
    return "".join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in NAV)


def build():
    urls = []
    for page in PAGES:
        html = SHELL.format(
            title=page["title"], desc=page["desc"], site=SITE, url=page["url"],
            schema=page["schema"], nav=nav_html(page["url"]), footnav=foot_html(),
            body=page["body"], email=EMAIL, ig=INSTAGRAM,
            phone=PHONE, phone_href=PHONE_HREF,
            headclass=page.get("headclass", ""),
        ).replace("__CONTACT__", INSTAGRAM)

        if STAGING:
            html = html.replace('content="index, follow, max-image-preview:large"',
                                'content="noindex, nofollow"')
        if page.get("noindex"):
            html = html.replace('content="index, follow, max-image-preview:large"',
                                'content="noindex, follow"')
        else:
            urls.append(page["url"])

        # Внутренние ссылки делаем относительными: страницы лежат плоско в корне,
        # поэтому одинаково работают и на своём домене, и на подпути вида
        # user.github.io/nadia-photo/. Абсолютные /css/... на подпути ломаются.
        html = re.sub(r'(href|src)="/([^"/][^"]*)"', r'\1="\2"', html)
        html = html.replace('href="/"', 'href="./"')

        (ROOT / page["file"]).write_text(html, encoding="utf-8")
        print("  ✓", page["file"])

    # sitemap
    entries = "\n".join(
        f"  <url><loc>{SITE}{u}</loc><changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if u == '/' else '0.8'}</priority></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n", encoding="utf-8")
    print("  ✓ sitemap.xml")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nDisallow: /\n" if STAGING else
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print("  ✓ robots.txt")


def selftest():
    """Мелкая проверка: шаблон подставился, плейсхолдеров не осталось."""
    build()
    for page in PAGES:
        html = (ROOT / page["file"]).read_text(encoding="utf-8")
        assert "{title}" not in html and "{body}" not in html, page["file"]
        assert "__CONTACT__" not in html, f"{page['file']}: незаменённый __CONTACT__"
        assert "mailto:" not in html, f"{page['file']}: остался mailto, почты нет"
        assert "__ROWS__" not in html, f"{page['file']}: незаменённый __ROWS__"
        assert html.count("<h1") == 1, f"{page['file']}: должен быть ровно один h1"
        assert f'<link rel="canonical" href="{SITE}{page["url"]}">' in html, page["file"]
        # noindex только на юридических
        if not STAGING:
            assert ("noindex" in html) == bool(page.get("noindex")), page["file"]
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert "/terms.html" not in sm and "/policy.html" not in sm, "юр. страницы попали в sitemap"
    assert sm.count("<url>") == len([p for p in PAGES if not p.get("noindex")])
    print("selftest: ok")


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        selftest()
    else:
        build()
        print("Готово.")
