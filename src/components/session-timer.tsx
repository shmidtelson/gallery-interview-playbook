"use client";

import { Pause, Play, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TOTAL_MINUTES } from "@/lib/interview";
import { cn } from "@/lib/utils";

function formatTime(totalSeconds: number) {
  const clamped = Math.max(0, totalSeconds);
  const m = Math.floor(clamped / 60);
  const s = clamped % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export function SessionTimer({
  remaining,
  running,
  onToggle,
  onReset,
  elapsedMin,
}: {
  remaining: number;
  running: boolean;
  onToggle: () => void;
  onReset: () => void;
  elapsedMin: number;
}) {
  const overtime = remaining <= 0;
  const late = remaining > 0 && remaining < 5 * 60;

  return (
    <div className="flex items-center gap-2">
      <div
        className={cn(
          "font-mono text-2xl font-semibold tabular-nums tracking-tight",
          overtime && "text-destructive",
          late && !overtime && "text-amber-400"
        )}
      >
        {formatTime(remaining)}
      </div>
      <div className="text-muted-foreground hidden text-xs sm:block">
        / {TOTAL_MINUTES}:00
        <div>
          прошло {Math.max(0, Math.floor(elapsedMin))} мин
        </div>
      </div>
      <Button
        type="button"
        size="icon"
        variant={running ? "secondary" : "default"}
        onClick={onToggle}
        aria-label={running ? "Пауза" : "Старт"}
      >
        {running ? <Pause /> : <Play />}
      </Button>
      <Button
        type="button"
        size="icon"
        variant="ghost"
        onClick={onReset}
        aria-label="Сбросить таймер"
      >
        <RotateCcw />
      </Button>
    </div>
  );
}
