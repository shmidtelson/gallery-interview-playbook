#!/usr/bin/env python3
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

pdfmetrics.registerFont(TTFont("Inter", "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"))

OUT = Path(__file__).with_name("verdict-2026-08-31.pdf")
INK = colors.HexColor("#1a1814")
MUTED = colors.HexColor("#5c564c")
LINE = colors.HexColor("#d8d0c4")
NO = colors.HexColor("#8f1d1d")
PAPER = colors.HexColor("#f6f1e8")
ROW = colors.HexColor("#efe8dc")


def style(name, **kwargs):
    base = dict(fontName="Inter", textColor=INK, leading=14)
    base.update(kwargs)
    return ParagraphStyle(name, **base)


STYLES = getSampleStyleSheet()
H1 = style("H1", fontName="Inter-Bold", fontSize=18, leading=22, spaceAfter=6)
H2 = style("H2", fontName="Inter-Bold", fontSize=11, leading=14, spaceBefore=14, spaceAfter=6)
META = style("META", fontSize=9, leading=12, textColor=MUTED)
BODY = style("BODY", fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
LI = style("LI", fontSize=10, leading=14, leftIndent=12, spaceAfter=3)
QUOTE = style(
    "QUOTE",
    fontSize=9.5,
    leading=13,
    textColor=MUTED,
    leftIndent=10,
    spaceBefore=2,
    spaceAfter=6,
)
CELL = style("CELL", fontSize=8.5, leading=11)
CELLB = style("CELLB", fontName="Inter-Bold", fontSize=8.5, leading=11)
VERDICT = style(
    "VERDICT",
    fontName="Inter-Bold",
    fontSize=16,
    leading=20,
    textColor=NO,
    spaceBefore=8,
    spaceAfter=8,
)


def p(text, st=BODY):
    return Paragraph(text, st)


def build():
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Вердикт собеседования — 31.08.2026",
        author="Техническое интервью, галереи / full-stack",
    )

    story = [
        p("Техническое интервью · full-stack галерей (PHP/Symfony + React)", META),
        p("31.08.2026 · расшифровка Video_2026-08-31_17-08-52.srt · ~47 мин", META),
        p("Не брать", VERDICT),
        p(
            "Вакансия: коммерческий Symfony, React, один человек под фаундером без дейликов. "
            "Кандидат: Laravel-бэкендер (аутстафф Ашана), коммерческого Symfony нет, "
            "фронт сейчас не пишет, кейс региона не дошёл до файлов и cutover."
        ),
        p("Оценки", H2),
    ]

    header = [
        p("Критерий", CELLB),
        p("Балл", CELLB),
        p("Факт", CELLB),
    ]
    rows = [
        [
            "PHP 8 / Symfony / Postgres",
            "1–2",
            "Laravel живой. «Коммерческого опыта симфонии не было». Doctrine — теория. Postgres/миграции не было.",
        ],
        [
            "React",
            "2",
            "Старый React/Umi. Сейчас чисто бэк. «Не так силен во фронте». Router v6 / публичные галереи — нет.",
        ],
        [
            "Кейс региона",
            "2",
            "Флаги сначала на фронте, потом инстанс + коннектор оплат. Нет блобов, очередей, rollback, 403 на API.",
        ],
        [
            "Самостоятельность",
            "2",
            "Негласный лид, ходит к SDM. Канбан, дейли, архком. Последний месяц «задач особо нету».",
        ],
        [
            "AI",
            "3",
            "Codex + китайские модели, валидирует. Риск: два месяца «только с AI», код смотрит по диагонали.",
        ],
        [
            "Плюсы (Kafka, Docker, платежи)",
            "3",
            "Kafka/Rabbit/K8s, Т-Банк. Stripe по эндпоинтам не знает. Go — книга. Next — не его.",
        ],
    ]
    data = [header]
    for crit, score, fact in rows:
        data.append([p(crit, CELLB), p(score, CELLB), p(fact, CELL)])

    table = Table(data, colWidths=[42 * mm, 14 * mm, 118 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), ROW),
                ("TEXTCOLOR", (0, 0), (-1, -1), INK),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
            ]
        )
    )
    story += [table, p("Стоп-факторы", H2)]

    stops = [
        "<b>Symfony.</b> Прямая цитата: коммерческого опыта не было. «Знаю бандлы» — не замена 2 годам в вакансии.",
        "<b>Режим работы.</b> Вам: один, задачи в 19:00, без спринтов. Ему: SDM, дейли, архком, простой без бэклога.",
        "<b>Кейс не про галереи.</b> Копия инстанса, валюта, юрлицо. Не фото, не zip/watermark, не ссылка клиента в момент копирования.",
        "<b>Нет вопросов про продукт.</b> ImageProxy и «не имею представления, что как».",
        "<b>AI-автопилот.</b> Инструмент взрослый, но два месяца пишет только агентом и ревьюит по диагонали. Ревьюера у вас не будет.",
    ]
    for item in stops:
        story.append(p("• " + item, LI))

    story += [
        p("Что было сильно", H2),
        p("• Не врал про Symfony и фронт.", LI),
        p("• Т-Банк руками: ссылка → редирект → возврат в корзину. Не «Stripe сам всё делает».", LI),
        p("• Коннектор оплат вместо if по стране.", LI),
        p("• AI: сравнивает модели, оставляет финальное слово за собой, ловит N+1 у коллег.", LI),
        p("Цитаты", H2),
        p("«Чтобы коммерческого опыта симфонии, ну, я бы сказал, не было.»", QUOTE),
        p("«Не так я силен во фронте, как силен в бэке.»", QUOTE),
        p("«Последние, наверное, два месяца только пишу с помощью AI.» / код «по диагонали».", QUOTE),
        p("«Последний, наверное, месяц задач особо нету.»", QUOTE),
        p("«Я бы делал всё-таки фичи флаги, но это именно корректно на том же самом фронте.»", QUOTE),
        p("«Я даже не имею представления, что как.»", QUOTE),
        p("Если всё же тестировать", H2),
        p(
            "Не как единственный full-stack. Только бэк на платежи/флаги. "
            "Кусок: выключить магазин на API (не кнопкой) и прогнать платёж/вебхук. "
            "Если без агента не читает чужую Doctrine-схему — стоп. "
            "Плюсы (Kafka, K8s) дыру в Symfony не закрывают."
        ),
        p(
            "Ограничение: SRT без реплик интервьюера, старт с середины фразы. "
            "Вердикт по речи кандидата. Symfony в проде в первой минуте не звучал.",
            META,
        ),
    ]

    def page(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(PAPER)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(18 * mm, 12 * mm, A4[0] - 18 * mm, 12 * mm)
        canvas.setFont("Inter", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 8 * mm, "Не для кандидата")
        canvas.drawRightString(A4[0] - 18 * mm, 8 * mm, f"{doc_.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=page, onLaterPages=page)


if __name__ == "__main__":
    build()
    print(OUT)
