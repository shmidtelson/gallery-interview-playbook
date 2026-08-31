"use client";

import { useMemo, useState } from "react";
import { BriefingView } from "@/components/briefing-view";
import { LiveView } from "@/components/live-view";
import { SessionTimer } from "@/components/session-timer";
import { VerdictView } from "@/components/verdict-view";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useInterviewSession } from "@/hooks/use-interview-session";
import { sectionByElapsed, sections } from "@/lib/interview";

export function InterviewConsole() {
  const session = useInterviewSession();
  const [tab, setTab] = useState("briefing");
  const [activeSection, setActiveSection] = useState(sections[0].id);
  const [showKeys, setShowKeys] = useState(true);

  const suggested = useMemo(
    () => sectionByElapsed(session.elapsedMin),
    [session.elapsedMin]
  );

  if (!session.hydrated) {
    return (
      <div className="text-muted-foreground flex min-h-svh items-center justify-center text-sm">
        Собираю сценарий…
      </div>
    );
  }

  return (
    <TooltipProvider>
      <div className="min-h-svh">
        <header className="border-foreground/10 bg-background/80 sticky top-0 z-20 border-b backdrop-blur-md">
          <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-3 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
            <div className="min-w-0">
              <p className="text-[11px] font-medium tracking-[0.18em] text-amber-500/90 uppercase">
                Галереи · Full-stack · 60 минут
              </p>
              <div className="mt-1 flex flex-wrap items-center gap-2">
                <Input
                  value={session.state.candidate}
                  onChange={(event) => session.setCandidate(event.target.value)}
                  placeholder="Имя кандидата"
                  className="h-8 max-w-56"
                  aria-label="Имя кандидата"
                />
                <span className="text-muted-foreground hidden text-sm sm:inline">
                  По таймеру сейчас: {suggested.time} · {suggested.title}
                </span>
              </div>
            </div>
            <SessionTimer
              remaining={session.state.remaining}
              running={session.running}
              elapsedMin={session.elapsedMin}
              onToggle={() => session.setRunning(!session.running)}
              onReset={session.resetTimer}
            />
          </div>
        </header>

        <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
          <Tabs value={tab} onValueChange={setTab}>
            <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
              <TabsList className="h-auto">
                <TabsTrigger value="briefing">Зачем так</TabsTrigger>
                <TabsTrigger value="live">Созвон</TabsTrigger>
                <TabsTrigger value="verdict">Вердикт</TabsTrigger>
              </TabsList>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={session.resetSession}
              >
                Сбросить сессию
              </Button>
            </div>

            <TabsContent value="briefing">
              <BriefingView />
            </TabsContent>
            <TabsContent value="live">
              <LiveView
                activeId={activeSection}
                onSelect={setActiveSection}
                elapsedMin={session.elapsedMin}
                notes={session.state.notes}
                onNote={session.setNote}
                asked={session.state.asked}
                onToggleAsked={session.toggleAsked}
                showKeys={showKeys}
                onToggleKeys={() => setShowKeys((value) => !value)}
              />
            </TabsContent>
            <TabsContent value="verdict">
              <VerdictView
                scores={session.state.scores}
                onScore={session.setScore}
                notes={session.state.notes}
                verdictNote={session.state.verdictNote}
                onVerdictNote={session.setVerdictNote}
                exportMarkdown={session.exportMarkdown}
              />
            </TabsContent>
            </Tabs>
          <p className="text-muted-foreground mt-10 border-t border-foreground/10 pt-4 text-xs">
            Не шарьте этот экран кандидату — во вкладке «Созвон» есть ключи
            сильных и слабых ответов. Заметки остаются только в этом браузере.
          </p>
        </main>
      </div>
    </TooltipProvider>
  );
}
