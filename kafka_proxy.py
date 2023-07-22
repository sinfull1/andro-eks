
import pulumi_kubernetes as k8s
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import ContainerArgs, PodSpecArgs, PodTemplateSpecArgs
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
import pulumi


def create_kafka_proxy(eks_provider):
    # Define the metadata for the deployment
    labels = {"app": "kafka-proxy"}


    namespace = k8s.core.v1.Namespace(
        "kafka-proxy",
        metadata={
            "name": "kafka-proxy"
        },
        opts=pulumi.ResourceOptions(provider=eks_provider)
    )


    service = k8s.core.v1.Service(
        "kafka-proxy-svc",
        metadata={
            "name": "kafka-proxy-svc",
            "namespace": namespace.metadata["name"],
            "labels": {"app": "kafka-proxy"}
        },
        spec={
            "ports": [
                {"name": "http", "port": 8080, "protocol": "TCP", "targetPort": 8080}
            ],
            "selector": {
                "app": "kafka-proxy"
            },
            "type": "ClusterIP"
        },
        opts=pulumi.ResourceOptions(provider=eks_provider)
    )




    metadata = ObjectMetaArgs(
        name="kafka-proxy",
        namespace="kafka-proxy",
        labels=labels,
    )

    # Define the container for the deployment
    container = ContainerArgs(
        name="kafka-proxy",
        image="public.ecr.aws/p7u1n1n0/razor:kprxy",
    )

    # Define the pod spec for the deployment
    pod_spec = PodSpecArgs(
        containers=[container],
    )

    # Define the pod template for the deployment
    pod_template = PodTemplateSpecArgs(
        metadata=metadata,
        spec=pod_spec,
    )

    # Define the label selector for the deployment
    selector = LabelSelectorArgs(
        match_labels=labels,
    )

    # Define the deployment spec for the deployment
    deployment_spec = DeploymentSpecArgs(
        replicas=1,
        selector=selector,
        template=pod_template,
    )

    # Create the deployment
    deployment = Deployment(
        "kafka-proxy",
        metadata=metadata,
        spec=deployment_spec,
    )
