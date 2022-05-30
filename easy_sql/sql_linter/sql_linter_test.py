import unittest

from easy_sql.sql_linter.sql_linter import SqlLinter

class SqlLinterTest(unittest.TestCase):

    def test_should_work_for_all_define_rule(self):
        sql="""-- backend: bigquery
-- target=variables
select
    translate('${data_date}', '-', '')  as data_date_no_ds
    , true                              as __create_hive_table__
    
-- target=temp.model_data
select * from sales_model_demo_with_label where date='${data_date_no_ds}'


-- target=temp.feature_stage_0_out
select * from ${temp_db}.model_data
"""
        sql_linter=SqlLinter(sql)
        sql_linter.set_include_rules(['L039', 'L048', 'BigQuery_L001'])
        sql_linter.set_exclude_rules(['L006', 'L009'])
        sql_linter.lint("bigquery")



    def test_should_work_when_have_template(self):
        sql="""-- backend: bigquery
-- target=template.dim_cols
product_name
, product_category

-- target=temp.dims
select @{dim_cols} from order_count
union
select @{dim_cols} from sales_amount

-- target=template.join_conditions
dim.product_name <=> #{right_table}.product_name
and dim.product_category <=> #{right_table}.product_category

-- target=temp.joined_data
select
dim.product_name
, dim.product_category
, oc.order_count
, sa.sales_amount 
from dims dim
    left join order_count oc on @{join_conditions(right_table=oc)}
    left join sales_amount sa on @{join_conditions(right_table=sa)}"""
        sql_linter=SqlLinter(sql)
        sql_linter.lint("bigquery")

    def test_should_work_when_have_function(self):
        sql="""-- backend: bigquery
-- target=variables
select ${plus(2, 2)} as a

-- target=temp.dims
select * from order_count where value < ${a}
"""
        sql_linter=SqlLinter(sql)
        sql_linter.lint("bigquery")



if __name__ == '__main__':
    unittest.main()