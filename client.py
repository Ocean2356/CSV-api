import cmd
import requests

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
        # print(response)
        # print(response.json())
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
        # print(response)
        # print(response.content)
        # print(response.json())
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
        # self.file[inp] = response.json()["dataset_id"]
        if self.file == None:
            self.file = {}
        self.file.update({inp: response.json()["dataset_id"]})
        # print(self.file)
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

    def do_EOF(self, inp):
        '''exit the application.'''
        return self.do_exit(inp)
    
    def do_exit(self, inp):
        '''exit the application.'''
        print("Bye")
        return True


if __name__ == '__main__':
    Client().cmdloop()