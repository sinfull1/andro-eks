loki_stack_values = {
    "loki": {
        "enabled": True,
        "config": {
            "auth_enabled": False,
            "server": {
                "http_listen_port": 3100
            },
            "ingester": {
                "lifecycler": {
                    "address": "127.0.0.1",
                    "ring": {
                        "kvstore": {
                            "store": "inmemory"
                        },
                        "replication_factor": 1
                    },
                    "final_sleep": "0s"
                },
                "chunk_idle_period": "5m",
                "chunk_retain_period": "30m"
            },
            "schema_config": {
                "configs": [
                    {
                        "from": "2020-01-01",
                        "store": "boltdb-shipper",
                        "object_store": "s3",
                        "schema": "v11",
                        "index": {
                            "prefix": "index_",
                            "period": "24h"
                        }
                    }
                ]
            },
            "storage_config": {
                "boltdb_shipper": {
                    "active_index_directory": "/data/loki/index",
                    "cache_location": "/data/loki/index_cache",
                    "shared_store": "s3"
                },

                "aws": {
                    "bucketnames": "my-loki-logs",
                    "endpoint": "https://s3.ap-south-1.amazonaws.com/",
                    "region": "ap-south-1",
                    "access_key_id": "AKIAVYCFWIXRMUYT2NC6",
                    "secret_access_key": "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",
                    "insecure": False,
                    "sse_encryption": False,
                    "http_config": {
                        "idle_conn_timeout": "90s",
                        "response_header_timeout": "0s",
                        "insecure_skip_verify": False
                    },
                    "s3forcepathstyle": False
                }
            },
            "limits_config": {
                "enforce_metric_name": False
            },
            "compactor": {
                "working_directory": "/data/loki/compactor",
                "shared_store": "aws",
                "compaction_interval": "5m"
            }
        },
        "persistence": {
            "enabled": True,
            "size": "10Gi",
            "storageClassName": "gp2"
        },
        "service": {
            "type": "ClusterIP",
        },
    },
    "promtail": {
        "enabled": True,
        "config": {
            "server": {
                "http_listen_port": 9080,
                "grpc_listen_port": 0
            },

            "positions": {
                "filename": "/run/promtail/positions.yaml",

            },

            "clients": [
                {
                    ## This is the URL to the loki service
                    "url": "http://gf-loki-stack.loki-ns.svc.cluster.local:3100/loki/api/v1/push",
                    "batchsize": 102400,
                    "batchwait": 1,
                    ## "backoff_config": {
                    ##     "minbackoff": "100ms",
                    ##     "maxbackoff": "5s",
                    ##     "maxretries": 10,
                    ## },
                    ## This is the name of the cluster  where promtail is running
                    "external_labels": {
                        "cluster": "k8s",
                        "namespace": "grafana-loki",
                    },
                }
            ],
            ## This is the config to scrape all kubernetes pods

        },
        "service": {
            "type": "ClusterIP"
        },
    },
    "grafana": {
        "enabled": True,
        "sidecar": {
            "datasources": {
                "enabled": True
            }
        },
        "image": {
            "tag": "8.3.5"
        }
    }
}
