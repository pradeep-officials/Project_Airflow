from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
print('pradeep################################')

print(spark)
print('printing all configs##########')
print(spark.sparkContext.getConf().getAll())
print('spark sesion created###############################')
inp = spark.read.format('csv').options(header=True, inferSchema=True).option("delimiter", ",").load('/tmp/processed_user.csv')##the input file needs to be in spark worker container
print('file read,df created################')
inp.createOrReplaceTempView("users")
print('temp vew created#########################')
res = spark.sql("select *  from users")
res.show()
print('res df created#######################')
# res.show(10, False)
res.write.csv('/tmp/output/',mode="overwrite",header=True)
print('output saved created####################')

