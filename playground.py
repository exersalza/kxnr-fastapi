import docker
from docker.models.containers import Container
from docker.models.images import Image

client = docker.from_env()
container: Container = client.containers.get('58d')
con = {
    'name': container.name,
    'id': container.id,
    'labels': container.labels,
    'images': container.image.tags,
    'short_id': container.short_id,
    'diff': container.diff(),
    'status': container.status,
}

print(container.image.tags)

