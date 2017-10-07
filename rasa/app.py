from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter

tasks = list()
interpreter = None
model_path = "/Users/ma0/Desktop/contraslash/keynotes/chatbots-intro/rasa/models/default/model_20171006-164306"
config_path = "/Users/ma0/Desktop/contraslash/keynotes/chatbots-intro/rasa/config.json"


def configure():
    global interpreter
    interpreter = Interpreter.load(
        Metadata.load(model_path),
        RasaNLUConfig(config_path)
    )


def extration_and_classification(raw_text):
    global interpreter
    response = interpreter.parse(raw_text)
    entities = {
        "indexes": list(),
        "tasks": list()
    }
    for entity in response["entities"]:
        if entity["entity"] == "task":
            entities["tasks"].append(entity["value"])
        elif entity["entity"] == "task_id":
            entities["indexes"].append(int(entity["value"]))
    return(
        entities,
        response["intent"]["name"]
    )


def production(intent, entities):
    if intent == "list":
        return "Todas las tareas son: \n{}".format(
            "{}".format(
                "\n".join(
                    [
                        "{} - {}".format(x, y) for x, y in zip(
                            range(len(tasks)),
                            tasks
                        )
                    ]
                )
            )
        )

    elif intent == "show":
        return "Las tareas solicitadas son: {}".format(
            "\n".join(
                [tasks[i] for i in entities["indexex"]]
            )
        )
    elif intent == "create":
        [tasks.append(task) for task in entities["tasks"]]
        return "Tareas agregadas"
    elif intent == "delete":
        [tasks.pop(index) for index in entities["indexes"]]
        return "Tareas eliminadas"
    else:
        "No entiendo lo que quieres decir"


if __name__ == "__main__":
    print("Loading model")
    configure()
    raw_text = input("Bienvenido a tu lista de tareas, que deseas hacer > ")
    while raw_text != "salir":
        entities, intent = extration_and_classification(raw_text)
        response = production(intent, entities)

        print(response) if response is not None else ""
        raw_text = input("que otra cosa deseas hacer > ")
