// packer.js
const fs = require('fs');
const path = require('path');

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    input: '',
    output: ''
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--input' || args[i] === '-i') {
      options.input = args[i + 1] || '';
      i++;
    } else if (args[i] === '--output' || args[i] === '-o') {
      options.output = args[i + 1] || '';
      i++;
    }
  }

  return options;
}

// Recursively sanitize sensitive keys in objects/arrays
function sanitizeValue(key, value) {
  if (typeof value === 'string') {
    const keyLower = key.toLowerCase();
    
    // Check for webhook URLs
    if (value.startsWith('http') && (keyLower.includes('url') || keyLower.includes('webhook'))) {
      try {
        const urlObj = new URL(value);
        return `${urlObj.protocol}//[REDACTED_HOST]${urlObj.pathname}`;
      } catch (e) {
        return 'https://[REDACTED_URL]';
      }
    }
    
    // Check for standard sensitive words
    const sensitiveWords = ['token', 'key', 'secret', 'password', 'auth', 'credential', 'api_key', 'apikey'];
    if (sensitiveWords.some(word => keyLower.includes(word))) {
      return '[REDACTED_SECRET]';
    }
  }
  return value;
}

function sanitizeObject(obj) {
  if (Array.isArray(obj)) {
    return obj.map(item => sanitizeObject(item));
  } else if (obj !== null && typeof obj === 'object') {
    const sanitized = {};
    for (const [key, value] of Object.entries(obj)) {
      // Redact credential references in n8n structure
      if (key === 'credentials' && value !== null && typeof value === 'object') {
        sanitized[key] = {};
        for (const [credType, credVal] of Object.entries(value)) {
          sanitized[key][credType] = { id: '[REDACTED_CREDENTIAL_ID]', name: `[REDACTED_CREDENTIAL_NAME]` };
        }
      } else {
        sanitized[key] = sanitizeValue(key, sanitizeObject(value));
      }
    }
    return sanitized;
  }
  return obj;
}

function main() {
  const options = parseArgs();

  if (!options.input) {
    console.error('Error: Input file path is required. Use --input or -i.');
    process.exit(1);
  }

  const inputPath = path.resolve(options.input);
  if (!fs.existsSync(inputPath)) {
    console.error(`Error: File not found: ${inputPath}`);
    process.exit(1);
  }

  let workflow;
  try {
    const content = fs.readFileSync(inputPath, 'utf8');
    workflow = JSON.parse(content);
  } catch (err) {
    console.error(`Error: Failed to parse input file as JSON: ${err.message}`);
    process.exit(1);
  }

  console.log('Sanitizing n8n workflow credentials and secrets...');
  const sanitizedWorkflow = sanitizeObject(workflow);

  // Determine output path
  let outputPath = options.output;
  if (!outputPath) {
    const ext = path.extname(options.input);
    const dir = path.dirname(options.input);
    const base = path.basename(options.input, ext);
    outputPath = path.join(dir, `${base}_template${ext}`);
  }

  try {
    fs.writeFileSync(outputPath, JSON.stringify(sanitizedWorkflow, null, 2) + '\n', 'utf8');
    console.log(`[SUCCESS] Sanitized workflow template saved to: ${outputPath}`);
  } catch (err) {
    console.error(`Error: Failed to write output file: ${err.message}`);
    process.exit(1);
  }
}

main();
