# 🌐 Skill: n8n-workflow-packer

An automated utility skill to package and sanitize exported n8n workflow JSON files for secure version control in Git. Automatically redacts database credentials, webhook URLs, and private API tokens.

---

## 🛠️ Triggers

This skill is triggered when an agent or developer needs to version control n8n workflows, clean workflow configurations, or share n8n templates publicly.
- "sanitize n8n workflow"
- "pack n8n template"
- "run n8n-workflow-packer"
- "prepare n8n json"

---

## 🚀 Usage Guide

### Requirements
- Node.js (v18+)

### Command Execution
Run the script using `node` from the repository root:

```bash
# Sanitize and create a template in the same directory (default appends _template.json)
node skills/automation/n8n-workflow-packer/scripts/packer.js --input my_workflow.json

# Define a specific output path
node skills/automation/n8n-workflow-packer/scripts/packer.js \
  --input my_workflow.json \
  --output templates/my_workflow_clean.json
```

### Options
*   `-i`, `--input`: Path to the exported n8n workflow JSON file (required).
*   `-o`, `--output`: Target path to save the sanitized template JSON (default: `<input_basename>_template.json`).
