import asyncio
from playwright.async_api import async_playwright, TimeoutError

ANSWER = "B"

accounts = [
{"username": "MAS-51", "wallet": "BBvm2Ti9evzoE9mMhiUMTgQawPZoQ8ZU9DkJsi9ZKmur"},
{"username": "MAS-52", "wallet": "29NBUTSyhBTDMQbCtSR8vtVCk5pZ2obyoXYzwBGiib5o"},
{"username": "MAS-53", "wallet": "APPojTDJgxjHyEaGJRpUZtNNq3GawG5R5MWPUkfBxq6E"},
{"username": "MAS-54", "wallet": "8HS4fD2iQCofdecNLpAaAe8QDyBAEqyDtfn2RH1UZYXg"},
{"username": "MAS-55", "wallet": "HNRNLjKiHr8PwLLufJEoPqA37HspAQzTBPfC7SBTWGpP"},
{"username": "MAS-56", "wallet": "AWQzA27wZCHmhwszaFrc2cGtLDVsT5k8u4w5ae6o6xCp"},
{"username": "MAS-57", "wallet": "5fT67wZU8uaF4sySzhMNgiofz3UMuDta4R6r3MipJSH3"},
{"username": "MAS-58", "wallet": "J3Tr3cLvfxnfCYgVGNPZGNuXSZdD4e2Govvu43EhX82D"},
{"username": "MAS-59", "wallet": "5sbT5NETxXkfMKrRy8sB86ds1GWrrN7kys8eB9cCPNmj"},
{"username": "MAS-60", "wallet": "ELCFKpXappiiKJGJeRHqmGFok1wt1gfZecQH67jhYBn1"},
{"username": "MAS-61", "wallet": "DyZ2jbR2m2Wit97ss9i9YbyqbTQbLueEA1418MzH7oaR"},
{"username": "MAS-62", "wallet": "2BbEtzMsf8Fd4JNySgWiZk3pQJtufvwE6wwyN3dEFPQ7"},
{"username": "MAS-63", "wallet": "4CH6DTpaomx8Tx29Qi3MKU9HjBDbgafYKnDDXS6kr8SU"},
{"username": "MAS-64", "wallet": "99R5PocKfFp5Ra6Q1tinTDL8SgWHgnatMnNU4LHdhxma"},
{"username": "MAS-65", "wallet": "8kYcFMxJbJg4ZpXAZzDG2YxBwJH2jXxPEupgRk7Ms3gx"},
{"username": "MAS-66", "wallet": "Gz9PdceqMAkZt9zkq7EHLwAxAkAJHGsmBcii6r8FxtGb"},
{"username": "MAS-67", "wallet": "8HUBbirxJZb2YsTV5ACg9LSzRbvZuhuX3H86yxQZUbtj"},
{"username": "MAS-68", "wallet": "3Q7nMnYGzk95eqKVWXM41i94nmeKCgzU58FMutESEfc4"},
{"username": "MAS-69", "wallet": "Gry41UDDUikWfACx2PuVj16wcZyQXLNb7Bk44NKtobKR"},
{"username": "MAS-70", "wallet": "8SghF3f3fXp6Ao8wmJTjYycWbjs6JK7nK9LtjpvRbv1Q"},
{"username": "MAS-71", "wallet": "8Pr192ujAJUkofWN6xHXV6uPEB8hqaPb1xLPAeSZUNmJ"},
{"username": "MAS-72", "wallet": "8vebivED3sGY55xB1RQsjPodfaAQstmN8sSzH18zN7XB"},
{"username": "MAS-73", "wallet": "Dt4E2mqfCZtxVohTqycW9K9DgWTE8YuiNPrEg8Pc1ALJ"},
{"username": "MAS-74", "wallet": "54tRNCQVScXxqCj3givZYTGXv9dbBTbRDhb5ZCNVMeot"},
{"username": "MAS-75", "wallet": "p7pu5s2bAJpChrz7vDroHU4E4EGMzPRuxXunvj75e2Y"},

]

async def handle_modal(page):
    modal = page.locator("#scamMigrationWarningModal")
    try:
        if await modal.is_visible(timeout=5000):
            print("⚠️ Closing modal...")
            buttons = modal.locator("button")
            if await buttons.count() > 0:
                await buttons.first.click()
                await page.wait_for_timeout(1000)
    except:
        pass

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        for acc in accounts:
            context = await browser.new_context()
            page = await context.new_page()

            print("Running account:", acc["username"])

            try:
                await page.goto("https://theros.io/prelaunch", timeout=80000)
                await page.wait_for_load_state("networkidle", timeout=15000)
            except TimeoutError:
                print(f"Timeout for {acc['username']}. Skipping.")
                await context.close()
                continue

            await handle_modal(page)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_selector("input", timeout=15000)

            inputs = await page.query_selector_all("input")
            if len(inputs) < 2:
                print(f"Not enough inputs for {acc['username']}, skipping")
                await context.close()
                continue

            await inputs[0].fill(acc["username"])
            await inputs[1].fill(acc["wallet"])

            if len(inputs) > 2:
                await inputs[2].fill("bot")

            await handle_modal(page)

            create_btn = page.locator("#registerBtn")
            try:
                await create_btn.click(timeout=9000)
            except TimeoutError:
                await create_btn.click(force=True)

            next_btn = page.locator("#nextQuestionBtn")
            try:
                await next_btn.wait_for(state="visible", timeout=8000)
                await next_btn.click()
            except:
                pass

            answer_selector = f"#answer{ANSWER.upper()}"
            try:
                await page.locator(answer_selector).click(timeout=20000)
                print("Answered:", ANSWER)
            except Exception as e:
                print(f"Failed to answer: {e}")

            await page.wait_for_timeout(1000)
            await context.close()

        await browser.close()
        print("🎉 All accounts processed successfully!")

if __name__ == "__main__":
    asyncio.run(run_bot())
