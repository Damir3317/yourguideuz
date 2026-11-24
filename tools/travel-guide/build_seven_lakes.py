# -*- coding: utf-8 -*-
"""Builds the bilingual 'Seven Lakes of Tajikistan' article pages.

Reuses the page template from build_article.py with this article's own
config. Source photos (already resized from the owner's originals 7l1..7l10)
live in images/seven-lakes/; WebP variants go to images/guide/seven-lakes/.

Run: python tools/travel-guide/build_seven_lakes.py
"""
import json, os
from PIL import Image
import build_article as B

HERE = os.path.dirname(os.path.abspath(__file__))
WA = "https://wa.me/998907433317"

B.DATE_ISO = "2026-11-24"

B.IMG = {
    "hero":     dict(file="seven-lakes/haft-kul-lake.jpg",          pos="50% 58%"),
    "canyon":   dict(file="seven-lakes/shing-valley-canyon.jpg",    pos="50% 62%"),
    "border":   dict(file="seven-lakes/border-crossing-dawn.jpg",   pos="50% 55%"),
    "car4x4":   dict(file="seven-lakes/4x4-tajikistan.jpg",         pos="50% 45%"),
    "bazaar":   dict(file="seven-lakes/penjikent-bazaar.jpg",       pos="50% 55%"),
    "picnic":   dict(file="seven-lakes/riverside-picnic-spot.jpg",  pos="50% 60%"),
    "pickup":   dict(file="seven-lakes/samarkand-hotel-pickup.jpg", pos="50% 60%"),
    "traveler": dict(file="seven-lakes/traveler-upper-lake.jpg",    pos="50% 45%"),
    "card_7lakes":    dict(file="7lakes2.jpg",        pos="50% 50%"),
    "card_samarkand": dict(file="samnight.jpg",       pos="50% 50%"),
    "card_shakh":     dict(file="aksaray-palace.jpg", pos="50% 50%"),
}

B.ALT = {
    "en": {
        "hero": "Turquoise mountain lake below rocky peaks at the Seven Lakes (Haft Kul), Fann Mountains, Tajikistan",
        "canyon": "The Shing River valley with one of the Seven Lakes between steep canyon walls, Tajikistan",
        "border": "Minibuses waiting at the Uzbekistan–Tajikistan border crossing near Samarkand at dawn",
        "car4x4": "4x4 vehicle used for the mountain road to the Seven Lakes in Tajikistan",
        "bazaar": "Fruit and vegetable stalls at the local bazaar in Penjikent, Tajikistan",
        "picnic": "Green riverside meadow by a mountain stream in the Haft Kul valley, Tajikistan",
        "pickup": "YourGuideUz sign in front of a minibus during an early-morning hotel pickup in Samarkand",
        "traveler": "Traveler standing on a rock above a turquoise lake in the Fann Mountains, Tajikistan",
        "card_7lakes": "Turquoise alpine lake in Tajikistan's Fann Mountains",
        "card_samarkand": "Registan Square in Samarkand illuminated at night",
        "card_shakh": "Towering tiled portal of the Ak-Saray Palace ruins, Shakhrisabz",
    },
    "ru": {
        "hero": "Бирюзовое горное озеро у скалистых вершин, Семь озёр (Хафткуль), Фанские горы, Таджикистан",
        "canyon": "Долина реки Шинг с одним из Семи озёр между отвесными стенами каньона, Таджикистан",
        "border": "Микроавтобусы у пограничного перехода между Узбекистаном и Таджикистаном под Самаркандом на рассвете",
        "car4x4": "Внедорожник 4x4 для горной дороги к Семи озёрам в Таджикистане",
        "bazaar": "Прилавки с фруктами и овощами на местном базаре в Пенджикенте, Таджикистан",
        "picnic": "Зелёный луг у горной речки в долине Хафткуль, Таджикистан",
        "pickup": "Табличка YourGuideUz у микроавтобуса во время раннего трансфера от отеля в Самарканде",
        "traveler": "Путешественник на камне над бирюзовым озером в Фанских горах, Таджикистан",
        "card_7lakes": "Бирюзовое горное озеро в Фанских горах Таджикистана",
        "card_samarkand": "Площадь Регистан в Самарканде с ночной подсветкой",
        "card_shakh": "Высокий изразцовый портал руин дворца Ак-Сарай, Шахрисабз",
    },
}

