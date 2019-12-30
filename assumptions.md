## Assumptions:
Because of the lack of any implementation at all and the project specification being in its first few revisions, there was quite a lot of ambiguity. This led to the team making a growing list of assumptions in order to be able to generate working tests for the functions. As this was our interpretation of the project, they might not be necessarily correct, but can be edited later on as the specification becomes clearer and more consultation occurs. 

* Assumed channel list is ordered in terms of ascending `channel_id` when calling `channels_list` and `channels_listall`
* Assumed private channels will still show up on the list when `channels_listall` is called. These channels will not be joinable however
* Assumed that invalid tokens provided to functions will mean that the function does not execute and will return `None`
* Assumed first channel is assigned `channel_id 0` and this increments by `1` per new channel
* Assumed duplicate channel names are permitted when channel_create is called, but these will have different unique `channel_ids`
* Assumed that if a user logs with `auth_login` in whilst a previously active token is issued that the previous token will become unauthenticated via `auth_logout`
* Assumed that each `pytest` runs a new session of Slackr. That means actions from previous tests are discarded
* Assumed that users can't `message_send` or interact with channels that they haven't joined. (Even though no exception is provided in the specification. `AccessError` perhaps')
* Assumed that blank messages `""` are not permitted
* Assumed that no escaping of input characters are required as of yet or sanitisation will be handled via front end
* Assumed on multiple occasions that `ValueError` and `AccessError` exceptions will be raised even when not listed (Please see relevant tests where this occurs for details)
* Assumed arbitrary numbers for `react_ID` as no valid numbers were provided. (Documented in code)
* Assumed that all input will be `ASCII`
* Assumed that creating a channel with `channels_create` does not automatically mean you've joined it
* Assumed that functions which accept a token will check the permission of the user when submitting their token. For invalid tokens or tokens without the correct permission and where `N/A` is listed as an exception, that `None` will be returned
* Assumed that first and last name should be at least one character. That is, empty inputs will throw exceptions
* Assumed that functions which return an empty dictionary without exception suggest that they have executed
* Assumed that `channel_addowner` works even when the user has not already joined the channel 
* Assumed that as the only owner in a channel, you can not `channel_removeowner` yourself
* Assumed that you can't `channel_join` or `channel_leave` twice. That is, join when you've already joined. No exception specified in specs
* Assumed that channels can have no users in them
* Assumed that calling `standup_start` while in a standup which is already active returns the amount of time remaining
* Assumed that first `u_id` starts at `0` and increments by `1` per new user

A few other minor assumptions have been made and have been commented in code accordingly. We expect that as we begin to implement the actual functions that the specifications and inner workings will become clearer, eliminating the need for these assumptions.
