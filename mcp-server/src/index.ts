import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'dayi-mcp-server',
  version: '0.1.0',
});

server.tool(
  'dayi_query',
  {
    type: z.enum(['medical', 'disease', 'doctor', 'symptom']),
    keyword: z.string().min(1),
  },
  async ({ type, keyword }) => {
    return {
      content: [
        {
          type: 'text',
          text: `TODO: bridge to Python Core for type=${type}, keyword=${keyword}`,
        },
      ],
      structuredContent: {
        status: 'todo',
        type,
        keyword,
      },
    };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
