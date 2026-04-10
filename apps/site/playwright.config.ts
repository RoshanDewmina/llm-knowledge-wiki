import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  forbidOnly: true,
  retries: 0,
  reporter: "line",
  use: {
    baseURL: "http://127.0.0.1:3001",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "bun --bun next start --hostname 127.0.0.1 --port 3001",
    url: "http://127.0.0.1:3001",
    reuseExistingServer: false,
    timeout: 120000,
    cwd: ".",
  },
  projects: [
    {
      name: "desktop-chromium",
      use: { browserName: "chromium", ...devices["Desktop Chrome"] },
    },
    {
      name: "tablet-chromium",
      use: { browserName: "chromium", ...devices["iPad (gen 7)"] },
    },
    {
      name: "mobile-chromium",
      use: { browserName: "chromium", ...devices["iPhone 14"] },
    },
  ],
});
