#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { parseArgs } = require('./analyzers/utils');

const cli = parseArgs();

if (!cli.dev || !cli.kata || !cli.treatment) {
  console.error('Uso: npm run finish-trial -- --dev <devId> --kata <kataId> --treatment <COM_IA|SEM_IA>');
  process.exit(1);
}

const dev = String(cli.dev).trim();
const kata = String(cli.kata).trim();
const treatment = String(cli.treatment).trim().toUpperCase();

const kataSourceDir = path.join(__dirname, '..', 'katas', kata);
const kataIndexFile = path.join(kataSourceDir, 'index.js');

if (!fs.existsSync(kataIndexFile)) {
  console.error(`❌ Erro: Arquivo ${kataIndexFile} não encontrado.`);
  process.exit(1);
}

// 1. Define o diretório de destino: trials/<dev>/<kata-tratamento>
const targetFolder = `${kata}-${treatment.toLowerCase().replace('_', '-')}`;
const targetDir = path.join(__dirname, '..', 'trials', dev, targetFolder);

fs.mkdirSync(targetDir, { recursive: true });

// 2. Copia o index.js resolvido para a subpasta do trial
const targetIndexFile = path.join(targetDir, 'index.js');
fs.copyFileSync(kataIndexFile, targetIndexFile);
console.log(`📂 Solução copiada para: ${targetIndexFile}`);

// 3. Se for COM_IA, garante que exista um prompts.md (cria modelo se não existir)
if (treatment === 'COM_IA') {
  const promptsFile = path.join(targetDir, 'prompts.md');
  if (!fs.existsSync(promptsFile)) {
    fs.writeFileSync(
      promptsFile,
      '# Prompts Utilizados no Trial\n\n> Copie e cole aqui o histórico de prompts utilizados com a IA.\n',
      'utf8'
    );
    console.log(`📝 Arquivo criado: ${promptsFile}`);
  }
}

// 4. Executa o metrics-runner na subpasta do trial
console.log('📊 Calculando métricas de qualidade do código...');
try {
  execSync(`npm run metrics -- --path "${targetDir}"`, { stdio: 'inherit' });
} catch (error) {
  console.error('⚠️ Falha ao calcular métricas.');
}

// 5. Restaura o index.js original em katas/ via Git
try {
  execSync(`git restore "${kataIndexFile}"`, { stdio: 'inherit' });
  console.log(`🧹 ${kataIndexFile} restaurado para o esqueleto original via Git.`);
} catch (error) {
  console.error(`⚠️ Erro ao restaurar ${kataIndexFile}. Verifique alterações manualmente.`);
}

console.log(`\n✅ Processo de trial concluído com sucesso para [${dev} | ${kata} | ${treatment}]!`);