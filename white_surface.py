import tkinter as tk
from tkinter.scrolledtext import ScrolledText


def main():
    root = tk.Tk()
    root.title("Jeff")
    root.configure(bg="white")
    root.geometry("400x300")

    output = ScrolledText(root, height=10, width=40, state="disabled", bg="white", relief="sunken")
    output.pack(padx=10, pady=10, fill="both", expand=True)

    def show_welcome():
        output.configure(state="normal")
        output.insert(tk.END, "Welcome to Jeff!\n")
        output.configure(state="disabled")

    tk.Button(root, text="Show Welcome", command=show_welcome).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
