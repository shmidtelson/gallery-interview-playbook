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
RULE = colors.HexColor("#8f1d1d")
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
        P("Рекомендация: отказ", DEC),
        P(
            "Оценка только по сказанному в разговоре. Темы, которые интервьюер не ставил "
            "(хранение фото, процедура переключения), в баллах не участвуют."
        ),
        P(
            "Кандидата на эту позицию не нанимать. Роль требует коммерческий Symfony, React "
            "и работу с фаундером без спринтов. Кандидат — backend на Laravel в аутстаффе. "
            "Коммерческого Symfony нет. React сейчас не пишет. Формат работы — команда, daily, "
            "SDM. Риск по стеку и контуру управления, не по недосказанному кейсу."
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
                    "Нет",
                    "Коммерческого опыта нет. Doctrine — на уровне сравнения с Active Record.",
                ],
                [
                    "React, router v6",
                    "Нет",
                    "Краткий опыт в прошлом. Сейчас только backend. Фронтенд сам считает слабой стороной.",
                ],
                [
                    "PostgreSQL, Doctrine",
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
                    "Да, с риском",
                    "Агенты и проверка результата. Два месяца пишет в основном через AI, просмотр поверхностный.",
                ],
                [
                    "Работа без спринтов",
                    "Нет",
                    "Канбан, daily, SDM, архком. При пустом бэклоге простой около месяца.",
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
            "Обязательные пункты по Symfony, React и формату работы не закрыты. "
            "Kafka, Kubernetes и платежи это не компенсируют.",
            BODY,
        ),
        P("Оценка компетенций", H2),
        P("Шкала: 1 слабо · 2 ниже порога роли · 3 приемлемо · 4 сильно", META),
        Spacer(1, 2 * mm),
        table(
            [
                ["Компетенция", "Балл", "Смысл для найма"],
                [
                    "PHP / Symfony / данные",
                    "2",
                    "Закроет Laravel. Не закроет ваш Symfony и Doctrine без обучения на вашей базе.",
                ],
                [
                    "React",
                    "2",
                    "Не закрывает публичные галереи.",
                ],
                [
                    "Кейс (как задали)",
                    "3",
                    "Флаги, коннектор оплат, второй инстанс, данные. Первый импульс — флаги на фронте. По базе — «зависит от схемы».",
                ],
                [
                    "Автономия",
                    "2",
                    "Силён как неформальный лид в команде. Продукт без внешнего потока задач сам не ведёт.",
                ],
                [
                    "AI",
                    "3",
                    "Применяет сознательно. Без второго ревьюера опасен режим «агент пишет — человек смотрит по диагонали».",
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
            "таблицей — «зависит от схемы». По заданным темам это 3: достаточно для обсуждения "
            "в команде, не жёсткий план единственного архитектора."
        ),
        P("Риски при найме на текущую роль", H2),
        P(
            "1. <b>Срок выхода.</b> Нужно осваивать Symfony на вашей базе. Один исполнитель — простой поставки.",
            LI,
        ),
        P(
            "2. <b>Фронтенд.</b> Сам сказал, что фронтенд слабее backend. Клиентскую галерею в интервью не разбирали.",
            LI,
        ),
        P(
            "3. <b>Оплаты.</b> Первый ответ — флаги на фронте; коннектор на backend тоже назвал. Риск в спешке выключить только меню.",
            LI,
        ),
        P(
            "4. <b>Контур управления.</b> Daily и SDM. Около месяца без задач при пустом бэклоге.",
            LI,
        ),
        P(
            "5. <b>AI без второго ревьюера.</b> Два месяца пишет в основном агентом, просмотр поверхностный.",
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
                    "Профиль: mid-level backend Laravel в команде. Не единственный full-stack на эту вакансию.",
                    BODY,
                ),
            ]
        ),
        P("Дальнейшие действия", H2),
        P(
            "По этой вакансии — отказ. Рассматривать как узкий backend (платежи, флаги, интеграции) "
            "только если роль будет изменена и Symfony/React закроет другой человек. "
            "Пока роль не менялась, этот путь не предлагается."
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
