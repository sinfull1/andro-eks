import pulumi
from lokistack import loki_stack_values
from kafka.kafka_bitnami_values import kafka_values
from mimir.mimir_values import mimir_values
import pulumi_awsx as awsx
import pulumi_aws as aws
import pulumi_eks as eks
import pulumi_kubernetes as k8s

config = pulumi.Config()


def create_cluster(tags=None):
    if tags is None:
        tags = {}
    eks_vpc = awsx.ec2.Vpc("andromeda-eks-vpc",
                          instance_tenancy="default",
                          enable_dns_hostnames=True,
                          number_of_availability_zones=2,
                          tags=tags)

    eks_cluster = eks.Cluster("andromeda-cluster",
                              name="andromeda-cluster",
                              # Put the cluster in the new VPC created earlier
                              vpc_id=eks_vpc.vpc_id,
                              # Public subnets will be used for load balancers
                              public_subnet_ids=eks_vpc.public_subnet_ids,
                              # Private subnets will be used for cluster nodes
                              private_subnet_ids=eks_vpc.private_subnet_ids,
                              # Change configuration values to change any of the following settings
                              instance_type="t3.medium",
                              #instance_role=aws.iam.Role.get("cluster-node-role", "cluster-node-role"),
                              desired_capacity=2,
                              min_size=2,
                              max_size=2,
                              # Do not give worker nodes a public IP address
                              node_associate_public_ip_address=False,
                              # public_access_cidrs=["0.0.0.0/0"],
                              # Uncomment the next two lines for private cluster (VPN access required)
                              endpoint_private_access=True,
                              # use this tooo script socometing
                              # node_user_data=user_data,
                              public_access_cidrs=["0.0.0.0/0"],
                              endpoint_public_access=True,
                              )

    eks_provider = k8s.Provider("eks-provider", kubeconfig=eks_cluster.kubeconfig_json)

    example = aws.eks.Addon("aws-ebs-csi-driver",
                            addon_name="aws-ebs-csi-driver",
                            addon_version="v1.16.0-eksbuild.1",
                            cluster_name=eks_cluster.name,
                            resolve_conflicts="OVERWRITE")
    pulumi.export("kubeconfig",example.cluster_name)
    return eks_provider



def create_kafka(eks_provider):
    namespace = k8s.core.v1.Namespace(
        "kafka",
        metadata={
            "name": "kafka"
        },
        opts=pulumi.ResourceOptions(provider=eks_provider)
    )

    charts = k8s.helm.v3.Chart("kafka",
                               k8s.helm.v3.ChartOpts(chart="kafka",
                                                     namespace=namespace.metadata["name"],
                                                     version="20.0.0",
                                                     fetch_opts=k8s.helm.v3.FetchOpts(
                                                         repo="https://charts.bitnami.com/bitnami"
                                                     ),
                                                     values=kafka_values
                                                     ),
                               opts=pulumi.ResourceOptions(provider=eks_provider))


def create_loki(eks_provider):
    namespace = k8s.core.v1.Namespace(
        "loki-ns",
        metadata={
            "name": "loki-ns"
        },
        opts=pulumi.ResourceOptions(provider=eks_provider)

    )


    # Create the Helm chart resource
    chart = k8s.helm.v3.Chart("gf-loki-stack",
                              k8s.helm.v3.ChartOpts(
                                  chart="loki-stack",
                                  version="2.6.1",
                                  namespace=namespace.metadata["name"],
                                  fetch_opts=k8s.helm.v3.FetchOpts(
                                      repo="https://grafana.github.io/helm-charts"
                                  ),
                                  values=loki_stack_values
                              ), opts=pulumi.ResourceOptions(provider=eks_provider))



def create_grafana_operator(eks_provider):
    charts = k8s.helm.v3.Chart("grafana-agent",
                               k8s.helm.v3.ChartOpts(chart="grafana-agent-operator",
                                                     namespace="default",
                                                     version="0.2.12",
                                                     fetch_opts=k8s.helm.v3.FetchOpts(
                                                         repo="https://grafana.github.io/helm-charts"
                                                     )
                                                     ),
                               opts=pulumi.ResourceOptions(provider=eks_provider))

def create_kube_metrics(eks_provider):
    charts = k8s.helm.v3.Chart("kube-state-metrics",
                               k8s.helm.v3.ChartOpts(chart="kube-state-metrics",
                                                     namespace="default",
                                                     version="4.31.0",
                                                     fetch_opts=k8s.helm.v3.FetchOpts(
                                                         repo="https://prometheus-community.github.io/helm-charts"
                                                     )
                                                     ),
                               opts=pulumi.ResourceOptions(provider=eks_provider))




def create_clickhouse(eks_provider):
    charts = k8s.helm.v3.Chart("clickhouse-operator",
                               k8s.helm.v3.ChartOpts(chart="altinity-clickhouse-operator",
                                                     namespace="default",
                                                     version="0.20.3",
                                                     fetch_opts=k8s.helm.v3.FetchOpts(
                                                         repo="https://docs.altinity.com/clickhouse-operator/"
                                                     )
                                                     ),
                               opts=pulumi.ResourceOptions(provider=eks_provider))


def create_mimir(eks_provider):
    namespace = k8s.core.v1.Namespace(
        "mimir",
        metadata={
            "name": "mimir"
        },
        opts=pulumi.ResourceOptions(provider=eks_provider)
    )

    charts = k8s.helm.v3.Chart("mimir",
                               k8s.helm.v3.ChartOpts(chart="mimir-distributed",
                                                     namespace=namespace.metadata["name"],
                                                     version="4.1.0",
                                                     fetch_opts=k8s.helm.v3.FetchOpts(
                                                         repo="https://grafana.github.io/helm-charts"
                                                     ),
                                                     values=mimir_values
                                                     ),
                               opts=pulumi.ResourceOptions(provider=eks_provider))

def create_contour(eks_provider):
    namespace = k8s.core.v1.Namespace(
        "projectcontour",
        metadata={
            "name": "projectcontour"
        },
        opts=pulumi.ResourceOptions(provider=eks_provider)
    )

    charts = k8s.helm.v3.Chart("contour",
                               k8s.helm.v3.ChartOpts(chart="contour",
                                                     namespace=namespace.metadata["name"],
                                                     version="11.0.0",
                                                     fetch_opts=k8s.helm.v3.FetchOpts(
                                                         repo="https://charts.bitnami.com/bitnami"
                                                     ),
                                                     ),
                               opts=pulumi.ResourceOptions(provider=eks_provider))



