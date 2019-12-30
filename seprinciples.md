# Software Engineering Principles
For iteration 2, we were able to create a working implementation of the required functions and endpoints for the application to work. However, many software engineering and design principles were neglected in the rush to create a working product. However, as iteration 3 only consists of minor updates to the specification, most of the effort was focused on the quality of our code and such software engineering principles. Therefore, after the required updates were made to our project to satisfy the new specifications, all our attention was shifted to refactoring and re-testing our code to meet good software engineering design practices. A variety of tools and methods were used, as covered in the lectures and tutorials, as listed below. As a result, the code was a lot more readable, maintainable and of a more sturdy quality. In doing this, we removed design smells such as rigidity, fragility, immobility, viscosity, opacity, needless complexity/repetition and coupling. Through further abstraction, we found our resulting code to be:
 - Extensible
 - Reusable
 - Maintainable
 - Understadable
 - Testable


## Explain methods used to refactor code to make it more maintable - (KEY CHANGES)
A variety of methods were used to refactor our code, as listed below. In refactoring our code, not only were we able to reduce the line count, we were able to make it *sturdier/efficient* in general and therefore more maintable than previously. Our code is a lot less convulted than previously submitted and infinitely more readable, making it easier for others to work on it in the future if required. Another benefit of refactoring is the reduction of redundant and inefficient code, which improves the time complexity of program, even though it is not necessarily measured.

### DRY
*Don't Repeat Yourself...* We refactored our program with this method significantly, as most of our functions had previously shared the same lines of code, which were copy pasted. Additionally, some of our functions shared code, which could have been seperated as a helper function. For example, we previously had the following lines at the start of every function to authenticate the user and decode their `u_id` from their token:

` if token not in valid_tokens:
    raise AccessError("Invalid token or user is not logged in") 
userID = jwt.decode(token.encode("utf-8"), "table_flip", algorithms=["HS256"])["u_id"] ` 

This was replaced with one line:

` u_id = decodeToken(token) `

As this was used in all our functions, it saved a significant amount of code and made our program more modular. More instances of this can be found in our ` appdata.py ` file, which contained all these new helper functions. More of these functions impelenting **DRY** included: ` getUser() `, ` getUserByEmail() `, ` getChannel() `, ` getMessage() `, ` getMessageChannel() `, ` isUserChan() `, ` getUserPerm() `. Each of these functions were shared by more modules many times and saved countless lines of code and repetition. On average, each module was reduced by 5-10 lines and had multiple *indents* removed. Initially, due to the amount of looping required to search for data, our modules had a lot of nested looping, which involved a ridiculous amount of indenting. This was reduced as a result of implementing these DRY functions.

### KISS
*Keep it Simple Stupid...* This method is harder to explain specifically, but we found ourselves reviewing our previous code in many instances and try to cut down on unnecessary complexity, especially when it came to looping. We also found ourself storing data in the most simple and most accessible way to avoid further complexity. By reducing nested looping and nested `if` and other conditional statements, we were able to simplify our code and make it a lot easier to read and maintain. However, due to the original implementation, we found ourself stuck in some undesirable situations with complexity which was difficult to avoid...

### Encapsulation
By encapsulating, we aimed to hide the internal representation of our data from our modules (similar to an ADT). Originally we had all of our data stored in a file called ` shared_stuff.py ` and used many imports and global variables to access information. This was rather fragile and was highly coupled. In retrospect, having our information stored as a *class* would have been a better implementation, but at this point, it had become too difficult to overhaul our program to implement classes, so we had to continue with our original implementation, which involved data and functions, similar to attributes and methods. 

The aim of this was to remove data manipulation and operations from modules and move them into the data file, so that the implementation and storage of data was independent of accessing data. This also meant we could reduce our imports and use of global variables. An example of functions we created for encapsulation included: ` decodeToken() `, ` setPermission() `, ` addToken() `, ` removeToken() `, ` resetReq() `, ` setPassword() `, ` createUser() `, ` newChannel() `, ` addMessage() ` etc. These were stored with our data in the file ` appdata.py ` and were seperate from our modules which utilised these functions. These functions were also partially in line with *DRY* too and helped us reduce our line count and complexity. In doing so, we were able to reduce the complexity and line count of most of our modules down to around *15* lines, which in some instances, was almost half of the original.

Note that we found ourself in some tricky instances, where encapsulation would greatly complicate our program due to the original implmenetation being poorly planned. In these cases, we attempted to abstract and encapsulate, but found that further attempts would only increase line counts greatly, add fragility and require extensive overhauling of our program, which negatively impacted the correctness of our code.

### Top down thinking
This method would have been a lot more useful at the start of our implemenation, rather than at the end when refactoring. However, when we worked on `appdata.py`, our new helper functions and the new functions such as uploading profile pictures, we applied top down thinking by breaking the problem into pieces and steps, creating a skeleton for each step and working into smaller pieces. We then provided psuedocode/commenting to describe the function of each piece to gain an idea of what was required, before starting work from the top down (higher level -> small functions).

