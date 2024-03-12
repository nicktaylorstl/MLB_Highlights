with highlights as (select * from `mlbhighlights`.`highlights`.`2023_reg`),
data as (select * from `mlbhighlights`.`games`.`2023_reg`)
select * from highlights