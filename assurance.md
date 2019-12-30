# Assurance
As assurance that our implementation of this iteration was complete and correct as per specifications, we conducted many software verification and validation tests and approaches. These included utilising many methods and tools, which produced both ordinal and absolute measurements as results. The results and feedback from these tools were noted and then analysed. If issues were discovered, these were added to the task board and rectified in the next sprint/iteration. By also considering acceptance criteria based on the specification's requirements and the previous iteration's user stories, we were able to create assurance that our implementation of the backend is *fit for purpose*.

## Demonstration of an understanding of the need for software verification and validation
Software verification and validation go hand in hand in creating quality products which meet user standards...

#### Verification
Verification entails that the software has been built correctly. Formal verification is not possible due to complexity and cost (also not covered in this course). To verify the software, we tested the quality of our solution to ensure it was free from bugs and errors. This was done via *unit tests (white box)* and *integration testing*. Unit tests involved our individual PyTests, which tested individual functions to ensure they run without error. Integration testing ensured all our components worked together and was able to run through the server. We conducted reviews and inspections of our code during our standups to ensure verification of our product and compliance with standards/specifications. We also used tools which are mentioned below such as Pylint to ensure code quality and PyTest coverage to verify the quality of our solution and tests themselves.
#### Validation
Validation involves ensuring the correct solution was developed. We checked that all specifications/requirements were satisfied from the shoes of the user. This was done via *virtual acceptance testing*, without the actual clients, as they were not available. We as a team got together and went through functions and use cases of the product via Postman/ARC and also by role-playing via the front end. This allowed us to gain a feel of how the user would respond to our solution and if it would satisfy their requirements. This was done in reference to our *user stories* and *acceptance criteria* which are listed below. These acceptance criteria were generated based on user stories and requirements from iteration 1. We went through each user story and ticked it off if we believed our fulfilled the solution, hence validating our solution thoroughly. 

## Development of appropriate acceptance criteria based on user stories and requirements.

###### Ability to login, register if not logged in, and log out

1. As a user, I want to be able to register my account with my email, password and full name so that I can create an account for me to access the application.
	* Register for a new account with an email, password, first and last name provided
	* If registration is successful, should receive a valid token and user ID
	* The email should be of a valid email format for successful registration
	* The email should not already be associated with another account
	* The password should be at least 6 characters long
	* The first name should be between 1 and 50 characters long
	* The last name should be between 1 and 50 characters long
	* A handle is generated using a combination of the users lowercase first and last name, capped at 20 characters
	* The handle should be unique to each user
2. As a user, I want to be able to login to my account with my email and password so that I can use the application securely.
	* Login with an email and password combination
	* When logged in, user is assigned a unique token and told their user ID
	* If an invalid email, unregistered email or incorrect password an error should occur
3. As a user, I want to be able to log out of my account, so that I can end my session securely when I’m done using the application.
	* Log out with a currently valid token
	* When logging out, user’s unique token is invalidated and can no longer be used
	* Return a value that confirms the logout was successful

###### Ability to reset password if forgotten it

7. As a user, I want to be able to reset my password using my email address, so I can regain access to my account if I forget my password.
	* When provided a valid registered email, the password should be reset via an email sent to the accounts registered email
	* A unique reset code should be sent to the users registered email
	* When a valid reset code is provided, the user should be able to reset their password
	* The new password should not be shorter than 6 characters
	* If a valid code and password are provided, the users password should be updated

###### Ability to see a list of channels

8. As a user, I want to be able to view all the channels I am currently in, so that I can view and choose which channel I am messaging in.
	* Function should accept a valid token and if not return an error
	* When a valid token is provided, a list of channels that the user is part of should be provided
9. As a user, I want to be able to browse all public channels available by name, so that I can view and join channels.
	* Function should accept a valid token and if not return an error
	* When a valid token is provided, a list of public channels that exist should be provided

###### Ability to create a channel, join a channel, invite someone else to a channel, and leave a channel

10. As a user, I want to be able to create a new public or private channel, so that I can start my own channels to my personal preference.
	* Provided a valid token, channel name and whether the channel should be public, a new channel should be created
	* The channel name should be less than 20 characters long
	* The channel should be made to either be public or private
	* If an invalid token is provided or the name is too long, an error should occur
11. As a user, I want to be able to join a channel, so that I can join and message other users within the channel.
	* Provided a valid token and channel ID, user should join the channel
	* If the channel ID is invalid or does not exist, an error should occur
	* If the channel is a private channel and the user is not an admin, an error should occur
	* If an invalid token is provided, an error should occur
12. As a user, I want to be able to invite other users to a channel, so that I can message my friends and colleagues within a channel.
	* Provided a valid token, channel ID and user ID, user should be invited to the channel and will be come a member of the channel immediately
	* If inviting to a channel which the requesting user is not part of, an error should occur
	* If the user ID does not exist, an error should occur
13. As a user, I want to be able to leave a channel, so that I am no longer receiving messages from other users within a channel if I don’t want to.
	* Provided a valid token and channel ID, user should leave the channel immediately
	* If the channel ID is invalid or does not exist, an error should occur

