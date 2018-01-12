# Financial Analysis Tool
##########################################################################################
# Import libraries
import os
import pandas as pd
import scipy as scipy
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from scipy.stats import iqr
import re
import sys
import time

# Try to import pandas Data Reader library as it is not installed by default on anaconda
try:
    import pandas_datareader.data as web
except ImportError: # If the import fails perform a pip install
    import pip      # import pip library
    pip.main(['install', 'pandas_datareader'],) # Install Pandas Datareader
import pandas_datareader as web # Now import the library
from pandas_datareader._utils import RemoteDataError
import MasterDSG as dsg
import MasterRegression as lin_reg # import stats module
style.use('ggplot')               # Use ggplot for Graphs

##########################################################################################
def mainMenu():             # Main Menu Function
    os.system('cls')        # Clear the terminal screen
    print_mainMenu()        # Calls the print Main menu function
    while True:             # While true loop
        try:                # try the following
            choice = input("Please Select An Option From 1-6: ") # Ask the user for an input
            if choice == "1":                           # If input is 1, perform task
                os.system('cls')                        # Clear the terminal screen
                ticker_menu()                           # Calls Ticker Menu Function
            elif choice == "2":                         # Else if input is 2, perform task
                os.system('cls')                        # Clear the terminal screen
                des_stat_menu()                         # Calls the descriptive stats menu Function
            elif choice == "3":                         # Else if input is 3, perform task
                os.system('cls')                        # Clear the terminal screen
                graph_func()                            # Calls the graph menu Function
            elif choice == "4":                         # Else if input is 4, perform task
                os.system('cls')                        # Clear the terminal screen
                date_reg()                           # Calls the predictive stats menu Function
            elif choice == "5":                         # Else if input is 5, perform task
                os.system('cls')                        # Clear the terminal screen
                dev_info()                              # Calls the developer information function
            elif choice == "6":                         # Else if input is 6, perform task
                print("\nExiting Financial Analysis Tool") # Prints to the terminal
                exit()                                  # Forces the system to exit the program
                break                                   # Breaks the while loop
            else:                                       # If the input is anything else
                print("\nInvalid Selection. Please Choose an Option From 1-6.\n\n") # Any  inputs other than integer values 1-5 we print an error message
        except ValueError:                              # Additional safety net to catch any inputs that would cause an error
                os.system('cls')
                print("That is not a recognized date. Please Enter a Suitable Date.")
                load_screen(0.4)
                os.system('cls')
                date_menu()

    return                                              # Ends the while loop

##########################################################################################

def des_stat_menu():                                    # Defines Statistics Menu
    check_selection()    #checks and prints ticker  and dates status.
    ticker_status()      #this will be consistent throughout all menus.
    print(46 * "-" , "MENU" , 46 * "-")                             # Prints 46 "-" symbols, followed by "Menu" and 46 more "-" symbols
    print("Please Select The Statisitics You Wish To Examine")      # Prints the rest of the descriptive stats menu
    print("1. Mean")
    print("2. Standard Deviation")
    print("3. Coefficient of Variation")
    print("4. Range")
    print("5. All Statistics")
    print("6. Plot Box & Whisker")
    print("7. Return to Main Menu")
    print(99 * "-")                                                 # Prints 99 more "-" symbols , for aesthetic purposes
    try: #while loop created as a way of catching errors.
        while True: #this will be consistent throughout all menus.
            choice = input("Please Select an Option From 1-7: ")
            if choice == "1":
                dsg.mean(dsg.close)                                 # Calls the mean function the the close variable from the dsg module
            elif choice == "2":
                dsg.std_dev(dsg.close)
            elif choice == "3":
                dsg.co_v(dsg.close)
            elif choice == "4":
                dsg.range_(dsg.close)
            elif choice == "5":
                print("\nAll stats: ")
                dsg.all_(dsg.close)
            elif choice == "6":
                print("\nBox and Whisker ")
                dsg.box_whisker(dsg.close)
            elif choice == "7":
                print("\nReturning to Main Menu")
                os.system('cls')
                print_mainMenu()
                break
            else:
                # Any integer inputs other than values 1-7 we print an error message
                print("\nInvalid selection. Please choose an option from 1-7.\n\n")
    except ValueError:
                print("\nInvalid selection. Please choose an option from 1-7.\n\n")
    return

