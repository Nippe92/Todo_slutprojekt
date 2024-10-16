from rich.console import Console
from rich.table import Table
import json

console = Console()
table = Table()

class ToDo:
    def __init__(self, task_name, status="EJ KLAR!"):
        self.task_name = task_name
        self.status = status

    def done_Tasks(self):
        self.status = "KLAR!"

class Todo_list:
    def __init__(self):
        self.task_list = []  # tom lista för att hålla uppgifterna

    def add_task(self, task_name):
        task = ToDo(task_name) #kallar på uppgiftens namn från ToDo klassen.
        self.task_list.append(task) #lägger till en uppgift i taskslistan.

    def show_task(self):
        #nedan skapas en "box med uppgifterna med en kolumn för vardera kategori."
        table = Table(title="Din todo lista")
        table.add_column(header="uppgiftnummer", no_wrap=True, justify="left")
        table.add_column(header="Uppgift", no_wrap=True, justify="left")
        table.add_column(header="Status", no_wrap=True, justify="left")

        if not self.task_list: #Finns inga uppgifter så skrivs nedan meddelande ut.
            console.print("Inga uppgifter tillgängliga.")
            return
        else:
            for index, task in enumerate (self.task_list, 1): #sätter nummer på uppgifterna.
                if task.status == "EJ KLAR!": #om status är ej klar så blir uppgiften röd annars grön.
                    table.add_row(str(index),task.task_name, task.status, style="red")
                else:
                    table.add_row(str(index),task.task_name, task.status, style="green")
        console.print(table)

    def complete_task(self, task_index):
        if 0 <= task_index < len(self.task_list): #kollar om numret är inom det giltiga området.
            task = self.task_list[task_index] #kollar upp uppgiften som valts
            task.done_Tasks() #byter ut statusen till klar.
            print(f"Uppgift {task.task_name} har markerats som klar.")
        else:
            print("Ogiltigt uppgiftsnummer. Försök igen")

    def delete_task(self, task_index): 
        if 0 <= task_index < len(self.task_list):
            task = self.task_list.pop(task_index) 
            print(f"Uppgift '{task.task_name}' har tagits bort! ")
        else:
            print("Ogiltigt uppgiftsnummer. Försök igen.")

    def add_json(self): #lägger till uppgifterna i en json fil.
        j_file = []
        for task in self.task_list:
            j_file.append({
                "task_name": task.task_name,
                "status": task.status
            })
        with open("ToDoList.json", "w", encoding="UTF-8") as file: 
            json.dump(j_file, file, ensure_ascii=False, indent=2)#ensure_ascii gör så att jag kan använda åäö.
        print("Uppgifterna har nu sparats. ")

    def load_json(self, filename="ToDoList.json"):
        try:
            with open(filename, "r", encoding="UTF-8") as file:
                data = json.load(file)
                for item in data:
                    task = ToDo(item["task_name"], item["status"])
                    self.task_list.append(task)
                print("Uppgifterna är nu uppladdade.")
        except FileNotFoundError:
            print("Ingen fil hittades, skapar en ny!")
        
    

def main():
    todo_list = Todo_list()
    todo_list.load_json()  # Ladda uppgifter från JSON-fil om den finns


    while True:
        print("skriv med en siffra vilket val du vill göra.\n")
        print("1: Lägg till uppgift\n")
        print("2: Visa uppgifter\n")
        print("3: Uppdatera status\n")
        print("4: ta bort uppgift.\n")
        print("5: Spara och avsluta\n")
        val = input("Välj ett alternativ: ")


        if val == "1":
            task_name = input("Ange en uppgift att lägga till: ")
            todo_list.add_task(task_name)
            console.print(f"uppgiften: {task_name} har lagts till.\n", style="bright_green")
            
        elif val == "2":
            todo_list.show_task()


        elif val == "3":
            todo_list.show_task()
            task_index = int(input("Ange numret på uppgiften att markera som klar: ")) - 1
            todo_list.complete_task(task_index)

        elif val == "4":
            todo_list.show_task()
            task_index = int(input("Ange numret på uppgiften att ta bort: ")) - 1
            todo_list.delete_task(task_index)

        elif val == "5":
            todo_list.add_json()  # Spara till JSON när programmet avslutas
            print("Programmet avslutas...")
            break

        else:
            print("Ogiltigt val, försök igen.")



main()