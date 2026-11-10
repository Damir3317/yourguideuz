# -*- coding: utf-8 -*-
"""Generates the bilingual 'Why visit Uzbekistan' article pages, optimized images and the listing card."""
import json, math, os, re, sys
from html import escape
from PIL import Image

SCR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCR, "..", ".."))
SITE = "https://yourguideuz.com"
DATE_ISO = "2026-11-11"

# ---------------------------------------------------------------- images
IMG = {
    "hero":            dict(file="registan.jpg",            pos="50% 55%"),
    "registan_night":  dict(file="qw.jpg",                  pos="50% 50%"),
    "bukhara_skyline": dict(file="bukhara.jpg",             pos="50% 50%"),
    "khiva_dawn":      dict(file="x6.jpg",                  pos="50% 50%"),
    "suzani":          dict(file="suzani-artisan.jpg",      pos="50% 32%"),
    "plov":            dict(file="tt1.jpg",                 pos="50% 62%"),
    "charvak":         dict(file="charvak.jpg",             pos="50% 50%"),
    "seven_lakes":     dict(file="tajikistan-lakes.jpg",    pos="50% 50%"),
    "bukhara_arch":    dict(file="b6.jpg",                  pos="50% 42%"),
    "bukhara_sunset":  dict(file="bk.jpg",                  pos="50% 50%"),
    "khiva_skyline":   dict(file="x5.jpg",                  pos="50% 50%"),
    "card_samarkand":  dict(file="samnight.jpg",            pos="50% 50%"),
    "card_bukhara":    dict(file="bk.jpg",                  pos="50% 50%"),
    "card_khiva":      dict(file="kalta-minor-sunset.jpg",  pos="50% 50%"),
}
ALT = {
    "en": {
        "hero": "Registan Square in Samarkand, Uzbekistan, at sunrise",
        "registan_night": "Registan Square in Samarkand lit up in the evening, with visitors in the foreground",
        "bukhara_skyline": "Bukhara old city skyline at sunset",
        "khiva_dawn": "Minaret and turquoise domes of Itchan Kala in Khiva at sunrise",
        "suzani": "Artisan hand-embroidering a traditional suzani textile in an Uzbek workshop",
        "plov": "Traditional Uzbek plov served in decorated bowls with bread, salad and tea",
        "charvak": "Charvak Reservoir and snow-capped mountains near Tashkent",
        "seven_lakes": "Turquoise lake in the Fann Mountains near the Seven Lakes, Tajikistan",
        "bukhara_arch": "Brick archway lined with textile stalls in the old town of Bukhara",
        "bukhara_sunset": "Ark Fortress gate at sunset in Bukhara",
        "khiva_skyline": "Itchan Kala skyline with minarets and domes at sunset, Khiva",
        "card_samarkand": "Gur-e-Amir Mausoleum illuminated at night in Samarkand",
        "card_bukhara": "Ark Fortress gate at sunset in Bukhara",
        "card_khiva": "Kalta Minor Minaret above the walls of Itchan Kala at sunset, Khiva",
    },
    "ru": {
        "hero": "Площадь Регистан в Самарканде, Узбекистан, на рассвете",
        "registan_night": "Площадь Регистан в Самарканде с вечерней подсветкой и туристами на переднем плане",
        "bukhara_skyline": "Панорама старого города Бухары на закате",
        "khiva_dawn": "Минарет и бирюзовые купола Ичан-Калы в Хиве на рассвете",
        "suzani": "Мастер вручную вышивает традиционный сюзане в узбекской мастерской",
        "plov": "Традиционный узбекский плов в расписных пиалах с лепёшкой, салатом и чаем",
        "charvak": "Чарвакское водохранилище и заснеженные горы недалеко от Ташкента",
        "seven_lakes": "Бирюзовое озеро в Фанских горах у Семи озёр, Таджикистан",
        "bukhara_arch": "Кирпичная арка с лавками тканей в старом городе Бухары",
        "bukhara_sunset": "Ворота крепости Арк на закате, Бухара",
        "khiva_skyline": "Панорама Ичан-Калы с минаретами и куполами на закате, Хива",
        "card_samarkand": "Мавзолей Гур-Эмир с вечерней подсветкой, Самарканд",
        "card_bukhara": "Ворота крепости Арк на закате, Бухара",
        "card_khiva": "Минарет Кальта-Минор над стенами Ичан-Калы на закате, Хива",
    },
}
CAP = {
    "en": {
        "registan_night": "Registan Square in the evening light.",
        "bukhara_skyline": "Bukhara: a historic center made for walking.",
        "khiva_dawn": "Khiva: minarets and domes inside Itchan Kala.",
        "suzani": "Embroidery and textile crafts are still practiced by hand.",
        "plov": "Plov, the dish at the heart of Uzbek food culture.",
        "charvak": "Charvak Reservoir, a popular day trip from Tashkent.",
        "seven_lakes": "The lakes of the Fann Mountains in neighboring Tajikistan.",
        "bukhara_arch": "An old-town passage in Bukhara.",
        "bukhara_sunset": "The Ark Fortress gate in Bukhara.",
        "khiva_skyline": "Itchan Kala, Khiva, at sunset.",
    },
    "ru": {
        "registan_night": "Площадь Регистан в вечерней подсветке.",
        "bukhara_skyline": "Бухара: исторический центр, созданный для пеших прогулок.",
        "khiva_dawn": "Хива: минареты и купола внутри Ичан-Калы.",
        "suzani": "Вышивка и текстильные ремёсла по-прежнему делаются вручную.",
        "plov": "Плов — блюдо, лежащее в основе узбекской кулинарной культуры.",
        "charvak": "Чарвакское водохранилище — популярная однодневная поездка из Ташкента.",
        "seven_lakes": "Озёра Фанских гор в соседнем Таджикистане.",
        "bukhara_arch": "Проход в старом городе Бухары.",
        "bukhara_sunset": "Ворота крепости Арк в Бухаре.",
        "khiva_skyline": "Ичан-Кала, Хива, на закате.",
    },
}

