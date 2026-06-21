// harvester.js
const fs = require('fs');
const path = require('path');

function getApiKey() {
  let key = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
  if (!key) {
    try {
      const envPath = 'C:\\Users\\araga\\.hermes\\.env';
      if (fs.existsSync(envPath)) {
        const content = fs.readFileSync(envPath, 'utf8');
        const match = content.match(/^GOOGLE_API_KEY\s*=\s*(.+)$/m);
        if (match) {
          key = match[1].trim();
        }
      }
    } catch (e) {
      // Ignore
    }
  }
  return key;
}

const apiKey = getApiKey();

// CLI arguments parsing
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    limit: 5,
    output: 'news_summary.md'
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--limit' || args[i] === '-l') {
      options.limit = parseInt(args[i + 1], 10) || 5;
      i++;
    } else if (args[i] === '--output' || args[i] === '-o') {
      options.output = args[i + 1] || 'news_summary.md';
      i++;
    }
  }

  return options;
}

// Fetch helper with error handling
async function fetchJson(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.warn(`Warning: Failed to fetch ${url}: ${err.message}`);
    return null;
  }
}

async function getTopHNStories(limit) {
  console.log('Fetching top stories from Hacker News...');
  const topIds = await fetchJson('https://hacker-news.firebaseio.com/v0/topstories.json');
  if (!topIds || !topIds.length) {
    console.error('Error: Could not retrieve top stories from Hacker News.');
    process.exit(1);
  }

  const stories = [];
  const targetCount = Math.min(limit * 2, topIds.length); // Fetch slightly more to filter out Ask/Show HN if needed
  
  console.log(`Retrieving details for top ${targetCount} items...`);
  for (let i = 0; i < targetCount && stories.length < limit; i++) {
    const id = topIds[i];
    const item = await fetchJson(`https://hacker-news.firebaseio.com/v0/item/${id}.json`);
    if (item && item.title) {
      stories.push({
        title: item.title,
        url: item.url || `https://news.ycombinator.com/item?id=${id}`,
        score: item.score,
        by: item.by
      });
    }
  }

  return stories;
}

async function generateSummary(stories) {
  if (!apiKey) {
    console.error('Error: The GEMINI_API_KEY environment variable is not defined.');
    process.exit(1);
  }

  const systemInstruction = `You are a Senior Technical Researcher and Curator.
Your task is to analyze the provided list of trending stories from Hacker News and generate a clean, executive summary newsletter in Markdown format.

Your newsletter must:
1. Have a clear, engaging main title (e.g., "Hacker News Digest: [Current Topic]").
2. Organize selected stories logically (filter out pure clickbait or marketing fluff).
3. For each story, provide:
   - A clickable markdown link to the source.
   - A concise, SRE-grade summary of why this topic is technically relevant and what developers/architects need to know.
4. Keep it direct, human, and SRE-grade.

ANTI-SLOP DIRECTIVE:
Do NOT use AI conversational clichés, buzzwords, or introductory fluff (like "delve", "tapestry", "moreover", "furthermore", "it is important to note", "in this digest, we will explore"). Write in a direct, natural, human developer tone.`;

  const prompt = `Analyze these trending Hacker News stories and generate a curated markdown digest:\n\n${JSON.stringify(stories, null, 2)}`;
  
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;

  console.log('Sending stories to Gemini for curation and summarization...');
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              { text: prompt }
            ]
          }
        ],
        systemInstruction: {
          parts: [
            { text: systemInstruction }
          ]
        },
        generationConfig: {
          temperature: 0.3
        }
      })
    });

    if (!res.ok) {
      throw new Error(`Gemini API returned HTTP ${res.status}: ${await res.text()}`);
    }

    const data = await res.json();
    const output = data.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!output) {
      throw new Error('Empty response from Gemini API.');
    }
    return output;
  } catch (err) {
    console.error(`Error communicating with Gemini: ${err.message}`);
    process.exit(1);
  }
}

async function main() {
  const options = parseArgs();
  
  const stories = await getTopHNStories(options.limit);
  console.log(`Fetched ${stories.length} stories successfully.`);

  const summaryMarkdown = await generateSummary(stories);
  
  const outputPath = path.resolve(options.output);
  fs.writeFileSync(outputPath, summaryMarkdown.trim() + '\n', 'utf8');
  console.log(`✅ Curation complete! Report saved successfully to: ${outputPath}`);
}

main();
