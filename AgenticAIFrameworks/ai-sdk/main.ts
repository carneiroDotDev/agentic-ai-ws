import { anthropic } from '@ai-sdk/anthropic';
import { google } from '@ai-sdk/google';
import { openai } from '@ai-sdk/openai';
import { generateText, tool, type LanguageModelV1 } from 'ai';
import { z } from 'zod';
import * as readline from 'readline';
import * as fsTools from './file-system-tools.js';

// Determine which model to use based on available API keys
function getModel(): LanguageModelV1 {
  if (process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
    console.log('Using Google Gemini model\n');
    return google('gemini-2.0-flash-exp');
  } else if (process.env.ANTHROPIC_API_KEY) {
    console.log('Using Anthropic Claude model\n');
    return anthropic('claude-3-5-sonnet-20241022');
  } else if (process.env.OPENAI_API_KEY) {
    console.log('Using OpenAI GPT model\n');
    return openai('gpt-4o');
  } else {
    throw new Error(
      'No API key found. Please set GOOGLE_GENERATIVE_AI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY in your .env file',
    );
  }
}

// Create tools for the AI agent
const tools = {
  writeFile: tool({
    description:
      'Write content to a todo file. Use markdown format for better organization.',
    parameters: z.object({
      filePath: z
        .string()
        .describe('The path to the file (e.g., "todos.md" or "shopping-list.txt")'),
      content: z.string().describe('The content to write to the file'),
    }),
    execute: async ({ filePath, content }) => {
      console.log(`📝 Writing to file: ${filePath}`);
      const result = fsTools.writeFile(filePath, content);
      if (result.success) {
        console.log(`✅ Successfully wrote to ${filePath}`);
      } else {
        console.log(`❌ Failed to write to ${filePath}: ${result.message}`);
      }
      return result;
    },
  }),

  readFile: tool({
    description: 'Read the content of a todo file',
    parameters: z.object({
      filePath: z
        .string()
        .describe('The path to the file to read (e.g., "todos.md")'),
    }),
    execute: async ({ filePath }) => {
      console.log(`📖 Reading file: ${filePath}`);
      const result = fsTools.readFile(filePath);
      if (result.success) {
        console.log(`✅ Successfully read ${filePath}`);
      } else {
        console.log(`❌ Failed to read ${filePath}: ${result.message}`);
      }
      return result;
    },
  }),

  deleteFile: tool({
    description: 'Delete a todo file',
    parameters: z.object({
      filePath: z
        .string()
        .describe('The path to the file to delete (e.g., "todos.md")'),
    }),
    execute: async ({ filePath }) => {
      console.log(`🗑️  Deleting file: ${filePath}`);
      const result = fsTools.deleteFile(filePath);
      if (result.success) {
        console.log(`✅ Successfully deleted ${filePath}`);
      } else {
        console.log(`❌ Failed to delete ${filePath}: ${result.message}`);
      }
      return result;
    },
  }),

  listTodos: tool({
    description: 'List all todo files in the todos directory',
    parameters: z.object({}),
    execute: async () => {
      console.log(`📋 Listing all todo files...`);
      const result = fsTools.listTodos();
      if (result.success) {
        console.log(`✅ Found ${result.files?.length || 0} todo file(s)`);
      } else {
        console.log(`❌ Failed to list todos: ${result.message}`);
      }
      return result;
    },
  }),
};

// System prompt for the agent
const systemPrompt = `You are a helpful todo list manager assistant. 

CRITICAL INSTRUCTIONS:

1. FILE NAMES:
   - ALWAYS add .md extension to filenames if the user doesn't specify an extension
   - If user says "AI-Poland", save it as "AI-Poland.md"
   - If user says "shopping-list", save it as "shopping-list.md"

2. ADDING TASKS:
   - When user says "add task X" or "add X to my list", format it as: - [ ] X
   - Automatically capitalize the first letter of tasks
   - Example: "add do the homework" becomes "- [ ] Do the homework"

3. COMPLETING TASKS:
   - When user says "complete task X" or "mark X as done":
   - Read the file, find the task containing X, change - [ ] to - [x]
   - Be flexible with matching (partial matches are OK)

4. DELETING TASKS:
   - When user says "delete task X" or "remove task X":
   - Read the file, find and remove the line containing task X
   - Be flexible with matching

5. TASK FORMAT:
   Always use markdown checkbox format:
   - [ ] Incomplete task
   - [x] Completed task

6. FILE STRUCTURE:
   When creating new todo files, use this format:
   # [Filename without extension]
   
   - [ ] Task 1
   - [ ] Task 2

Be conversational, efficient, and always confirm actions taken.`;

// CLI interface
async function main() {
  console.log('🤖 Todo Agent - Your AI-powered todo list manager\n');
  console.log('Type your requests or "exit" to quit.\n');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const askQuestion = (query: string): Promise<string> => {
    return new Promise((resolve) => rl.question(query, resolve));
  };

  // Agent loop
  while (true) {
    const userInput = await askQuestion('\n💬 You: ');

    if (userInput.toLowerCase() === 'exit') {
      console.log('\n👋 Goodbye!');
      rl.close();
      break;
    }

    if (!userInput.trim()) {
      continue;
    }

    console.log('\n🤔 Agent is thinking...\n');

    try {
      const result = await generateText({
        model: getModel(),
        system: systemPrompt,
        prompt: userInput,
        tools,
        maxSteps: 10, // Limit the number of tool calls to prevent infinite loops
      });

      // Display detailed tool call information
      if (result.steps && result.steps.length > 0) {
        let toolCallCounter = 0;
        
        result.steps.forEach((step) => {
          if (step.toolCalls && step.toolCalls.length > 0) {
            step.toolCalls.forEach((toolCall) => {
              toolCallCounter++;
              console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
              console.log(`🔧 Tool Call #${toolCallCounter}`);
              console.log(`📌 Tool Name: ${toolCall.toolName}`);
              console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
              
              // Log the request (arguments)
              console.log(`📤 Tool Request:`);
              console.log(JSON.stringify(toolCall.args, null, 2));
              console.log();
            });
          }

          if (step.toolResults && step.toolResults.length > 0) {
            step.toolResults.forEach((toolResult) => {
              console.log(`📥 Tool Response:`);
              console.log(JSON.stringify(toolResult.result, null, 2));
              console.log();
            });
          }

          // Show text generated by the LLM after processing tool results
          if (step.text && step.text.trim()) {
            console.log(`💭 LLM Processing:`);
            console.log(`   ${step.text}`);
            console.log();
          }
        });
      }

      // Display the agent's response
      console.log(`\n🤖 Agent: ${result.text}\n`);
    } catch (error) {
      console.error('❌ Error:', error instanceof Error ? error.message : 'Unknown error');
    }
  }
}

// Handle errors and exit
process.on('SIGINT', () => {
  console.log('\n\n👋 Goodbye!');
  process.exit(0);
});

// Run the agent
main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});