def prep_images():
    outdir = os.path.join(ROOT, "images", "guide")
    os.makedirs(outdir, exist_ok=True)
    seen = set()
    for key, d in IMG.items():
        f = d["file"]
        im = Image.open(os.path.join(ROOT, "images", f))
        d["w"], d["h"] = im.size
        stem = os.path.splitext(f)[0]
        d["stem"] = stem
        d["widths"] = [w for w in (640, 1024, 1600) if w <= im.size[0]] or [im.size[0]]
        if im.size[0] not in d["widths"] and im.size[0] <= 1600 and im.size[0] > d["widths"][-1]:
            d["widths"].append(im.size[0])
        if stem in seen:
            continue
        seen.add(stem)
        rgb = im.convert("RGB")
        for w in d["widths"]:
            out = os.path.join(outdir, f"{stem}-{w}.webp")
            h = round(im.size[1] * w / im.size[0])
            rgb.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=78, method=6)

def picture(key, lang, sizes, eager=False, cls=""):
    d = IMG[key]
    srcset = ", ".join(f"/images/guide/{d['stem']}-{w}.webp {w}w" for w in d["widths"])
    attrs = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    style = f' style="object-position:{d["pos"]}"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img src="/images/{d["file"]}" width="{d["w"]}" height="{d["h"]}" alt="{escape(ALT[lang][key])}" '
            f'{attrs} decoding="async"{style}{c}></picture>')

BODY_SIZES = "(min-width: 1100px) 720px, (min-width: 800px) 720px, 100vw"
PAIR_SIZES = "(min-width: 800px) 356px, 100vw"

def figure(key, lang):
    return (f'<figure class="article-figure">{picture(key, lang, BODY_SIZES)}'
            f'<figcaption>{escape(CAP[lang][key])}</figcaption></figure>')

def figure_pair(k1, k2, lang):
    cells = "".join(
        f'<figure class="article-figure">{picture(k, lang, PAIR_SIZES)}<figcaption>{escape(CAP[lang][k])}</figcaption></figure>'
        for k in (k1, k2))
    return f'<div class="article-figure-pair">{cells}</div>'

def expand_placeholders(body, lang):
    body = re.sub(r"\[\[FIG2 (\w+)\|(\w+)\]\]", lambda m: figure_pair(m.group(1), m.group(2), lang), body)
    body = re.sub(r"\[\[FIG (\w+)\]\]", lambda m: figure(m.group(1), lang), body)
    return body

