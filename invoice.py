from docxtpl import DocxTemplate
from twilio.rest import Client
import os

def invoice_gen(name, mobile_number, e_name, user_id, bill_no, formatted_datetime, invoice_list, ds):
    doc = DocxTemplate(r"Invoices\invoice_templatefn.docx")
    invoice_list = list(invoice_list)
    
    for row in invoice_list:
        last_column = row[-1]  # Access the last column
        second_last_column = row[-2]  # Access the column before the last
        
        # Calculate the division result
        result = float(last_column) / float(second_last_column)
        
        # Convert the tuple to a list and insert the result at the 3rd index (4th position)
        row_list = list(row)
        row_list.insert(3, result)
        
        # Update the invoice_list with the modified row
        invoice_list[invoice_list.index(row)] = tuple(row_list)
    
    # Calculate subtotal, discount, and sales tax
    sb_tot = sum([float(x[4]) for x in invoice_list])

    # Round to two decimal places
    sb_tot = round(sb_tot, 2)

    discount = sb_tot * ds / 100
    discount = round(discount, 2)

    sales_tax = 18 * sb_tot / 100
    sales_tax = round(sales_tax, 2)


    # Render the invoice
    doc.render({
        "name": name,
        "phone": mobile_number,
        "e_name": e_name,
        "user_id": user_id,
        "bill_no": bill_no,
        "date": formatted_datetime,
        "invoice_list": invoice_list,
        "subtotal": sb_tot,
        "discount": discount,
        "sales_tax": sales_tax,
        "total": round((sb_tot - discount + sales_tax),2)
    })
    
    # Save the invoice document
    doc_path = rf"Invoices\{bill_no}_invoice.docx"
    doc.save(doc_path)
    
    # Send the document via WhatsApp
    