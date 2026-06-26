from graph.workflow import build_graph
from langgraph.types import Command


def main():

    graph = build_graph()

    print("\n***************************************** Healthcare Copilot *****************************************")

    user_query = input("\nEnter patient details:\n\n")

    initial_state = {
        "user_query": user_query,
        "patient_info": None,
        "therapy_plan": None,
        "next_agent": ""
    }

    config = {
        "configurable": {
            "thread_id": "patient_001"
        }
    }


    result = graph.invoke(initial_state, config=config)

    print("\n" + "=" * 50)
    print("FINAL STATE")
    print("=" * 50)

    print('Patient info: \n')
    print(result['patient_info'])
    
    print("\n" + "-" * 50)
    print('Therapy plan: \n')
    print(result['therapy_plan'])

    print("\n" + "-" * 50)
    print("\nQA RESULT")
    print(result["qa_result"])


    if "__interrupt__" in result:

        approval = input(
            "\nApprove? (approved/rejected): "
        )

        result = graph.invoke(
            Command(resume=approval),
            config=config
        )

    print("\n" + "-" * 50)
    print(result["approval_status"])


if __name__ == "__main__":
    main()