from langgraph.graph import StateGraph, START, END

from agents.human_review import human_review
from agents.qa import qa_agent
from agents.report import report_agent
from agents.retriever import retrieval_agent
from graph.state import HealthcareState

from agents.supervisor import supervisor
from agents.intake import intake_agent
from agents.planner import planning_agent
from langgraph.checkpoint.memory import InMemorySaver


def route_agent(state: HealthcareState):

    return state["next_agent"]


def build_graph():

    workflow = StateGraph(HealthcareState)

    # Nodes
    workflow.add_node("supervisor", supervisor)
    workflow.add_node("intake", intake_agent)
    workflow.add_node("retriever", retrieval_agent)
    workflow.add_node("planner", planning_agent)
    workflow.add_node("qa", qa_agent)
    workflow.add_node("human_review", human_review)
    workflow.add_node("report", report_agent)

    # Start
    workflow.add_edge(START, "supervisor")

    # Routing from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        route_agent,
        {
            "intake": "intake",
            "retriever": "retriever",
            "planner": "planner",
            "qa": "qa",
            "human_review": "human_review",
            "report": "report",
            "end": END
        }
    )

    # Return to supervisor after each agent
    workflow.add_edge("intake", "supervisor")
    workflow.add_edge("retriever", "supervisor")
    workflow.add_edge("planner", "supervisor")
    workflow.add_edge("qa", "supervisor")
    workflow.add_edge("human_review", "supervisor")
    workflow.add_edge("report", "supervisor")

    checkpointer = InMemorySaver()

    return workflow.compile(checkpointer=checkpointer)
