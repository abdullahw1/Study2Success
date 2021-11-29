# Product Specifications

- [Product Specifications](#product-specifications)
  - [Description](#description)
  - [Contributors](#contributors)
  - [Non-functional Requirements](#non-functional-requirements)
  - [Functional Requirements](#functional-requirements)
    - [General Feature](#general-feature)
    - [Memorizing](#memorizing)
      - [1. Input a markdown file and ouput flash cards](#1-input-a-markdown-file-and-ouput-flash-cards)
      - [2. Share flash cards (add to their account)](#2-share-flash-cards-add-to-their-account)
      - [3. Mind map of flash cards](#3-mind-map-of-flash-cards)
      - [4. Change order of flash cards based on how often user got answer correct](#4-change-order-of-flash-cards-based-on-how-often-user-got-answer-correct)
      - [5. Create pdf of flash cards to print](#5-create-pdf-of-flash-cards-to-print)
    - [Notes](#notes)
      - [1. Render markdown notes](#1-render-markdown-notes)
      - [2. Convert markdown notes to pdf](#2-convert-markdown-notes-to-pdf)
      - [3. Share notes with other people (add to their account)](#3-share-notes-with-other-people-add-to-their-account)
      - [4. Find text in files](#4-find-text-in-files)
      - [5. Quickly rename files using regular expression](#5-quickly-rename-files-using-regular-expression)
      - [6. Add ability to navigate between notes using this syntax [[this other note]]](#6-add-ability-to-navigate-between-notes-using-this-syntax-this-other-note)
    - [Time Management](#time-management)
      - [1.  Create time blocks](#1--create-time-blocks)
      - [2. Use pomodoro timer](#2-use-pomodoro-timer)
      - [3. Add todo tracker](#3-add-todo-tracker)
      - [4. Track hours worked per day](#4-track-hours-worked-per-day)

## Description
- Date: 09/21/2021
- Product Name: [Study2Success](https://github.com/HoaTNNguyen/Study2Success)
- Problem Statement: TBD

## Contributors
1. Hoa Nguyen: https://github.com/HoaTNNguyen
2. Ngan Ngo: https://github.com/RachelNgo
3. Jerusalem Ilag: https://github.com/jeruilag
4. Abdullah Waheed: https://github.com/abdullahw1

## Non-functional Requirements
1. Password has to be at least 8 characters and 1 number.
2. The app should render a note under 1KB within 1 second in all systems.
3. The app is able to render its layout to different screen sizes (laptop, ipad, phone).
   
## Functional Requirements

### General Feature
1. Ability for users to sign-up, login/logout. 
2. Be able to delete account

### Memorizing
#### 1. Input a markdown file and ouput flash cards
- DRI: [@Hoa Nguyen](https://github.com/HoaTNNguyen)
- Summary: User is able to input a markdown file and turn it into flashcards
- Actors: User
- Preconditions: 
  1. User is already logged in
  2. User is in Flashcards tab
  3. User has a markdown file
- Triggers: User presses import button
- Primary Sequence:
  1. The app pops up a small window waiting for user to select a markdown file
  2. User select a markdown file from their computer
  3. The app creates folders of flashcards according to #tag names in the markdown file
  4. The app shows new folders
- Postconditions: Folders of flashcards are created from a markdown file

#### 2. Share flash cards (add to their account)
- DRI: [@Hoa Nguyen](https://github.com/HoaTNNguyen)
- Summary: User is able to share their flashcards with other users whom the users already added in their account
- Actors: User, other user
- Preconditions:
  1. User is already logged in
  2. User is in Flashcards tab
  3. User has other users in his/her friend list
  4. User has flashcards
- Triggers: User presses share button
- Primary Sequence:
  1. The app shows a drop down list of friends
  2. User selects friends that he/she wants to share with
  3. User presses share
  4. The app send notification to the users who get shared
  5. The app let user know that the flashcards has been shared
- Postconditions: The flashcards are shared and added to other users' repository

#### 3. Mind map of flash cards
- DRI: [@Hoa Nguyen](https://github.com/HoaTNNguyen)
- Summary: User is able to mind map their flashcards
- Actors: User
- Preconditions:
  1. User is already logged in
  2. User is in Flashcards tab
  3. User has Flashcards
- Triggers: User presses Create Mindmap button
- Primary Sequence:
  1. The app asks user to select a Mindmap pattern
  2. User selects a Mindmap pattern
  3. User selects Flashcards to add it in a position in the pattern
  4. User presses done button
- Postconditions: A Mindmap of Flashcards is created

#### 4. Change order of flash cards based on how often user got answer correct
- DRI: [@Hoa Nguyen](https://github.com/HoaTNNguyen)
- Summary: The app changes order of Flashcards based on how often user got anser correct whenever the user open a Flashcard folder
- Actors: User
- Preconditions:
  1. User is logged in
  2. User has Flashcards
  3. User is in a Flashcards folder
  4. User answer at least one Flashcard
- Triggers: User opens a Flashcard folder
- Primary Sequence:
  1. The app keeps track the number of time the user got answer correct for a Flashcard
  2. The app sorts the order of Flashcards based on the number of time the user got answer correct increasingly (Flashcard that is answered less correct will be appeared on the top)
- Postconditions: The order of Flashcared is sorted based on how often user got answer correct

#### 5. Create pdf of flash cards to print
- DRI: [@Jerusalem Ilag](https://github.com/jeruilag)
- Summary: Create a pdf of flash cards to print
- Actors: User
- Preconditions:
	  i. User is already logged in
	 ii. User is in the Flashcards tab
	iii. User has notes
- Triggers: User clicks "Convert to PDF"
- Primary Sequence:
	  i. A window of directories pops up
	 ii. User selects where they want to save it to
	iii. User selects "Confirm"
- Postconditions: The flashcards are saved in .pdf format in the proper location

### Notes
#### 1. Render markdown notes
- DRI: [@Abdullah Waheed](https://github.com/abdullahw1)
- Summary: Create a plain text
- Actors: User
- Preconditions:
	1. User is logged in
	2. input markdown file of flash cards is created
- Triggers: User selects a note they want to view in detail that allows for markdown text to be converted to html code
- Primary Sequence:
	1. User must select an already created markdown input file 
	2. User must select what the type of note they want to select.
	3. User edits the markdown note file 
	4. The file is saved
- Postconditions: User is presented with the rendered markdown notes.

#### 2. Convert markdown notes to pdf
- DRI: [@Abdullah Waheed](https://github.com/abdullahw1)
- Summary: User is able to convert and save markdown notes to pdf format. 
- Actors: User
- Preconditions:
	1. User is logged in
	2. Markdown note is created
	3. Markdown note is rendered  
- Triggers: User selects option to convert to pdf
- Primary Sequence
	1. User is given an options to choose which markdown note they want converted to pdf
	2. User inputs option
	3. Pdf gets saved
- Post conditions: The users notes are converted to pdf form.

#### 3. Share notes with other people (add to their account)
- DRI: [@Abdullah Waheed](https://github.com/abdullahw1)
- Summary: Users will be able to use feature to share their notes with other users 
- Actors: User
- Preconditions
	1. User is logged in
	2. User already has note
	3. User knows which note they want to share 
- Triggers: User selects the option to share notes. 
- Primary Sequence:
	1. User selects to share note  
	2. User is given the notes they selected
- Postconditions: The application will let user know that note has been shared

#### 4. Find text in files
- DRI: [@Abdullah Waheed](https://github.com/abdullahw1)
- Summary: Feature will allow for user to key text from files
- Actors: User
- Preconditions:
	1. User is logged in
	2. User has note files 
- Triggers: User searches key text in search menu
- Primary Sequence:
	1. User selects search option  
	2. User enters keywords
- Postconditions: User is presented with notes containing searched keywords.

#### 5. Quickly rename files using regular expression
- DRI: [@Jerusalem Ilag](https://github.com/jeruilag)
- Summary: Quickly rename files using regular expressions
- Actors: User
- Preconditions:
	 i. User is logged in
	ii. User has a file
- Triggers: User clicks "Rename file"
- Primary Sequence:
	 i. User inputs the name they want the file to be called
	ii. User presses "Confirm"
- Postconditions:
	i. File now has the new name given by the user

#### 6. Add ability to navigate between notes using this syntax [[this other note]]
- DRI: [@Jerusalem Ilag](https://github.com/jeruilag)
- Summary: Add ability to navigate between notes using this syntax [[this other note]]
- Actors: User
- Preconditions:
          i. User is logged in
         ii. User is in one of their notes
        iii. User has multple notes
- Triggers: User types in [[name of other note]]
- Primary Sequence:
        i. User types in [[name of other note]]
- Postconditions:
        i. User is now viewing their other note.


### Time Management
#### 1.  Create time blocks
- DRI: [@Ngan Ngo](https://github.com/RachelNgo)
- Summary: Feature which users could make blocks of time.
- Actors: The Users
- Preconditions: The users has logged in
- Trigger: Open the "time blocks"
- Primary Sequence: 
    1. System show users a calendar with dates.
    2. Users select a date from a calendar
    3. Users create their event title and tasks with a due time.
    4. System automatically show up the event in the users's calendar with a block of time.
    5. Users log out
- Postconditions: Users had an event in their calendar

#### 2. Use pomodoro timer
- DRI: [@Ngan Ngo](https://github.com/RachelNgo)
- Summary: Feature which users could estimate how many pomodoros each task will take
- Actors: User
- Preconditions: The Users has logged in. 
- Trigger: the users open the "Pomodoro timer"
- Primary Sequence:
   1. Decide task to be done
   2. Set timer to 25 min 
   3. Work until timer run out
- Postconditions: The Users would focus on a single task at a time.

#### 3. Add todo tracker
- DRI: [@Ngan Ngo](https://github.com/RachelNgo)
- Summary: Feature which users could organize and manage their to-do items 
- Actors: User
- Preconditions: The Users has logged in.
- Triggers: The Users select "To Do Tracker " option
- Primary sequence:
   1. System prompt the users to do a list.
   2. The users make a list, sort them according to their priority.
   3. System show the list with the checklist.
   4. The Users log out.
- Postconditions: The Users can add, delete and mark the todo list.

#### 4. Track hours worked per day
- DRI: [@Jerusalem Ilag](https://github.com/jeruilag)
- Summary: User can see how long they have been studying flash cards for
- Actors: User
- Preconditions:
         i. User is already logged in
        ii. User has flash cards
- Triggers: User clicks "How long have I been studying?"
- Primary Sequence:
         i. User clicks the button
        ii. A time will be displayed with how long the user has had flash cards open for
- Postconditions: User will know how long they have been studying for that day
