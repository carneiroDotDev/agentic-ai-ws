import * as fs from 'fs';
import * as path from 'path';

// Base directory for all file system operations (todos folder)
const BASE_DIR = path.join(process.cwd(), 'todos');

// Ensure the base directory exists
function ensureBaseDir(): void {
  if (!fs.existsSync(BASE_DIR)) {
    fs.mkdirSync(BASE_DIR, { recursive: true });
  }
}

// Validate that a path is within the allowed directory
function validatePath(filePath: string): string {
  const normalizedPath = path.normalize(filePath);
  const fullPath = path.resolve(BASE_DIR, normalizedPath);
  const baseDirResolved = path.resolve(BASE_DIR);

  if (!fullPath.startsWith(baseDirResolved)) {
    throw new Error(
      `Access denied: Path "${filePath}" is outside the allowed directory`,
    );
  }

  return fullPath;
}

// Get relative path from base directory
function getRelativePath(fullPath: string): string {
  const baseDirResolved = path.resolve(BASE_DIR);
  return path.relative(baseDirResolved, fullPath);
}

/**
 * Write content to a file
 */
export function writeFile(
  filePath: string,
  content: string,
): { success: boolean; message: string; path: string } {
  try {
    ensureBaseDir();
    const fullPath = validatePath(filePath);

    // Ensure the directory exists
    const dir = path.dirname(fullPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(fullPath, content, 'utf8');

    return {
      success: true,
      message: `File written successfully: ${getRelativePath(fullPath)}`,
      path: getRelativePath(fullPath),
    };
  } catch (error) {
    return {
      success: false,
      message: `Error writing file: ${error instanceof Error ? error.message : 'Unknown error'}`,
      path: filePath,
    };
  }
}

/**
 * Read content from a file
 */
export function readFile(filePath: string): {
  success: boolean;
  content?: string;
  message: string;
  path: string;
} {
  try {
    ensureBaseDir();
    const fullPath = validatePath(filePath);

    if (!fs.existsSync(fullPath)) {
      return {
        success: false,
        message: `File not found: ${getRelativePath(fullPath)}`,
        path: getRelativePath(fullPath),
      };
    }

    const content = fs.readFileSync(fullPath, 'utf8');

    return {
      success: true,
      content,
      message: `File read successfully: ${getRelativePath(fullPath)}`,
      path: getRelativePath(fullPath),
    };
  } catch (error) {
    return {
      success: false,
      message: `Error reading file: ${error instanceof Error ? error.message : 'Unknown error'}`,
      path: filePath,
    };
  }
}

/**
 * Delete a file
 */
export function deleteFile(pathToDelete: string): {
  success: boolean;
  message: string;
  path: string;
} {
  try {
    ensureBaseDir();
    const fullPath = validatePath(pathToDelete);

    if (!fs.existsSync(fullPath)) {
      return {
        success: false,
        message: `File not found: ${getRelativePath(fullPath)}`,
        path: getRelativePath(fullPath),
      };
    }

    const stats = fs.statSync(fullPath);

    if (!stats.isFile()) {
      return {
        success: false,
        message: `Path is not a file: ${getRelativePath(fullPath)}`,
        path: getRelativePath(fullPath),
      };
    }

    fs.unlinkSync(fullPath);
    return {
      success: true,
      message: `File deleted successfully: ${getRelativePath(fullPath)}`,
      path: getRelativePath(fullPath),
    };
  } catch (error) {
    return {
      success: false,
      message: `Error deleting file: ${error instanceof Error ? error.message : 'Unknown error'}`,
      path: pathToDelete,
    };
  }
}

/**
 * List all todo files in the directory
 */
export function listTodos(): {
  success: boolean;
  files?: string[];
  message: string;
} {
  try {
    ensureBaseDir();

    if (!fs.existsSync(BASE_DIR)) {
      return {
        success: true,
        files: [],
        message: 'No todos directory yet',
      };
    }

    const files = fs
      .readdirSync(BASE_DIR)
      .filter((file) => file.endsWith('.md') || file.endsWith('.txt'))
      .map((file) => file);

    return {
      success: true,
      files,
      message: `Found ${files.length} todo file(s)`,
    };
  } catch (error) {
    return {
      success: false,
      message: `Error listing todos: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

