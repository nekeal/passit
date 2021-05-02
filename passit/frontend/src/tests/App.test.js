// import puppeteer from "puppeteer";
//
// require('dotenv').config();
//
// describe("Login page",  () => {
//   let browser, page;
//   let username = process.env.TEST_LOGIN;
//   let password = process.env.TEST_PASSWORD;
//
//   beforeEach(async () => {
//     browser = await puppeteer.launch({
//       headless: false
//     });
//     page = await browser.newPage();
//
//     await page.emulate({
//       viewport: {
//         width: 1300,
//         height: 600
//       },
//       userAgent: ""
//     });
//
//     await page.goto("http://localhost:3000/login");
//   });
//
//   test("Correct login", async () => {
//     await page.waitForSelector("form.form");
//     await page.click("input[name=username]");
//     await page.type("input[name=username]", username);
//     await page.click("input[name=password]");
//     await page.type("input[name=password]", password);
//     await page.click("button[type=submit]");
//
//     await page.waitForNavigation();
//
//     expect(page.url()).toBe("http://localhost:3000/");
//
//
//     browser.close();
//   }, 60000);
// });
//
// describe("Dashboard page", () => {
//   let browser, page;
//
//   beforeEach(async () => {
//     let accessToken = process.env.TEST_ACCESS_TOKEN;
//     let refreshToken = process.env.TEST_REFRESH_TOKEN;
//
//     browser = await puppeteer.launch({
//       headless: false,
//       // slowMo: 50
//     });
//     page = await browser.newPage();
//
//     await page.emulate({
//       viewport: {
//         width: 1300,
//         height: 600
//       },
//       userAgent: ""
//     });
//
//     await page.goto("http://localhost:3000/");
//     await page.evaluate((accessToken, refreshToken) => {
//       localStorage.setItem("access-token", accessToken);
//       localStorage.setItem("refresh-token", refreshToken);
//     }, accessToken, refreshToken);
//     await page.goto("http://localhost:3000/");
//   });
//
//   test("Add minimal announcement", async () => {
//     await page.waitForSelector(".announcement-header div img:nth-child(2)");
//     await page.click(".announcement-header div img:nth-child(2)");
//     await page.waitForSelector("form.form");
//     await page.click("input[name=title]");
//     await page.type("input[name=title]", "Minimal announcement");
//     await page.click("textarea[name=content]");
//     await page.type("textarea[name=content]", "Announcement content");
//     await page.click("button[type=submit]");
//     await page.waitForSelector("form.form", { hidden: true });
//     let title = await page.$eval(".announcements .MuiPaper-root .header h6", e => e.innerText);
//     let content = await page.$eval(".announcements .MuiPaper-root .content p", e => e.innerText);
//     expect(title).toBe("Minimal announcement");
//     expect(content).toBe("Announcement content");
//
//     browser.close();
//   }, 60000);
//
//   test("Add announcement with attachment", async () => {
//     await page.waitForSelector(".announcement-header div img:nth-child(2)");
//     await page.click(".announcement-header div img:nth-child(2)");
//     await page.waitForSelector("form.form");
//     await page.click("input[name=title]");
//     await page.type("input[name=title]", "Announcement with attachment");
//     await page.click("textarea[name=content]");
//     await page.type("textarea[name=content]", "Announcement content");
//     const [ fileChooser ] = await Promise.all([
//       page.waitForFileChooser(),
//       page.click("form.form .add-attachment")
//     ]);
//     await fileChooser.accept(["/home/sans/Pictures/Wallpapers/kreator.jpg"]);
//     await page.click("button[type=submit]");
//     await page.waitForSelector("form.form", { hidden: true });
//     let attachment = await page.$eval(".announcements .MuiPaper-root .attachment", e => e.innerText);
//     expect(attachment).toMatch(/kreator.*\.jpg/);
//
//     browser.close();
//   }, 60000);
//
//   test("Edit announcement", async () => {
//     // await page.waitForSelector(".announcement-header div img:nth-child(2)");
//     // await page.click(".announcement-header div img:nth-child(2)");
//     // await page.waitForSelector("form.form");
//     // await page.click("input[name=title]");
//     // await page.type("input[name=title]", "Announcement to edit");
//     // await page.click("textarea[name=content]");
//     // await page.type("textarea[name=content]", "Announcement content");
//     // await page.click("button[type=submit]");
//     // await page.waitForSelector("form.form", { hidden: true });
//     // let title = await page.$eval(".announcements .MuiPaper-root .header h6", e => e.innerText);
//     // let content = await page.$eval(".announcements .MuiPaper-root .content p", e => e.innerText);
//     // expect(title).toBe("Announcement to edit");
//     // expect(content).toBe("Announcement content");
//     //
//     // await page.waitFor(5000);
//
//     // await page.waitForSelector(".menu-icon");
//     //
//     // await page.$eval(".menu-icon", elem => elem.click());
//     // await page.$eval(".news-edit", elem => elem.click());
//     // await page.waitForSelector("form.form");
//     //
//     // await page.click("input[name=title]");
//     // await page.click("input[name=title]");
//     // let inputValue = await page.$eval("input[name=title]", elem => elem.value);
//     // for(let i = 0; i < inputValue.length; i++) await page.keyboard.press("Backspace");
//     // await page.type("input[name=title]", "Edited announcement");
//     //
//     // await page.click("textarea[name=content]");
//     // inputValue = await page.$eval("textarea[name=content]", elem => elem.value);
//     // for(let i = 0; i < inputValue.length; i++) await page.keyboard.press("Backspace");
//     // await page.type("textarea[name=content]", "Edited content");
//     //
//     // await page.click("button[type=submit]");
//     // await page.waitForSelector("form.form", { hidden: true });
//     // title = await page.$eval(".announcements .MuiPaper-root .header h6", e => e.innerText);
//     // content = await page.$eval(".announcements .MuiPaper-root .content p", e => e.innerText);
//     // expect(title).toBe("Edited announcement");
//     // expect(content).toBe("Edited content");
//
//
//     browser.close();
//   }, 60000);
// });