B.CAP = {
    "en": {
        "canyon": "Between the lakes, the road follows the river through a narrow canyon.",
        "border": "Early morning at the border crossing.",
        "car4x4": "A 4x4 is the usual choice for the road up the valley.",
        "bazaar": "Fresh fruit for the picnic from the Penjikent bazaar.",
        "picnic": "Riverside spots like this are perfect for a picnic.",
        "pickup": "Early-morning pickup from your hotel in Samarkand.",
        "traveler": "One of the upper lakes on a clear day.",
    },
    "ru": {
        "canyon": "Между озёрами дорога идёт вдоль реки по узкому каньону.",
        "border": "Раннее утро на пограничном переходе.",
        "car4x4": "Для дороги по долине обычно выбирают внедорожник 4x4.",
        "bazaar": "Свежие фрукты для пикника с базара в Пенджикенте.",
        "picnic": "Такие места у реки идеально подходят для пикника.",
        "pickup": "Ранний трансфер от вашего отеля в Самарканде.",
        "traveler": "Одно из верхних озёр в ясный день.",
    },
}

B.ART = {
    "en": dict(
        lang="en", locale="en_US", slug="seven-lakes-tajikistan", path="/travel-guide/seven-lakes-tajikistan",
        body_file=os.path.join("seven-lakes", "en_body.html"),
        h1="Seven Lakes of Tajikistan: A Complete Travel Guide",
        seo_title="Seven Lakes Tajikistan: Day Trip Guide from Samarkand",
        description="Plan a Seven Lakes day trip from Samarkand: how to reach Haft Kul in the Fann Mountains of Tajikistan, the border crossing, best season and travel tips.",
        keywords="Seven Lakes Tajikistan, Seven Lakes tour from Samarkand, Haft Kul Tajikistan, Seven Lakes day trip, Fann Mountains Tajikistan, How to get to Seven Lakes, Samarkand to Seven Lakes, Seven Lakes travel guide",
        category="Nature & Day Trips", category_full="Nature & Day Trips · Tajikistan",
        lede="Discover the stunning mountain lakes of Haft Kul and learn how to visit them on a day trip from Samarkand.",
        date_text="November 24, 2026", read_fmt="{n} min read",
        bc_home="Home", bc_guide="Travel Guide", bc_short="Seven Lakes of Tajikistan",
        toc_title="In this article", langs_label="Read this article in",
        faq_title="Frequently Asked Questions",
        faq=[
            ("How far are the Seven Lakes from Samarkand?", "About an hour's drive to the Jartepa–Sarazm border, then usually around two hours through Penjikent and up the valley, depending on the road. Plan for a full day, returning to Samarkand in the late afternoon."),
            ("Can I visit all seven lakes in one day?", "In good conditions, yes. A day trip usually includes short stops at each lake, ending at Hazorchashma, the highest one. Road and weather conditions can sometimes limit access to the upper lakes."),
            ("Do I need a visa to visit Tajikistan?", "It depends on your nationality: some travelers enter visa-free, others need an e-Visa or a visa issued in advance. Check the current rules before your trip and make sure you can re-enter Uzbekistan."),
            ("Is a 4x4 vehicle necessary?", "It is strongly recommended. The road up the valley is narrow and partly unpaved, and a 4x4 with an experienced local driver makes the journey safer and more comfortable."),
            ("What should I bring for the trip?", "Your passport, cash in small notes, drinking water, comfortable shoes, a warm layer, sun protection and any personal medication."),
        ],
        tours_eyebrow="Plan It With Us", tours_title="Tours That Match This Guide",
        tours_view="View Tour",
        tours=[
            ("card_7lakes", "Seven Lakes of Tajikistan", "1 day · Tajikistan", "A full-day cross-border trip from Samarkand into the Fann Mountains, with stops at the lakes and a picnic.", "/tours#tour-tajikistan"),
            ("card_samarkand", "Samarkand: The Essentials in One Day", "1 day · Samarkand", "A private guide and car for the day: Gur-Emir, Registan, Bibi-Khanym, Shah-i-Zinda and the paper village of Konigil.", "/tours#tour-samarkand"),
            ("card_shakh", "Shakhrisabz: Birthplace of Timur", "1 day · Shakhrisabz", "Another mountain-road day trip from Samarkand, to the hometown of Amir Temur and the ruins of the Ak-Saray Palace.", "/tours#tour-shakhrisabz"),
        ],
        cta_title="Visit the Seven Lakes with YourGuideUz",
        cta_paras=["Hotel pickup in Samarkand, help with the border crossing and a local 4x4 driver in Tajikistan, all arranged for you.",
                   "Tell us your dates and group size, and we will plan the day around you."],
        cta_html=(f'<a href="{WA}?text=Hi%20YourGuideUz!%20I%27d%20like%20to%20visit%20the%20Seven%20Lakes%20of%20Tajikistan." class="btn btn-accent">Message Us on WhatsApp</a>\n'
                  '        <a href="/tours#tour-tajikistan" class="btn btn-ghost-light">View the Seven Lakes Tour</a>'),
        og_alt="Turquoise mountain lake at the Seven Lakes (Haft Kul) in Tajikistan's Fann Mountains",
        og_image="/images/seven-lakes/haft-kul-og.jpg", og_size=(1200, 630),
    ),
    "ru": dict(
        lang="ru", locale="ru_RU", slug="sem-ozer-tadzhikistana", path="/ru/travel-guide/sem-ozer-tadzhikistana",
        body_file=os.path.join("seven-lakes", "ru_body.html"),
        h1="Семь озёр Таджикистана: полный путеводитель",
        seo_title="Семь озёр Таджикистана: поездка из Самарканда за день",
        description="Как съездить на Семь озёр (Хафткуль) из Самарканда за один день: дорога в Фанские горы, переход границы, лучший сезон и советы для путешественников.",
        keywords="Семь озёр Таджикистан, тур на Семь озёр из Самарканда, Хафткуль, Маргузорские озёра, Фанские горы, как добраться до Семи озёр, Самарканд Семь озёр, поездка на Семь озёр за один день",
        category="Природа и поездки на день", category_full="Природа и поездки на день · Таджикистан",
        lede="Откройте для себя горные озёра Хафткуль и узнайте, как посетить их за один день из Самарканда.",
        date_text="24 ноября 2026", read_fmt="{n} мин чтения",
        bc_home="Главная", bc_guide="Путеводитель", bc_short="Семь озёр Таджикистана",
        toc_title="В этой статье", langs_label="Читать статью на языке",
        faq_title="Часто задаваемые вопросы",
        faq=[
            ("Как далеко Семь озёр от Самарканда?", "Около часа на машине до перехода Жартепа — Саразм, затем обычно около двух часов через Пенджикент и вверх по долине, в зависимости от дороги. Рассчитывайте на целый день с возвращением в Самарканд ближе к вечеру."),
            ("Можно ли увидеть все семь озёр за один день?", "При хороших условиях — да. Обычно в поездке есть короткие остановки у каждого озера, а последняя — у Хазорчашмы, самого высокого из них. Состояние дороги и погода иногда ограничивают проезд к верхним озёрам."),
            ("Нужна ли виза в Таджикистан?", "Это зависит от гражданства. Одни путешественники могут въехать без визы, другим нужна электронная виза или виза, оформленная заранее. Перед поездкой проверьте актуальные требования и убедитесь, что сможете снова въехать в Узбекистан."),
            ("Обязателен ли внедорожник 4x4?", "Очень желателен. Дорога по долине узкая и местами грунтовая, а внедорожник с опытным местным водителем делает поездку безопаснее и комфортнее."),
            ("Что взять с собой в поездку?", "Паспорт, наличные мелкими купюрами, питьевую воду, удобную обувь, тёплую кофту, защиту от солнца и личные лекарства."),
        ],
        tours_eyebrow="Спланируйте с нами", tours_title="Туры по теме путеводителя",
        tours_view="Смотреть тур",
        tours=[
            ("card_7lakes", "Семь озёр Таджикистана", "1 день · Таджикистан", "Поездка из Самарканда в Фанские горы с пересечением границы, остановками у озёр и пикником.", "/tours#tour-tajikistan"),
            ("card_samarkand", "Самарканд: основное за один день", "1 день · Самарканд", "Индивидуальный гид и авто на день: Гур-Эмир, Регистан, Биби-Ханум, Шахи-Зинда и бумажная деревня Конигиль.", "/tours#tour-samarkand"),
            ("card_shakh", "Шахрисабз: родина Тамерлана", "1 день · Шахрисабз", "Ещё одна поездка на день из Самарканда по горной дороге — на родину Амира Темура, к руинам дворца Ак-Сарай.", "/tours#tour-shakhrisabz"),
        ],
        cta_title="Поезжайте на Семь озёр с YourGuideUz",
        cta_paras=["Трансфер от отеля в Самарканде, помощь с переходом границы и местный водитель на внедорожнике в Таджикистане — мы всё организуем.",
                   "Напишите нам даты и количество человек, и мы спланируем день под вас."],
        cta_html=(f'<a href="{WA}?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%20%D0%A5%D0%BE%D1%87%D1%83%20%D0%BF%D0%BE%D0%B5%D1%85%D0%B0%D1%82%D1%8C%20%D0%BD%D0%B0%20%D0%A1%D0%B5%D0%BC%D1%8C%20%D0%BE%D0%B7%D1%91%D1%80%20%D0%A2%D0%B0%D0%B4%D0%B6%D0%B8%D0%BA%D0%B8%D1%81%D1%82%D0%B0%D0%BD%D0%B0." class="btn btn-accent">Написать в WhatsApp</a>\n'
                  '        <a href="/tours#tour-tajikistan" class="btn btn-ghost-light">Тур на Семь озёр</a>'),
        og_alt="Бирюзовое горное озеро, Семь озёр (Хафткуль), Фанские горы, Таджикистан",
        og_image="/images/seven-lakes/haft-kul-og.jpg", og_size=(1200, 630),
    ),
}

