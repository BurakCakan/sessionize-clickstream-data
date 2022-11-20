create table results as (
    select *
    from num_session_before_order
    cross join time_until_order
);