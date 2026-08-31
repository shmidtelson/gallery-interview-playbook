"use client";

import { Copy } from "lucide-react";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import {
  criteria,
  scoreLabels,
  sections,
  verdictGuide,
} from "@/lib/interview";
import { cn } from "@/lib/utils";

export function VerdictView({
  scores,
  onScore,
  notes,
  verdictNote,
  onVerdictNote,
  exportMarkdown,
}: {
  scores: Record<string, number>;
  onScore: (id: string, value: number) => void;
  notes: Record<string, string>;
  verdictNote: string;
  onVerdictNote: (value: string) => void;
  exportMarkdown: () => string;
}) {
  const [copied, setCopied] = useState(false);
  const filled = criteria.filter((c) => (scores[c.id] ?? 0) > 0);
  const must = criteria.filter((c) => c.must);
  const mustAvg =
    must.reduce((sum, c) => sum + (scores[c.id] ?? 0), 0) /
    Math.max(
      1,
      must.filter((c) => (scores[c.id] ?? 0) > 0).length
    );
  const suggestion =
    filled.length < 4
      ? "Сначала проставьте обязательные оценки — подсказка появится сама."
      : mustAvg >= 3.4
        ? "Скорее брать. Плюсы можно не добирать."
        : mustAvg >= 2.6
          ? "Брать с оговоркой: испытательный кусок на флаге магазина, не «выйдет на работу и разберётся»."
          : "Скорее не брать. Дыра в обязательном, плюсы не спасут.";

  async function copyNotes() {
    await navigator.clipboard.writeText(exportMarkdown());
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  return (
    <div className="space-y-8">
      <header className="max-w-2xl space-y-2">
        <h2 className="font-heading text-3xl">Вердикт, пока память свежая</h2>
        <p className="text-muted-foreground leading-relaxed">
          Ставьте 1–4 сразу после звонка. Не усредняйте «приятный человек» с
          Symfony. Плюсы не закрывают дыру в обязательном.
        </p>
      </header>

      <div className="grid gap-4">
        {criteria.map((criterion) => {
          const value = scores[criterion.id] ?? 0;
          return (
            <Card key={criterion.id} className="bg-card/70">
              <CardHeader className="flex flex-row items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <CardTitle className="text-base">{criterion.title}</CardTitle>
                    {criterion.must ? (
                      <Badge>обязательно</Badge>
                    ) : (
                      <Badge variant="outline">плюс</Badge>
                    )}
                  </div>
                  <p className="text-muted-foreground mt-1 text-sm">
                    {criterion.hint}
                  </p>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-1.5">
                  {[1, 2, 3, 4].map((n) => (
                    <Button
                      key={n}
                      type="button"
                      size="sm"
                      variant={value === n ? "default" : "outline"}
                      onClick={() => onScore(criterion.id, n)}
                      className={cn(value === n && "bg-amber-500 text-zinc-950")}
                    >
                      {n} · {scoreLabels[n]}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <Card className="border-amber-500/30 bg-amber-500/8">
        <CardHeader>
          <CardTitle>Подсказка по сумме</CardTitle>
        </CardHeader>
        <CardContent className="leading-relaxed">{suggestion}</CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-3">
        {verdictGuide.map((item) => (
          <Card key={item.id} className="bg-card/70">
            <CardHeader>
              <CardTitle>{item.title}</CardTitle>
            </CardHeader>
            <CardContent className="text-muted-foreground text-sm leading-relaxed">
              {item.when}
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="space-y-2">
        <label htmlFor="verdict-note" className="text-sm font-medium">
          Решение своими словами
        </label>
        <Textarea
          id="verdict-note"
          value={verdictNote}
          onChange={(event) => onVerdictNote(event.target.value)}
          placeholder="Брать / с оговоркой / нет. Одна причина. Что проверить на испытательном, если берёте."
          className="min-h-32"
        />
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <Button type="button" onClick={copyNotes}>
          <Copy />
          {copied ? "Скопировано" : "Скопировать заметки"}
        </Button>
        <p className="text-muted-foreground text-sm">
          В буфер попадёт markdown: оценки, заметки по блокам, вердикт.
        </p>
      </div>

      <section>
        <h3 className="mb-3 text-sm font-medium">Заметки с созвона</h3>
        <div className="grid gap-3">
          {sections.map((section) => {
            const text = notes[section.id]?.trim();
            if (!text) return null;
            return (
              <Card key={section.id} size="sm" className="bg-card/70">
                <CardHeader>
                  <CardTitle className="text-sm">{section.title}</CardTitle>
                </CardHeader>
                <CardContent className="whitespace-pre-wrap leading-relaxed">
                  {text}
                </CardContent>
              </Card>
            );
          })}
          {!sections.some((section) => notes[section.id]?.trim()) ? (
            <p className="text-muted-foreground text-sm">
              Пока пусто — пишите в блоке «Созвон», сюда подтянется.
            </p>
          ) : null}
        </div>
      </section>
    </div>
  );
}
