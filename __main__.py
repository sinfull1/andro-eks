from user_store import create_user_and_bucket
from eks_infra import *
from kafka_proxy import create_kafka_proxy

config = pulumi.Config()





#create_user_and_bucket("log", tags={"app": "log"})
eks_provider = create_cluster(tags={"app": "log"})

#create_loki(eks_provider)
#create_kafka(eks_provider)
#create_grafana_operator(eks_provider)
#create_kube_metrics(eks_provider)
#create_clickhouse(eks_provider)
#create_mimir(eks_provider)
#create_contour(eks_provider)
#create_kafka_proxy(eks_provider)