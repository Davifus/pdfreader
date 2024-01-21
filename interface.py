import fitz
import tkinter as tk
from tkinter import filedialog

class PDFViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Reader")

        self.canvas = tk.Canvas(master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(master, command=self.on_scroll)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-4>", self.on_mousewheel)  # For Linux
        self.canvas.bind("<Button-5>", self.on_mousewheel)  # For Linux

        self.pdf_document = None
        self.current_page = 0

        self.page_label = tk.Label(master, text="")
        self.page_label.pack()

        menubar = tk.Menu(master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_pdf)
        menubar.add_cascade(label="File", menu=file_menu)
        master.config(menu=menubar)

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_document = fitz.open(file_path)
            self.show_page()

    def show_page(self):
        if self.pdf_document:
            page = self.pdf_document.load_page(self.current_page)
            pix = page.get_pixmap()
            img = tk.PhotoImage(data=pix.tobytes("ppm"))
            self.canvas.config(scrollregion=(0, 0, pix.width, pix.height))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.canvas.image = img

            # Set GUI window size to match PDF page size
            self.master.geometry(f"{pix.width}x{pix.height}")

            # Update page number label
            """ self.page_label.config(text=f"Page: {self.current_page + 1}/{self.pdf_document.page_count}") """

    def on_canvas_configure(self, event):
        width = event.width
        height = event.height
        self.canvas.config(scrollregion=(0, 0, width, height))

    def on_mousewheel(self, event):
        if event.delta > 0 and self.current_page > 0:
            self.current_page -= 1
            self.show_page()
        elif event.delta < 0 and self.current_page < self.pdf_document.page_count - 1:
            self.current_page += 1
            self.show_page()

    def on_scroll(self, *args):
        self.canvas.event_generate("<<Scroll>>")

        # Update scrollbar position
        scroll_position = self.canvas.yview()[0]
        page_index = round(scroll_position * (self.pdf_document.page_count - 1))
        if page_index != self.current_page:
            self.current_page = page_index
            self.show_page()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewerApp(root)
    root.mainloop()


#list of feature left
#scroll bar reflect pdf scrolling
#layer current page on top of the pdf?
#find word/letter/etc function
#highlighting function
#saving highlightinged into database
#upload pdf to db to reference
#sign in portion that lets you load pdf with highlighted
    
