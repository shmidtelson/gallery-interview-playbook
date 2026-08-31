#!/usr/bin/env python3
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

pdfmetrics.registerFont(TTFont("Inter", "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"))

OUT = Path(__file__).with_name("verdict-2026-08-31.pdf")
INK = colors.HexColor("#1c1916")
MUTED = colors.HexColor("#5a554c")
LINE = colors.HexColor("#d4cdc2")
RULE = colors.HexColor("#6b4a12")
ROW = colors.HexColor("#f1ebe2")
PAPER = colors.white
HEAD = colors.HexColor("#2a2622")


def S(name, **kwargs):
    base = dict(fontName="Inter", textColor=INK, leading=13)
    base.update(kwargs)
    return ParagraphStyle(name, **base)


H1 = S("H1", fontName="Inter-Bold", fontSize=16, leading=20, spaceAfter=4)
H2 = S("H2", fontName="Inter-Bold", fontSize=10.5, leading=13, spaceBefore=11, spaceAfter=5)
META = S("META", fontSize=8.5, leading=11, textColor=MUTED)
BODY = S("BODY", fontSize=9.5, leading=13, alignment=TA_JUSTIFY, spaceAfter=5)
LI = S("LI", fontSize=9.5, leading=13, leftIndent=10, spaceAfter=2.5)
CELL = S("CELL", fontSize=8, leading=10.5)
CELLB = S("CELLB", fontName="Inter-Bold", fontSize=8, leading=10.5)
DEC = S("DEC", fontName="Inter-Bold", fontSize=12, leading=15, textColor=RULE, spaceBefore=6, spaceAfter=6)


def P(text, st=BODY):
    return Paragraph(text, st)


def table(rows, widths, header=True):
    data = []
    for i, row in enumerate(rows):
        st = CELLB if header and i == 0 else CELL
        bold_first = header and i > 0
        data.append(
            [
                P(cell, CELLB if (j == 0 and bold_first) or (header and i == 0) else st)
                for j, cell in enumerate(row)
            ]
        )
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), ROW),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("TEXTCOLOR", (0, 0), (-1, 0), HEAD),
    ]
    t.setStyle(TableStyle(cmds))
    return t


