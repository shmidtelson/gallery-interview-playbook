"use client";

import { Eye, EyeOff } from "lucide-react";
import { QuestionCard } from "@/components/question-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { sectionByElapsed, sections, type Section } from "@/lib/interview";
import { cn } from "@/lib/utils";

export function LiveView({
  activeId,
  onSelect,
  elapsedMin,
  notes,
  onNote,
  asked,
  onToggleAsked,
  showKeys,
  onToggleKeys,
}: {
  activeId: string;
  onSelect: (id: string) => void;
  elapsedMin: number;
  notes: Record<string, string>;
  onNote: (sectionId: string, value: string) => void;
  asked: string[];
  onToggleAsked: (questionId: string) => void;
  showKeys: boolean;
  onToggleKeys: () => void;
}) {
  const suggested = sectionByElapsed(elapsedMin);
  const active = sections.find((s) => s.id === activeId) ?? sections[0];

  return (
    <div className="grid gap-6 lg:grid-cols-[240px_minmax(0,1fr)]">
      <nav className="lg:sticky lg:top-24 lg:self-start">
        <p className="text-muted-foreground mb-2 text-[11px] font-medium tracking-wide uppercase">
          Ход часа
        </p>
        <ol className="flex gap-2 overflow-x-auto pb-2 lg:flex-col lg:overflow-visible lg:pb-0">
          {sections.map((section) => (
            <li key={section.id} className="min-w-[11rem] lg:min-w-0">
              <button
                type="button"
                onClick={() => onSelect(section.id)}
                className={cn(
                  "w-full rounded-lg border px-3 py-2.5 text-left transition-colors",
                  active.id === section.id
                    ? "border-amber-500/40 bg-amber-500/10"
                    : "hover:bg-muted/40 border-transparent bg-transparent",
                  suggested.id === section.id &&
                    active.id !== section.id &&
                    "border-dashed border-foreground/20"
                )}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-[11px] text-amber-500/90">
                    {section.time}
                  </span>
                  {suggested.id === section.id ? (
                    <Badge variant="secondary">сейчас</Badge>
                  ) : null}
                </div>
                <div className="mt-1 text-sm leading-snug font-medium">
                  {section.title}
                </div>
              </button>
            </li>
          ))}
        </ol>
      </nav>

      <div className="space-y-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="max-w-2xl">
            <p className="font-mono text-xs text-amber-500/90">{active.time} мин</p>
            <h2 className="font-heading mt-1 text-2xl leading-tight sm:text-3xl">
              {active.title}
            </h2>
            <p className="text-muted-foreground mt-2 leading-relaxed">
              {active.goal}
            </p>
          </div>
          <Button
            type="button"
            variant={showKeys ? "secondary" : "outline"}
            onClick={onToggleKeys}
          >
            {showKeys ? <EyeOff /> : <Eye />}
            {showKeys ? "Скрыть ключи" : "Показать ключи"}
          </Button>
        </div>

        {active.readAloud ? (
          <blockquote className="border-amber-500/40 bg-amber-500/8 rounded-xl border-l-4 px-4 py-3 text-sm leading-relaxed sm:text-base">
            <p className="mb-1 text-[11px] font-medium tracking-wide text-amber-500/90 uppercase">
              Зачитать и замолчать
            </p>
            {active.readAloud}
          </blockquote>
        ) : null}

        <Facilitation section={active} />

        <div className="space-y-3">
          {active.questions.map((question) => (
            <QuestionCard
              key={question.id}
              question={question}
              asked={asked.includes(question.id)}
              onToggleAsked={() => onToggleAsked(question.id)}
              showKeys={showKeys}
            />
          ))}
        </div>

        <div>
          <label
            htmlFor={`notes-${active.id}`}
            className="mb-1.5 block text-sm font-medium"
          >
            Заметки по блоку
          </label>
          <Textarea
            id={`notes-${active.id}`}
            value={notes[active.id] ?? ""}
            onChange={(event) => onNote(active.id, event.target.value)}
            placeholder="Цитаты, дыры, что переспросить в следующем блоке"
            className="min-h-28"
          />
        </div>
      </div>
    </div>
  );
}

function Facilitation({ section }: { section: Section }) {
  return (
    <div className="bg-muted/30 rounded-xl px-4 py-3">
      <p className="text-muted-foreground mb-2 text-[11px] font-medium tracking-wide uppercase">
        Как вести этот кусок
      </p>
      <ul className="space-y-1.5 text-sm leading-relaxed">
        {section.facilitation.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
