// generator.js
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.GEMINI_API_KEY;

function getGitDiff() {
  try {
    // Check if inside a git repository
    execSync('git rev-parse --is-inside-work-tree', { stdio: 'ignore' });
  } catch (e) {
    console.error('Error: Not a git repository.');
    process.exit(1);
  }

  // Get staged changes
  let diff = execSync('git diff --cached', { encoding: 'utf8' }).trim();
  
  if (!diff) {
    console.log('No staged changes found. Checking unstaged changes...');
    diff = execSync('git diff', { encoding: 'utf8' }).trim();
  }

  return diff;
}

async function generatePrInfo(diff) {
  if (!apiKey) {
    console.error('Error: The GEMINI_API_KEY environment variable is not defined.');
    console.error('Define it by running: export GEMINI_API_KEY="your-token"');
    process.exit(1);
  }

  const systemInstruction = `You are a Principal Software Engineer and SRE lead.
Your task is to analyze the provided git diff and generate:
1. A single-line Conventional Commit message (e.g., feat: add support for X, fix: resolve memory leak, docs: update readme).
2. A professional Pull Request (PR) description in English.

PR Description Template:
## Goal
[Briefly explain the goal of the changes in a direct, natural human tone]

## Proposed Changes
- [File or component name]: [Key changes made]

## Verification
- [Briefly describe how to test or verify these changes]

ANTI-SLOP DIRECTIVE:
You must strictly write like a human. Avoid all AI jargon, buzzwords, or clichés (such as "delve", "tapestry", "moreover", "furthermore", "revolutionize", "pivotal", "in today's digital landscape", "it is important to note"). Keep it technical, SRE-grade, and concise.

Output format:
Your output must follow this exact format:
[COMMIT_MESSAGE]
<Single-line conventional commit message>
[PR_DESCRIPTION]
<PR description in Markdown format>`;

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        contents: [
          {
            role: 'user',
            parts: [
              { text: `Analyze this git diff and generate commit message and PR description:\n\n\`\`\`diff\n${diff}\n\`\`\`` }
            ]
          }
        ],
        systemInstruction: {
          parts: [
            { text: systemInstruction }
          ]
        },
        generationConfig: {
          temperature: 0.1
        }
      })
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`API returned status ${response.status}: ${errText}`);
    }

    const data = await response.json();
    const resultText = data.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!resultText) {
      throw new Error('Invalid API response format or empty output text.');
    }

    // Parse the commit message and PR description
    const commitMatch = resultText.match(/\[COMMIT_MESSAGE\]\s*([\s\S]*?)\s*\[PR_DESCRIPTION\]/);
    const prMatch = resultText.match(/\[PR_DESCRIPTION\]\s*([\s\S]*)/);

    const commitMessage = commitMatch ? commitMatch[1].trim() : 'feat: update codebase';
    const prDescription = prMatch ? prMatch[1].trim() : resultText;

    return { commitMessage, prDescription };

  } catch (err) {
    console.error('Error calling Gemini API:', err.message);
    process.exit(1);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'show';

  const diff = getGitDiff();
  if (!diff) {
    console.log('No changes detected in the git workspace. Make some changes before running this command.');
    process.exit(0);
  }

  console.log('Analyzing Git diff with Gemini...');
  const { commitMessage, prDescription } = await generatePrInfo(diff);

  if (command === 'show') {
    console.log('\n======================================================');
    console.log('🔑 PROPOSED CONVENTIONAL COMMIT MESSAGE:');
    console.log('======================================================');
    console.log(commitMessage);
    console.log('\n======================================================');
    console.log('📄 PROPOSED PULL REQUEST DESCRIPTION:');
    console.log('======================================================');
    console.log(prDescription);
    console.log('======================================================\n');
  } else if (command === 'commit') {
    console.log(`Executing git commit -m "${commitMessage}"...`);
    try {
      execSync(`git commit -m "${commitMessage.replace(/"/g, '\\"')}"`, { stdio: 'inherit' });
      console.log('✅ Changes successfully committed!');
    } catch (e) {
      console.error('Failed to execute git commit:', e.message);
    }
  } else if (command === 'save') {
    let outputIdx = args.indexOf('--output');
    let output = outputIdx !== -1 ? args[outputIdx + 1] : 'PR_DESCRIPTION.md';
    
    fs.writeFileSync(output, prDescription, 'utf8');
    console.log(`✅ PR description saved to: ${output}`);
    console.log(`🔑 Suggested Commit Message: ${commitMessage}`);
  } else {
    console.log('Available commands:');
    console.log('  show                               - Displays commit message and PR description');
    console.log('  commit                             - Runs git commit with the generated message');
    console.log('  save [--output <path>]              - Saves PR description to file');
    process.exit(1);
  }
}

main();
