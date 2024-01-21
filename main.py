import fitz  

pdf_input = 'Gayle Laakmann McDowell - Cracking the Coding Interview_ 189 Programming Questions and Solutions-CareerCup (2015).pdf' 
pdf_output = 'highlighted_example.pdf'
words_to_highlight = ['Google']

def highlight_pdf(input_path, output_path, words_to_highlight):

    # Open the PDF file
    pdf_document = fitz.open(input_path)

    #page lists
    page_delete = []

    # Iterate through each page
    for page_number in range(pdf_document.page_count):

        # Get the page
        page = pdf_document[page_number]

        # Search for words on the page
        found_words = any(page.search_for(word) for word in words_to_highlight)
        

        # If no word is found, add the page to the list for deletion
        if not found_words:
            page_delete.append(page_number)

        # Search for words and highlight them
        for word in words_to_highlight:
            word_instances = page.search_for(word)
            
            # Highlight each instance of the word
            for inst in word_instances:
                highlight = page.add_highlight_annot(inst)

                # You can customize the highlight color if needed
                highlight.set_colors([1, 1, 0])  # Yellow color
            

    new_pdf = fitz.open()
    for page_number in range(pdf_document.page_count):
        if page_number not in page_delete:
            new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number + 1)

    # Save the new PDF to the output file
    new_pdf.save(output_path)
    new_pdf.close()
    pdf_document.close()




highlight_pdf(pdf_input, pdf_output, words_to_highlight)


