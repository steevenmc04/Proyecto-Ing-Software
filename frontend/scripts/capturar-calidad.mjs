import { spawnSync } from "node:child_process";
import { writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "@playwright/test";

const actual = dirname(fileURLToPath(import.meta.url));
const frontend = resolve(actual, "..");
const raiz = resolve(frontend, "..");
const evidencias = resolve(raiz, "docs", "evidencias");
const npm = "npm";
const python = process.env.PYTHON || "python";

const limpiarAnsi = (texto) =>
  texto
    .replace(/\u001b\[[0-?]*[ -/]*[@-~]/g, "")
    .replace(/\r/g, "")
    .trim();

function ejecutar(nombre, comando, argumentos, cwd) {
  const usaCmd = process.platform === "win32" && comando === npm;
  const ejecutable = usaCmd ? process.env.ComSpec || "cmd.exe" : comando;
  const argumentosReales = usaCmd
    ? ["/d", "/s", "/c", [comando, ...argumentos].join(" ")]
    : argumentos;
  const resultado = spawnSync(ejecutable, argumentosReales, {
    cwd,
    encoding: "utf8",
    env: { ...process.env, FORCE_COLOR: "0", NO_COLOR: "1" },
    maxBuffer: 20 * 1024 * 1024,
  });
  const salida = limpiarAnsi(
    [resultado.stdout, resultado.stderr].filter(Boolean).join("\n"),
  );
  if (resultado.status !== 0) {
    const detalle = resultado.error?.message || salida;
    throw new Error(`${nombre} fallo con codigo ${resultado.status}\n${detalle}`);
  }
  return {
    nombre,
    comando: [comando, ...argumentos].join(" "),
    salida,
  };
}

const resultados = [
  ejecutar("Backend, cobertura y Ruff", python, ["-m", "ruff", "check", "app", "tests", "seed.py", "scripts"], raiz),
  ejecutar("Pruebas backend y cobertura", python, ["-m", "pytest", "-q"], raiz),
  ejecutar("Pruebas frontend", npm, ["test"], frontend),
  ejecutar("Pruebas E2E", npm, ["run", "test:e2e"], frontend),
  ejecutar("Build de produccion", npm, ["run", "build"], frontend),
];

const escapar = (valor) =>
  valor
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

async function capturar(titulo, items, archivo) {
  const bloques = items
    .map(
      (item) => `
        <section>
          <div class="resultado"><span>APROBADO</span><code>${escapar(item.comando)}</code></div>
          <h2>${escapar(item.nombre)}</h2>
          <pre>${escapar(item.salida)}</pre>
        </section>`,
    )
    .join("");

  await page.setContent(`<!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8">
        <style>
          * { box-sizing: border-box; }
          body { margin: 0; background: #eef2f5; color: #17212b; font: 16px Arial, sans-serif; }
          header { padding: 30px 44px; background: #123c52; color: white; }
          h1 { margin: 0 0 8px; font-size: 29px; letter-spacing: 0; }
          header p { margin: 0; color: #d6e5eb; }
          main { padding: 24px 44px 36px; }
          section { margin-bottom: 20px; padding: 20px; border: 1px solid #cbd5dc; border-radius: 6px; background: white; }
          h2 { margin: 14px 0 10px; font-size: 19px; }
          .resultado { display: flex; align-items: center; gap: 12px; }
          .resultado span { padding: 5px 9px; border-radius: 4px; background: #d8f3e5; color: #12633a; font-size: 12px; font-weight: 700; }
          code { color: #365261; font: 13px Consolas, monospace; }
          pre { margin: 0; padding: 16px; overflow: hidden; background: #101820; color: #e8f0f3; font: 12px/1.45 Consolas, monospace; white-space: pre-wrap; }
        </style>
      </head>
      <body>
        <header>
          <h1>${escapar(titulo)}</h1>
          <p>Sistema de Gestion de Caja de Ahorros - ejecucion automatica real</p>
        </header>
        <main>${bloques}</main>
      </body>
    </html>`);

  await page.screenshot({
    path: resolve(evidencias, archivo),
    fullPage: true,
  });
}

await capturar("Pruebas automatizadas", resultados.slice(0, 4), "15_pruebas.png");
await capturar("Cobertura backend", [resultados[1]], "16_cobertura.png");
await capturar("Build final del frontend", [resultados[4]], "17_build_final.png");
await browser.close();

const pytest = resultados[1].salida;
const pruebasBackend = pytest.match(/(\d+) passed/)?.[1] ?? "no detectado";
const cobertura = pytest.match(/Total coverage: ([0-9.]+%)/)?.[1] ?? "no detectada";
const e2e = resultados[3].salida.match(/(\d+) passed/)?.[1] ?? "no detectado";
const frontendTests = resultados[2].salida.match(/Tests\s+(\d+) passed/)?.[1] ?? "no detectado";

writeFileSync(
  resolve(evidencias, "RESULTADOS_VERIFICACION.md"),
  `# Resultados de verificacion

Resultados generados por \`npm run evidencias:calidad\` a partir de comandos reales.

| Verificacion | Resultado |
|---|---|
| Ruff | Aprobado |
| Pruebas backend | ${pruebasBackend} aprobadas |
| Cobertura backend | ${cobertura} |
| Pruebas frontend | ${frontendTests} aprobadas |
| Pruebas E2E | ${e2e} aprobadas |
| Build Vite | Aprobado |

Evidencias: \`15_pruebas.png\`, \`16_cobertura.png\` y
\`17_build_final.png\`.
`,
  "utf8",
);

console.log("Evidencias de calidad generadas correctamente.");