def prep_images():
    """Like build_article.prep_images, but never rewrites WebP files that already exist."""
    outdir = os.path.join(B.ROOT, "images", "guide")
    for d in B.IMG.values():
        im = Image.open(os.path.join(B.ROOT, "images", d["file"]))
        d["w"], d["h"] = im.size
        d["stem"] = os.path.splitext(d["file"])[0]
        d["widths"] = [w for w in (640, 1024, 1600) if w <= im.size[0]] or [im.size[0]]
        if im.size[0] not in d["widths"] and im.size[0] <= 1600 and im.size[0] > d["widths"][-1]:
            d["widths"].append(im.size[0])
        rgb = None
        for w in d["widths"]:
            out = os.path.join(outdir, f"{d['stem']}-{w}.webp")
            if os.path.exists(out):
                continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            rgb = rgb or im.convert("RGB")
            rgb.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS).save(out, "WEBP", quality=78, method=6)

def main():
    prep_images()
    ga, header, tail = B.site_chrome()
    info = {}
    for lang in ("en", "ru"):
        page, meta = B.render(lang, ga, header, tail)
        info[lang] = meta
        out = os.path.join(B.ROOT, "articles", lang, B.ART[lang]["slug"] + ".html")
        open(out, "w", encoding="utf-8", newline="\n").write(page)
    print(json.dumps(info))

if __name__ == "__main__":
    main()