# ---------------------------------------------------------------- site chrome
def site_chrome():
    s = open(os.path.join(ROOT, "travel-guide.html"), encoding="utf-8").read().replace("\r\n", "\n")
    head_i = s.index('<div class="nav-scrim">')
    head_j = s.index("</header>") + len("</header>")
    header = s[head_i:head_j]
    tail = s[s.index("<footer"):]
    ga = s[s.index("<!-- Google tag"):s.index("</script>", s.index("gtag('config'")) + len("</script>")]
    def absolutize(h):
        h = re.sub(r'href="index\.html"', 'href="/"', h)
        h = re.sub(r'href="(?!https?:|/|#|mailto:|tel:)([^"]+)"', r'href="/\1"', h)
        h = re.sub(r'src="(assets|images)/', r'src="/\1/', h)
        return h
    return ga, absolutize(header), absolutize(tail)

# ---------------------------------------------------------------- article definitions
ART = {
    "en": dict(
        lang="en", locale="en_US", slug="why-visit-uzbekistan", path="/travel-guide/why-visit-uzbekistan",
        h1="Why Visit Uzbekistan? 5 Reasons to Discover This Hidden Gem of Central Asia",
        seo_title="Why Visit Uzbekistan? 5 Reasons to Discover This Hidden Gem",
        description="Discover 5 reasons to visit Uzbekistan, from ancient Silk Road cities and authentic culture to delicious food, beautiful landscapes and affordable travel.",
        keywords="Why visit Uzbekistan, Reasons to visit Uzbekistan, Uzbekistan travel guide, Things to do in Uzbekistan, Uzbekistan culture and history, Best places to visit in Uzbekistan, Uzbekistan tourism, Travel to Uzbekistan, Samarkand Bukhara Khiva itinerary, Best time to visit Uzbekistan, Uzbekistan travel itinerary",
        category="Travel Inspiration", category_full="Travel Inspiration · Uzbekistan Travel Guide",
        lede="Uzbekistan is one of the most fascinating destinations in Central Asia, where ancient Silk Road cities, impressive Islamic architecture, welcoming people, and centuries-old traditions come together.",
        date_text="November 11, 2026", read_fmt="{n} min read",
        bc_home="Home", bc_guide="Travel Guide", bc_short="Why Visit Uzbekistan?",
        toc_title="In this article", langs_label="Read this article in",
        faq_title="Frequently Asked Questions",
        faq=[
            ("Is Uzbekistan worth visiting?", "Yes. Uzbekistan offers a unique combination of Silk Road history, impressive architecture, traditional cuisine, welcoming hospitality, and beautiful landscapes."),
            ("How many days are enough for Uzbekistan?", "For a first visit, 7–10 days is a good starting point. This allows travelers to explore Tashkent, Samarkand, and Bukhara at a comfortable pace."),
            ("What is the best time to visit Uzbekistan?", "Spring and autumn are generally the most comfortable seasons for sightseeing."),
            ("Is Uzbekistan suitable for first-time travelers?", "Yes. With reasonable planning, Uzbekistan can be a rewarding destination for first-time visitors to Central Asia."),
            ("Which cities should I visit in Uzbekistan?", "Samarkand, Bukhara, Khiva, and Tashkent are among the most popular destinations. Each offers a different experience."),
            ("Can I visit the Seven Lakes from Uzbekistan?", "Yes. Travelers staying in Samarkand can arrange a trip to the Seven Lakes region in neighboring Tajikistan. Border crossing requirements and travel arrangements should be checked before departure."),
        ],
        tours_eyebrow="Plan It With Us", tours_title="Tours That Match This Guide",
        tours_view="View Tours",
        tours=[
            ("card_samarkand", "Samarkand: The Essentials in One Day", "1 day · Samarkand", "A private guide and car for the day: Gur-Emir, Registan, Bibi-Khanym, Shah-i-Zinda and the paper village of Konigil."),
            ("card_bukhara", "Bukhara Old City Discovery", "1 day · Bukhara", "Ark Fortress, Poi Kalyan complex, Bolo-Hauz Mosque, Magoki-Attori and Lyabi-Hauz — Bukhara's old city in a single day."),
            ("card_khiva", "Khiva: Ancient Traditions", "1 day · Khiva", "All ten icons of Itchan Kala in a single guided walk — from the Ata-Darvaza gate to the Tash-Hovli Palace."),
        ],
        cta_title="Discover Uzbekistan with YourGuideUz",
        cta_paras=["Planning your first trip to Uzbekistan?",
                   "Explore Samarkand, Bukhara, Tashkent, Khiva, and beyond with local experiences, private tours, comfortable transportation, and personalized travel arrangements.",
                   "Let us help you discover the real Uzbekistan — its history, culture, food, and everyday life."],
        cta_btn="Explore Our Tours", cta_btn2="Contact Us",
        og_alt="Registan Square in Samarkand, Uzbekistan, at sunrise",
        publisher_name="YourGuideUz",
        listing_name="Travel Guide", home_name="Home",
        site_name="YourGuideUz",
    ),
    "ru": dict(
        lang="ru", locale="ru_RU", slug="pochemu-stoit-posetit-uzbekistan", path="/ru/travel-guide/pochemu-stoit-posetit-uzbekistan",
        h1="Почему стоит посетить Узбекистан? 5 главных причин открыть для себя эту страну",
        seo_title="Почему стоит посетить Узбекистан? 5 главных причин",
        description="Почему стоит посетить Узбекистан? Древние города Шёлкового пути, восточная культура, национальная кухня, горы и незабываемое гостеприимство.",
        keywords="Почему стоит посетить Узбекистан, Путешествие по Узбекистану, Туризм в Узбекистане, Что посмотреть в Узбекистане, Достопримечательности Узбекистана, Самарканд Бухара Хива, Культура Узбекистана, Когда лучше ехать в Узбекистан, Маршрут по Узбекистану, Отдых в Узбекистане, Путеводитель по Узбекистану",
        category="Вдохновение для путешествий", category_full="Вдохновение для путешествий · Путеводитель по Узбекистану",
        lede="Узбекистан — одно из самых интересных направлений Центральной Азии, где древние города Великого шёлкового пути, впечатляющая исламская архитектура, гостеприимные люди и многовековые традиции создают особую атмосферу.",
        date_text="11 ноября 2026", read_fmt="{n} мин чтения",
        bc_home="Главная", bc_guide="Путеводитель", bc_short="Почему стоит посетить Узбекистан?",
        toc_title="В этой статье", langs_label="Читать статью на языке",
        faq_title="Часто задаваемые вопросы",
        faq=[
            ("Стоит ли ехать в Узбекистан?", "Да. Узбекистан сочетает богатую историю Великого шёлкового пути, впечатляющую архитектуру, национальную кухню, гостеприимство и красивые природные пейзажи."),
            ("Сколько дней нужно для путешествия по Узбекистану?", "Для первого знакомства со страной хорошим вариантом будут 7–10 дней. Этого времени достаточно, чтобы в комфортном темпе посетить Ташкент, Самарканд и Бухару."),
            ("Когда лучше всего посещать Узбекистан?", "Обычно наиболее комфортные сезоны для осмотра достопримечательностей — весна и осень."),
            ("Подходит ли Узбекистан для первого путешествия в Центральную Азию?", "Да. При правильном планировании Узбекистан может стать отличным направлением для первого знакомства с Центральной Азией."),
            ("Какие города стоит посетить в Узбекистане?", "Самарканд, Бухара, Хива и Ташкент — одни из самых популярных направлений. Каждый город предлагает собственную атмосферу и впечатления."),
            ("Можно ли посетить Семь озёр из Узбекистана?", "Да. Путешественники, остановившиеся в Самарканде, могут организовать поездку в регион Семи озёр в соседнем Таджикистане. Перед поездкой необходимо проверить актуальные требования для пересечения границы и организационные условия."),
        ],
        tours_eyebrow="Спланируйте с нами", tours_title="Туры по теме путеводителя",
        tours_view="Смотреть туры",
        tours=[
            ("card_samarkand", "Самарканд: основное за один день", "1 день · Самарканд", "Индивидуальный гид и авто на день: Гур-Эмир, Регистан, Биби-Ханум, Шахи-Зинда и бумажная деревня Конигиль."),
            ("card_bukhara", "Бухара, знакомство со старым городом", "1 день · Бухара", "Крепость Арк, комплекс Пои-Калян, мечеть Боло-Хауз, Магоки-Аттори и Ляби-Хауз — старый город Бухары за один день."),
            ("card_khiva", "Хива: древние традиции", "1 день · Хива", "Все десять памятников Ичан-Калы за одну пешую экскурсию — от ворот Ата-Дарваза до дворца Таш-Хаули."),
        ],
        cta_title="Откройте Узбекистан вместе с YourGuideUz",
        cta_paras=["Планируете своё первое путешествие по Узбекистану?",
                   "Откройте для себя Самарканд, Бухару, Ташкент, Хиву и другие направления с помощью индивидуальных экскурсий, местных впечатлений, комфортного транспорта и персонально составленных маршрутов.",
                   "Мы поможем вам познакомиться с настоящим Узбекистаном — его историей, культурой, кухней и повседневной жизнью."],
        cta_btn="Посмотреть экскурсии", cta_btn2="Связаться с нами",
        og_alt="Площадь Регистан в Самарканде, Узбекистан, на рассвете",
        publisher_name="YourGuideUz",
        listing_name="Путеводитель", home_name="Главная",
        site_name="YourGuideUz",
    ),
}
OTHER = {"en": "ru", "ru": "en"}
LANG_NAME = {"en": "English", "ru": "Русский"}

