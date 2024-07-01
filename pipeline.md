```mermaid
%%{ init: { 'flowchart': { 'curve': 'monotoneX' } } }%%
graph LR;
user_purchases_events_source[user_purchases_events_source] -->|user_purchases|join_user_purchases[join_user_purchases];
join_user_purchases[join_user_purchases] -->|pre-join|join[join];
join_user_activities[join_user_activities] -->|pre-join|join[join];
user_activity_events_source[user_activity_events_source]

```