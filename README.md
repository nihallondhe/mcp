# MCP — Model Context Protocol Project

This repository contains the folder structure for a Model Context Protocol (MCP) project.

## Structure

```
mcp/
├── README.md
├── host/          # User-facing app that orchestrates requests to MCP servers
├── client/        # Connection logic, session handling, and auth
├── servers/
│   ├── file-server/   # MCP server exposing file tools & resources
│   ├── db-server/     # MCP server exposing database tools & resources
│   └── api-server/    # MCP server exposing API tools & resources
├── shared/        # Common schemas, types, and helpers
├── tests/         # Unit and integration tests
├── docs/          # Protocol notes, setup, and architecture docs
└── examples/      # Demo implementations for onboarding
```

## Components

- **Host**: The user-facing application that manages MCP client instances and orchestrates LLM interactions.
- **Client**: Handles connections, sessions, and authentication with MCP servers.
- **Servers**: Individual MCP servers that expose tools, resources, or prompts.
- **Shared**: Reusable schemas, types, and utility functions across the project.
- **Tests**: Unit and integration test suites.
- **Docs**: Architecture documentation, protocol notes, and setup guides.
- **Examples**: Sample client and server implementations for quick onboarding.