def strip_tags(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()

def build_toc(body):
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    return items

def abs_url(path):
    return SITE + path

def render(lang, ga, header, tail):
    a = ART[lang]
    o = ART[OTHER[lang]]
    guide = "/ru/travel-guide" if lang == "ru" else "/travel-guide"
    if lang == "ru":
        header = header.replace('href="/travel-guide"', 'href="/ru/travel-guide"')
        tail = tail.replace('href="/travel-guide"', 'href="/ru/travel-guide"')
    body_raw = open(os.path.join(SCR, f"{lang}_body.html"), encoding="utf-8").read()
    toc = build_toc(body_raw)
    faq_html = "".join(
        f'<details class="faq-item"><summary>{escape(q)}</summary><div class="faq-answer"><p>{escape(ans)}</p></div></details>'
        for q, ans in a["faq"])
    body = expand_placeholders(body_raw, lang).replace('href="/travel-guide"', f'href="{guide}"')
    # words -> reading time
    text = strip_tags(re.sub(r"<figcaption>.*?</figcaption>", "", body)) + " " + a["lede"] + " " + " ".join(q + " " + x for q, x in a["faq"])
    words = len(re.findall(r"\w+", text))
    wpm = 200 if lang == "en" else 180
    minutes = max(1, math.ceil(words / wpm))
    read = a["read_fmt"].format(n=minutes)

    toc_items = toc + [("faq", escape(a["faq_title"]))]
    toc_html = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc_items)

    canon = abs_url(a["path"]); alt_url = abs_url(o["path"])
    en_url = abs_url(ART["en"]["path"]); ru_url = abs_url(ART["ru"]["path"])
    og_img = f"{SITE}/images/{IMG['hero']['file']}"
    hero = IMG["hero"]
    title = escape(a["seo_title"])
    desc = escape(a["description"], quote=True)

    ld_article = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": a["h1"], "description": a["description"],
        "image": [og_img], "datePublished": DATE_ISO, "dateModified": DATE_ISO,
        "author": {"@type": "Organization", "name": "YourGuideUz", "url": SITE + "/"},
        "publisher": {"@type": "Organization", "name": "YourGuideUz", "url": SITE + "/"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": canon},
        "inLanguage": lang, "articleSection": a["category"],
    }
    ld_crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": a["bc_home"], "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": a["bc_guide"], "item": SITE + guide},
            {"@type": "ListItem", "position": 3, "name": a["bc_short"], "item": canon},
        ],
    }
    jd = lambda o_: json.dumps(o_, ensure_ascii=False, indent=2)

    tour_cards = ""
    for key, ttl, meta, txt in a["tours"]:
        d = IMG[key]
        srcset = ", ".join(f"/images/guide/{d['stem']}-{w}.webp {w}w" for w in d["widths"])
        tour_cards += f'''
      <article class="tour-card">
        <div class="tour-media"><picture><source type="image/webp" srcset="{srcset}" sizes="(min-width: 980px) 380px, (min-width: 660px) 50vw, 100vw"><img src="/images/{d['file']}" width="{d['w']}" height="{d['h']}" alt="{escape(ALT[lang][key])}" loading="lazy" decoding="async"></picture></div>
        <div class="tour-body">
          <div class="tour-meta"><span>{escape(meta)}</span></div>
          <h3>{escape(ttl)}</h3>
          <p>{escape(txt)}</p>
          <div class="tour-foot"><span></span><a href="/tours" class="btn btn-ghost btn-sm">{escape(a['tours_view'])}</a></div>
        </div>
      </article>'''

    cta_ps = "\n      ".join(f"<p>{escape(p)}</p>" for p in a["cta_paras"])

    page = f'''<!doctype html>
<html lang="{lang}">
<head>
{ga}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{escape(a['keywords'], quote=True)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="ru" href="{ru_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<meta name="theme-color" content="#3fa0c4">
<meta property="og:type" content="article">
<meta property="og:site_name" content="YourGuideUz">
<meta property="og:locale" content="{a['locale']}">
<meta property="og:locale:alternate" content="{o['locale']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="{hero['w']}">
<meta property="og:image:height" content="{hero['h']}">
<meta property="og:image:alt" content="{escape(a['og_alt'], quote=True)}">
<meta property="article:published_time" content="{DATE_ISO}">
<meta property="article:modified_time" content="{DATE_ISO}">
<meta property="article:section" content="{escape(a['category'], quote=True)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
<script type="application/ld+json">
{jd(ld_article)}
</script>
<script type="application/ld+json">
{jd(ld_crumbs)}
</script>
</head>
<body data-page="article" data-fixed-lang class="page-header">

{header}

<main>

<section class="hero hero-sm hero-plain article-head">
  <div class="container">
    <div class="hero-content">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">{a['bc_home']}</a><span>/</span><a href="{guide}">{a['bc_guide']}</a><span>/</span><span aria-current="page">{escape(a['bc_short'])}</span></nav>
      <p class="eyebrow">{escape(a['category_full'])}</p>
      <h1>{escape(a['h1'])}</h1>
      <p class="hero-lede">{escape(a['lede'])}</p>
      <div class="article-meta">
        <span class="article-lang" lang="{lang}" title="{LANG_NAME[lang]}">{lang.upper()}</span>
        <time datetime="{DATE_ISO}">{a['date_text']}</time>
        <span>{read}</span>
      </div>
      <p class="article-langs">{a['langs_label']}:
        <a href="{a['path']}" hreflang="{lang}" lang="{lang}" aria-current="true">{LANG_NAME[lang]}</a>
        <a href="{o['path']}" hreflang="{OTHER[lang]}" lang="{OTHER[lang]}">{LANG_NAME[OTHER[lang]]}</a>
      </p>
    </div>
  </div>
</section>

<article class="article-wrap">
  <div class="container">
    <figure class="article-cover">
      <picture><source type="image/webp" srcset="{", ".join(f"/images/guide/{hero['stem']}-{w}.webp {w}w" for w in hero['widths'])}" sizes="(min-width: 1200px) 1152px, 100vw"><img src="/images/{hero['file']}" width="{hero['w']}" height="{hero['h']}" alt="{escape(ALT[lang]['hero'])}" loading="eager" fetchpriority="high" decoding="async" style="object-position:{hero['pos']}"></picture>
    </figure>

    <div class="article-layout">
      <aside class="article-toc">
        <nav aria-label="{escape(a['toc_title'])}">
          <p class="article-toc-title">{escape(a['toc_title'])}</p>
          <ol>{toc_html}</ol>
        </nav>
      </aside>
      <div class="article-body">
{body}
<h2 id="faq">{escape(a['faq_title'])}</h2>
<div class="faq-list">{faq_html}</div>
      </div>
    </div>
  </div>
</article>

<section class="bg-alt">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow">{escape(a['tours_eyebrow'])}</p>
      <h2>{escape(a['tours_title'])}</h2>
    </div>
    <div class="tour-grid">{tour_cards}
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="cta-band" style="background:linear-gradient(135deg, var(--blue-700), var(--blue-900));">
      <h2>{escape(a['cta_title'])}</h2>
      {cta_ps}
      <div class="cta-actions">
        <a href="/tours" class="btn btn-accent">{escape(a['cta_btn'])}</a>
        <a href="/contact" class="btn btn-ghost-light">{escape(a['cta_btn2'])}</a>
      </div>
    </div>
  </div>
</section>

</main>

{tail}'''
    return page, dict(words=words, minutes=minutes)

def main():
    prep_images()
    ga, header, tail = site_chrome()
    info = {}
    for lang, outpath in (("en", "articles/en/why-visit-uzbekistan.html"), ("ru", "articles/ru/pochemu-stoit-posetit-uzbekistan.html")):
        page, meta = render(lang, ga, header, tail)
        info[lang] = meta
        full = os.path.join(ROOT, outpath)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w", encoding="utf-8", newline="\n").write(page)
    print(json.dumps(info))

if __name__ == "__main__":
    main()
