import flask
from flask.json import jsonify
import json
import uuid
from main import City
from Car import Car
from TrafficLight import TrafficLight

games = {}

app = flask.Flask(__name__)


def getAgents(model, trafficLights, cars):
    for agent in model.schedule.agents:
        if isinstance(agent, Car):
            cars.append(
                {
                    "id": agent.unique_id,
                    "x": float(agent.pos[0]),
                    "z": float(agent.pos[1]),
                    "orientation": agent.orientation,
                    "speedX": float(agent.speed[0]),
                    "speedZ": float(agent.speed[1]),
                    "turn": agent.turn,
                }
            )
        elif isinstance(agent, TrafficLight):
            trafficLights.append(
                {
                    "id": agent.unique_id,
                    "x": float(agent.pos[0]),
                    "z": float(agent.pos[1]),
                    "state": agent.state,
                    "orientation": agent.orientation,
                }
            )


@app.route("/games", methods=["POST"])
def create():
    global games
    id = str(uuid.uuid4())
    model = City()
    games[id] = model
    trafficLights = []
    cars = []
    getAgents(model, trafficLights, cars)
    return (
        "ok",
        201,
        (
            {
                "Location": f"/games/{id}",
                "cars": json.dumps(cars),
                "trafficLights": json.dumps(trafficLights),
            }
        ),
    )


@app.route("/games/<id>", methods=["GET"])
def queryState(id):
    global model
    model = games[id]
    model.step()
    trafficLights = []
    cars = []
    getAgents(model, trafficLights, cars)
    return (
        "ok",
        200,
        {
            "Location": f"/games/{id}",
            "cars": json.dumps(cars),
            "trafficLights": json.dumps(trafficLights),
        },
    )


app.run()
# app.run(host=)
