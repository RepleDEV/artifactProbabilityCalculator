import request from "request-promise";
import cheerio, { Cheerio, CheerioAPI, Element } from "cheerio";
import { promises as fs } from "fs";
import path from "path";

function processTable($table: Cheerio<Element>, $: CheerioAPI): {[key: string]: number} {
    const $items = $($table).find("tr").slice(1);
    let res: {[key: string]: number} = {};

    for (let i = 0; i < $items.length;i++) {
        const $item = $($items[i]);

        const [label, value] = $item.children().toArray().map((x) => $(x).text());

        res[label] = +(value.replace("%", ""));
    }

    return res;
}

async function webscrape(): Promise<void> {
    // Webscrape
    const data = await request("https://genshin-impact.fandom.com/wiki/Artifacts/Distribution");
    const $ = cheerio.load(data);

    const $tables = $(".wikitable.sortable").slice(0, 22);
    // Tables (index) 0-2 = Main stat distribution for sands, goblet, circlet respectively
    const mainStatDistributionTables: Cheerio<Element>[] = $tables.splice(0, 3);
    // Next 2 is sub stat distribution for flower and feather respectively
    let subStatDistribution = $tables.splice(0, 2) as Cheerio<Element>[];
    // Next few has differing sub stat distributions depending on the main stat
    //! Sands
    const sandsMainStats = ["HP%", "ATK%", "DEF%", "Energy Recharge%", "Elemental Mastery"]; // List of main stats
    const sandsSubStatDistributionTables = ($tables.splice(0, 5) as Cheerio<Element>[]); // Get table of main stats

    let sandsSubStatDistributionObject: {[key: string]: Cheerio<Element>} = {}; // Empty object to store said distributions
    for (let i = 0;i < sandsSubStatDistributionTables.length;i++) {
        const sandsSubStatDistributionTable = sandsSubStatDistributionTables[i];

        // Make main stat as key to object with table as item
        sandsSubStatDistributionObject[sandsMainStats[i]] = sandsSubStatDistributionTable;
    }
    // Do the same for other 2 types
    //! Goblet
    const gobletMainStats = ["HP%", "ATK%", "DEF%", "Elm_Phys_Bonus", "Elemental Mastery"]; // List of main stats
    const gobletSubStatDistributionTables = ($tables.splice(0, 5) as Cheerio<Element>[]); // Get table of main stats

    let gobletSubStatDistributionObject: {[key: string]: Cheerio<Element>} = {}; // Empty object to store said distributions
    for (let i = 0;i < gobletSubStatDistributionTables.length;i++) {
        const gobletSubStatDistributionTable = gobletSubStatDistributionTables[i];

        // Make main stat as key to object with table as item
        gobletSubStatDistributionObject[gobletMainStats[i]] = gobletSubStatDistributionTable;
    }
    //! Circlet
    const circletMainStats = ["HP%", "ATK%", "DEF%", "CRIT Rate%", "CRIT DMG%", "Healing Bonus%", "Elemental Mastery"]; // List of main stats
    const circletSubStatDistributionTables = ($tables.splice(0, 7) as Cheerio<Element>[]); // Get table of main stats

    let circletSubStatDistributionObject: {[key: string]: Cheerio<Element>} = {}; // Empty object to store said distributions
    for (let i = 0;i < circletSubStatDistributionTables.length;i++) {
        const circletSubStatDistributionTable = circletSubStatDistributionTables[i];

        // Make main stat as key to object with table as item
        circletSubStatDistributionObject[circletMainStats[i]] = circletSubStatDistributionTable;
    }
    // Process tables into values

    const flowerSubStatDistribution = processTable(subStatDistribution[0], $);
    const featherSubStatDistribution = processTable(subStatDistribution[1], $)

    //! Sands
    const sandsSubStatDistributionObjectFinal: {[key: string]: {[key: string]: number}} = {}
    for (const mainStat in sandsSubStatDistributionObject) {
        sandsSubStatDistributionObjectFinal[mainStat] = processTable(sandsSubStatDistributionObject[mainStat], $);
    }
    //! Goblet
    const gobletSubStatDistributionObjectFinal: {[key: string]: {[key: string]: number}} = {}
    for (const mainStat in gobletSubStatDistributionObject) {
        gobletSubStatDistributionObjectFinal[mainStat] = processTable(gobletSubStatDistributionObject[mainStat], $);
    }
    //! Circlet
    const circletSubStatDistributionObjectFinal: {[key: string]: {[key: string]: number}} = {}
    for (const mainStat in circletSubStatDistributionObject) {
        circletSubStatDistributionObjectFinal[mainStat] = processTable(circletSubStatDistributionObject[mainStat], $);
    }

    //! Main stat distributions
    const sandsMainStatDistributionObject = processTable(mainStatDistributionTables[0], $);
    const gobletMainStatDistributionObject = processTable(mainStatDistributionTables[1], $);
    const circletMainStatDistributionObject = processTable(mainStatDistributionTables[2], $);

    const finalOutput = JSON.stringify({
        mainStats: {
            sands: sandsMainStatDistributionObject,
            goblet: gobletMainStatDistributionObject,
            circlet: circletMainStatDistributionObject
        },
        subStats: {
            flower: flowerSubStatDistribution,
            feather: featherSubStatDistribution,
            sands: sandsSubStatDistributionObjectFinal,
            goblet: gobletSubStatDistributionObjectFinal,
            circlet: circletSubStatDistributionObjectFinal
        }
    });

    await fs.writeFile(path.resolve("./file_2.json"), finalOutput);
}

webscrape()