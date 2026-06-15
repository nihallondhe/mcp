# MCP Integration Guide for Kiro


## Overview


Model Context Protocol (MCP) servers extend Kiro's capabilities by providing specialized tools and data access. This steering guide covers MCP configuration, usage patterns, and best practices.


---


## Section 1: MCP Configuration


### 1.1 Configuration File Locations


**Workspace-level** (takes precedence):
```
.kiro/settings/mcp.json
```


**User-level** (global, lower precedence):
```
~/.kiro/settings/mcp.json
```


**Precedence Order:** Workspace config > User config


### 1.2 JSON Structure Requirements


```json
{
  "mcpServers": {
    "server-name": {
      "command": "python|docker|fastmcp",
      "args": ["arg1", "arg2"],
      "env": {}
    }
  }
}
```


**Critical Rules:**
- Single `mcpServers` object only (NOT multiple nested objects)
- No duplicate `mcpServers` keys
- Valid JSON structure required (use JSON validator before saving)
- Commas between server definitions required
- No trailing commas in arrays


### 1.3 Common Configuration Errors


| Error | Cause | Fix |
|-------|-------|-----|
| `Unexpected token '{'` | Multiple `mcpServers` objects or stray braces | Merge all servers into ONE `mcpServers` object |
| `is not valid JSON` | Syntax error (missing comma, trailing comma, unescaped quotes) | Validate JSON structure |
| `Tool not available` | MCP server not running or not configured | Check config, restart Kiro, verify server startup |


---


## Section 2: MCP Server Types


### 2.1 Python MCP Servers


**Configuration:**
```json
{
  "command": "python",
  "args": ["C:\\path\\to\\server.py"]
}
```


**When to use:**
- FastMCP-based servers
- Local Python scripts
- Direct file/resource access


**Advantages:**
- Fast startup
- Direct file system access
- No containerization overhead


---


### 2.2 Docker MCP Servers


**Configuration:**
```json
{
  "command": "docker",
  "args": [
    "run",
    "-i",
    "--rm",
    "-p", "3000:3000",
    "image-name"
  ]
}
```


**When to use:**
- Containerized deployments
- Remote access scenarios
- Reproducible environments


**Prerequisites:**
- Docker must be installed and running
- Image must be pre-built: `docker build -t image-name .`
- stdin/stdout communication via `-i` flag


**Important Notes:**
- Use `-i` for stdin/stdout MCP protocol communication
- `-rm` cleans up container after exit
- Port forwarding with `-p` is optional (only needed for HTTP endpoints)


---


### 2.3 FastMCP Cloud Servers


**Configuration:**
```json
{
  "command": "fastmcp",
  "args": ["run", "https://mcp-endpoint.url"]
}
```


**When to use:**
- Remote MCP endpoints
- AWS documentation servers
- Third-party cloud MCPs


---


## Section 3: MCP Tool Discovery & Usage


### 3.1 How to Access MCP Tools


**Step 1: Verify Configuration**
- Check `.kiro/settings/mcp.json` or `~/.kiro/settings/mcp.json`
- Ensure proper JSON syntax


**Step 2: Restart Kiro**
- Close and reopen Kiro IDE
- MCP servers auto-start on Kiro launch


**Step 3: Call MCP Tools**
- Tools become available after server startup
- Use tool name format: `mcp_<server-name>_<tool-name>`


### 3.2 Tool Availability Troubleshooting


| Symptom | Root Cause | Solution |
|---------|-----------|----------|
| Tool not found error | MCP not configured | Add server to mcp.json, restart Kiro |
| Server won't start | Python/Docker not available | Install Python 3.10+ or Docker |
| Command not found | Wrong file path | Use absolute path, verify file exists |
| Permission denied | Insufficient permissions | Check file permissions, use `python -c "import fastmcp"` |


---


## Section 4: kiro-context-locator MCP (Reference Implementation)


### 4.1 Purpose


Dynamic infrastructure resource lookup from JSON files stored in a `resources/` folder.


### 4.2 Configuration


**Python (Direct):**
```json
{
  "kiro-context-locator": {
    "command": "python",
    "args": ["C:\\path\\to\\kiro\\kiro_context_locator\\server.py"]
  }
}
```


**Docker (Containerized):**
```json
{
  "kiro-context-locator": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "-p", "3000:3000",
      "kiro-context-locator"
    ]
  }
}
```


### 4.3 Available Tools


**Tool 1: `get_infra_resource`**
```
get_infra_resource(resource_name: str) -> str
```
- Searches `resources/` folder for matching JSON file
- Case-insensitive filename matching
- Whitespace-trimmed search
- Returns compact, token-optimized output
- On error: Lists available resources


**Tool 2: `list_all_resources`**
```
list_all_resources() -> str
```
- Returns comma-separated list of all resource file names
- No parameters required


### 4.4 Using kiro-context-locator


**Example 1: List available resources**
```
list_all_resources()
→ "environments, execution-role-identifier, iam-execution-role, resources, service-main-service, task-def-web-api-task-def"
```


**Example 2: Get infrastructure resource**
```
get_infra_resource("service-main-service")
→ '{"clusterArn":"arn:aws:ecs:us-east-1:123456789012:cluster/production",...}'
```


**Example 3: Resource not found**
```
get_infra_resource("s3-buckets")
→ "ERROR: Resource 's3-buckets' not found. Available: environments, execution-role-identifier, iam-execution-role, resources, service-main-service, task-def-web-api-task-def"
```