def graph_func():
    check_selection()
    ticker_status()
    print(46 * "-" , "MENU" , 46 * "-")
    print("Please Select The Graph You Wish to Examine")                # Print Graph Menu
    print("1. Closing Price")
    print("2. Closing Price with Trendline")
    print("3. Moving Average of Price")
    print("4. Closing Price vs. Moving Average")
    print("5. Closing Price vs. Moving Average (With Volume)")
    print("6. Weighted Moving Average")
    print("7. Moving Average Convergence/Divergence (With Signal Line)")
    print("8. Bollinger Bands")
    print("9. Candlestick Graph")
    print("10. Return to Main Menu")
    print(99 * "-")
    while True:
        try:
            choice = input("Please Select an Option From 1-10: ")
            if choice == "1":
                print("\nClosing Price:")
                print("Please Close Graph to Proceed")
                dsg.closing(dsg.close) #calls necessary functions from other module.
                os.system('cls')
                graph_func() #reshows the original graph menu each time a graph is closed. Gives a fresh screen for user to continue analysis.
            elif choice == "2":
                print("\nClosing Price with Trendlines:")
                print("Please Close Graph to Proceed")
                dsg.close_trend()
                os.system('cls')
                graph_func()
            elif choice == "3":
                print("\nMoving Average Price: ")
                dsg.moving_avg(dsg.close)
                os.system('cls')
                graph_func()
            elif choice == "4":
                print("\nClosing Price vs. Moving Average: ")
                dsg.moving_avg_close(dsg.close)
                os.system('cls')
                graph_func()
            elif choice == "5":
                print("\nClosing Price vs. Moving Average (With Volume): ")
                dsg.moving_avg_vol(dsg.close)
                os.system('cls')
                graph_func()
            elif choice == "6":
                print("\nWeighted Moving Average: ")
                dsg.w_moving_avg(dsg.close)
                os.system('cls')
                graph_func()
            elif choice == "7":
                print("\nMoving Average Convergence/Divergence (With Signal Line): ")
                print("Please Close Graph to Proceed")
                dsg.macd_1()
                os.system('cls')
                graph_func()
            elif choice == "8":
                print("\nBollinger Bands")
                dsg.bbands(dsg.stock)
                os.system('cls')
                graph_func()
            elif choice == "9":
                print("\nCandlestick Graph ")
                print("Please Close Graph to Proceed")
                dsg.candlestick()
                os.system('cls')
                graph_func()
            elif choice == "10":
                print("\nReturning to Main Menu")
                mainMenu()
                break
            else:
                # Any integer inputs other than values 1-9 we print an error message
                print("\nInvalid selection. Please choose an option from 1-9.\n\n")
        except ValueError:
                print("\nInvalid selection. Please choose an option from 1-9.\n\n")
    return

def ticker_menu():
    ticker_status()
    print(46 * "-" , "MENU" , 46 * "-")
    print("Please Select The Company You Wish To Examine")
    print("1. List Company Ticker names")
    print("2. Search Company by Name")
    print("3. Search Company by Ticker")
    print("4. Change Company Under Examination")
    print("5. Change Date Range Under Examination")
    print("6. Return to Main Menu")
    print(99 * "-")
    while True:
        try:
            choice = input("Please Select an Option From 1-6: ")
            if choice == "1": #user can view all companies in one list
                ticker_list_all()
            elif choice == "2": #can search by name
                print("\nCompany Name Search Engine\n")
                company_name_search()
            elif choice == "3": #can search by ticker
                print("\nCompany Ticker Search Engine\n")
                company_ticker_search()
            elif choice == "4": #can straight away enter ticker to be examined.
                print("\nChange Company under Examination function")
                dsg.get_name()
                try:
                    dsg.start == False #if date ranges have already been entered go straight to main menu
                    mainMenu() #avoids user having to navigate back there themselves. Assumes once ticker and dates have been entered, user will want to proceed immediately with analysis.
                except (NameError, AttributeError, ValueError): #if variables start and end do not exist, date has not been selected yet.
                    date_menu() #bring them straight to date menu.
                    mainMenu() #from there straight to main menu.
            elif choice == "5":
                print("\nChange Date Range")
                date_menu() #use can choose to proceed straight to date menu.
                mainMenu() #brings them straight to main menu after.
            elif choice == "6":
                print("\nReturning to Main Menu")
                mainMenu()
                break
            else:
                # Any integer inputs other than values 1-5 we print an error message
                print("\nInvalid selection. Please choose an option from 1-6.\n\n")
        except ValueError:
                print("\nInvalid selection. Please choose an option from 1-6.\n\n")
    return

