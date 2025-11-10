# Quick Setup Guide

## 1. Create your .env file

Create a file named `.env` in this directory with at least one API key:

```bash
# Gemini API Key (one of these three is needed)
GOOGLE_GENERATIVE_AI_API_KEY="insert-secret-key-here"

# Anthropic API Key (one of these three is needed)
ANTHROPIC_API_KEY="insert-secret-key-here"

# OpenAI API Key (one of these is needed)
OPENAI_API_KEY="insert-secret-key-here"
```

Replace `insert-secret-key-here` with your actual API key from:
- Google Gemini: https://aistudio.google.com/app/apikey
- Anthropic Claude: https://console.anthropic.com/
- OpenAI GPT: https://platform.openai.com/api-keys

**Note**: You only need ONE API key, but you can have multiple. The agent will use them in this priority: Gemini → Claude → GPT.

## 2. Install dependencies

```bash
npm install
```

## 3. Run the agent

For production (no auto-reload):
```bash
npm start
```

For development (with auto-reload on code changes, ignoring todos folder):
```bash
npm run dev
```

**Note**: The dev script automatically ignores changes in the `todos/` folder to prevent the app from reloading while you're typing.

## Example Prompts to Try

### Creating and Managing Lists
- "Create a shopping list" (automatically creates shopping-list.md)
- "Create a todo list called work-tasks"
- "List all my todo files"

### Adding Tasks (Smart Formatting)
- "Add buy milk" → becomes "- [ ] Buy milk"
- "Add task do the homework" → becomes "- [ ] Do the homework"
- "Add finish report to work-tasks"

### Completing Tasks
- "Complete task buy milk"
- "Mark homework as done"
- "Complete the report task"

### Deleting Tasks
- "Delete task buy milk"
- "Remove homework from the list"

### Reading and Viewing
- "Show me my shopping list"
- "What's in my work-tasks?"
- "Read my todos"

### Other Operations
- "Delete the shopping list file"

**Note**: The agent is smart! You don't need to type ".md" extensions, and it automatically formats tasks with proper markdown checkboxes.

