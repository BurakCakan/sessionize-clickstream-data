create table time_until_order as (
with next_ts as (
	select
		_id,
		"customerId",
		"sessionId",
		timestamp,
		lead(timestamp,1,timestamp) over(partition by "sessionId" order by timestamp) as next_ts
	from sessions as t
),
durations as (
	select
		_id,
		"customerId",
		"sessionId",
		extract( epoch from next_ts - timestamp) as duration
	from next_ts
),
customer_sessions as (
	select
		s."customerId",
		s."sessionId",
		s._type,
		dense_rank() over(partition by s."customerId" order by s."sessionId" asc) as customer_session,
		d.duration
	from sessions as s
	inner join durations d on s._id = d._id
),
adjusted_duration as (
	select
		t.*,
		duration * (case when (sum(case when _type = 'placed_order' then 1 else 0 end) over(partition by "customerId", customer_session)) > 0 then 0 else 1 end) as adjusted_duration
	from customer_sessions t
),
rolling_sum as (
	select
		t.*,
		sum(adjusted_duration) over(partition by "customerId" order by customer_session) as rolling_sum
	from adjusted_duration t
),
session_with_order as (
	select
		*
	from rolling_sum
	where _type = 'placed_order'
),
prev as (
	select
		t.*,
		lag(rolling_sum,1,0) over(partition by "customerId" order by "sessionId") as prev_time
	from session_with_order as t
),
time_sessions as (
	select
		t.*,
		rolling_sum - prev_time as time_until_order
	from prev t
)
select
	percentile_cont(0.5) within group (order by time_until_order) as median_time
from time_sessions);