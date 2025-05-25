import logging
from datetime import datetime, UTC
from enum import StrEnum
from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages


logger = logging.getLogger(__name__)


CONTINUE_TO_TOOL = "continue_to_tool"
CHAT_MODEL_NAME = "qwen3:0.6b"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class NodeEnum(StrEnum):
    AGENT = "agent"
    TOOLS = "tools"


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


@tool
def get_current_time() -> dict:
    """Return the current UTC time in ISO-8601 format.
    
    Returns:
        Current UTC time in ISO-8601 format.

    Example:
        {"utc": "2025-05-21T06:42:00Z"}

    """
    return {"utc": datetime.now(tz=UTC).strftime(format=DATETIME_FORMAT)}


tools = [get_current_time]

llm = ChatOllama(model=CHAT_MODEL_NAME, temperature=0.0).bind_tools(tools=tools)


def agent_node(state: AgentState) -> dict[str, list[BaseMessage]]:
    """Invokes the LLM to determine the next Action or generate a response.

    This node takes the current list of messages from the state, passes them
    to the LLM, and expects the LLM to either provide a direct answer or
    request a tool call.

    Args:
        state: The current state of the agent, containing the message history.

    Returns:
        A dictionary with a "messages" key, containing a list with the
        LLM's response (an AIMessage).

    """
    logger.info("---AGENT NODE---")
    return {"messages": [llm.invoke(input=state["messages"])]}


def tool_node(state: AgentState) -> dict[str, list[ToolMessage]]:
    """Executes tools if called by the LLM in the last AIMessage.

    This node checks the last message in the state. If it's an AIMessage
    with tool calls, it iterates through each tool call, executes the
    corresponding tool, and collects the results as ToolMessage objects.

    Args:
        state: The current state of the agent, containing the message history.

    Returns:
        A dictionary with a "messages" key, containing a list of ToolMessage
        objects representing the output of the executed tools. If no tools
        were called, or if the last message was not an AIMessage with tool
        calls, an empty list is returned for "messages".

    """
    logger.info("---TOOL NODE---")

    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return {"messages": []}

    tool_messages: list[ToolMessage] = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        logger.info(f"Calling tool: {tool_name} with args: {tool_call['args']}")

        selected_tool = next(
            (t for t in tools if t.name == tool_name), None
        )

        if selected_tool:
            try:
                tool_output = selected_tool.invoke(input=tool_call["args"])
                tool_messages.append(
                    ToolMessage(
                        content=str(tool_output),
                        tool_call_id=tool_call["id"],
                        name=tool_name,
                    )
                )
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {e}")
                tool_messages.append(
                    ToolMessage(
                        content=f"Error executing tool {tool_name}: {e}",
                        tool_call_id=tool_call["id"],
                        name=tool_name,
                    )
                )
        else:
            logger.warning(f"Tool {tool_name} not found.")
            tool_messages.append(
                ToolMessage(
                    content=f"Tool {tool_name} not found.",
                    tool_call_id=tool_call["id"],
                    name=tool_name,
                )
            )

    return {"messages": tool_messages}

def should_continue(state: AgentState) -> str:
    """Determines whether to continue with tool execution or end the process.

    This function checks the last message in the state. If it's an AIMessage
    and contains tool calls, it directs the graph to the tool node. Otherwise,
    it signals the end of the execution.

    Args:
        state: The current state of the agent.

    Returns:
        A string indicating the next step: `CONTINUE_TO_TOOL` if tool
        execution is needed, or `END` to terminate the graph.

    """
    logger.info("---SHOULD CONTINUE---")
    last_message = state["messages"][-1]
    return CONTINUE_TO_TOOL if isinstance(last_message, AIMessage) and last_message.tool_calls else END


graph = StateGraph(state_schema=AgentState)

graph.add_node(node=NodeEnum.AGENT.value, action=agent_node)
graph.add_node(node=NodeEnum.TOOLS.value, action=tool_node)

graph.set_entry_point(key=NodeEnum.AGENT.value)

graph.add_conditional_edges(
    source=NodeEnum.AGENT.value,
    path=should_continue,
    path_map={
        CONTINUE_TO_TOOL: NodeEnum.TOOLS.value,
        END: END,
    },
)

graph.add_edge(start_key=NodeEnum.TOOLS.value, end_key=NodeEnum.AGENT.value)

app = graph.compile()
