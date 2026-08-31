"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { criteria, TOTAL_MINUTES } from "@/lib/interview";

const STORAGE_KEY = "vigbo-interview-session-v1";
const TOTAL_SECONDS = TOTAL_MINUTES * 60;

export type Scores = Record<string, number>;

export type SessionState = {
  candidate: string;
  notes: Record<string, string>;
  asked: string[];
  scores: Scores;
  verdictNote: string;
  remaining: number;
};

const emptyScores = (): Scores =>
  Object.fromEntries(criteria.map((c) => [c.id, 0]));

const defaultState = (): SessionState => ({
  candidate: "",
  notes: {},
  asked: [],
  scores: emptyScores(),
  verdictNote: "",
  remaining: TOTAL_SECONDS,
});

function loadState(): SessionState {
  if (typeof window === "undefined") return defaultState();
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultState();
    const parsed = JSON.parse(raw) as Partial<SessionState>;
    return {
      ...defaultState(),
      ...parsed,
      scores: { ...emptyScores(), ...parsed.scores },
      notes: parsed.notes ?? {},
      asked: parsed.asked ?? [],
    };
  } catch {
    return defaultState();
  }
}

export function useInterviewSession() {
  const [hydrated, setHydrated] = useState(false);
  const [state, setState] = useState<SessionState>(defaultState);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    setState(loadState());
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state, hydrated]);

  useEffect(() => {
    if (!running) return;
    const id = window.setInterval(() => {
      setState((prev) => {
        if (prev.remaining <= 0) return prev;
        return { ...prev, remaining: prev.remaining - 1 };
      });
    }, 1000);
    return () => window.clearInterval(id);
  }, [running]);

  useEffect(() => {
    if (state.remaining <= 0 && running) setRunning(false);
  }, [state.remaining, running]);

  const setCandidate = useCallback((candidate: string) => {
    setState((prev) => ({ ...prev, candidate }));
  }, []);

  const setNote = useCallback((sectionId: string, value: string) => {
    setState((prev) => ({
      ...prev,
      notes: { ...prev.notes, [sectionId]: value },
    }));
  }, []);

  const toggleAsked = useCallback((questionId: string) => {
    setState((prev) => {
      const has = prev.asked.includes(questionId);
      return {
        ...prev,
        asked: has
          ? prev.asked.filter((id) => id !== questionId)
          : [...prev.asked, questionId],
      };
    });
  }, []);

  const setScore = useCallback((criterionId: string, value: number) => {
    setState((prev) => ({
      ...prev,
      scores: { ...prev.scores, [criterionId]: value },
    }));
  }, []);

  const setVerdictNote = useCallback((verdictNote: string) => {
    setState((prev) => ({ ...prev, verdictNote }));
  }, []);

  const resetTimer = useCallback(() => {
    setRunning(false);
    setState((prev) => ({ ...prev, remaining: TOTAL_SECONDS }));
  }, []);

  const resetSession = useCallback(() => {
    setRunning(false);
    setState(defaultState());
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const elapsedMin = useMemo(
    () => (TOTAL_SECONDS - state.remaining) / 60,
    [state.remaining]
  );

  const exportMarkdown = useCallback(() => {
    const lines: string[] = [
      `# Собеседование${state.candidate ? `: ${state.candidate}` : ""}`,
      "",
      `Дата: ${new Date().toLocaleString("ru-RU")}`,
      "",
      "## Оценки",
      ...criteria.map((c) => {
        const n = state.scores[c.id] ?? 0;
        return `- ${c.title}: ${n ? `${n}/4` : "—"}`;
      }),
      "",
      "## Заметки",
      ...Object.entries(state.notes)
        .filter(([, text]) => text.trim())
        .map(([id, text]) => `### ${id}\n\n${text.trim()}`),
      "",
      "## Вердикт",
      state.verdictNote.trim() || "—",
    ];
    return lines.join("\n");
  }, [state]);

  return {
    hydrated,
    state,
    running,
    setRunning,
    setCandidate,
    setNote,
    toggleAsked,
    setScore,
    setVerdictNote,
    resetTimer,
    resetSession,
    elapsedMin,
    exportMarkdown,
  };
}