##########################################################################################

def ticker_list_all(): #function for listing all ticker names,
    path="http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchan0ge=nasdaq&render=download"
    load_csv = pd.read_csv(path, usecols = [0, 1])
    load_screen(0.2) #loading function called as it takes a few seconds.
    print("The List of Companies Is As Follows: \n{}".format(load_csv))
    while True:
        try:
            print("1. Choose Company Now")
            print("2. Return to Ticker Menu")
            choice = input("Please Choose an Option: ")
            if choice == "1": #brings them to function which defines global variable ticker.
                dsg.get_name() #from there it goes to date menu to main menu.
                date_menu()
                mainMenu()
            elif choice == "2":
                os.system('cls')
                ticker_menu()
                break
            else:
                print("\nInvalid selection. Please choose an option from 1-2.\n\n")
        except ValueError:
                print("\nInvalid selection. Please choose an option from 1-2.\n\n")
    return

def company_name_search(): #searches nasdaq website for tickers.
    path="http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchan0ge=nasdaq&render=download"
    load_csv = pd.read_csv(path, usecols = [0, 1], index_col = 0)
    load_screen(0.2)
    match = input('\n\nEnter Company Name to Search:')
    match = load_csv["Name"].str.contains((re.escape(match)), case = False)
    search = load_csv.loc[match]
    if search.empty:
        print("No Company Found")
        retry = input("\nWould you like to search again? [Y/N]: ")
        if retry == "Y" or retry == "y":
            company_name_search()
        elif retry == "N" or retry == "n":
            os.system('cls')
            ticker_menu()
        else:
             print("\nIncorrect selection, please choose a valid option\n\n")
    else:
        os.system('cls')
        print("\n", search)
    while True:
        try:
            print("\n1. Choose Company Now")
            print("2. Search for Company Names again")
            print("3. Return to Ticker Menu")
            choice = input("Please Select an Option: ")
            if choice == "1": #user can go from here to entering in ticker.
                dsg.get_name()
                try: #if date has already been entered they will go straight to main menu after.
                    dsg.start == False
                    mainMenu()
                except (NameError, AttributeError): #if it does not, they will be brought to date menu.
                    date_menu()
                    mainMenu()
            elif choice == "2": #option to search again
                os.system("cls")
                company_name_search()
            elif choice == "3": #or go back to ticker menu.
                os.system('cls')
                ticker_menu()
                break
            else:
                # Any integer inputs other than values 1-3 we print an error message
                print("\nInvalid selection. Please choose an option from 1-3.\n\n")
        except ValueError:
                print("\nInvalid selection. Please choose an option from 1-3.\n\n")
    return

##########################################################################################

def company_ticker_search(): #same idea as above but searches by ticker instead of name.
    path="http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchan0ge=nasdaq&render=download"
    load_csv = pd.read_csv(path, usecols = [0, 1], index_col = 1)
    load_screen(0.2)
    tick_match = input('\n\nEnter Company Ticker to Search:')
    match_tick = load_csv["Symbol"].str.contains((re.escape(tick_match)), case = False)
    tick_search = load_csv.loc[match_tick]
    if tick_search.empty:
        print("No Company Found")
        retry = input("\nWould you like to search again? [Y/N]: ")
        if retry == "Y" or retry == "y":
            os.system("cls")
            company_ticker_search()
        elif retry == "N" or retry == "n":
            os.system("cls")
            ticker_menu()
        else:
            print("\nIncorrect selection, please choose a valid option\n\n")
    else:
        os.system("cls")
        print("\n", tick_search)
    while True:
        try:
            print("\n1. Choose Company Now")
            print("2. Search for Company Ticker Again")
            print("3. Return to Ticker Menu")
            choice = input("Please Select an Option: ")
            if choice == "1":
                dsg.get_name()
                try:
                    dsg.start == False
                    mainMenu()
                except (NameError, AttributeError):
                    date_menu()
            elif choice == "2":
                os.system("cls")
                company_ticker_search()
            elif choice == "3":
                os.system('cls')
                ticker_menu()
                break
            else:
                # Any integer inputs other than values 1-3 we print an error message
                print("\nInvalid Selection. Please Choose an Option From 1-3.\n\n")
        except ValueError:
                print("\nInvalid selection. Please choose an option from 1-3.\n\n")
    return

