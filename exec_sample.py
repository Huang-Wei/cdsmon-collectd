from docker import Client
import os
import sys

def main():
    pod_name = os.environ.get("POD_NAME", None)

    if not pod_name:
        print 'make sure POD_NAME is injected to the container as an env variable'
        sys.exit(1)

    cli = Client(base_url='unix://var/run/docker.sock')

    containers = cli.containers(filters={'label': 'io.kubernetes.pod.name='+pod_name})

    container_id = None
    for container in containers:
        if container['Labels']['io.kubernetes.container.name'] == 'nginx':
            container_id = container['Id']
            break
        # if container['Labels']['io.kubernetes.container.name'] not in ('cdsmon-collectd', 'POD'):
        #     container_id = container['Id']
        #     break

    if not container_id:
        print 'cannot pick container id automatically'
        sys.exit(1)

    cmd = cli.exec_create(container=container_id, cmd='hostname')
    print cli.exec_start(cmd)

if __name__ == '__main__':
    main()
