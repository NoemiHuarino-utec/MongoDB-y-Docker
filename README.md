# MongoDB-y-Docker

Este es un repositorio donde desarrollamos un Caso Práctico con MongoDB y Docker del curso Base de Datos 2

## Estructura

- **Config Servers:** Hay 3 (configsvr1, configsvr2, configsvr3), cada uno es un nodo que almacenan la metadata del clúster, formando un Replica Set configReplSet.

- **Shards:** Hay dos shards (shard1 y shard2), cada uno con tres réplicas, formando dos Replica Sets shard1 y shard2.

- **Mongos:** Es el enrutador de MongoDB, que dirige las consultas al shard correcto.
