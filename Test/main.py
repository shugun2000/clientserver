log_file = "ClientChatLog.txt"

while True:
    user_input = input ("Me: ") #This is the input
    if user_input.lower() == "bye":
        print("Log Chat Ended.")
        break #This will break the loop with user type "bye"

    

    with open(log_file, "a") as file:
        file.write(f"Me: {user_input}\n")
        file.write(response + "\n")