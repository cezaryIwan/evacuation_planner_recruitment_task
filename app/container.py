import punq
from app.services.road_map_service import RoadMapService

def create_container():
    container = punq.Container()

    container.register(RoadMapService, RoadMapService)
    container.register()

    return container

container = create_container()