##########################################################################################

def print_mainMenu(): #main menu text is put in a function to be called rather than repitive printing statments throughout.
    os.system('cls')
    ticker_status()
    print(46 * "-" , "MENU" , 46 * "-")
    print("Welcome To This Financial Analysis Tool. Please Select a Company You Want To Analyse: ")
    print("1. Change Company Ticker & Date")
    print("2. Descriptive Statistics")
    print("3. Graphs")
    print("4. Predictive Statistics")
    print("5. Developer Information")
    print("6. Exit")
    print(99 * "-")

##########################################################################################

def dev_info(): #option 5 on main menu.
        os.system('cls')
        print("\n", 37 * "-" , "Developer Information" , 37 * "-")
        print("Shane Hickey   - 13702405 - BComm")
        print("Conor Rothwell - 17200644 - BSc")
        print("David Keppel   - 17203847 - BEng")
        print("\n1. Return to Main Menu")
        print(98 * "-")
        while True:
            try:
                choice = input("Please Select an Option: ")
                if choice == "1":
                    print("\nReturning to Main Menu")
                            ## You can add your code or functions here
                    print_mainMenu()
                    break
                else:
                    # Any integer inputs other than values 1-5 we print an error message
                    print("\nIncorrect selection, please choose a valid option\n\n")
            except ValueError:
                    print("\nIncorrect selection, please choose a valid option\n\n")
        return

##########################################################################################

def date_menu(): #menu which allows users to choose preset dates or define their own custom dates.
    os.system('cls')
    ticker_status()
    print(46 * "-" , "MENU" , 46 * "-")
    print("Please Select A Range For Analysis")
    print("1. One Day")
    print("2. One Week")
    print("3. One Month")
    print("4. Six Months")
    print("5. One Year")
    print("6. Five Years")
    print("7. Custom Range")
    print("8. Return to Main Menu")
    print(99 * "-")
    while True:
        try:
            choice = input("Please select an option: ")
            if choice == "1":
                print("One Day Selected")
                dsg.day(1) #uses day function defined in the DSG modules. uses 1 day as an argument.
                date_choice()
            elif choice == "2":
                print("One Week Selected")
                dsg.day(7) #day function is called again and again, just changing the argument used.
                date_choice() #gives users the chance to change their mind/confirm their selection.
            elif choice == "3":
                print("\nOne Month Selected")
                dsg.day(365/12)
                date_choice()
            elif choice == "4":
                print("\nSix Months Selected")
                dsg.day(365/2)
                date_choice()
            elif choice == "5":
                print("\nOne Year Selected")
                dsg.day(365)
                date_choice()
            elif choice == "6":
                print("\nFive Years Selected")
                dsg.day(5*365)
                date_choice()
            elif choice == "7":
                print("\nCustom Range") #custom range as defined in DSG module.
                dsg.custom_range()
                while dsg.start > dt.date.today() or dsg.end > dt.date.today(): #ensures dates arent in the future.
                    print("Dates Cannot Be In The Future. Please Try Again")
                    dsg.custom_range()
                date_choice()
            elif choice == "8":
                print("\nReturning to Main Menu")
                mainMenu()
                break
            else:
                # Any integer inputs other than values 1-8 we print an error message
                print("\nInvalid selection. Please chose an option from 1-7.\n\n")
        except ValueError:
                print("\nIncorrect selection, please choose a valid option\n\n")
    return

##########################################################################################
 #function used to print loading while system is performing longer tasks
