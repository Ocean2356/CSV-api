import cmd
import requests
import pandas as pd
from io import StringIO

class Client(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '>>> '
        self.intro  = 'Welcome to the client shell. Type help or ? to list commands.\n'
        self.file = {}
        self.do_list("")

    def do_list(self, inp):
        '''list all datasets on the server.'''
        url = "http://localhost:8000/datasets"
        methode = "GET"
        response = requests.request(methode, url)
        if response.json()["message"] == "no_datasets":
            print("No datasets on the server.")
            return
        self.file = response.json()["datasets"]
        if response.json()["message"] == "datasets_list":
            print("Datasets on the server:")
            for i in self.file:
                print(i)
    

    def do_clear(self, inp):
        '''clear all datasets on the server.'''
        url = "http://localhost:8000/datasets"
        methode = "DELETE"
        response = requests.request(methode, url)
        if response.json()["message"] == "datasets_cleared":
            self.file.clear()
            print("All datasets on the server are cleared.")
            return
    

    def do_create(self, inp):
        '''create a dataset on the server.'''
        url = "http://localhost:8000/datasets"
        methode = "POST"
        files = {"dataset": open(inp, "rb")}
        response = requests.request(methode, url, files=files)
        self.file.update({inp: response.json()["dataset_id"]})
        if response.json()["message"] == "dataset_created":
            print("Dataset created on the server, id: %s" % response.json()["dataset_id"])

    def do_delete(self, inp):
        '''delete a dataset from the server.'''
        print(self.file)
        url = "http://localhost:8000/datasets/" + self.file[inp]
        methode = "DELETE"
        response = requests.request(methode, url)
        if response.json()["message"] == "dataset_deleted":
            del self.file[inp]
            print("Dataset deleted from the server.")

    def do_info(self, inp):
        '''get information about a dataset on the server.'''
        url = "http://localhost:8000/datasets/" + self.file[inp]
        methode = "GET"
        response = requests.request(methode, url)
        if response.json()["message"] == "dataset_info":
            print("Dataset information:")
            print("filename: %s" % response.json()["filename"])
            print("size: %s" % response.json()["size"])

    def do_excel(self, inp):
        '''get a dataset from the server in excel format.'''
        url = "http://localhost:8000/datasets/" + self.file[inp] + "/excel"
        methode = "GET"
        response = requests.request(methode, url)
        if response.json()["message"] == "dataset_not_found":
            print("Dataset not found.")
            return
        if response.json()["message"] == "dataset_excel":
            filename = inp.split(".")[0]
            csv_file = StringIO(response.json()["dataset_excel"])
            df = pd.read_csv(csv_file)
            df.to_excel("%s.xlsx" % filename)
            print("Dataset saved as %s.xlsx" % filename)

    def do_stats(self, inp):
        '''get statistics about a dataset on the server.'''
        url = "http://localhost:8000/datasets/" + self.file[inp] + "/stats"
        methode = "GET"
        response = requests.request(methode, url)
        if response.json()["message"] == "dataset_not_found":
            print("Dataset not found.")
            return
        if response.json()["message"] == "dataset_stats":
            print("Dataset statistics:")
            stats = response.json()["stats"]
            print(stats)

    def do_plot(self, inp):
        '''plot a dataset from the server.'''
        url = "http://localhost:8000/datasets/" + self.file[inp] + "/plot"
        methode = "GET"
        file_response = requests.get(url, stream=True)
        if file_response.status_code == 404:
            print("Dataset not found.")
            return
        if file_response.status_code == 200:
            filename = inp.split(".")[0]
            file_content = file_response.content
            content_type = file_response.headers["Content-Type"]
            if content_type == "application/pdf":
                with open("%s.pdf" % filename, "wb") as file:
                    file.write(file_content)
                print("Dataset saved as %s.pdf" % filename)


    def do_EOF(self, inp):
        '''exit the application.'''
        return self.do_exit(inp)
    
    def do_exit(self, inp):
        '''exit the application.'''
        print("Bye")
        return True


if __name__ == '__main__':
    Client().cmdloop()