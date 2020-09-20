const puppeteer = require('puppeteer');
const readline = require('readline');
const { stdin } = require('process');
const devices = puppeteer.devices;

task = async urls => {
    const browser = await puppeteer.launch()
    const pages = await Promise.all(
        urls.map(async url => {
            const page = await browser.newPage()
            //TODO: Make device emulation configurable
            await page.emulate(devices['iPhone X'])
            await page.goto(url,{waitUntil:'load'}).catch(reason => console.log('page timed out :'+url))
            console.log(url)
            return page
        })
    )

    const contents = Promise.all(
        pages.map(async page => await page.content())
    )

    //TODO: make image screenshot configurable
    if(false){
        const screenshots = Promise.all(
            pages.map(async page => {
                //TODO: refine image storage
                const path = page.url().replace(/\.|\/|\:/g, '') + ".png"
                console.log(path)
                await page.screenshot({ path })
            })
        )
        await screenshots
    }
    await contents
    await browser.close()
}

urls = []
stdinInterface = readline.createInterface({input:stdin})
stdinInterface.on('line', line => urls.push(line))
stdinInterface.on('close',() => task(urls))
