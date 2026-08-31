"use client";

import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import type { Question } from "@/lib/interview";
import { cn } from "@/lib/utils";

export function QuestionCard({
  question,
  asked,
  onToggleAsked,
  showKeys,
}: {
  question: Question;
  asked: boolean;
  onToggleAsked: () => void;
  showKeys: boolean;
}) {
  return (
    <article
      className={cn(
        "rounded-xl border bg-card/60 p-4",
        asked && "border-primary/30"
      )}
    >
      <div className="flex items-start gap-3">
        <Checkbox
          checked={asked}
          onCheckedChange={() => onToggleAsked()}
          aria-label="Вопрос задан"
          className="mt-1"
        />
        <div className="min-w-0 flex-1 space-y-3">
          <div>
            <p className="text-[11px] font-medium tracking-wide text-amber-500/90 uppercase">
              Сказать
            </p>
            <p className="text-base leading-snug font-medium text-pretty">
              {question.ask}
            </p>
            <p className="text-muted-foreground mt-1.5 text-sm leading-relaxed">
              {question.why}
            </p>
            {question.nudge ? (
              <p className="mt-2 text-sm text-amber-200/80">{question.nudge}</p>
            ) : null}
          </div>

          {question.followUps.length > 0 ? (
            <div>
              <p className="text-muted-foreground mb-1 text-[11px] font-medium tracking-wide uppercase">
                Если отвечает плоско
              </p>
              <ul className="space-y-1 text-sm leading-relaxed">
                {question.followUps.map((item) => (
                  <li key={item} className="pl-3 -indent-3">
                    — {item}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}

          {showKeys ? (
            <div className="grid gap-3 sm:grid-cols-2">
              <SignalList tone="strong" items={question.strong} />
              <SignalList tone="weak" items={question.weak} />
            </div>
          ) : (
            <Badge variant="outline" className="text-muted-foreground">
              Подсказки скрыты
            </Badge>
          )}
        </div>
      </div>
    </article>
  );
}

function SignalList({
  tone,
  items,
}: {
  tone: "strong" | "weak";
  items: string[];
}) {
  return (
    <div
      className={cn(
        "rounded-lg px-3 py-2.5 text-sm leading-relaxed",
        tone === "strong"
          ? "bg-emerald-500/8 text-emerald-100/90"
          : "bg-rose-500/8 text-rose-100/90"
      )}
    >
      <p className="mb-1.5 text-[11px] font-semibold tracking-wide uppercase">
        {tone === "strong" ? "Сильный" : "Слабый"}
      </p>
      <ul className="space-y-1">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
