const fs = require('fs');
const readline = require('readline');

const PROFILE_API = 'https://plantsservices.sc.egov.usda.gov/api/PlantProfile?symbol=';
const CHAR_API = 'https://plantsservices.sc.egov.usda.gov/api/PlantCharacteristics/';

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchWithRetry(url, maxRetries = 10) {
    let attempt = 0;
    while (attempt < maxRetries) {
        try {
            const response = await fetch(url);
            if (response.status === 404) {
                return { ok: false, status: 404 };
            }
            if (response.ok) {
                return { ok: true, status: response.status, response };
            }
            if (response.status === 429 || response.status >= 500) {
                console.log(`\nHTTP ${response.status} on ${url}. Retrying... (${attempt + 1}/${maxRetries})`);
                attempt++;
                const backoff = Math.pow(2, attempt) * 1000;
                await delay(backoff);
                continue;
            }
            return { ok: false, status: response.status };
        } catch (err) {
            console.log(`\nNetwork error on ${url}: ${err.message}. Retrying... (${attempt + 1}/${maxRetries})`);
            attempt++;
            await delay(Math.pow(2, attempt) * 1000);
        }
    }
    throw new Error(`Failed to fetch ${url} after ${maxRetries} retries.`);
}

function stripHtml(html) {
    return html.replace(/<[^>]*>?/gm, '');
}

async function scrapeUsda() {
    const args = process.argv.slice(2);
    // Usage: node src/usda_scraper.js [limit] [symbol_to_test]
    let limit = args[0] && !isNaN(args[0]) ? parseInt(args[0]) : Infinity;
    let targetSymbol = args.find(a => a.length > 2 && isNaN(a));

    if (!fs.existsSync('plantlst.txt')) {
        console.error("plantlst.txt not found.");
        return;
    }

    const outputFile = 'usda_data.jsonl';
    const processedSymbols = new Set();
    if (fs.existsSync(outputFile)) {
        const lines = fs.readFileSync(outputFile, 'utf8').split('\n');
        for (const line of lines) {
            if (line.trim()) {
                try {
                    const data = JSON.parse(line);
                    processedSymbols.add(data.symbol);
                } catch (e) {}
            }
        }
    }

    console.log(`Already processed ${processedSymbols.size} symbols. Resuming...`);

    const fileStream = fs.createReadStream('plantlst.txt');
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    let count = 0;
    let isHeader = true;

    for await (const line of rl) {
        if (isHeader) {
            isHeader = false;
            continue;
        }

        const match = line.match(/^"([^"]+)"/);
        if (!match) continue;
        const symbol = match[1];

        if (targetSymbol && symbol !== targetSymbol) continue;
        if (!targetSymbol && processedSymbols.has(symbol)) continue;

        try {
            process.stdout.write(`Fetching ${symbol}... `);
            const profileRes = await fetchWithRetry(PROFILE_API + symbol);
            
            if (!profileRes.ok && profileRes.status === 404) {
                console.log(`Not found (404)`);
                fs.appendFileSync(outputFile, JSON.stringify({ symbol: symbol, not_found: true }) + '\n');
                processedSymbols.add(symbol);
                continue;
            }
            
            const profile = await profileRes.response.json();
            const plantId = profile.Id;
            
            if (plantId) {
                const charRes = await fetchWithRetry(CHAR_API + plantId);
                let traits = null;
                
                if (charRes.ok) {
                    const characteristics = await charRes.response.json();
                    const getTrait = (name) => {
                        const trait = characteristics.find(c => c.PlantCharacteristicName === name);
                        return trait ? trait.PlantCharacteristicValue : null;
                    };

                    const foundTraits = {
                        moistureUse: getTrait('Moisture Use'),
                        minTempF: getTrait('Temperature, Minimum (°F)'),
                        droughtTolerance: getTrait('Drought Tolerance'),
                        shadeTolerance: getTrait('Shade Tolerance'),
                        precipitationMin: getTrait('Precipitation, Minimum'),
                        precipitationMax: getTrait('Precipitation, Maximum')
                    };

                    // Check if any trait is non-null
                    if (Object.values(foundTraits).some(v => v !== null)) {
                        traits = foundTraits;
                    }
                }

                const plantData = {
                    symbol: symbol,
                    scientificName: stripHtml(profile.ScientificName),
                    commonName: profile.CommonName,
                    traits: traits
                };
                
                fs.appendFileSync(outputFile, JSON.stringify(plantData) + '\n');
                processedSymbols.add(symbol);
                console.log(traits ? "SUCCESS: Captured physiological traits." : "INFO: Profile saved (no traits available).");
                count++;
                
                if (count >= limit) break;
            } else {
                console.log("No Plant ID.");
                fs.appendFileSync(outputFile, JSON.stringify({ symbol: symbol, error: "No Plant ID" }) + '\n');
                processedSymbols.add(symbol);
            }
        } catch (err) {
            console.error(`\nFatal error on ${symbol}: ${err.message}`);
            process.exit(1);
        }
        
        await delay(500);
    }
    
    console.log(`\nScraping session complete. Added ${count} records.`);
}

scrapeUsda().catch(console.error);