def load_screen(t): # it is important to note that we do realize calling this function adds a couple of seconds.
    text_company = "Loading . . .\n" #we feel it is a nice feature that lets the user know whats going on, rather than just buffering.
    for l in text_company:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(t)

##########################################################################################

def date_choice(): #function is used in various places throughout to give users a chance to change their mind on date selection.
    retry = input("\nAre you happy with your selection? [Y/N]: ")
    if retry == "Y" or retry == "y":
        os.system("cls")
        try:
            dsg.ticker == False
            ticker_menu()
        except (NameError, AttributeError): #if no ticker has been selected yet. Go straight to ticker menu
            ticker_menu()
            mainMenu()
    elif retry == "N" or retry == "n":
        os.system("cls")
        date_menu()
    else:
        print("\nIncorrect selection, please choose a valid option\n\n")

###################################################################################

def date_reg_choice(): #same as above, just altered to use the regression dates instead.
    retry = input("\nAre you happy with your selection? [Y/N]: ")
    if retry == "Y" or retry == "y":
        date_reg_pred()
    elif retry == "N" or retry == "n":
        os.system("cls")
        date_reg()
    else:
        print("\nIncorrect selection, please choose a valid option\n\n")

####################################    FIX

def date_pred_choice(): #uses prediction dates.
    retry = input("\nAre you happy with your selection? [Y/N]: ")
    if retry == "Y" or retry == "y":
        os.system('cls')
        ticker_pred_status()
        lin_reg.LinRegress(dsg.ticker)
        os.system('pause')
        mainMenu()
    elif retry == "N" or retry == "n":
        os.system("cls")
        date_pred()
    else:
        print("\nIncorrect selection, please choose a valid option\n\n")



#this function is deployed when users enter into Stats menu, graphs, menu and predictive menu.
#This is the function which actually fetches company data from internet. Up until now users have only defined variables for use in the get_data() function here.
def check_selection(): #stops users jumping straight to statistics, graphs, and regression menus.
    while True:       #they need to select their ticker and date range before it is possible to look at any of this.
        pass          # function also includes errors to catch overflow errors, such as trying to examine a company from 1900 - 2017.
        try:          #included a catch here to pick up RemoteDataErrors which come about because of poor connection. Catches them and loops until connection succesful. Would crash otherwise.
            dsg.get_data()      #this is where data is actually fetched.
            break
        except NameError:
            os.system('cls')
            print("ERROR: No Ticker And/Or Dates Selected.\nPlease Choose From Options Below to Proceed.")
            load_screen(0.4) #loading function called to allow time to read error message.
            os.system('cls') #users then understand that they first must enter tickers and dates before proceeding.
            ticker_menu()
            break
        except OverflowError:
            os.system('cls')
            print("ERROR: The Date You Have Selected is Out of Range. Plase try again.")
            load_screen(0.4)
            os.system('cls')
            date_menu()
        except RemoteDataError:                                     # if remote data error occurs
            print("Connection Failure - Reconnecting..")
        except: #undefined except used to catch a specific date entry error.
            os.system('cls')
            print("You Have Entered an Unrecognized Date. Please Re-Enter An Appropriate Date.")
            load_screen(0.4)
            date_menu()          # Prints error message while returning to menu
    return


def ticker_status(): #function is used at the top of each screen throughout the programme to show the user their selection.
    try:
        print("Ticker Selected: \t{}".format(dsg.ticker.upper()))
        comp = 1
    except (NameError, AttributeError, ValueError):
        print("Company Ticker: None Selected")
        comp = 0
    try:
        print("Start Date: \t\t{}\nEnd Date: \t\t{}".format(dsg.start, dsg.end))
        datcomp = 1
    except (NameError, AttributeError, ValueError):
        print("Start Date: \tNone Selected\nEnd Date: \tNone Selected")
        datcomp = 0
    if comp == 0 and datcomp == 0:
        print("Please Choose a Company and Date Range Before Proceeding")
    elif comp == 1 and datcomp == 0:
        print("Company Selected, Please Choose a Date Range Before Proceeding")
    elif comp == 0 and datcomp == 1:
        print("Date Range Selected, Please Choose a Company Before Proceeding")

