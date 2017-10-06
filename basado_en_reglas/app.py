__author__ = "Mauricio Collazos"

tasks = list()


def extraction(raw_text):
    entities = {
        "indexes": list(),
        "tasks": list()
    }
    words = raw_text.split()

    # Extract indexes:
    for word in words:
        try:
            task_index = int(word)
            entities["indexes"].append(task_index)
        except ValueError:
            pass
    # Extract Taks:
    if ":" in raw_text:
        tasks = raw_text[raw_text.index(":")+1:]
        entities["tasks"] = tasks.split(",")
    return entities


def classification(raw_text):
    if "listar" in raw_text:
        return "list"
    if "mostrar" in raw_text:
        return "show"
    if "crear" in raw_text:
        return "create"
    if "eliminar" in raw_text:
        return "delete"
    return ""


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
    # print()
    raw_text = input("Bienvenido a tu lista de tareas, que deseas hacer > ")
    while raw_text != "salir":
        entities = extraction(raw_text)
        intent = classification(raw_text)
        response = production(intent, entities)

        print(response) if response is not None else ""
        raw_text = input("que otra cosa deseas hacer > ")
