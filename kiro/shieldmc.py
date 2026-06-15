import subprocess
import shlex
import os
from fastmcp import FastMCP, Context
from fastmcp.server.elicitation import AcceptedElicitation, DeclinedElicitation, CancelledElicitation


# Initialize the Security Shield Server
mcp = FastMCP("security-shield")


# Strict dynamic rule engines to scan strings before they can execute
BLOCKED_KEYWORDS = ["rm -rf", "destroy", "delete", "purge", "--force", "drop", "terminate"]
BLOCKED_FILES = [".aws/credentials", ".env", "id_rsa", "kube/config", "id_ed25519"]


@mcp.tool()
async def execute_local_command(ctx: Context, command: str) -> str:
    """
    Parses, validates, and runs terminal commands locally after intercepting 
    the request and securing explicit user approval inside Kiro.
    """
    cmd_clean = command.strip()


    # 1. Inspect for malicious/destructive string patterns
    if any(keyword in cmd_clean.lower() for keyword in BLOCKED_KEYWORDS):
        return f"\u274c SECURITY BLOCK: Command rejected. Prohibited destructive lifecycle keyword detected."


    if any(secret in cmd_clean for secret in BLOCKED_FILES):
        return f"\u274c SECURITY BLOCK: Command rejected. Unauthorized access attempt to sensitive credential directories."


    # 2. Dynamic Human-in-the-Loop User Elicitation Card
    # Setting response_type=None shifts the UI into a binary click-to-approve mode
    try:
        result = await ctx.elicit(
            message=f"Kiro AI wants to execute this local command:\n\n`{cmd_clean}`\n\nDo you want to allow this run?",
            response_type=None
        )
        
        # 3. Dynamic Action Verification Pattern Matching
        if result.action != "accept":
            return f"\u26a0\ufe0f USER REFUSED: Terminal execution aborted by the engineer (Action: {result.action})."
            
    except Exception as e:
        return f"\u274c ELICITATION FAILURE: Could not request authorization card from Kiro interface: {str(e)}"


    # 4. Secure Argument Splitting (Bypasses shell=True injection vulnerabilities)
    try:
        parsed_args = shlex.split(cmd_clean)
    except ValueError as format_err:
        return f"\u274c PARSING ERROR: Command contains invalid shell escaping structures: {str(format_err)}"


    # 5. Safe Execution Engine
    try:
        result_process = subprocess.run(
            parsed_args, 
            capture_output=True, 
            text=True, 
            timeout=45
        )
        
        if result_process.returncode == 0:
            # Token Saving Action: Limit return block logs to keep prompt scope condensed
            stdout_clean = result_process.stdout[:3000] + "\n[Truncated for token optimization]" if len(result_process.stdout) > 3000 else result_process.stdout
            return f"\u2705 Executed Successfully:\n{stdout_clean}"
        else:
            return f"\u274c Command Failed (Exit Code {result_process.returncode}):\n{result_process.stderr}"
            
    except subprocess.TimeoutExpired:
        return f"\u274c EXECUTION TIMEOUT: The command execution crossed the 45-second execution allowance wall."
    except Exception as run_err:
        return f"\u274c ENGINE ERROR: System process execution failure: {str(run_err)}"


if __name__ == "__main__":
    mcp.run()