### General
A few more general changes we made, included the addition of more detailed commenting which explained the purpose and intention of our code, making it easier to read. We also tried to adhere to a straight-forward naming scheme, so that the names of functions and variables were intuitive. Additionally, we provided extensive commenting in our `appdata.py` file (renamed from `shared_stuff.py`) about the structure of our data and examples of how data would be stored and accessed, making it easier to work with. 
### Pylint
We utilised Pylint to objectively evaluate the quality and style of our code and used it's warnings as advice on how to improve our code quality. We did not blindly listen to everything it said, as a lot of it was irrelevant, unnecessary and out of context for our requirements. For these cases, we disabled these warnings. For more reasonable warnings, we made changes to fix the problem and re-ran Pylint until we were satisfied with the quality of our code. We ended up achieving a **9.96/10** score, which we were all satisfied with. 

We ran Pylint with: `pylint3 --disable=C0326,R0801,C0301,C0103,W0603,W0611,C0411,C0116,W0622,C0303,C0305,C0114,C0304,W0603,W1401,R1720 /server`

Warnings we disabled included:

| **Disabled** | **Justification** |
| -------- | ------------- |
| **C0114** Missing docstring | Excessive. Disabled as consulated with tutor. |
| **C0411** Missing docstring | Excessive. Disabled as consulated with tutor. |
| **C0303** Trailing whitespace | Excessive. Disabled as consulated with tutor. |
| **C0305** Trailing newline | Excessive. Disabled as consulated with tutor. |
| **C0303** Missing whitespace | Excessive. Disabled as consulated with tutor. |
| **C0326** Wrong Number of Spaces | Excessive. Disabled as consulated with tutor. |
| **R0913** Too many arguments | Required for uploadphoto. Part of specification. |
| **R0801** Similar lines | Picked up in Pytest, which is required for testing. |
| **C0301** Line too long | Picked up the 1000 character lorem ipsum string used for testing. |
| **W0622** Redefining built-in | Redefining ValueError, as required by spec. |
| **C0103** Invalid name | Disagreement in naming scheme. |
| **W0603** Using global statement | Require in original implemenation with global variables. |
| **W1401** Backslash | Required for Regex |
| **R1720** No-else-raise | Required for raising errors in except. From lecture code. |

All these warnings were read, and upon consultation with the team, disabled due to false positives or just being excessive.

## Clear justification of the use of particular design methods
We aimed to agree upon all our design methods during team meetings before implementing them, especially when it came down to shared functions and data. We aimed to seperate our data from our implemenations of modules to add abstraction, whilst making our data easily and intuitively accessible. This section is easier to explain in person, but our design methods were primarily focused around global variables initially, as suggested in the course lectures. We tried to refactor and shift towards abstraction, but had to maintain a lot of our design methods. The primary structure of our data, as reflected by our ER diagram, involved the seperation of data where possible, but in line with the speification, so that data could be easily accessed, whether it be an array or dictionary (e.g We added the most recent data to the end of a list and accessed the end of the list directly for the most recent data). Admiteddly, we had to put up with our initial poor design and restructure and refactor it where possible to comply with these newly discoverd software engineering principles, as we had initially only aimed to have everything functioning, with no regard for maintainability.

## Submission of well-designed, thought out code that implements principles discussed in lectures
*This is demonstrated through the actual code itself, however this is a supplement.* Many of the principles explained in the lectures, have been covered above (DRY, KISS etc.). However, a few topics covered included decorators and the use of imports:
### Decorators
Apart from the `@APP.route` decorators as part of FLASK, we did not use decorators of our own as this concept was introduced too late to us in the lectures. Whilst Hayden said these weren't expected to be used, we acknowledge that the use of decorators could have improved the quality of our code. However, to implement decorators at this stage would have been too late and would have required us to overhaul large sections of our code, which was not worth the effort, given the time remaining.
### Imports
In the week 8 lectures and tutorials, imports were covered properly, which cleared things up. We used the method of packaging, which meant adding `__init__.py` files to directories of our project so they were traeted as containing packages. This was a lot cleaner than absolute importing and also adding `import sys` , `sys.path.append('/server/')` etc. We also avoided the use of wildcard `*` imports and were sure to only import the components which were required to avoid clashing or added complexity.

## Testing
Testing was mostly the same as the previous iteration, in that we shared most of our unit tests from before. We ran `python3-coverage` in conjunction with Pytest to ensure that **100%** of our tests still passed and that we still maintained **~99%** coverage, as previously justified. For this iteration, we focused more on the *frontend*, ensuring it was correctly implemented. We did this by running user stories and usage scenarios indvidually and together as a group to validate the correctness of our program. Most of this was similar to the description given in the previous iteration. Additionally though, we added Pytests involving **httplib2**, as suggested by our tutor, which built ontop of our original unit tests through Pytest, by accessing functions through the FLASK server, testing the correctness of the server too.
