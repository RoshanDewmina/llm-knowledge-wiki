import type { Page } from "@playwright/test";
import { expect, test } from "@playwright/test";

function attachErrorCollectors(page: Page) {
  const consoleErrors: string[] = [];
  const pageErrors: string[] = [];

  page.on("console", (message) => {
    if (message.type() === "error") {
      consoleErrors.push(message.text());
    }
  });

  page.on("pageerror", (error) => {
    pageErrors.push(String(error));
  });

  return {
    assertClean() {
      expect.soft(consoleErrors, "unexpected browser console errors").toEqual([]);
      expect.soft(pageErrors, "unexpected page errors").toEqual([]);
    },
  };
}

test.describe("wiki reader", () => {
  test("renders the main wiki routes", async ({ page }) => {
    const errors = attachErrorCollectors(page);

    await page.goto("/");
    await expect(page.locator(".pageTitle")).toHaveText("Wiki Index");
    const viewport = page.viewportSize();
    if (viewport && viewport.width <= 880) {
      await expect(page.locator(".mobileDrawer")).toBeVisible();
    } else {
      await expect(page.getByText("LLM Knowledge Wiki").first()).toBeVisible();
    }

    await page.goto("/concepts/transformer-architecture");
    await expect(page.locator(".pageTitle")).toHaveText("Transformer Architecture");
    await expect(page.getByRole("heading", { name: "Related Page Previews" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Backlink Previews" })).toBeVisible();

    await page.goto("/sources");
    await expect(page.locator(".pageTitle")).toHaveText("Sources");
    await expect(page.getByRole("link", { name: /Residual Stream Notes/i }).first()).toBeVisible();

    await page.goto("/search?q=transformer");
    await expect(page.locator(".pageTitle")).toHaveText("Search The Wiki");
    await expect(page.getByRole("link", { name: /Transformer Architecture/i }).first()).toBeVisible();
    await expect(page.locator(".searchIntro .searchFilters").first()).toBeVisible();

    await page.goto("/search?q=transformer&type=concept&section=concepts&status=reviewed&minConfidence=0.8");
    await expect(page.locator(".pageTitle")).toHaveText("Search The Wiki");
    await expect(page.locator(".metaCard").filter({ hasText: "Results" })).toBeVisible();
    await expect(page.getByRole("link", { name: /Transformer Architecture/i }).first()).toBeVisible();

    await page.goto("/reviews/review-queue");
    await expect(page.locator(".pageTitle")).toHaveText("Review Queue");
    await expect(page.getByRole("heading", { name: "Recommended Next Pass" })).toBeVisible();

    await page.goto("/raw/articles/2026/2026-04-08-example-com-residual-stream-notes.md");
    await expect(page.locator(".pageTitle")).toHaveText("Residual Stream Notes");
    await expect(page.locator(".metaCard").filter({ hasText: "Compiled Page" }).getByRole("link")).toBeVisible();

    errors.assertClean();
  });

  test("keeps the responsive layouts usable", async ({ page }, testInfo) => {
    const errors = attachErrorCollectors(page);

    await page.goto("/concepts/transformer-architecture");
    await expect(page.locator(".pageTitle")).toHaveText("Transformer Architecture");

    const viewport = page.viewportSize();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(2);

    if (viewport && viewport.width <= 880) {
      await expect(page.locator(".mobileDrawer")).toBeVisible();
    }

    if (viewport && viewport.width <= 1100) {
      await expect(page.locator(".mobileRail")).toBeVisible();
    }

    await page.screenshot({
      path: `test-results/${testInfo.project.name}-concept.png`,
      fullPage: true,
    });

    errors.assertClean();
  });
});
