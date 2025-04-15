
Bash接続する

```
docker-compose exec mongodb24-primary /bin/sh
docker-compose exec mongodb24-secondary /bin/sh
docker-compose exec mongodb4-primary /bin/sh
docker-compose exec mongodb8-primary /bin/sh
```

Mongoに入る

```
# 2.4, 4
mongo

# 8
mongosh
```


```
use test

db.users.find({})

db.users.insert(
	{name: "テストユーザー", email: "test@example.com", age: 30, createdAt: new Date()}
);

db.users.update(
    { email: "test@example.com" },
    { $set: { age: 35 } }
);

db.users.remove({email: "test@example.com"});
```

oplogを確認する

```
use local
rs.slaveOk()
db.oplog.rs.find({})
```

oplogのサイズを確認する

```
rs0:SECONDARY> db.oplog.rs.stats()
{
	"ns" : "local.oplog.rs",
	"count" : 4,
	"size" : 492, // 実際に使用されているバイト数
	"avgObjSize" : 123,
	"storageSize" : 11356061616,  // 確保されたストレージサイズ (固定サイズ)
	"numExtents" : 6,
	"nindexes" : 0,
	"lastExtentSize" : 623927296,
	"paddingFactor" : 1,
	"systemFlags" : 0,
	"userFlags" : 0,
	"totalIndexSize" : 0,
	"indexSizes" : {

	},
	"capped" : true,
	"max" : NumberLong("9223372036854775807"),
	"ok" : 1
}
```

レプリケーションの確認

```
rs0:SECONDARY> rs.status()
{
	"set" : "rs0",
	"date" : ISODate("2025-04-04T05:09:32Z"),
	"myState" : 2,
	"syncingTo" : "mongodb-primary:27017",
	"members" : [
		{
			"_id" : 0,
			"name" : "mongodb-primary:27017",
			"health" : 1,
			"state" : 1,
			"stateStr" : "PRIMARY",
			"uptime" : 503,
			"optime" : Timestamp(1742367118, 1),
			"optimeDate" : ISODate("2025-03-19T06:51:58Z"),
			"lastHeartbeat" : ISODate("2025-04-04T05:09:31Z"),
			"lastHeartbeatRecv" : ISODate("2025-04-04T05:09:31Z"),
			"pingMs" : 0
		},
		{
			"_id" : 1,
			"name" : "mongodb-secondary:27017",
			"health" : 1,
			"state" : 2,
			"stateStr" : "SECONDARY",
			"uptime" : 504,
			"optime" : Timestamp(1742367118, 1),
			"optimeDate" : ISODate("2025-03-19T06:51:58Z"),
			"self" : true
		},
		{
			"_id" : 2,
			"name" : "mongodb-arbiter:27017",
			"health" : 1,
			"state" : 7,
			"stateStr" : "ARBITER",
			"uptime" : 503,
			"lastHeartbeat" : ISODate("2025-04-04T05:09:31Z"),
			"lastHeartbeatRecv" : ISODate("2025-04-04T05:09:30Z"),
			"pingMs" : 0
		}
	],
	"ok" : 1
}
```

同期日時の確認

```
rs0:SECONDARY> db.printSlaveReplicationInfo()
source:   mongodb-secondary:27017
     // 現在日時に近ければ正常に同期している
	 syncedTo: Wed Mar 19 2025 06:51:58 GMT+0000 (UTC)
		 = 1376327 secs ago (382.31hrs)
source:   mongodb-arbiter:27017
	 no replication info, yet.  State: ARBITER
```

2.4からダンプを取る

```
# mongodump --out /tmp
connected to: 127.0.0.1
Fri Apr  4 05:55:53.205 all dbs
Fri Apr  4 05:55:53.395 DATABASE: test	 to 	/tmp/test
Fri Apr  4 05:55:53.400 	test.system.indexes to /tmp/test/system.indexes.bson
Fri Apr  4 05:55:53.403 		 1 objects
Fri Apr  4 05:55:53.404 	test.users to /tmp/test/users.bson
Fri Apr  4 05:55:53.406 		 1 objects
Fri Apr  4 05:55:53.407 	Metadata for test.users to /tmp/test/users.metadata.json
```

2.4のダンプファイルを修正
(2.4の形式から4や8へリストアするとエラーになる場合があるため、補正)

```
python metadata.py
```


4や8へリストアする

```
# mongorestore --db test /tmp/dump/test --drop
```
