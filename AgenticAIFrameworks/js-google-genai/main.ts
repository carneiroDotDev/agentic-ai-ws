import {
  FunctionDeclaration,
  GoogleGenerativeAI,
  SchemaType,
} from '@google/generative-ai';
import * as readline from 'readline';
import * as fsTools from './file-system-tools.js';

// Initialize the Google Generative AI client
if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
  console.error('❌ Error: GOOGLE_GENERATIVE_AI_API_KEY not found in .env file');
  process.exit(1);
}

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);

// Define the tools that the agent can use
const tools: FunctionDeclaration[] = [
  {
    name: 'writeFile',
    description:
      'Write content to a todo file. Use markdown format for better organization. Always add .md extension if not provided.',
    parameters: {
      type: SchemaType.OBJECT,
      properties: {
        filePath: {
          type: SchemaType.STRING,
          description: 'The path to the file (e.g., "todos.md" or "shopping-list.md")',
        },
        content: {
          type: SchemaType.STRING,
          description: 'The content to write to the file',
        },
      },
      required: ['filePath', 'content'],
    },
  },
  {
    name: 'readFile',
    description: 'Read the content of a todo file',
    parameters: {
      type: SchemaType.OBJECT,
      properties: {
        filePath: {
          type: SchemaType.STRING,
          description: 'The path to the file to read (e.g., "todos.md")',
        },
      },
      required: ['filePath'],
    },
  },
  {
    name: 'deleteFile',
    description: 'Delete a todo file',
    parameters: {
      type: SchemaType.OBJECT,
      properties: {
        filePath: {
          type: SchemaType.STRING,
          description: 'The path to the file to delete (e.g., "todos.md")',
        },
      },
      required: ['filePath'],
    },
  },
  {
    name: 'listTodos',
    description: 'List all todo files in the todos directory',
    parameters: {
      type: SchemaType.OBJECT,
      properties: {},
    },
  },
];

// Execute a tool call
function executeTool(toolName: string, args: any): any {
  console.log(`📝 Executing: ${toolName}`);

  switch (toolName) {
    case 'writeFile':
      console.log(`📝 Writing to file: ${args.filePath}`);
      const writeResult = fsTools.writeFile(args.filePath, args.content);
      if (writeResult.success) {
        console.log(`✅ Successfully wrote to ${args.filePath}`);
      } else {
        console.log(`❌ Failed to write to ${args.filePath}: ${writeResult.message}`);
      }
      return writeResult;

    case 'readFile':
      console.log(`📖 Reading file: ${args.filePath}`);
      const readResult = fsTools.readFile(args.filePath);
      if (readResult.success) {
        console.log(`✅ Successfully read ${args.filePath}`);
      } else {
        console.log(`❌ Failed to read ${args.filePath}: ${readResult.message}`);
      }
      return readResult;

    case 'deleteFile':
      console.log(`🗑️  Deleting file: ${args.filePath}`);
      const deleteResult = fsTools.deleteFile(args.filePath);
      if (deleteResult.success) {
        console.log(`✅ Successfully deleted ${args.filePath}`);
      } else {
        console.log(`❌ Failed to delete ${args.filePath}: ${deleteResult.message}`);
      }
      return deleteResult;

    case 'listTodos':
      console.log(`📋 Listing all todo files...`);
      const listResult = fsTools.listTodos();
      if (listResult.success) {
        console.log(`✅ Found ${listResult.files?.length || 0} todo file(s)`);
      } else {
        console.log(`❌ Failed to list todos: ${listResult.message}`);
      }
      return listResult;

    default:
      return { error: `Unknown tool: ${toolName}` };
  }
}

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

// Agent loop implementation
async function runAgentLoop(userMessage: string): Promise<string> {
  const model = genAI.getGenerativeModel({
    model: 'gemini-2.0-flash-exp',
    tools: [{ functionDeclarations: tools }],
  });

  const chat = model.startChat({
    history: [],
  });

  let toolCallCounter = 0;
  let maxSteps = 10;
  let currentStep = 0;

  // Send initial user message with system prompt
  let result = await chat.sendMessage([systemPrompt, userMessage].join('\n\n'));

  while (currentStep < maxSteps) {
    currentStep++;
    const response = result.response;

    // Check if there are function calls
    const functionCalls = response.functionCalls();

    if (!functionCalls || functionCalls.length === 0) {
      // No more tool calls, return the final text
      return response.text();
    }

    // Execute each function call
    const functionResponses = functionCalls.map((call) => {
      toolCallCounter++;
      console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
      console.log(`🔧 Tool Call #${toolCallCounter}`);
      console.log(`📌 Tool Name: ${call.name}`);
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

      // Log the request (parameters)
      console.log(`📤 Tool Request:`);
      console.log(JSON.stringify(call.args, null, 2));
      console.log();

      // Execute the tool
      const toolResult = executeTool(call.name, call.args);

      console.log(`📥 Tool Response:`);
      console.log(JSON.stringify(toolResult, null, 2));
      console.log();

      return {
        functionResponse: {
          name: call.name,
          response: toolResult,
        },
      };
    });

    // Send the function responses back to the model
    result = await chat.sendMessage(functionResponses);

    // Show the LLM's response after processing tool results
    const llmResponse = result.response.text();
    if (llmResponse && llmResponse.trim()) {
      console.log(`💭 LLM Processing:`);
      console.log(`   ${llmResponse}`);
      console.log();
    }
  }

  // Max steps reached
  return result.response.text() || 'Maximum steps reached.';
}

// CLI interface
async function main() {
  console.log('🤖 Todo Agent - Google Generative AI SDK (Raw Implementation)\n');
  console.log('Using Google Gemini 2.0 Flash\n');
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
      const response = await runAgentLoop(userInput);
      console.log(`\n🤖 Agent: ${response}\n`);
    } catch (error) {
      console.error(
        '❌ Error:',
        error instanceof Error ? error.message : 'Unknown error',
      );
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

