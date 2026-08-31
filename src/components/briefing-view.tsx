"use client";

import { briefing, greenFlags, redFlags } from "@/lib/interview";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function BriefingView() {
  return (
    <div className="space-y-8">
      <header className="max-w-3xl space-y-3">
        <p className="text-[11px] font-medium tracking-[0.2em] text-amber-500/90 uppercase">
          Сценарий на 60 минут
        </p>
        <h1 className="font-heading text-3xl leading-tight text-pretty sm:text-4xl">
          {briefing.headline}
        </h1>
        <p className="text-muted-foreground text-base leading-relaxed text-pretty">
          Роль — единственный full-stack под фаундером: PHP 8 / Symfony, React,
          Postgres, галереи фотографов. Час нужен не чтобы «проверить уровень»,
          а чтобы увидеть, разберётся ли человек в сути переезда и выключения
          функций — или будет закрывать тикеты вслепую.
        </p>
      </header>

      <div className="grid gap-4 lg:grid-cols-3">
        {briefing.decisions.map((item) => (
          <Card key={item.id} className="bg-card/70">
            <CardHeader className="border-b">
              <Badge variant="secondary">{item.verdict}</Badge>
              <CardTitle className="text-lg leading-snug">{item.title}</CardTitle>
            </CardHeader>
            <CardContent className="text-muted-foreground leading-relaxed">
              {item.body}
            </CardContent>
          </Card>
        ))}
      </div>

      <section className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <Card className="bg-card/70">
          <CardHeader>
            <CardTitle>Как вести час</CardTitle>
          </CardHeader>
          <CardContent>
            <ol className="space-y-3 text-sm leading-relaxed">
              {briefing.principles.map((item, index) => (
                <li key={item} className="flex gap-3">
                  <span className="font-mono text-amber-500/90">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span>{item}</span>
                </li>
              ))}
            </ol>
          </CardContent>
        </Card>

        <Card className="bg-card/70">
          <CardHeader>
            <CardTitle>До звонка</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3 text-sm leading-relaxed">
              {briefing.preCall.map((item) => (
                <li key={item} className="border-foreground/10 border-l-2 pl-3">
                  {item}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <FlagCard title="Зелёные" tone="strong" items={greenFlags} />
        <FlagCard title="Красные" tone="weak" items={redFlags} />
      </section>
    </div>
  );
}

function FlagCard({
  title,
  tone,
  items,
}: {
  title: string;
  tone: "strong" | "weak";
  items: string[];
}) {
  return (
    <Card className="bg-card/70">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2.5 text-sm leading-relaxed">
          {items.map((item) => (
            <li
              key={item}
              className={
                tone === "strong"
                  ? "text-emerald-100/90"
                  : "text-rose-100/85"
              }
            >
              {item}
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