def ticker_pred_status(): #used in the prediction screen to show tickr and dates selected.
    try:
        print("Ticker Selected: \t{}".format(dsg.ticker.upper()))
    except (NameError, AttributeError):
        print("Company Ticker: None Selected")
    try:
        print("Training Start Date: \t{}".format(dsg.start_train))
    except (NameError, AttributeError):
        print("Training Start Date: \tNone Selected")
    try:
        print("Training End Date: \t{}".format(dsg.end_train))
    except (NameError, AttributeError):
        print("Training End Date: \tNone Selected")

################################################################################

def date_reg(): #sub menu in regression section. User selectes dates for training model.
    os.system('cls')
    check_selection()
    ticker_pred_status()
    print(46 * "-" , "MENU" , 46 * "-")
    print("Please Select A Range For Training Data")
    print("1. Past Day")
    print("2. Past Week")
    print("3. Past Month")
    print("4. Past Six Months")
    print("5. Past Year")
    print("6. Past Five Years")
    print("7. Custom Range")
    print("8. Return to Main Menu")
    print(99 * "-")
    while True:
        try:
            choice = input("Please select an option: ")
            if choice == "1":
                print("One Day Selected")
                dsg.day_train(1)
                date_reg_choice()
            elif choice == "2":
                print("One Week Selected")
                dsg.day_train(7)
                date_reg_choice()
            elif choice == "3":
                print("\nOne Month Selected")
                dsg.day_train(30)
                date_reg_choice()
            elif choice == "4":
                print("\nSix Months Selected")
                dsg.day_train(180)
                date_reg_choice()
            elif choice == "5":
                print("\nOne Year Selected")
                dsg.day_train(365)
                date_reg_choice()
            elif choice == "6":
                print("\nFive Years Selected")
                dsg.day_train(5*365)
                date_reg_choice()
            elif choice == "7":
                print("\nCustom Range")
                dsg.custom_range_train()
                while dsg.start_train > dsg.end_train:#
                    print("Training Start Date Must Be Before Training End Date. Please Re-Enter")
                    dsg.custom_range_train()
                while dsg.start_train > dt.date.today() or dsg.end_train > dt.date.today():
                    print("Training Dates Cannot Be In The Future. Please Try Again")
                    dsg.custom_range_train()
                date_reg_choice()
            elif choice == "8":
                print("\nReturning to Main Menu")
                mainMenu()
                break
            else:
                # Any integer inputs other than values 1-8 we print an error message
                print("\nInvalid selection. Please chose an option from 1-8.\n\n")
        except ValueError:
                print("\nInvalid selection, please choose a valid option\n\n")
    return

def date_reg_pred(): #sub menu for users to select their prediciton date.
    os.system('cls')
    ticker_pred_status()
    print(46 * "-" , "MENU" , 46 * "-")
    print("Please Select A Date For Which You Want A Predicted Closing Price")
    print("1. One Day")
    print("2. One Week")
    print("3. One Month")
    print("4. Six Months")
    print("5. One Year")
    print("6. Five Years")
    print("7. Custom Date")
    print("8. Return to Main Menu")
    print(99 * "-")
    while True:
        try:
            choice = input("Please select an option: ")
            if choice == "1":
                print("One Day Selected")
                dsg.reg_day(1)
                date_pred_choice()
            elif choice == "2":
                print("One Week Selected")
                dsg.reg_day(7)
                date_pred_choice()
            elif choice == "3":
                print("\nOne Month Selected")
                dsg.reg_day(30)
                date_pred_choice()
            elif choice == "4":
                print("\nSix Months Selected")
                dsg.reg_day(180)
                date_pred_choice()
            elif choice == "5":
                print("\nOne Year Selected")
                dsg.reg_day(365)
                date_pred_choice()
            elif choice == "6":
                print("\nFive Years Selected")
                dsg.reg_day(5*365)
                date_pred_choice()
            elif choice == "7":
                print("\nCustom Range")
                dsg.custom_range_pred()
                date_pred_choice()
            elif choice == "8":
                print("\nReturning to Main Menu")
                mainMenu()
                break
            else:
                # Any integer inputs other than values 1-8 we print an error message
                print("\nInvalid selection. Please chose an option from 1-8.\n\n")
        except ValueError:
                print("\nInvalid selection, please choose a valid option\n\n")
    return



mainMenu()
