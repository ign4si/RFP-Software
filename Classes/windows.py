import tkinter as tk


class Windows(tk.Frame):
    def __init__(self, parent,controller):
        super().__init__(self, parent)
        self.controller = controller
        
    def select_folder(self):
        global folder

        folder = tk.filedialog.askdirectory()

        tk.messagebox.showinfo(
            title='Selected Folder',
            message=folder
        )
        return folder
        # frame = Workspace(controller.container, controller)
        # controller.frames[Workspace] = frame
        # frame.grid(row=0, column=0, sticky="nsew")
        
        # controller.show_frame(Workspace)'
    
    def clear(self):
        for widgets in self.winfo_children():
            widgets.destroy()
    
    def select_file(self):
        file = tk.filedialog.askopenfilename()

        tk.messagebox.showinfo(
            title='Selected File',
            message=file
        )
        return file
        # frame = Sonnet(controller.container, controller)
        # controller.frames[Sonnet] = frame
        # frame.grid(row=0, column=0, sticky="nsew")

        controller.show_frame(Sonnet)
    # def select_compensation(self,controller):
    #     global compensation_file

    #     compensation_file = tk.filedialog.askopenfilename()

    #     tk.messagebox.showinfo(
    #         title='Selected File',
    #         message=compensation_file
    #     )
        # frame = Compensation(controller.container, controller)
        # controller.frames[Compensation] = frame
        # frame.grid(row=0, column=0, sticky="nsew")

        # controller.show_frame(Compensation)