###### Within a channel, ability to view all messages, view the members of the channel, and the details of the channel

14. As a user in a channel, I want to be able to see the name of the channel I am currently in, so that I can see which channel I am messaging in. `+` As a user in a channel, I want to be able to see a list of users in the current channel, so I know exactly who I am messaging with. `+` As a user in a channel, I want to be able to see who the owner is in the list of users for the current channel, so that I know who made and controls the channel.
	* Given a valid token and channel ID, return the name of the channel, a list of members and a list of owners
	* If the channel ID is not valid or the user is not part of the channel, an error should occur
17. As a user in a channel, I want to be able to see all the messages sent and exchanged in a channel, so that I know what has been said by who.
	* Given a valid token, channel ID and a message ID, a list of up to 50 messages should be returned
	* The index of the last message returned should also be returned.
	* If less than 50 messages were returned, this should be indicated when returning the values
	* If the channel ID is invalid or the starting message index is greater than the total messages in the channel, an error should occur
	* If the user is not a member of the channel, an error should occur and nothing should be returned

###### Within a channel, ability to send a message now, or to send a message at a specified time in the future

18. As a user in a channel, I want to be able to send messages now, so that I can communicate with other users immediately.
	* Given a token, channel ID and message, a message should be sent to the channel immediately.
	* If the message is longer than 1000 characters, an error should occur
	* If the user making the request is not part of the channel, an error should occur
	* When the message is sent successfully, the message ID should be provided
19. As a user in a channel, I want to be able to schedule messages to send, so that I can send messages at a specific time later on, even if I’m not available at the time.
	* Given a token, channel ID, message and time, a message should be sent to the channel automatically at the specified time
	* If the message is longer than 1000 characters, an error should occur
	* If the user making the request is not part of the channel, an error should occur
	* If the time provided is in the past, an error should occur
	* When the request is accepted and scheduled, the message ID should be provided

###### Within a channel, ability to edit, remove, pin, unpin, react, or unreact to a message

20. As a user in a channel, I want to be able to edit my messages, so that I can correct or modify my message if I make a mistake.
	* Given a valid token, message ID and new message, the text of an existing message should be updated immediately
	* An error should occur if the message ID was sent by the user and the user is not an admin of Slackr or the owner of the channel
21. As a user in a channel, I want to be able to delete messages, so that I can remove mistakes or take back things that I have said.
	* Given a valid token, message ID and new message, an existing message should be removed from the channel immediately
	* An error should occur if the message ID was sent by the user and the user is not an admin of Slackr or the owner of the channel
	* An error should occur if the message ID does not exist or is invalid
22. As a user in a channel, I want to be able to pin messages, so that everyone else can see important messages.
	* Given a token and message ID, mark the message as pinned immediately
	* If the message ID is invalid or the message with the ID is already pinned, an error should occur
	* If the user making the request is not a member or not an admin, an error should occur
23. As a user in a channel, I want to be able to unpin a message, so that the message isn’t pinned when it’s no longer important
	* Given a token and message ID, unmark the message as pinned immediately
	* If the message ID is invalid or the message with the ID is not already pinned, an error should occur
	* If the user making the request is not a member or not an admin, an error should occur

24. As a user in a channel, I want to be able to react to messages, so that I can share how I feel about a message.
	* Given a valid token, message ID and react ID, add the react ID to the message on behalf of the user
	* If the message ID or react ID is not valid, an error should occur
	* If the message already has an active react from the user, an error should occur
25. As a user in a channel, I want to be able to remove my reaction from a message, so that I can undo a mistake or in case I change my mind.
	* Given a valid token, message ID and react ID, remove the react ID to the message on behalf of the user
	* If the message ID or react ID is not valid, an error should occur
	* If the message does not already have a react from the user, an error should occur

###### Ability to view user anyone's user profile, and modify a user's own profile (name, email, handle, and profile photo)

26. As a user, I want to be able to view the profile of any other user and see their full name, handle, email address and profile photo, so that I can learn more about the people I am talking with.
	* Given a token and user ID, return the email, first name, last name and handle of the specified user
	* If the user does not exist, an error should occur
27. As a user, I want to be able to edit the full name, handle, email address and photo on my own profile, so that I can update my information and what other users see on my profile.
	* Given a token and a combination of a first name, last name, handle, email address or profile picture link, update the corresponding information on the users profile
	* If the first name and last name are not between 1 and 50 characters long each, an error should occur
	* If the email address is invalid or taken, an error should occur
	* If the handle is not between 3 and 20 characters or taken, an error should occur

###### Ability to search for messages based on a search string

28. As a user, I want to be able to search messages for a specific string, so that I can find sent messages which are relevant to what I am looking for.
	* Given a token and query string, return a list of all messages sent from all channels the user is part of that contains the query string
	* The list of returned messages should contain the message ID, sender ID, time sent, message content, if it was pinned and the reacts attached to the message
    
###### Ability to modify a user's admin privileges: (MEMBER, ADMIN, OWNER)

