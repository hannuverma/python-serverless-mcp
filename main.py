from fastmcp import FastMCP


mcp = FastMCP("IIITSONEPAT MCP serverless")


@mcp.tool()
async def getDetails():
    """
    This function is used to get details about IIITSONEPAT
    """
    return {
        "name": "IIITSONEPAT",
        "address": "Oneil Road, Sonepat, Haryana",
        "established": 2019,
    }

app = mcp.http_app(stateless_http=True, json_response=True)