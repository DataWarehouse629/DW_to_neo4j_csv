# readme

## 再次清洗数据

观察源数据集：
```
product/productId: B00006HAXW
review/userId: A1RSDE90N6RSZF
review/profileName: Joseph M. Kotow
review/helpfulness: 9/9
review/score: 5.0
review/time: 1042502400
review/summary: Pittsburgh - Home of the OLDIES
review/text: I have all of the doo wop DVD's and this one is as good or better than the
1st ones. Remember once these performers are gone, we'll never get to see them again.
Rhino did an excellent job and if you like or love doo wop and Rock n Roll you'll LOVE
this DVD !!

product/productId: B00006HAXW
```

从movies.txt文件可以清洗出所有的productID与reviewerID的对应关系，以及reviewerID和profileName的对应关系。将其存入到csv文件中。

## 架设服务器

`neo4j 3.5.14`已经架设在云服务器`8.129.66.202:7687`

## neo4j-import所需的csv文件格式

```
# users.csv 用户ID和用户名，暂时不进行去重
userId:ID(User-ID),profileName:string
"A141HP4LYPWMSR","Brian E. Erland ""Rainbow Sphinx"""
"A328S9RN3U5M68","Grady Harp"
...

# titles.csv 产品名和产品标题（由作业1获得）
productId:ID(Product-ID),title:string
"B003AI2VGA","The Virgin of Juarez"
"B0078V2LCY","My Kingdom (English Subtitled)"
...

# not_found.csv 没能匹配到的产品（由作业1获得）
productId:ID(Product-ID)
"B002LSIAQU"
"B0041XQRR2"
...

# reviews.csv 用户ID与产品ID间的关系
:START_ID(User-ID),:END_ID(Product-ID)
"A141HP4LYPWMSR","B003AI2VGA"
"A328S9RN3U5M68","B003AI2VGA"
...

```

## 导入到库

由于服务器性能较低，并且数据量较大（百万数量级的联系），所以使用neo4j的import进行数据导入，将4个csv文件分别作为节点和联系导入数据库t.db。


```bash
neo4j-admin import --database=t.db --nodes:Product not_found.csv --nodes:Product titles.csv  --nodes:User users.csv --relationships:REVIEWED reviews.csv --ignore-duplicate-nodes=true --high-io=true 
```


图数据库的“模式”如下所示：

```sql
(:User{userId, profileName})-[:REVIEWES]->(:Product{productId, <title>})
```

也可以使用以CQL语句导入到数据库。
```sql
LOAD CSV WITH HEADERS FROM 'file:///titles.csv' AS row
MATCH (p: Product {productId: row.productId})
SET p.title = row.title;
```

结果如下

![result](info.png)

## 创建主键

为了便于查询，添加主键
```sql
CREATE INDEX ON :Product(productId)
CREATE INDEX ON :User(userId)
```    


## 已知

一个profile一个id只能一次