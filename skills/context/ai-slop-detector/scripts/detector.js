// detector.js
const fs = require('fs');
const path = require('path');

const apiKey = process.env.GEMINI_API_KEY;

// List of common AI-slop patterns (regexes)
const slopPatterns = [
  { name: 'delve', regex: /\bdelve(s|d|r|g)?\b/gi, suggestion: 'use "explore", "examine", or "look into"' },
  { name: 'tapestry', regex: /\btapestry\b/gi, suggestion: 'use "structure", "complex system", or "combination"' },
  { name: 'testament', regex: /\btestament\b/gi, suggestion: 'use "proof", "evidence", or "demonstration"' },
  { name: 'moreover', regex: /\bmoreover\b/gi, suggestion: 'use "also" or "in addition"' },
  { name: 'furthermore', regex: /\bfurthermore\b/gi, suggestion: 'use "also" or "next"' },
  { name: 'bespoke', regex: /\bbespoke\b/gi, suggestion: 'use "custom", "tailored", or "specific"' },
  { name: 'revolutionize', regex: /\brevolutionize(d|s|g)?\b/gi, suggestion: 'use "improve", "transform", or "change"' },
  { name: 'pivotal', regex: /\bpivotal\b/gi, suggestion: 'use "key", "important", or "critical"' },
  { name: 'throat-clearing intro', regex: /\b(in today's digital landscape|it is important to note that|in this article we will)\b/gi, suggestion: 'remove or write directly' }
];

function checkFile(filePath) {
  if (!fs.existsSync(filePath)) {
    console.error(`Erro: Arquivo não encontrado: ${filePath}`);
    process.exit(1);
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');
  let totalMatches = 0;
  const reports = [];

  lines.forEach((line, idx) => {
    slopPatterns.forEach(pattern => {
      let match;
      // Reset regex index for safety
      pattern.regex.lastIndex = 0;
      while ((match = pattern.regex.exec(line)) !== null) {
        totalMatches++;
        reports.push({
          line: idx + 1,
          word: match[0],
          pattern: pattern.name,
          suggestion: pattern.suggestion,
          snippet: line.trim()
        });
      }
    });
  });

  console.log(`\n=== RELATÓRIO DE AUDITORIA DE SLOP: ${path.basename(filePath)} ===`);
  if (totalMatches === 0) {
    console.log('✅ Nenhum padrão de slop de IA detectado! Excelente escrita.');
    process.exit(0);
  }

  reports.forEach(r => {
    console.log(`\nLine ${r.line}: Encontrado "${r.word}" (Padrão: ${r.pattern})`);
    console.log(`  > Trecho: "${r.snippet}"`);
    console.log(`  > Sugestão: ${r.suggestion}`);
  });

  console.log(`\n======================================================`);
  console.log(`FIM: Encontrados ${totalMatches} termos robóticos.`);
  console.log(`======================================================\n`);
  process.exit(0);
}

async function cleanFile(filePath, outputPath) {
  if (!apiKey) {
    console.error('Erro: A variável de ambiente GEMINI_API_KEY não está definida.');
    console.error('Defina-a executando: export GEMINI_API_KEY="seu-token"');
    process.exit(1);
  }

  if (!fs.existsSync(filePath)) {
    console.error(`Erro: Arquivo não encontrado: ${filePath}`);
    process.exit(1);
  }

  const content = fs.readFileSync(filePath, 'utf8');
  console.log(`Lendo ${filePath} (${content.length} caracteres)...`);
  console.log('Enviando para o Gemini para higienização (remover jargões de IA)...');

  const systemInstruction = `Você é um editor de texto sênior e especialista em escrita técnica humana, clara e objetiva.
Sua tarefa é reescrever o texto fornecido pelo usuário eliminando qualquer vestígio de "AI-slop" (jargões artificiais comumente gerados por LLMs, como as palavras "delve", "tapestry", "testament", "moreover", "furthermore", "bespoke", "revolutionize", "pivotal", e frases introdutórias clichês como "in today's digital landscape", "it is important to note").
Regras de saída:
- Mantenha a mesma língua do texto original (se a entrada for em inglês, a saída deve ser em inglês; se for em português, a saída deve ser em português).
- Mantenha exatamente o mesmo significado técnico e factual.
- Torne a prosa direta, concisa, ativa e com vocabulário natural e humano.
- Não altere blocos de código nem links markdown.
- Retorne APENAS o texto reescrito limpo, sem explicações extras.`;

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
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
              { text: content }
            ]
          }
        ],
        systemInstruction: {
          parts: [
            { text: systemInstruction }
          ]
        },
        generationConfig: {
          temperature: 0.2
        }
      })
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`API retornou status ${response.status}: ${errText}`);
    }

    const data = await response.json();
    const cleanText = data.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!cleanText) {
      throw new Error('Formato de resposta da API inválido ou texto de saída vazio.');
    }

    fs.writeFileSync(outputPath, cleanText, 'utf8');
    console.log(`\n[SUCESSO] Texto higienizado com sucesso!`);
    console.log(`Arquivo salvo em: ${outputPath} (${cleanText.length} caracteres).`);

  } catch (err) {
    console.error('Erro ao chamar a API do Gemini:', err.message);
    process.exit(1);
  }
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'check') {
    const file = args[1];
    if (!file) {
      console.log('Uso: node detector.js check <file_path>');
      process.exit(1);
    }
    checkFile(file);
  } else if (command === 'clean') {
    const file = args[1];
    let outputIdx = args.indexOf('--output');
    let output = outputIdx !== -1 ? args[outputIdx + 1] : null;

    if (!file || !output) {
      console.log('Uso: node detector.js clean <file_path> --output <output_path>');
      process.exit(1);
    }
    cleanFile(file, output);
  } else {
    console.log('Comandos disponíveis:');
    console.log('  check <file_path>                   - Verifica padrões de IA no arquivo');
    console.log('  clean <file_path> --output <path>   - Higieniza o arquivo usando Gemini API');
    process.exit(1);
  }
}

main();