### 4.5 Adding Resources to kiro-context-locator


**Directory Structure:**
```
kiro_context_locator/
├── server.py
├── Dockerfile
└── resources/
    ├── environments.json
    ├── service-main-service.json
    ├── task-def-web-api-task-def.json
    └── [your-resource-name].json
```


**To add a new resource:**
1. Create JSON file: `resources/your-resource-name.json`
2. Add infrastructure data to the file
3. Restart MCP server or Kiro
4. Call: `get_infra_resource("your-resource-name")`


**Example Resource File:**
```json
// resources/s3-buckets.json
{
  "buckets": [
    {
      "name": "my-org-logs-bucket",
      "region": "us-east-1",
      "created_date": "2024-01-15T10:30:00Z"
    },
    {
      "name": "my-org-artifacts-bucket",
      "region": "us-east-1",
      "created_date": "2024-01-20T14:45:00Z"
    }
  ]
}
```


---


## Section 5: MCP Best Practices


### 5.1 Do's


✅ **DO:** Use workspace-level mcp.json for project-specific MCPs  
✅ **DO:** Verify JSON syntax before saving (use online JSON validators)  
✅ **DO:** Use absolute file paths in configuration  
✅ **DO:** Restart Kiro after config changes  
✅ **DO:** Call MCP tools directly (no need to restart for each call)  
✅ **DO:** Store infrastructure data in resource files, not code  
✅ **DO:** Use case-insensitive resource name lookups  


### 5.2 Don'ts


❌ **DON'T:** Create multiple `mcpServers` objects in JSON  
❌ **DON'T:** Leave trailing commas in JSON arrays  
❌ **DON'T:** Use relative paths (always use absolute paths)  
❌ **DON'T:** Assume tools are available without restarting Kiro  
❌ **DON'T:** Mix Python and Docker servers without proper dependencies  
❌ **DON'T:** Store sensitive data in resource JSON files without encryption  
❌ **DON'T:** Call MCP tools before server startup completes  


---


## Section 6: Common Workflows


### 6.1 Workflow: Query Infrastructure via MCP


**Step 1:** Verify MCP is running
```
list_all_resources()
```


**Step 2:** Get specific resource
```
get_infra_resource("service-main-service")
```


**Step 3:** Parse response
- Extract data from returned JSON/text
- Use in deployment or configuration tasks


### 6.2 Workflow: Add New Infrastructure Resource


**Step 1:** Create resource JSON file
```
kiro_context_locator/resources/my-new-resource.json
```


**Step 2:** Add infrastructure data
```json
{
  "key1": "value1",
  "key2": "value2"
}
```


**Step 3:** Query via MCP
```
get_infra_resource("my-new-resource")
```


### 6.3 Workflow: Switch Between Python and Docker


**Current: Python**
```json
{
  "kiro-context-locator": {
    "command": "python",
    "args": ["C:\\path\\to\\server.py"]
  }
}
```


**Switch to Docker:**
1. Build image: `docker build -t kiro-context-locator .`
2. Update config:
```json
{
  "kiro-context-locator": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "-p", "3000:3000", "kiro-context-locator"]
  }
}
```
3. Restart Kiro


---


## Section 7: Troubleshooting MCP Issues


### Issue 1: MCP Server Won't Start


**Symptoms:** Tool not found, connection refused  
**Diagnosis:**
- Check Python/Docker installation
- Verify file paths are correct
- Check file permissions


**Resolution:**
```bash
# Test Python installation
python --version


# Test Docker installation
docker --version


# Check file exists
ls -la /path/to/server.py
```


### Issue 2: JSON Configuration Error


**Symptoms:** "Unexpected token", "is not valid JSON"  
**Diagnosis:**
- Multiple `mcpServers` objects
- Stray braces or commas
- Unescaped quotes


**Resolution:**
- Use single, unified `mcpServers` object
- Validate JSON online
- Check for duplicate keys


### Issue 3: Tool Calls Return "Not Available"


**Symptoms:** Tool exists but returns "not available" error  
**Diagnosis:**
- MCP server crashed
- Kiro not refreshed after config change
- Server startup incomplete


**Resolution:**
1. Restart Kiro
2. Verify server startup in logs
3. Check MCP config syntax
4. Wait 5-10 seconds after Kiro launch before calling tools


---


## Section 8: Reference: MCP Configuration Template


### Complete Minimal Setup


```json
{
  "mcpServers": {
    "kiro-context-locator": {
      "command": "python",
      "args": [
        "C:\\path\\to\\kiro\\kiro_context_locator\\server.py"
      ]
    }
  }
}
```


### Multi-Server Setup


```json
{
  "mcpServers": {
    "aws-docs": {
      "command": "fastmcp",
      "args": ["run", "https://knowledge-mcp.global.api.aws"],
      "env": {},
      "autoApprove": ["aws___read_documentation"]
    },
    "kiro-context-locator": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-p", "3000:3000", "kiro-context-locator"]
    }
  }
}
```


---


## Summary


- **Configuration:** Use workspace-level `.kiro/settings/mcp.json`
- **Syntax:** Single `mcpServers` object, valid JSON required
- **Usage:** Call MCP tools directly after Kiro restart
- **Resources:** Store infrastructure data in `resources/` folder as JSON
- **Troubleshooting:** Verify config, restart Kiro, check server startup
- **Best Practice:** Use absolute paths, validate JSON, restart after config changes