29. As an owner of a channel, I want to be able to edit the permissions of other users in my channel to a member, admin or owner, so I can control what permissions they have over my channel.
	* Given a valid token, user ID and permission ID, update the permission ID of the user immediately if authorised
	* If the user id does not exist or the permission id is invalid, an error should occur
	* If the requesting user does not have admin or owner permissions, an error should occur

###### Ability to begin a "standup", which is a 15 minute period where users can send messages that at the end of the period will automatically be collated and summarised to all users

30. As a user in a channel, I want to be able to start a 15 minute standup, so that I can create a mock standup with my team members over the internet, being a firm believer in AGILE. `+` As a user in a channel, I want to be able to receive a collated summary of messages after a standup, so that I can easily view messages exchanged during the standup.
	* Given a token and channel ID, start a standup in the channel for a duration of 15 minutes.
	* Return the time the standup is due to finish
	*  At the end of the 15 minute period, send a message containing all standup messages to the channel from the user who started the standup
	* The collated messages should indicate who said what by appending their name before the message
	* All messages sent by standup send in this period should not be sent to the channel, but instead added to the standup messages
	* If the channel ID is invalid or a standup is already active, an error should occur
	* If the user starting the standup is not a member of the channel, an error should occur
31. As a user in a channel, I want to be able to participate in a standup, so that my opinions and thoughts can be heard by my team members in the standup. 
	* Given a valid token, channel ID and message, add a message to the standup messages buffer, given that a standup is active in the channel
	* If the channel ID is invalid, a standup is not active or the message is longer than 1000 characters, an error should occur
	* If the user is not part of the channel, an error should occur


## Demonstration of appropriate tool usage for assurance (code coverage, linting, etc.)
#### Code coverage / PyTest

` ALL TESTS PASSED - COVERAGE 99%+ `

| **Function** | **Passed** | **Coverage** | **Remarks** |
| - | :-: | :-: | - |
| auth_login | 5/5 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| auth_logout | 2/2 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| auth_register | 10/10 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| auth_passwordreset_request | 5/5 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| auth_passwordreset_reset | 4/4 | **100%** | Unique tokens can't be tested. Tested via frontend & ARC - good. |
| channel_invite | 6/6 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| channel_details | 5/5 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| channel_messages | 8/8 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| channel_leave | 5/5 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| channel_join | 4/4 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| channel_addowner | 8/8 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| channel_removeowner | 5/5 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| channels_list | 5/5 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| channels_listall | 6/6 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| channels_create | 6/6 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| message_sendlater | 8/8 | 92% | Good coverage. All tests conducted. Frontend + ARC - good. |
| message_send | 7/7 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| message_remove | 7/7 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| message_edit | 7/7 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| message_react | 6/6 | 98% | Good coverage. Most tests conducted. Frontend + ARC - OK. Limited by frontend. Only 1 valid reactID makes it difficult to test more cases... |
| message_unreact | 9/9 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| message_pin | 7/7 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| message_unpin | 6/6 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| user_profile | 4/4 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| user_profile_setname | 6/6 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| user_profile_setemail | 6/6 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| user_profile_sethandle | 6/6 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| user_profile_uploadphoto | -/- | XXX | NOT IMPLEMENTED (ITER 3) |
| standup_start | **OK** | XXX | Tested manually using Postman/ARC in combination with front end. |
| standup_send | **OK** | XXX | Tested manually using Postman/ARC in combination with front end. |
| search | 10/10 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |
| admin_userpermission_change | 7/7 | **100%** | Excellent coverage. All tests conducted. Frontend + ARC - good. |

#### Linting
`Pylint` was used on our code to check code quality. The results of this were used as a reference only and not as an objective measure of code quality. The results of pylint were manually reviewed and issues were rectified where deemed appropriate. Some issues identified were unrequired or too strict for our purposes, so instead of overriding these warnings, we noted them and moved on. A perfect score for Pylint was not achieved, but we were able to greatly improve the quality of our code as a result.

#### Front end
To mimic the user experience and real-life use cases, we also ran tests via the front end, despite the issues which existed in the current state of the front end. We found the front end to be an easy way to test things intuitively via a graphical interface. The developer console was also used in conjunction to ensure all requests were OK. This testing also ensured our routes were correct and highlighted some issues which were not covered in our other tests. In conjunction with the front end, we also added setup lines to our `server.py` to create users and other properties consistently to save time and ensure consistent results.

#### Postman/ARC
Especially in our earlier stages, we used ARC and Postman to make CRUD requests. This allowed us to ensure functions were working by examining the returned output and checking the HTTP status code. This was a more tedious process as we had to manually construct and fill in each request, but it allowed us to specify exactly what the input is and check the output character for character. Additionally, we were able to trigger errors and check that they were raised correctly as per the specifications. This was useful for testing specific things, especially before implementation was complete enough to use the front end. Additionally, the front end was unable to test certain functions such as standups and search, requiring us to manually create make the requests. By using these utilities, we were able to assure that functions were working individually as expected.

