import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests-e2e',
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: [['list'], ['html', { outputFolder: 'playwright-report', open: 'never' }]],
  expect: {
    timeout: 15_000,
  },
  use: {
    baseURL: 'http://127.0.0.1:5173',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: [
    {
      command:
        'python scripts/preparar_e2e.py && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000',
      cwd: '..',
      env: {
        DATABASE_URL: 'sqlite:///./e2e_caja_ahorros.db',
        ORIGENES_CORS: 'http://127.0.0.1:5173',
      },
      url: 'http://127.0.0.1:8000/api/v1/salud',
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
    },
    {
      command: 'npm run dev -- --host 127.0.0.1 --port 5173',
      url: 'http://127.0.0.1:5173/login',
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
    },
  ],
})
