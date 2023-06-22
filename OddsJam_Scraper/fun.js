import puppeteer from 'puppeteer';
import { BingChat } from 'bing-chat'

async function example() {
  const api = new BingChat({
    cookie: process.env.BING_COOKIE
  })

  const res = await api.sendMessage('Hello World!')
  console.log(res.text)
}

example()
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://oddsjam.com/nba/articles', {waitUntil: 'domcontentloaded'});
  // Wait for 5 seconds
  console.log(await page.content())


  var content = await page.content()
  console.log('yoo' + content)

  //extract and store all strings in "/mlb/
//   // Type in the username and continue forward
// await page.type('input[name="email"]', 'hello@sirajraval.com');
// await Promise.all([page.waitForNavigation(), page.click('button[type="submit"]')]);

// console.log(await page.content());
const regex = /\/nba\/[^\s"']+/g;

const urls = content.match(regex);
var article = "https://oddsjam.com"
var matched_path
var counter = 1
if (urls) {
  urls.forEach((url) => {
    counter+=1
    if(counter == 10) 
    {
      matched_path = url
      console.log(url + 'the one!')
    }
    console.log(url);
  });
} else {
  console.log("No matching URLs found.");
}


var combined_article = article + matched_path
console.log(' finish ' + combined_article)
await page.goto('https://oddsjam.com/nba/articles', {waitUntil: 'domcontentloaded'});
// Wait for 5 seconds
console.log(await page.content())



  // Take screenshot
  await browser.close();
})();