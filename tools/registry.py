from tools.file_ops import read_text_file, write_immutable_summary
from tools.memory import search_historical_reports

AVAILABLE_TOOLS = {
    "read_text_file": read_text_file,
    "write_immutable_summary": write_immutable_summary,
    "search_historical_reports": search_historical_reports,
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "read_text_file",
            "description": "Read text content of a workspace file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "Filename to read.",
                    }
                },
                "required": ["file_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_immutable_summary",
            "description": "Save an immutable chronological audit report.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Full text report.",
                    }
                },
                "required": ["content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_historical_reports",
            "description": (
                "Search past historical summaries semantically for prior"
                " context."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query_string": {
                        "type": "string",
                        "description": "Natural language search query.",
                    }
                },
                "required": ["query_string"],
            },
        },
    },
]
