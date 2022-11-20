create table num_session_before_order as (
with customer_sessions as (
	select
		"customerId",
		_type,
		"sessionId",
		dense_rank() over(partition by "customerId" order by "sessionId" asc) as customer_session
	from sessions as s
),
session_with_order as (
	select
		*
	from customer_sessions
	where _type = 'placed_order'
),
prev as (
	select
		t.*,
		lag(customer_session,1,0) over(partition by "customerId" order by "sessionId") as prev_session
	from session_with_order as t
),
num_sessions as (
	select
		t.*,
		customer_session - prev_session - 1 as num_session_before_order
	from prev t
)
select
	percentile_cont(0.5) within group (order by num_session_before_order) as median_num_session
from num_sessions);