def build():
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title="Заключение по кандидату — 31.08.2026",
        author="Найм, full-stack галерей",
    )

    story = [
        P("Конфиденциально · внутренний документ по найму", META),
        P("Заключение по кандидату", H1),
        P(
            "31 августа 2026 · техническое интервью, ~47 мин · "
            "роль: full-stack (PHP 8 / Symfony, React), галереи для фотографов · "
            "источник: Video_2026-08-31_17-08-52.srt",
            META,
        ),
        P("Рекомендация: брать с оговоркой", DEC),
        P(
            "Оценка только по сказанному в разговоре. Темы, которые интервьюер не ставил "
            "(хранение фото, процедура переключения), в баллах не участвуют."
        ),
        P(
            "Можно брать, если закрывает пробную задачу на вашей кодовой базе. Без проверки — не оформлять. "
            "Коммерческого Symfony и Doctrine нет. React сейчас не пишет. PHP, API, платежи и контур с AI "
            "достаточны, чтобы войти в чужой Symfony за дни. Спринтов нет (канбан). Проверка: сам ли "
            "двигает задачу без daily/SDM и выключает оплату на API."
        ),
        P("Соответствие вакансии", H2),
        table(
            [
                ["Требование", "Статус", "Комментарий"],
                [
                    "PHP 8, от 2 лет",
                    "Частично",
                    "PHP и Laravel есть, включая e-commerce и интеграции.",
                ],
                [
                    "Symfony",
                    "Нет опыта",
                    "Факт. С PHP и его AI — закрываемый пробел, не отказ.",
                ],
                [
                    "Doctrine / миграции",
                    "Нет опыта",
                    "Нет Symfony в проде — нет Doctrine. Проверяется одной задачей на вашей схеме.",
                ],
                [
                    "React, router v6",
                    "Слабее",
                    "Сейчас только backend. AI закроет рутину. Публичная галерея — если задача его коснётся.",
                ],
                [
                    "PostgreSQL",
                    "Не показано",
                    "Живые миграции и разбор чужой схемы в разговоре не было.",
                ],
                [
                    "API",
                    "Да",
                    "Сервисы, BFF, Kafka, платёжный сценарий Т-Банка.",
                ],
                [
                    "AI",
                    "Да",
                    "Агенты, сверка моделей, финальное слово за собой. Так и ожидали в вакансии.",
                ],
                [
                    "Без спринтов",
                    "Да",
                    "Канбан, не спринты.",
                ],
                [
                    "Без дейликов, один на фаундера",
                    "Вопрос",
                    "Daily, SDM. Месяц ждал доску. На испытательном видно: пишет сам или ждёт постановку.",
                ],
                [
                    "Stripe, Go, Next.js",
                    "Не опора",
                    "Stripe по шагам не знает. Go изучает. Next.js — соседняя команда.",
                ],
            ],
            [42 * mm, 28 * mm, 108 * mm],
        ),
        P(
            "AI смягчает пробел по Symfony/Doctrine. Не смягчает необходимость пробной задачи.",
            BODY,
        ),
        P("Система оценки", H2),
        P(
            "Шкала 1–4, без «тройки за среднее»: 1 слабо · 2 ниже порога роли по опыту · "
            "3 приемлемо по заданным вопросам · 4 сильно, без страховки. "
            "Решение по обязательным (PHP/Symfony, React, кейс, автономия, AI): "
            "≥3.4 и нет единиц — брать; 2.5–3.3 или двойки, которые закрывает AI/проба — оговорка; "
            "<2.5 — отказ. Здесь среднее ≈ 2.4. По баллам отказ. Сдвиг в оговорку — потому что "
            "AI делает Symfony/Doctrine закрываемыми, баллы за опыт не повышаем. "
            "Пробная задача: зелёный / красный, не ещё один балл."
        ),
        P("Оценка компетенций", H2),
        P("Баллы — про опыт в разговоре, не про прогноз с AI.", META),
        Spacer(1, 2 * mm),
        table(
            [
                ["Компетенция", "Балл", "Смысл для найма"],
                [
                    "PHP / Symfony / Doctrine",
                    "2",
                    "Опыта Symfony/Doctrine нет. PHP есть. С AI растёт шанс закрыть пробел, не балл за опыт.",
                ],
                [
                    "React",
                    "2",
                    "Слабее backend. Для флагов/API может хватить. Публичная галерея не доказана.",
                ],
                [
                    "Кейс (как задали)",
                    "3",
                    "Флаги, коннектор оплат, второй инстанс, данные. Первый импульс — флаги на фронте. По базе — «зависит от схемы».",
                ],
                [
                    "Автономия",
                    "2",
                    "Без спринтов работает. Daily и простой без доски — привычка. Проверяется.",
                ],
                [
                    "AI",
                    "3",
                    "Применяет сознательно, сравнивает модели, оставляет проверку за собой.",
                ],
                [
                    "Инфра и интеграции",
                    "3",
                    "Полезный фон. Не заменяет пробел в стеке продукта.",
                ],
            ],
            [42 * mm, 14 * mm, 122 * mm],
        ),
        P("Кейс: что оценивалось", H2),
        P(
            "В разговоре стояли отключение функций, оплаты и второй контур. Кандидат предложил "
            "feature flags (сначала фронтенд, затем «везде») и коннектор оплат на backend. "
            "Сценарий Т-Банка разложил по шагам. Второй инстанс обосновал ценой двух релизов "
            "и задержкой. По данным колебался между изоляцией сбоев и одной универсальной "
            "таблицей — «зависит от схемы». По заданным темам это 3."
        ),
        P("Что проверить до оформления", H2),
        P(
            "Одна задача на стейджинге, 2–4 дня, постановка вечером: "
            "1) прочитать схему Doctrine и написать, что трогает; "
            "2) выключить магазин/оплату на API; "
            "3) прогнать тест оплаты или явный отказ. "
            "Зелёный — тянет. Красный (не входит в схему, чинит только UI, ждёт ТЗ) — отказ."
        ),
        P("Риски, если берёте", H2),
        P(
            "1. <b>Symfony/Doctrine.</b> Опыта нет. С AI закрываемо, если пробная задача зелёная.",
            LI,
        ),
        P(
            "2. <b>Фронтенд.</b> Слабее backend. Не стоп, пока задачи на API и флагах.",
            LI,
        ),
        P(
            "3. <b>Оплаты.</b> Первый ответ — флаги на фронте. Ловится в пробной задаче.",
            LI,
        ),
        P(
            "4. <b>Постановка.</b> Привык к daily/SDM. На испытательном — прямой канал, без имитации команды.",
            LI,
        ),
        KeepTogether(
            [
                P("Сильные стороны", H2),
                P("Честно обозначил отсутствие Symfony и слабость фронтенда.", LI),
                P("Платёжный сценарий Т-Банка описал по шагам: ссылка, редирект, возврат, фиксация.", LI),
                P("Для нескольких платёжных систем предлагает коннектор, а не ветвление по стране.", LI),
                P("Сравнивает модели, ловит лишние запросы у коллег.", LI),
                P("Считает стоимость двух релизов и задержку до инстанса в другой стране.", LI),
                P(
                    "Профиль: backend Laravel + рабочий AI. На эту роль — да, если пробная задача на вашей схеме зелёная.",
                    BODY,
                ),
            ]
        ),
        P(
            "Ограничение записи: почти нет реплик интервьюера, старт с середины фразы. "
            "Хранение файлов и процедура переключения в разговоре не ставились — в оценке их нет.",
            META,
        ),
    ]

    def page(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(PAPER)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(16 * mm, 10 * mm, A4[0] - 16 * mm, 10 * mm)
        canvas.setFont("Inter", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(16 * mm, 6.5 * mm, "Конфиденциально")
        canvas.drawRightString(A4[0] - 16 * mm, 6.5 * mm, str(doc_.page))
        canvas.restoreState()

    doc.build(story, onFirstPage=page, onLaterPages=page)


if __name__ == "__main__":
    build()
    print(OUT)
