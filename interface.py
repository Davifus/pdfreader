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
        
        self.pdf_document = None
        self.current_page = 0
        self.search_results = []
        self.current_result_index = 0

        self.search_entry = tk.Entry(master)
        self.search_entry.pack(side=tk.TOP, padx=10, pady=10)

        self.search_button = tk.Button(master, text="Search", command=self.search_word)
        self.search_button.pack(side=tk.TOP)

        self.next_button = tk.Button(master, text="Next", command=self.next_result)
        self.next_button.pack(side=tk.TOP)

        self.prev_button = tk.Button(master, text="Previous", command=self.prev_result)
        self.prev_button.pack(side=tk.TOP)

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

    def search_word(self):
        query = self.search_entry.get().strip().lower()
        if query and self.pdf_document:
            self.search_results = []
            for page_number in range(len(self.pdf_document)):
                page = self.pdf_document.load_page(page_number)
                text = page.get_text().lower()
                start = 0
                while True:
                    start = text.find(query, start)
                    if start == -1:
                        break
                    self.search_results.append((page_number, start))
                    start += 1
            
            if self.search_results:
                self.current_result_index = 0
                self.show_search_result()
            else:
                print("No matches found.")

    def show_search_result(self):
        page_number, start = self.search_results[self.current_result_index]
        self.current_page = page_number
        self.show_page()
        self.highlight_search_result(start, len(self.search_entry.get()))

    def highlight_search_result(self, start, length):
        page = self.pdf_document.load_page(self.current_page)
        text_instances = page.search_for(self.search_entry.get(), quads=True)
        
        if text_instances:  # Check if there are search results
            # Iterate over all search result quads
            for quad in text_instances:
                # Ensure quad has enough elements to access
                if len(quad) >= 8:
                    # Extract coordinates
                    x0, y0, x1, y1, x2, y2, x3, y3 = quad[:8]

                    # Draw rectangle around searched text
                    self.canvas.create_rectangle(x0, y0, x2, y2, outline='red')
        else:
            print("No search results found.")



    def next_result(self):
        self.current_result_index = (self.current_result_index + 1) % len(self.search_results)
        self.show_search_result()

    def prev_result(self):
        self.current_result_index = (self.current_result_index - 1) % len(self.search_results)
        self.show_search_result()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewerApp(root)
    root.mainloop()






#####list of feature left######
#scroll bar reflect pdf scrolling -> PAUSE
#layer current page on top of the pdf -> DONE
#search function -> sort of work but cant get it to highlight the words
    
#highlighting function
#- the main.py has highlighting function but user has to input word in it.
""" https://pymupdf.readthedocs.io/en/latest/recipes-annotations.html """

#saving highlightinged into database
#upload pdf to db to reference
#sign in portion that lets you load pdf with highlighted
#print to printer
#zoom in and out
    
