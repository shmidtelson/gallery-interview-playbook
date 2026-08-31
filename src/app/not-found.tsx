export default function NotFound() {
  return (
    <main className="mx-auto flex min-h-svh max-w-lg flex-col justify-center px-6">
      <p className="text-[11px] font-medium tracking-[0.18em] text-amber-500/90 uppercase">
        404
      </p>
      <h1 className="font-heading mt-2 text-3xl">Такой страницы нет</h1>
      <p className="text-muted-foreground mt-3 leading-relaxed">
        Сценарий собеседования живёт на главной. Вернитесь туда и откройте
        вкладку «Созвон».
      </p>
      <a href="./" className="mt-6 text-sm text-amber-400 underline-offset-4 hover:underline">
        На главную
      </a>
    </main>
  );
}
